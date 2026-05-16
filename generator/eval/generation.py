import json
import time
import openai
import tiktoken
import re
from tqdm import tqdm
from math import ceil
from typing import List, Optional

from accelerate.utils import set_seed
from torch.utils.data.dataloader import DataLoader
from transformers import StoppingCriteria, StoppingCriteriaList

from eval.utils import TokenizedDataset, complete_code

from openai import OpenAI
import os
from pathlib import Path


def extract_target_code_segment(code_text: str, function_name: str) -> Optional[str]:
    """
    从文本中截取到第一个函数/方法定义之前的内容。
    
    新逻辑：
    从第一个字符开始，找到第一个 FUNCTION_BLOCK/FUNCTION/METHOD，
    截取这之前的所有内容。
    
    参数:
        code_text: 可能包含多个 FUNCTION_BLOCK/FUNCTION/METHOD 的代码文本
        function_name: 目标函数名（保留参数兼容性，但不使用）
    
    返回:
        截取到第一个定义之前的内容，如果未找到定义或内容为空则返回 None
    """
    print("enter extract_target_code_segment")
    if not code_text:
        return None
    
    lines = code_text.split('\n')
    first_definition_idx = None
    
    # 定义匹配模式：FUNCTION_BLOCK/FUNCTION/METHOD
    definition_pattern = re.compile(
        r'^\s*(FUNCTION_BLOCK|FUNCTION|METHOD)\s+',
        re.IGNORECASE
    )
    
    # 查找第一个函数定义的位置
    for idx, line in enumerate(lines):
        if definition_pattern.search(line):
            first_definition_idx = idx
            break
    
    if first_definition_idx is None:
        # 没有找到任何函数定义，返回 None
        return None
    
    # 截取从开头到第一个定义之前的所有内容
    if first_definition_idx == 0:
        # 第一行就是定义，没有之前的内容
        return None
    
    extracted_lines = lines[0:first_definition_idx]
    extracted_code = '\n'.join(extracted_lines).strip()
    
    return extracted_code if extracted_code else None


def _resolve_function_name(doc: dict, idx: int) -> str:
    """
    解析函数名称，与 process_generations.py 中的逻辑保持一致
    优先使用 task_id（新格式），然后使用 fpath_tuple，最后回退到其他字段
    """
    # 优先使用 task_id（新格式）
    task_id = doc.get("task_id")
    if task_id:
        return str(task_id)
    
    # 其次使用 fpath_tuple 的最后一个值（去掉扩展名）
    metadata = doc.get("metadata", {}) or {}
    if isinstance(metadata, dict):
        fpath_tuple = metadata.get("fpath_tuple")
        if fpath_tuple and isinstance(fpath_tuple, list) and fpath_tuple:
            fpath_value = str(fpath_tuple[-1])
            # 去掉扩展名，只保留文件名部分
            name_without_ext = Path(fpath_value).stem
            if name_without_ext:
                return name_without_ext
    
    # 如果没有 fpath_tuple，回退到原来的逻辑
    explicit = doc.get("function_name")
    if explicit:
        return explicit
    if isinstance(metadata, dict):
        meta_fn = metadata.get("function_name")
        if meta_fn:
            return meta_fn
    title = doc.get("title")
    if title:
        return title
    return f"result_{idx}"

#OLD TASK INFO:
#You are performing a code writing task. Based on the provided definition section of a Structured Text FUNCTION or FUNCTION_BLOCK, you must implement the corresponding logic (implementation) section of the code.
#You are skilled at analyzing and reusing similar code fragments provided as references, and implementing the logic section according to the given definitions.

