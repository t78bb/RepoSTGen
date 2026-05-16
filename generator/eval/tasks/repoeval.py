"""RepoCoder: Repository-Level Code Completion Through Iterative Retrieval and Generation
https://aclanthology.org/2023.emnlp-main.151/

The RepoEval dataset released by Microsoft includes repository-level code generation problems. 
"""
import os
import time
import json
import re
import numpy as np
from pathlib import Path
from tqdm import tqdm
from typing import Dict, List, Optional

from eval.base import Task
from eval.tasks.custom_metrics.repoeval_ESEM import (
    process_prediction, compute_EM, compute_ES
)
from eval.tasks.custom_metrics.repoeval_execution import (
    copy_all_repos, setup_repos, check_tests, eval_generation
)

_CITATION = """
@article{zhang2023repocoder,
  title={RepoCoder: Repository-Level Code Completion Through Iterative Retrieval and Generation},
  author={Fengji Zhang and Bei Chen and Yue Zhang and Jacky Keung and Daoguang Zan and Yi Mao and Jian-Guang Lou and Weizhu Chen},
  journal={EMNLP},
  year={2023}
}
"""


STOP_WORDS = ["\nclass", "\ndef", "\n#", "\n@", "\nprint", "\nif", "\n```", "<file_sep>"]

def create_all_tasks():
    """Creates a dictionary of tasks from a list of levels
    :return: {task_name: task}
        e.g. {multiple-py: Task, multiple-java: Task}
    """
    return {
        f"repoeval-{split}": create_task(split)
        for split in ["api", "line", "function"]
    }


def create_task(split):
    class RepoEval(GeneralRepoEval):
        def __init__(self, **kwargs):
            super().__init__(split, **kwargs)

    return RepoEval


def _normalize_title(title: str) -> str:
    return title.replace("/", "\\").split("\\")[-1].lower().strip()


def _normalize_function_name(function_name: Optional[str]) -> str:
    if not function_name:
        return ""
    name = function_name.lower().strip()
    if name.endswith(".st"):
        name = name[:-3]
    return name


def _should_skip_doc(title: Optional[str], function_name: Optional[str]) -> bool:
    if not title or not function_name:
        return False
    normalized_title = _normalize_title(title)
    normalized_function_name = _normalize_function_name(function_name)
    if not normalized_function_name:
        return False
    return normalized_title == f"{normalized_function_name}.st"


def filter_docs_for_prompt(
    docs: List[Dict], function_name: Optional[str], topk: int
) -> List[Dict]:
    filtered = []
    if not docs or topk <= 0:
        return filtered
    for doc in docs:
        print(doc.get("title"), function_name)
        if not _should_skip_doc(doc.get("title"), function_name):
            print(doc.get("title"))
            filtered.append(doc)
            if len(filtered) >= topk:
                break
    
    return filtered


