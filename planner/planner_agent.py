#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
"""
规划器代理模块

目标：
- 接收：query JSON 内容（如 FB_counter.json）、待补全函数名、函数类型、项目名称
- 调用 context_window.collect_contexts 获取被调用位置的上下文窗口
- 将 requirement / provide_code / 上下文窗口 组装成 prompt
- 调用大语言模型，生成「功能规划设计步骤」，为后续代码生成提供指引

当前版本：
- 所有输入均使用硬编码示例，方便你本地调试和后续集成。
"""

import sys
import json
from pathlib import Path
from typing import List, Optional

# 添加项目根目录到 Python 路径，确保可以导入 planner 模块
REPO_ROOT = Path(__file__).parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# 智增增 / OpenAI API 配置（与 verifier 中保持一致风格）
ZHIZENGZENG_API_KEY = os.getenv("ZHIZENGZENG_API_KEY")
ZHIZENGZENG_BASE_URL = os.getenv("ZHIZENGZENG_BASE_URL", "https://api.zhizengzeng.com/v1")

from planner.context_window import (
    PlannerConfig,
    collect_contexts,
    ContextWindow,
    collect_similar_contexts
)


def build_planning_prompt(
    requirement: str,
    provide_code: str,
    function_name: str,
    function_type: str,
    project_name: str,
    contexts: List[ContextWindow],
    similar_file_context: Optional[List[str]] = None,
) -> str:
    """
    构造用于规划的 Prompt，将需求、已有声明代码和调用上下文综合起来。
    """
    context_blocks = []
    for idx, ctx in enumerate(contexts, 1):
        block = [
            f"【上下文片段 {idx}】",
            f"- 文件: {ctx.file_path}",
            f"- 行号: {ctx.line_number}",
            f"- 类型: {ctx.context_type}",
            "```st",
            ctx.code_window.strip(),
            "```",
        ]
        context_blocks.append("\n".join(block))

    context_section = "\n\n".join(context_blocks) if context_blocks else "（未找到调用上下文，仅根据需求和声明规划）"

    # 相似函数源码（来自检索到的其他 ST 文件）
    similar_blocks: List[str] = []
    if similar_file_context:
        for idx, code in enumerate(similar_file_context, 1):
            block = [
                f"【相似函数源码片段 {idx}】",
                "```st",
                code.strip(),
                "```",
            ]
            similar_blocks.append("\n".join(block))
    similar_section = "\n\n".join(similar_blocks) if similar_blocks else "（未提供相似函数源码，仅基于当前函数信息规划）"

#     prompt = f"""
# 你是 IEC 61131-3 / CODESYS ST 领域的高级架构师，现在需要为一个函数块/函数编写**实现步骤规划**，帮助后续代码生成更贴近真实 ground truth。

# ==================== 基本信息 ====================
# - 项目名称: {project_name}
# - 函数类型: {function_type}
# - 函数名: {function_name}

# ==================== 需求说明（requirement） ====================
# {requirement.strip()}

# ==================== 已有声明部分====================
# ```st
# {provide_code.strip()}
# ```

# ==================== 调用上下文窗口（来自项目代码） ====================
# {context_section}

# ==================== 相似函数源码片段（来自检索结果，可作为参考实现风格） ====================
# {similar_section}

# ==================== 核心编写规则（必须严格遵守） ====================
# 1. 步骤仅聚焦函数 / 函数块的核心执行逻辑，不包含：
# - 额外的 “约束和假设”“无状态特性” 等非执行步骤内容；
# - 对调用场景的冗余描述（如 “提供给主程序用于显示” 这类无执行意义的内容）；
# - 重复的校验逻辑（如已校验非负则无需再提 “强制设为零” 之外的解释）。
# 2. 每一步仅描述一个独立的操作 / 逻辑，语言简洁、无修饰，直接说明 “做什么”；
# 3. 步骤中引用的变量名、类型必须与声明部分 / 调用上下文完全一致；
# 4. 仅处理「明确要求」的内容，不做任何额外的“健壮性优化”“边界防护”“异常容错”等过度设计。
# 5. 步骤数量控制在 3-6 步，仅保留核心逻辑，剔除所有非必要的补充说明。