generator_system_prompt = """
ROLE:
You are an expert in Structured Text (ST) programming for IEC 61131-3–compliant PLCs using the Codesys development environment.
TASK:
You shall complete the corresponding code logic implementation based on the requirement description of the function to be completed and the provided definition section of the Structured Text (ST) FUNCTION or FUNCTION_BLOCK.
CONSTRAINTS:
- The generated code must strictly conform to the Structured Text syntax and semantic rules of the Codesys platform.
- You MAY freely define local variables using VAR blocks.
- You MUST and ONLY output Structured Text (ST) code.
- Do NOT include any explanations, descriptions, comments outside the code, or any natural language text.
- Do NOT include markdown formatting, headings, or bullet points.
- Do NOT include code fences or triple backticks.
- Do NOT repeat the input.
- If the code being fixed is a FUNCTION, Use `RETURN;` to return.
- In all code generation tasks, regardless of whether the target generation object is a FUNCTION_BLOCK or a FUNCTION, only the logic implementation part strictly corresponding to the object type is allowed to be generated; the generation of METHODS or any other code structures that are not of the target type is strictly prohibited.
- You MUST NOT define or modify the following declaration sections:
    VAR_INPUT
    VAR_OUTPUT
    VAR_IN_OUT

OUTPUT FORMAT:
```
#code here
```

"""


# 只在有 API key 时初始化 OpenAI 客户端（用于 api 模式）
client = None
openai_api_key = os.getenv("OPENAI_API_KEY") or os.getenv("API_KEY")
openai_api_base = os.getenv("OPENAI_API_BASE") or os.getenv("BASE_URL")
if openai_api_key:
    try:
        client_kwargs = {"api_key": openai_api_key}
        if openai_api_base:
            client_kwargs["base_url"] = openai_api_base
        client = OpenAI(**client_kwargs)
    except Exception:
        client = None

class EndOfFunctionCriteria(StoppingCriteria):
    """Custom `StoppingCriteria` which checks if all generated functions in the batch are completed."""
    def __init__(self, start_length, eof_strings, tokenizer, check_fn=None):
        self.start_length = start_length
        self.eof_strings = eof_strings
        self.tokenizer = tokenizer
        if check_fn is None:
            check_fn = lambda decoded_generation: any(
                [stop_string in decoded_generation for stop_string in self.eof_strings]
            )
        self.check_fn = check_fn

    def __call__(self, input_ids, scores, **kwargs):
        """Returns true if all generated sequences contain any of the end-of-function strings."""
        decoded_generations = self.tokenizer.batch_decode(input_ids[:, self.start_length :])
        return all([self.check_fn(decoded_generation) for decoded_generation in decoded_generations])

class TooLongFunctionCriteria(StoppingCriteria):
    """Custom `StoppingCriteria` which checks if the generated function is too long by a certain multiplier based on input length."""

    def __init__(self, input_length, multiplier):
        self.input_length = input_length
        self.multiplier = multiplier

    def __call__(self, input_ids, scores, **kwargs):
        """Returns true if generated sequence is too long."""
        return input_ids.shape[1] > int(self.input_length * self.multiplier)
        