def get_retrieved_prompt(docs):
    """Builds the retrieved prompt based on a list of docs"""
    if not docs:
        return ""
    start_line = "Here are some relevant code fragments from other files of the repo:"
    sep_line = "--------------------------------------------------"
    intro_line = "the below code fragment can be found in:"
    
    title_block = intro_line + '\n' + '__TITLE__' + '\n' + sep_line
    
    # 对 docs 中的 doc['title'] 进行去重
    seen_titles = set()
    unique_docs = []
    for doc in docs:
        title = doc.get('title', '')
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_docs.append(doc)
    
    retrieved_prompt = start_line + '\n' + sep_line + '\n'
    
    # 项目代码根目录
    project_code_base = Path(r"F:\项目级st补全\repo_gen_project\dataset\project_code")
    
    for doc in unique_docs:
        title = doc.get('title', '')
        if not title:
            continue
        
        # 提取项目名（第一个 '-' 之前的部分）
        if '-' in title:
            project_name = title.split('-')[0]
        else:
            # 如果没有 '-'，尝试从路径中提取
            project_name = title.split('\\')[0] if '\\' in title else title.split('/')[0]
        
        # 提取文件名（最后一个 '\\' 或 '/' 后面的部分）
        if '\\' in title:
            filename = title.split('\\')[-1]
        elif '/' in title:
            filename = title.split('/')[-1]
        else:
            filename = title
        
        # 构建完整文件路径
        file_path = project_code_base / project_name / "FUN" / filename
        print("retrieved file path:", file_path)
        # 读取文件内容
        file_content = ""
        if file_path.exists() and file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
            except Exception as e:
                # 如果读取失败，使用原来的 doc['text'] 作为回退
                print(f"Warning: Failed to read file {file_path}: {e}")
                file_content = doc.get('text', '')
        else:
            # 如果文件不存在，使用原来的 doc['text'] 作为回退
            print(f"Warning: File not found: {file_path}")
            file_content = doc.get('text', '')
        
        # 原来的代码（已注释）
        # title, text = doc['title'], doc['text']
        # retrieved_prompt += title_block.replace('__TITLE__', title) + '\n'
        # retrieved_prompt += doc['text'] + '\n' + sep_line + '\n'
        
        # 新逻辑：使用完整文件内容
        retrieved_prompt += title_block.replace('__TITLE__', title) + '\n'
        retrieved_prompt += file_content + '\n' + sep_line + '\n'
    
    # add '# ' to each line except for the last line
    retrieved_prompt = "\n".join(
        [ "# " + x for x in retrieved_prompt.split('\n')[:-1]]
    ) + '\n'
    
    # 添加 global 和 struct 目录的文件内容
    # 从 unique_docs 中提取项目名（使用第一个 doc 的项目名）
    project_name = None
    if unique_docs and len(unique_docs) > 0:
        title = unique_docs[0].get("title", "")
        if title:
            if "-" in title:
                project_name = title.split("-")[0]
            elif "\\" in title:
                project_name = title.split("\\")[0]
            elif "/" in title:
                project_name = title.split("/")[0]
    
    # 如果找到项目名，读取 global 和 struct 目录的文件
    if project_name:
        project_dir = project_code_base / project_name
        for subdir_name in ["global", "struct"]:
            subdir = project_dir / subdir_name
            if subdir.exists() and subdir.is_dir():
                files = [f for f in subdir.iterdir() if f.is_file() and f.suffix == ".st"]
                if files:
                    if subdir_name == "global":
                        retrieved_prompt += "# Global variables and constants from this project (for reference):\n"
                    elif subdir_name == "struct":
                        retrieved_prompt += "# Custom data structures and types from this project (for reference):\n"
                    else:
                        retrieved_prompt += f"# Files from {subdir_name}/ directory (for reference):\n"
                    for file_path in sorted(files):
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                content = f.read()
                                # 添加文件名（带 # 前缀）
                                retrieved_prompt += f"# {file_path.name}\n"
                                # 为文件内容的每一行添加 '# ' 前缀
                                for line in content.split('\n'):
                                    retrieved_prompt += f"# {line}\n"
                        except Exception as e:
                            print(f"Warning: Failed to read {file_path}: {e}")
    
    return retrieved_prompt