# ==================== 特别注意 ====================
# 仅处理「明确要求」的内容，不做任何额外的诸如“健壮性优化”“边界防护”“异常容错”等过度设计。
# ==================== 你的任务 ====================
# 1. 基于上述需求、声明和调用上下文，推断该函数块/函数在整个项目中的职责、输入输出意义以及与其他模块的交互关系。
# 2. 给出一个**分步骤的功能规划/设计说明**，每一步都要尽量贴近调用场景。
# 3. 规划结果要适合后续直接转换为 ST 实现代码，注意：
#    - 不要给出具体 ST 代码，只写步骤/逻辑。
#    - 引用调用上下文中的变量名、调用方式，保持语义一致。
#    - 如果发现调用方式隐含了某些约束（例如只在某些状态下调用），在规划里明确写出。

# ==================== 输出格式要求 ====================
# 请严格使用如下中文结构化格式输出（不要添加多余解释）：

# 功能规划:
# 1. ...
# 2. ...
# 3. ...
# N. ...
# """

    prompt = f"""
You are a senior architect in the field of IEC 61131-3 / CODESYS ST. You are required to create an implementation step plan for a function block/function to help the subsequent code generation align more closely with the actual ground truth.

==================== Basic Information ====================
- Project Name:  {project_name}
- Function Type: {function_type}
- Function Name: {function_name}

==================== Requirement Description ====================
{requirement.strip()}

==================== Existing Declaration Section ====================
```st
{provide_code.strip()}
```

==================== Call Context Window (From Project Code) ====================
{context_section}

==================== Similar Function Source Code Snippets (From Retrieval Results, for Reference of Implementation Style) ====================
{similar_section}

==================== Core Writing Rules (Must Be Strictly Followed) ====================
1. Steps shall only focus on the core execution logic of the function/function block, and exclude the following content:
- Extra non-execution step content such as "constraints and assumptions" and "stateless characteristics";
- Redundant descriptions of the call scenario (e.g., content with no execution meaning such as "provided to the main program for display");
- Duplicate validation logic (e.g., no additional explanations other than "force set to zero" are needed if non-negativity has already been validated).
2. Each step shall describe only one independent operation/logic with concise, unadorned language that directly states what to do;
3. Variable names and types referenced in the steps must be completely consistent with those in the declaration section and call context;
4. Only process the content explicitly required, without any over-engineering such as additional "robustness optimization", "boundary protection" or "exception fault tolerance";
5. Limit the number of steps to 3-6, retaining only the core logic and removing all unnecessary supplementary explanations.

==================== Special Notes ====================
Only process the content explicitly required, without any over-engineering such as additional "robustness optimization", "boundary protection", "exception fault tolerance" and the like.
==================== Your Tasks ====================
1. Based on the aforementioned requirements, declarations and call context, infer the responsibility of the function block/function in the entire project, the meaning of its inputs and outputs, and its interaction with other modules;
2. Create a step-by-step function plan/design specification that aligns as closely as possible with the call scenario;
3. The plan results shall be suitable for direct conversion into ST implementation code, with the following notes:
- Do not provide specific ST code, only write the steps/logic;
- Reference the variable names and call methods in the call context to maintain semantic consistency;
- If any implicit constraints are found in the call method (e.g., called only under certain states), specify them clearly in the plan.

==================== Output Format Requirements ====================
Please output strictly in the following English structured format (no extra explanations added):

Function Plan:
1. ...
2. ...
3. ...
N. ...
"""
    return prompt.strip()