def parallel_generations(
        task,
        dataset,
        accelerator,
        model,
        tokenizer,
        n_tasks,
        args,
        curr_sample_idx: int = 0,
        save_every_k_tasks: int = -1,
        intermediate_generations: Optional[List[Optional[List[Optional[str]]]]] = None,
        intermediate_save_generations_path: Optional[str] = None,
):
    if args.load_generations_path:
        # load generated code
        with open(args.load_generations_path) as fp:
            generations = json.load(fp)
            if accelerator.is_main_process:
                print(
                    f"generations loaded, {n_tasks} selected from {len(generations)} with {len(generations[0])} candidates"
                )
        return generations[:n_tasks]

    set_seed(args.seed, device_specific=True)

    # Setup generation settings
    gen_kwargs = {
        "do_sample": args.do_sample,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "top_k": args.top_k,
        "max_length": args.max_length_generation,
    }
    stopping_criteria = []
    # The input_length / start_length set to 0 for now will be adjusted later
    # Check if the task has a custom check_fn method for the stopping criteria
    if task.stop_words and tokenizer.eos_token:
        task.stop_words.append(tokenizer.eos_token)    
    if hasattr(task, "check_fn"):
        stopping_criteria.append(
            EndOfFunctionCriteria(0, task.stop_words, tokenizer, task.check_fn)
        )
    elif task.stop_words:
        stopping_criteria.append(
            EndOfFunctionCriteria(0, task.stop_words, tokenizer)
        )
    if hasattr(task, "max_length_multiplier") and task.max_length_multiplier:
        stopping_criteria.append(
            TooLongFunctionCriteria(0, task.max_length_multiplier)
        )
    
    if stopping_criteria:
        gen_kwargs["stopping_criteria"] = StoppingCriteriaList(stopping_criteria)

    if args.instruction_tokens:
        instruction_tokens = args.instruction_tokens.split(",")
        if len(instruction_tokens) != 3:
            raise ValueError(
                "Instruction tokens should contain exactly 3 tokens separated by a comma. If a token is empty, represent it as ''"
            )
        for token in instruction_tokens:
            if token.strip() != "":
                task.stop_words.append(token)
    else:
        instruction_tokens = None
    if accelerator.is_main_process:
        print(f"number of problems for this task is {n_tasks}")
    n_copies = ceil(args.n_samples / args.batch_size)

    ds_tokenized = TokenizedDataset(
        task,
        dataset,
        tokenizer,
        num_devices=accelerator.state.num_processes,
        max_length=args.max_length_input,
        limit_start=args.limit_start + curr_sample_idx,
        n_tasks=n_tasks,
        n_copies=n_copies,
        prefix=args.prefix,
        has_encoder=args.modeltype == "seq2seq",
        instruction_tokens=instruction_tokens,
    )

    # do not confuse args.batch_size, which is actually the num_return_sequences
    ds_loader = DataLoader(ds_tokenized, batch_size=1)

    is_loaded_in_8bit = getattr(model, "is_loaded_in_8bit", False)
    is_loaded_in_4bit = getattr(model, "is_loaded_in_4bit", False)
    if args.max_memory_per_gpu is not None:
        # The model is already sharded across multiple GPUs
        ds_loader = accelerator.prepare(ds_loader)
    elif not is_loaded_in_8bit and not is_loaded_in_4bit:
        # we only wrap data loader to avoid extra memory occupation
        model = model.to(accelerator.device)
        ds_loader = accelerator.prepare(ds_loader)
    else:
        # model.to() is not supported for 8bit and 4bit models
        model, ds_loader = accelerator.prepare(model, ds_loader)

    generations = complete_code(
        task,
        accelerator,
        model,
        tokenizer,
        ds_loader,
        n_tasks=n_tasks,
        limit_start=args.limit_start + curr_sample_idx,
        batch_size=args.batch_size,
        prefix=args.prefix,
        instruction_tokens=instruction_tokens,
        postprocess=args.postprocess,
        is_wrapped=is_loaded_in_8bit or is_loaded_in_4bit,
        save_every_k_tasks=save_every_k_tasks,
        intermediate_generations=intermediate_generations,
        intermediate_save_generations_path=intermediate_save_generations_path,
        **gen_kwargs,
    )
    return generations



def parse_code_snippets(text: str) -> List[str]:
    """Extract code pieces from a text string.
    Args:
        text: str, model prediciton text.
    Rets:
        code_pieces: list[str], code pieces in the text.
    """
    code_pieces = []
    while "```python" in text:
        st_idx = text.index("```python") + 10
        # end_idx = text.index("```", st_idx)
        if "```" in text[st_idx:]:
            end_idx = text.index("```", st_idx)
        else: 
            end_idx = len(text)
        code_pieces.append(text[st_idx:end_idx].strip())
        text = text[end_idx+3:].strip()
    return '\n\n'.join(code_pieces)



# %% OpenAI Generations
from openai import OpenAI, AzureOpenAI
# fill in specification here
gpt_tokenizer = tiktoken.get_encoding("cl100k_base")