class GeneralRepoEval(Task):
    """A task represents an entire benchmark including its dataset, problems,
    answers, generation settings and evaluation methods.
    """

    def __init__(
        self, split, k=[1, 10, 100], num_workers=16, timeout=3.0, topk_docs: int = 2, 
        dataset_path: str = None, dataset_name: str = None, data_files: dict = None, 
        cache_dir: str = None, args=None, tokenizer=None,
    ):
        super().__init__(
            dataset_path=dataset_path,
            dataset_name=dataset_name,
            data_files=data_files,
            cache_dir=cache_dir,
            stop_words=STOP_WORDS,
            requires_execution=args.allow_code_execution if args else False,
        )
        self.split = split
        self.k = k
        self.num_workers = num_workers
        self.timeout = timeout
        self.topk_docs = topk_docs
        
        self.setup_repoeval = args.setup_repoeval if args else False
        self.metric_output_path = args.metric_output_path if args else os.getcwd()
        self.repoeval_input_repo_dir = args.repoeval_input_repo_dir \
            if args and args.repoeval_input_repo_dir else "../retrieval/my_datasets"
        self.repoeval_cache_dir = args.repoeval_cache_dir if args else "tmp"

    def get_dataset(self):
        """Returns dataset for the task or an iterable of any object, that get_prompt can handle"""
        return self.dataset["test"]

    def preprocess_all_data(self, **kwargs):
        # """ concate the prompt and retrieved docs here. Save the new prompts as self.dataset["test"]['processed_prompt'], which is a list of str """
        
        # if "processed_prompt" in self.dataset["test"].column_names:
        #     return
        
        # required_keys = ['tokenizer', 'remove_linebreak', 'add_linebreak', 'max_length_input']
        # assert len([x for x in required_keys if x in kwargs]) == len(required_keys), "missing arguments in preprocessing"
        # tokenizer, remove_linebreak, add_linebreak, max_length_input= kwargs['tokenizer'], kwargs['remove_linebreak'], kwargs['add_linebreak'], kwargs['max_length_input']
        
        # # 适配新格式：新格式使用 provide_code 作为 prompt，旧格式使用 prompt
        # if 'prompt' in self.dataset["test"].column_names:
        #     prompts = self.dataset["test"]['prompt']
        # elif 'provide_code' in self.dataset["test"].column_names:
        #     prompts = self.dataset["test"]['provide_code']
        # else:
        #     raise ValueError("Dataset must have either 'prompt' or 'provide_code' column")
        # # 确保全部为字符串，防止下游 tokenizer 报类型错误
        # prompts = [p if isinstance(p, str) else "" for p in prompts]
        
        # if remove_linebreak:
        #     # remove the last linebreak for starcoder2
        #     prompts = [x if not x.endswith('\n') else x.rstrip() for x in prompts]
        
        # if add_linebreak:
        #     print("Adding linebreaks to the end of the prompts ..")
        #     prompts = [x+'\n' for x in prompts]
        
        # tokenizer.truncation_side = 'left'
        # if tokenizer.pad_token is None:
        #     tokenizer.add_special_tokens({'pad_token': '[PAD]'})

        # # Check if docs column exists and if we should use retrieval
        # has_docs = "docs" in self.dataset["test"].column_names
        # if self.topk_docs == 0 or not has_docs:
        #     max_doc_num = 0
        # else:
        #     max_doc_num = max([len(x) for x in self.dataset["test"]["docs"]])
        
        # if self.topk_docs == 0 or max_doc_num == 0:
        #     start = time.time()
        #     print(f"Preprocessing infile prompts ..")
        #     tokenized_prompts = tokenizer(prompts, truncation=True, padding=True, max_length=max_length_input)
        #     clean_prompts = tokenizer.batch_decode(tokenized_prompts.input_ids, skip_special_tokens=True)
        #     end = time.time()
        #     print(f"finished preprocessing with {end-start}s!")
            
        #     self.dataset["test"] = self.dataset["test"].add_column('processed_prompt', clean_prompts)
        # else:
        #     # raise NotImplementedError("Currently only support generation w/o retrieval") # TBD
        #     docs_list = self.dataset["test"]["docs"]
        #     metadata_list = (
        #         self.dataset["test"]["metadata"]
        #         if "metadata" in self.dataset["test"].column_names
        #         else [{}] * len(docs_list)
        #     )
        #     filtered_docs_list = []
        #     # for docs, metadata in zip(docs_list, metadata_list):
        #     #     fn = metadata.get("function_name") if isinstance(metadata, dict) else None
        #     # 获取 task_id 或 function_name 列表（用于过滤文档）
        #     task_ids = []
        #     function_names = []
        #     if "task_id" in self.dataset["test"].column_names:
        #         task_ids = self.dataset["test"]["task_id"]
        #     if "function_name" in self.dataset["test"].column_names:
        #         function_names = self.dataset["test"]["function_name"]
            
        #     for idx, (docs, metadata) in enumerate(zip(docs_list, metadata_list)):
        #         # 优先从 metadata 获取，然后从 function_name 列获取，最后从 task_id 列获取
        #         fn = None
        #         if isinstance(metadata, dict):
        #             fn = metadata.get("function_name")
        #         if not fn and function_names and idx < len(function_names):
        #             fn = function_names[idx]
        #         if not fn and task_ids and idx < len(task_ids):
        #             fn = task_ids[idx]
        #         filtered_docs_list.append(
        #             filter_docs_for_prompt(docs, fn, self.topk_docs)
        #         )
        #     retrieved_prompts = [
        #         get_retrieved_prompt(filtered) for filtered in filtered_docs_list
        #     ]
        #     # full_prompts = [r + p for r, p in zip(retrieved_prompts, prompts)]
            
        #     retrieved_max_length_input = infile_max_length_input = max_length_input // 2 - 2
            
        #     # retrieved prompts
        #     start = time.time()
        #     print(f"Preprocessing retrieved docs ({self.topk_docs} per example) ..")
        #     tokenizer.truncation_side = 'right'
        #     tokenized_retrieved_prompts = tokenizer(retrieved_prompts, truncation=True, padding=True, max_length=retrieved_max_length_input)
        #     clean_retrieved_prompts = tokenizer.batch_decode(tokenized_retrieved_prompts.input_ids, skip_special_tokens=True)
            
        #     # infile prompts 
        #     print(f"Preprocessing infile prompts ..")
        #     tokenizer.truncation_side = 'left'
        #     tokenized_prompts = tokenizer(prompts, truncation=True, padding=True, max_length=infile_max_length_input)
        #     clean_prompts = tokenizer.batch_decode(tokenized_prompts.input_ids, skip_special_tokens=True)
            
        #     full_prompts = [p + '\n\n' + r for p, r in zip(clean_prompts, clean_retrieved_prompts)]
            
        #     # test 
        #     print(f"test preprocessing ..")
        #     tokenzied_full_prompts = tokenizer(full_prompts, truncation=False, padding=True)
        #     assert len(tokenzied_full_prompts.input_ids[0]) <= max_length_input
        #     end = time.time()
            
        #     print(f"finished preprocessing with {end-start}s!")
            
        #     self.dataset["test"] = self.dataset["test"].add_column('processed_prompt', full_prompts)
        pass

    def get_prompt(self, doc):
        print("enter get_prompt")
        """Builds the prompt for the LM to generate from."""
        if "processed_prompt" in doc: 
            print("get prompt return earily")
            return doc["processed_prompt"]
        # 适配新格式：新格式使用 provide_code 作为 prompt，旧格式使用 prompt
        if "prompt" in doc:
            prompt = doc["prompt"]
        elif "provide_code" in doc:
            prompt = doc["provide_code"]
        else:
            # metadata = doc.get("metadata", {}) or {}
            # function_name = metadata.get("function_name") or doc.get("function_name")
            raise ValueError("Document must have either 'prompt' or 'provide_code' field")
        retrieved_docs = doc.get("docs", [])
        # 优先使用 function_name，如果没有则使用 task_id 作为回退
        function_name = doc.get("function_name") or doc.get("task_id")
        if not function_name:
            # 如果还是没有，尝试从其他可能的字段获取
            function_name = doc.get("metadata", {}).get("function_name") if isinstance(doc.get("metadata"), dict) else None
        filtered_docs = filter_docs_for_prompt(retrieved_docs, function_name, self.topk_docs)
        if filtered_docs:
            context = get_retrieved_prompt(docs=filtered_docs)
            prompt = prompt + '\n\n' + "Here are some relevant code fragments from other files of the repo:" + context
        
        # 添加 global 和 struct 目录的文件内容
        project_code_base = Path(r"F:\项目级st补全\repo_gen_project\dataset\project_code")
        
        # 从 filtered_docs 中提取项目名
        project_name = None
        print(f"[DEBUG] filtered_docs exists: {filtered_docs is not None}, length: {len(filtered_docs) if filtered_docs else 0}")
        if filtered_docs and len(filtered_docs) > 0:
            title = filtered_docs[0].get("title", "")
            print(f"[DEBUG] title from filtered_docs[0]: {title}")
            if title:
                if "-" in title:
                    project_name = title.split("-")[0]
                elif "\\" in title:
                    project_name = title.split("\\")[0]
                elif "/" in title:
                    project_name = title.split("/")[0]
        
        # 如果还没找到项目名，尝试从 metadata 获取
        if not project_name:
            metadata = doc.get("metadata", {})
            print(f"[DEBUG] project_name is None, trying metadata: {metadata}")
            if isinstance(metadata, dict):
                fpath_tuple = metadata.get("fpath_tuple", [])
                print(f"[DEBUG] fpath_tuple: {fpath_tuple}")
                if fpath_tuple and len(fpath_tuple) > 0:
                    project_name = fpath_tuple[0]
        
        # 如果找到项目名，读取 global 和 struct 目录的文件
        print(f"[DEBUG] Final project_name: {project_name}", flush=True)

        # code  这个调用上下文似乎影响不大
        if project_name:
            project_dir = project_code_base / project_name

            # 递归搜索项目目录下所有文件：若文件内容包含 function_name（且非同名文件），
            # 将该文件完整内容拼接进 prompt，用于补充被调用上下文。
            # if project_dir.exists() and project_dir.is_dir() and function_name:
            #     caller_files = []
            #     function_name_lower = str(function_name).strip().lower()
            #     for file_path in sorted(project_dir.rglob("*")):
            #         if not file_path.is_file():
            #             continue
            #         # 排除“自身文件”（文件名等于 function_name）
            #         if file_path.stem.strip().lower() == function_name_lower:
            #             continue
            #         try:
            #             content = file_path.read_text(encoding="utf-8")
            #         except Exception:
            #             continue
            #         if function_name in content:
            #             caller_files.append((file_path, content))

            #     if caller_files:
            #         prompt += "\n\n# Files referencing the target function (full context):\n"
            #         for file_path, content in caller_files:
            #             rel_path = file_path.relative_to(project_dir)
            #             prompt += f"# {rel_path}\n{content}\n"

            for subdir_name in ["global", "struct"]:
                subdir = project_dir / subdir_name
                if subdir.exists() and subdir.is_dir():
                    files = [f for f in subdir.iterdir() if f.is_file() and f.suffix == ".st"]
                    if files:
                        if subdir_name == "global":
                            prompt += "\n\n# Global variables and constants from this project (for reference):\n"
                        elif subdir_name == "struct":
                            prompt += "\n\n# Custom data structures and types from this project (for reference):\n"
                        else:
                            prompt += f"\n\n# Files from {subdir_name}/ directory (for reference):\n"
                        for file_path in sorted(files):
                            try:
                                with open(file_path, "r", encoding="utf-8") as f:
                                    content = f.read()
                                    prompt += f"# {file_path.name}\n{content}\n"
                            except Exception as e:
                                print(f"Warning: Failed to read {file_path}: {e}")
        
        return prompt

    def get_reference(self, doc):
        """Builds the reference solution for the doc (sample from the test dataset)."""
        # 适配新格式：新格式没有 reference，需要从 metadata 中获取 ground_truth
        if "reference" in doc:
            return [doc["reference"]]
        elif "metadata" in doc and isinstance(doc["metadata"], dict):
            ground_truth = doc["metadata"].get("ground_truth")
            if ground_truth:
                return [ground_truth]
        # metadata = doc.get("metadata", {}) or {}
        # function_name = metadata.get("function_name") or doc.get("function_name")
        # 如果都没有，返回错误标记
        return ["error"]

    def get_retrieved_sources(self, doc):
        # 优先使用 function_name，如果没有则使用 task_id 作为回退
        function_name = doc.get("function_name") or doc.get("task_id")
        filtered_docs = filter_docs_for_prompt(
            doc.get("docs", []), function_name, self.topk_docs
        )
        return [d.get("title") for d in filtered_docs if d.get("title")]

    def postprocess_generation(self, generation, idx, new_tokens_only=False):
        """Defines the postprocessing for a LM generation.
        :param generation: str
            code generation from LM
        :param idx: int
            index of doc in the dataset to which the generation belongs
        """
        if not new_tokens_only:
            prompt = self.get_prompt(self.dataset["test"][idx])
            generation = generation[len(prompt) :]
            return self._stop_at_stop_token(generation, self.stop_words)
        else:
            return generation

    def process_results(self, generations, references):
        """Takes the list of LM generations and evaluates them against ground truth references,
        returning the metric for the generations.
        :param generations: list(list(str))
            list of lists containing generations
        :param references: list(str)
            list of str containing refrences
        """
        # extract code blocks 
        CODE_BLOCK_PATTERN = r"```(\w*)\n(.*?)\n```"
        def extract_code(text: str, pattern: str = CODE_BLOCK_PATTERN):
            match = re.findall(pattern, text, flags=re.DOTALL)
            return match[0][1] if match else text
        
        generations = [[extract_code(x[0])] for x in generations]
        
        EM_scores, ES_scores = [], []
        clean_references, clean_generations = [], []
        for ref, gen in zip(references, generations):
            clean_ref, clean_gen = process_prediction(ref[0], gen[0])
            EM_scores.append(compute_EM(clean_ref, clean_gen))
            ES_scores.append(compute_ES(clean_ref, clean_gen))
            
            clean_references.append(clean_ref)
            clean_generations.append(clean_gen)
        
        import evaluate
        bleu = evaluate.load("bleu")
        try:
            bleu_results = bleu.compute(
                references=[[x] for x in clean_references],
                predictions=clean_generations,
            )
        except (ZeroDivisionError, ValueError) as e:
            # Handle edge cases where BLEU calculation fails
            print(f"Warning: BLEU calculation failed: {e}. Using default values.")
            bleu_results = {"bleu": 0.0, "precisions": [0.0, 0.0, 0.0, 0.0], "brevity_penalty": 0.0, "length_ratio": 0.0, "translation_length": 0, "reference_length": 0}
        
        results = {
            "bleu_results": bleu_results,
            "EM": np.mean(EM_scores),
            "ES": np.mean(ES_scores)
        }
        
        if self.split == "function" and self.requires_execution:
            # evaluate execution accuracy 
            metadata = self.dataset["test"]['metadata']
            
            setup_success = True
            if self.setup_repoeval:
                print("Running setup for RepoEval-func ..")
                setup_repos(input_dir=self.repoeval_input_repo_dir, output_dir=self.repoeval_cache_dir)
                print("Validating tests for RepoEval-func ..")
                setup_success = check_tests(output_dir=self.repoeval_cache_dir)
            else:
                copy_all_repos(input_dir=self.repoeval_input_repo_dir, output_dir=self.repoeval_cache_dir)
                
            if setup_success:
                print("Running evaluation for RepoEval-func ..")
                assert len(generations) == len(references) == len(metadata)
                
                tmp_output_path = self.metric_output_path + '.intermediate'
                if os.path.exists(tmp_output_path):
                    execution_results = json.load(open(tmp_output_path, 'r'))
                else:
                    execution_results = {}
                
                new_generation_count = 0
                for i, (gen, ref, meta) in enumerate(tqdm(zip(generations, references, metadata), total=len(generations))):
                    gen, ref = gen[0], ref[0]
                    repo = meta["fpath_tuple"][0]
                    task_id = meta["task_id"]
                    
                    if task_id in execution_results and execution_results[task_id] != "timeout":
                        continue
                    
                    return_result = eval_generation(
                        gen, ref, meta, return_output=False, eval_relevant_test_only=True,
                        input_dir=self.repoeval_input_repo_dir, output_dir=self.repoeval_cache_dir,
                    )
                    execution_results[task_id] = return_result
                    new_generation_count += 1
                    
                    if new_generation_count % 5 == 0 and new_generation_count > 0:
                        print(f"Saving intermediate results to {tmp_output_path} ..")
                        json.dump(execution_results, open(tmp_output_path, 'w'), indent=4)
                        
                print(f"Saving intermediate results to {tmp_output_path} ..")
                json.dump(execution_results, open(tmp_output_path, 'w'), indent=4)
                
                results["Pass@1"] = np.mean([1 if x == "success" else 0 for x in execution_results.values()])
                results["Num_computed"] = len(execution_results)
                results["Num_timeout"] = sum([1 if x == "timeout" else 0 for x in execution_results.values()])
        
        return results