def call_llm_for_plan(prompt: str) -> str:
    """
    调用大语言模型生成规划结果。

    说明：
    - 默认使用智增增 / OpenAI 风格的 Chat Completions 接口（与 verifier 中逻辑一致）。
    - 也支持传入自定义 llm_client。
    """
    # 为了保持简单，这里不暴露 llm_client/use_openai 参数，
    # 而是直接走与 verifier 相同的 zhizengzeng 调用路径。
    api_key = ZHIZENGZENG_API_KEY
    base_url = ZHIZENGZENG_BASE_URL

    if not api_key:
        raise RuntimeError(
            "未配置 ZHIZENGZENG_API_KEY，无法调用规划 LLM。\n"
            "请在命令行中设置：\n"
            "  set ZHIZENGZENG_API_KEY=你的API密钥\n"
            "  set ZHIZENGZENG_BASE_URL=https://api.zhizengzeng.com/v1"
        )

    # 构造 messages：简单使用一个 system + 一个 user
    # system_msg = (
    #     "你是熟悉 CODESYS / IEC 61131-3 Structured Text 的资深架构师，"
    #     "擅长根据需求说明、已有声明代码和调用上下文，为函数块和函数设计实现步骤规划，并且会严格遵守\"核心编写规则\"和\"特别注意\"中的限制."
    # )
    system_msg = (
        "You are a senior architect proficient in CODESYS / IEC 61131-3 Structured Text, skilled in designing implementation step plans for function blocks and functions based on requirement descriptions, existing declaration code and call contexts, and will strictly adhere to the constraints specified in the Core Writing Rules and Special Notes."
    )

#    print(prompt)
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt},
    ]

    try:
        import openai

        client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )

        # 简单提取第一条回复内容
        choice = response.choices[0]
        if hasattr(choice, "message") and hasattr(choice.message, "content"):
            return choice.message.content
        # 兜底处理
        return str(choice)

    except ImportError:
        raise ImportError("需要安装 openai 库: pip install openai")
    except Exception as e:
        raise RuntimeError(f"调用规划 LLM 失败: {e}")


def generate_plan_for_function(
    function_name: str,
    project_name: str,
) -> str:
    """
    为指定项目中的某个函数/函数块生成功能规划。

    参数:
        function_name: 函数名（例如: FB_counter）
        project_name: 项目名称（例如: counter）

    说明:
        - 自动从 dataset/query/repoeval_{project_name}/{function_name}.json 读取 requirement/provide_code
        - 自动根据 provide_code 判断 function_type（FUNCTION_BLOCK / FUNCTION / METHOD）
        - 自动从 dataset/project_code/{project_name} 中收集调用上下文
    """
    repo_root = Path(__file__).parent.parent

    # 1. 读取 query JSON
    query_json_path = (
        repo_root
        / "dataset"
        / "query"
        / f"repoeval_{project_name}"
        / f"{function_name}.json"
    )

    if not query_json_path.exists():
        raise FileNotFoundError(f"示例 query JSON 不存在: {query_json_path}")

    data = json.loads(query_json_path.read_text(encoding="utf-8"))
    requirement = data.get("requirement", "").strip()
    provide_code = data.get("provide_code", "").strip()

    # 2. 自动判断函数类型
    upper_provide = provide_code.lstrip().upper()
    if upper_provide.startswith("FUNCTION_BLOCK"):
        function_type = "function_block"
    elif upper_provide.startswith("FUNCTION"):
        function_type = "function"
    elif upper_provide.startswith("METHOD"):
        function_type = "method"
    else:
        # 默认按 FUNCTION_BLOCK 处理
        function_type = "function_block"

    # 3. 使用 context_window 收集调用上下文
    config = PlannerConfig(
        project_code_root=repo_root / "dataset" / "project_code",
        context_window_size=10,
        function_type=function_type,
    )

    contexts = collect_contexts(
        function_name=function_name,
        config=config,
        project_name=project_name,
    )

    # 4. 构造规划 Prompt
    prompt = build_planning_prompt(
        requirement=requirement,
        provide_code=provide_code,
        function_name=function_name,
        function_type=function_type,
        project_name=project_name,
        contexts=contexts,
    )

    # 5. 调用大模型生成规划
    plan_text = call_llm_for_plan(prompt)

    return plan_text