def openai_generations(
    task,
    dataset,
    model,
    n_tasks,
    args,
    curr_sample_idx: int = 0,
    save_every_k_tasks: int = -1,
    intermediate_generations: Optional[List[Optional[List[Optional[str]]]]] = None,
    intermediate_save_generations_path: Optional[str] = None,
):
    if args.load_generations_path:
        # load generated code
        with open(args.load_generations_path) as fp:
            generations = json.load(fp)
            print(
                f"generations loaded, {n_tasks} selected from {len(generations)} with {len(generations[0])} candidates"
            )
            # if accelerator.is_main_process:
        return generations[:n_tasks]
    
    def get_response(user_prompt: str, n_iters: int = 2, sleep: int = 10, **kwargs) -> List[str]:
        prompt_tokens = gpt_tokenizer.encode(user_prompt)
        user_prompt = gpt_tokenizer.decode(prompt_tokens[: args.max_length_input])
        
        i_iters = 0
        last_exception = None
        while i_iters < n_iters:
            i_iters += 1
            try:
                # 使用 RepoEval 格式（固定格式）
                messages = [
                    {"role": "system", "content": generator_system_prompt},
                    {"role": "system", "name": "example_user", "content": "Continue writing the following code:\n\n```\ndef return_none():\n```"},
                    {"role": "system", "name": "example_assistant", "content": "```\n    return None\n```"},
                    {"role": "user", "content": user_prompt},
                ]
                    
                response = client.chat.completions.create(
                    model=model, 
                    messages = messages,
                    **kwargs
                )
                return [c.message.content for c in response.choices]
            except Exception as e:
                last_exception = e
                print(f"\n[ERROR] OpenAI API call failed (attempt {i_iters}/{n_iters})")
                print(f"  Model: {model}")
                print(f"  Error type: {type(e).__name__}")
                print(f"  Error message: {str(e)}")
                if hasattr(e, 'status_code'):
                    print(f"  Status code: {e.status_code}")
                if hasattr(e, 'response'):
                    print(f"  Response: {e.response}")
                import traceback
                print(f"  Traceback:\n{''.join(traceback.format_exception(type(e), e, e.__traceback__))}")
                if i_iters < n_iters:
                    print(f"  Retrying after {i_iters * sleep} seconds...\n")
                    time.sleep(i_iters * sleep)
        # 如果所有重试都失败，抛出异常而不是返回空字符串
        print(f"\n[FATAL ERROR] All {n_iters} attempts failed. Last error: {str(last_exception)}")
        raise Exception(f"Failed to get response from OpenAI API after {n_iters} attempts. Last error: {str(last_exception)}") from last_exception

    # Setup generation settings
    gen_kwargs = {
        "max_tokens": args.max_length_generation,
        "temperature": args.temperature,
        "top_p": args.top_p,
    }
    
    save_every_k_tasks = args.save_every_k_tasks if args.save_every_k_tasks > 0 else n_tasks+1
    intermediate_generation_file = args.save_generations_path + '.partial'
    
    # 创建 prompt 目录（与 logs、readful_result 同级）
    if args.save_generations_path:
        output_dir = Path(args.save_generations_path).parent
        prompt_dir = output_dir / "prompt"
        prompt_dir.mkdir(parents=True, exist_ok=True)
    else:
        prompt_dir = None
    
    generations = []
    for i in tqdm(range(args.limit_start + curr_sample_idx, n_tasks)):
        # 当前样本文档（包含 requirement / provide_code / docs 等字段）
        doc = dataset[i]

        # 构造代码补全的 prompt（内部已做同名函数规避和检索拼接）
        i_prompt = task.get_prompt(doc=doc)
        # print(i_prompt)
        # 从 doc 中读取待补全函数的自然语言需求（来自 results.jsonl -> requirement 字段）
        requirement_info = doc.get("requirement", "") or ""
        
        # 计算 sample_idx（用于控制打印）
        sample_idx = i - (args.limit_start + curr_sample_idx)
        
        # 如果启用了 planner，读取规划结果（不修改 i_prompt）
        plan_text = ""
        if hasattr(args, 'skip_plan') and not args.skip_plan and hasattr(args, 'plan_results_dir') and args.plan_results_dir:
            try:
                # 获取函数名（用于查找对应的 planner 结果文件）
                function_name = _resolve_function_name(doc, i)
                # 清理文件名，移除或替换不安全的字符
                safe_filename = re.sub(r'[<>:"/\\|?*\n\r\t]+', '_', str(function_name))
                safe_filename = safe_filename.strip()
                if not safe_filename:
                    safe_filename = f"result_{i}"
                
                # 读取 planner 结果文件
                plan_file = Path(args.plan_results_dir) / f"{safe_filename}.txt"
                if plan_file.exists():
                    plan_text = plan_file.read_text(encoding='utf-8').strip()
            except Exception as e:
                # 如果读取 planner 结果失败，只打印警告，不中断流程
                if sample_idx < 2:
                    print(f"  ⚠ 读取规划结果失败 (task {i}): {e}")
        
        # 构造 user_prompt（与实际调用 LLM 相同的格式）
        if plan_text:
            # 如果有规划结果，加入规划说明
            user_prompt = (
                "This is the known requirement information for the function to be completed:\n"
                + requirement_info
                + "\nThis provides you with a plan of implementation steps for the function to be completed. Subsequent ST code must strictly follow this plan and must not deviate from the core logic. The following is the plan of implementation steps:\n"
                + plan_text
                + "\nContinue writing the following code:\n\n```\n"
                + i_prompt
                + "\n```"
            )
        else:
            # 如果没有规划结果，使用原始格式
            user_prompt = (
                "This is the known requirement information for the function to be completed:\n"
                + requirement_info
                # + "REMEMBER: If the code being fixed is a FUNCTION, Use `RETURN;` to return. Do NOT assign a value during RETURN. NEVER use `RETURN(value);`."
                + "\nContinue writing the following code:\n\n```\n"
                + i_prompt
                + "\n```"
            )
        
        # 保存 prompt 到文件
        if prompt_dir is not None:
            try:
                # 获取任务名称（使用与 readful_result 相同的命名逻辑）
                function_name = _resolve_function_name(doc, i)
                # 清理文件名，移除或替换不安全的字符（与 process_generations.py 中的 sanitize_filename 逻辑一致）
                safe_filename = re.sub(r'[<>:"/\\|?*\n\r\t]+', '_', str(function_name))
                safe_filename = safe_filename.strip()
                if not safe_filename:
                    safe_filename = f"result_{i}"
                
                prompt_file = prompt_dir / f"{safe_filename}.txt"
                with open(prompt_file, 'w', encoding='utf-8') as f:
                    f.write(user_prompt)
            except Exception as e:
                # 如果保存失败，只打印警告，不中断流程
                print(f"  ⚠ 保存 prompt 失败 (task {i}): {e}")
        # 打印 prompt 信息（仅打印前2个样本，避免输出过多）
        if sample_idx < 2:
            print(f"\n{'='*80}")
            print(f"Sample {sample_idx} (dataset index {i}) - Prompt (length: {len(i_prompt)} chars)")
            print(f"{'='*80}")
            # 打印前 2000 个字符
            prompt_preview = i_prompt[:2000] if len(i_prompt) > 2000 else i_prompt
            print(prompt_preview)
            if len(i_prompt) > 2000:
                print(f"\n... (truncated, total length: {len(i_prompt)} chars)")
                sources = task.get_retrieved_sources(doc)
                if sources:
                    print(f"检索来源: {', '.join(sources)}")
            print(f"{'='*80}\n")
        i_resp = get_response(
            user_prompt=user_prompt,
            **gen_kwargs,
        )  # list[str]

        # 代码片段截取：从多个代码段中提取目标代码段
        # 获取函数名（文件名）
        function_name = _resolve_function_name(doc, i)
        
        # 对每个候选结果进行处理
        filtered_responses = []
        print("11111" + function_name)
        print(i_resp)
        for resp_text in i_resp:
            if not resp_text or not isinstance(resp_text, str):
                filtered_responses.append(resp_text)
                print("zxy")
                continue
            
            # 提取匹配的代码段
            extracted = extract_target_code_segment(resp_text, function_name)
            if extracted:
                print("extracted successfully")
                filtered_responses.append(extracted)
            else:
                # 如果没找到匹配，保留原结果（避免丢失）
                print("extracted failed")
                filtered_responses.append(resp_text)
        
        i_resp = filtered_responses

        generations.append(i_resp)
        if len(generations) % save_every_k_tasks == 0:
            with open(intermediate_generation_file, 'w') as fp:
                json.dump(generations, fp)
    
    processed_generations = []
    for i, gs in enumerate(generations):
        processed_gs = [
            task.postprocess_generation(generation=g,idx=i,new_tokens_only=True) 
            for g in gs
        ]
        processed_generations.append(processed_gs)

    return intermediate_generations + processed_generations