def generate_plan_for_case(
    case: dict,
    project_name: str,
    function_name: Optional[str] = None,
    results_jsonl_path: Optional[Path] = None,
) -> tuple[str, str]:
    """
    为 query 目录中的一个 case（JSON 文件）生成功能规划（与 generation 粒度对齐）。

    参数:
        case: query 目录中的 JSON 文件内容（字典，包含 requirement 和 provide_code）
        project_name: 项目名称（例如: counter）
        function_name: 函数名（可选，如果提供则使用，否则尝试从 case 中提取）

    返回:
        (plan_text, user_prompt) 元组：
        - plan_text: LLM 生成的规划结果
        - user_prompt: 传给 LLM 的 user prompt（用于保存）

    说明:
        - case 来自 dataset/query/repoeval_{project_name}/{function_name}.json
        - 从 case 中读取 requirement 和 provide_code
        - 自动根据 provide_code 判断 function_type
        - 自动从 dataset/project_code/{project_name} 中收集调用上下文
    """
    repo_root = Path(__file__).parent.parent

    # 1. 确定 function_name
    if not function_name:
        # 尝试从 case 中提取（兼容 results.jsonl 格式）
        metadata = case.get("metadata", {})
        if isinstance(metadata, dict):
            function_name = metadata.get("function_name")
        
        # 如果还是没有，尝试从 task_id 提取
        if not function_name:
            function_name = case.get("task_id")
        
        if not function_name:
            raise ValueError("无法确定 function_name，请提供 function_name 参数或确保 case 中包含 metadata.function_name 或 task_id")

    # 2. 从 case 中读取 requirement 和 provide_code（query JSON 文件直接包含这些字段）
    requirement = case.get("requirement", "").strip()
    provide_code = case.get("provide_code", "").strip()

    if not provide_code:
        raise ValueError(f"case 中缺少 provide_code 字段")

    # 3. 自动判断函数类型
    upper_provide = provide_code.lstrip().upper()
    if upper_provide.startswith("FUNCTION_BLOCK"):
        function_type = "function_block"
    elif upper_provide.startswith("FUNCTION"):
        function_type = "function"
    elif upper_provide.startswith("METHOD"):
        function_type = "method"
    else:
        # 默认按 FUNCTION_BLOCK 处理
        function_type = "function_block"

    # 4. 使用 context_window 收集调用上下文
    config = PlannerConfig(
        project_code_root=repo_root / "dataset" / "project_code",
        context_window_size=10,
        function_type=function_type,
    )

    contexts = collect_contexts(
        function_name=function_name,
        config=config,
        project_name=project_name,
    )

    # 4.1 基于检索结果收集相似函数源码（可选，用于后续增强规划提示）
    # results.jsonl 的推荐来源：output/{timestamp_dir}/repoeval_{project_name}/results.jsonl
    # 如果调用方未显式提供，则回退到 output/{project_name}/results.jsonl（兼容老用法）
    if results_jsonl_path is None:
        results_jsonl_path = (
            repo_root
            / "output"
            / project_name
            / "results.jsonl"
        )
    project_code_dir = repo_root / "dataset" / "project_code" / project_name

    similar_file_context = collect_similar_contexts(
        function_name=function_name,
        results_jsonl_path=results_jsonl_path,
        project_code_dir=project_code_dir,
    )



    # 5. 构造规划 Prompt（加入相似函数源码信息）
    prompt = build_planning_prompt(
        requirement=requirement,
        provide_code=provide_code,
        function_name=function_name,
        function_type=function_type,
        project_name=project_name,
        contexts=contexts,
        similar_file_context=similar_file_context,
    )

    # 6. 调用大模型生成规划
    plan_text = call_llm_for_plan(prompt)

    return plan_text, prompt


def demo_run_planner() -> None:
    """
    演示：以 FB_counter 为例，跑通一条端到端流程（全部硬编码）。
    """
    project_name = "counter"
    function_name = "FB_counter"

    plan_text = generate_plan_for_function(
        function_name=function_name,
        project_name=project_name,
    )

    # 输出结果（后续可以改为写入文件或返回给调用方）
    #print(plan_text)


if __name__ == "__main__":
    demo_run_planner()


