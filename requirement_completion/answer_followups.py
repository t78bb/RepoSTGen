#!/usr/bin/env python3
"""
根据 ambiguity_check 提出的「追问列表」，用大模型基于“整个所属项目代码”生成回答。

核心思路：
- 读取 dataset/project_code/<项目> 下所有 .st 作为项目代码上下文（可选截断）
- 对每个 case 的追问列表一次性提问，让模型输出 JSON 回答列表
- 将 user_prompt 与回答结果落盘到 requirement_completion/output/<run_id>/ 下的 answers_* 目录

用法示例：
  cd requirement_completion
  python answer_followups.py --run-id 20260217_144310 --project repoeval_traffic_light
  python answer_followups.py --run-id 20260217_144310 --project repoeval_counter --case FB_counter
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import openai
except ImportError:
    openai = None

REQUIREMENT_COMPLETION_DIR = Path(__file__).resolve().parent
REPO_ROOT = REQUIREMENT_COMPLETION_DIR.parent
PROJECT_CODE_BASE = REPO_ROOT / "dataset" / "project_code"
CODE_DESCRIPTION_BASE = REPO_ROOT / "dataset" / "code_description"
# 开关：True=回答时加载整个项目代码；False=仅加载当前 case 对应代码
USE_ALL_PROJECT_CODE_CONTEXT = False

# 复用 output/run_id 约定
sys.path.insert(0, str(REQUIREMENT_COMPLETION_DIR))
from persist_io import DEFAULT_OUTPUT_DIR, make_run_id  # noqa: E402


def get_api_config() -> Tuple[str, str]:
    api_key = (
        os.getenv("ZHIZENGZENG_API_KEY")
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("API_KEY")
    )
    base_url = (
        os.getenv("BASE_URL")
        or os.getenv("ZHIZENGZENG_BASE_URL")
        or "https://api.zhizengzeng.com/v1"
    )
    if not api_key:
        raise RuntimeError("未找到 API 密钥，请设置 ZHIZENGZENG_API_KEY / OPENAI_API_KEY / API_KEY")
    return api_key, base_url


def project_dir_to_code_name(project_name: str) -> str:
    """repoeval_xxx -> xxx（匹配 project_code 目录名）"""
    return project_name[len("repoeval_") :] if project_name.startswith("repoeval_") else project_name


def load_project_code(
    project_name: str,
    project_code_base: Path = PROJECT_CODE_BASE,
    max_chars: int = 220_000,
    case_name: Optional[str] = None,
) -> Tuple[str, Dict[str, Any]]:
    """
    读取项目代码上下文（带文件名分隔）。过长则截断。
    - USE_ALL_PROJECT_CODE_CONTEXT=True：读取项目目录下所有 .st
    - USE_ALL_PROJECT_CODE_CONTEXT=False：只读取当前 case 对应的 .st（需传 case_name）
    返回 (code_text, meta)。
    """
    code_name = project_dir_to_code_name(project_name)
    project_dir = project_code_base / code_name
    if not project_dir.exists():
        # 容错：大小写/直接匹配失败时尝试不区分大小写
        lower = code_name.lower()
        match = next((d for d in project_code_base.iterdir() if d.is_dir() and d.name.lower() == lower), None)
        if match:
            project_dir = match

    if not project_dir.exists() or not project_dir.is_dir():
        return "", {"error": f"project_code 中找不到项目目录: {project_dir}"}

    if USE_ALL_PROJECT_CODE_CONTEXT:
        st_files = sorted(project_dir.rglob("*.st"))
    else:
        target_name = (case_name or "").strip()
        if not target_name:
            return "", {"error": "仅 case 模式下缺少 case_name"}
        # 优先按文件名精确匹配（不限定子目录），若有多个同名文件则全部纳入
        st_files = sorted(project_dir.rglob(f"{target_name}.st"))
        if not st_files:
            return "", {"error": f"未找到 case 对应代码文件: {target_name}.st（目录: {project_dir}）"}
    chunks: List[str] = []
    total = 0
    truncated = False

    for p in st_files:
        try:
            content = p.read_text(encoding="utf-8")
        except Exception:
            continue
        header = f"\n\n===== FILE: {p.relative_to(project_dir).as_posix()} =====\n"
        piece = header + content
        if total + len(piece) > max_chars:
            remaining = max_chars - total
            if remaining > 2000:
                chunks.append(piece[:remaining] + "\n\n...（项目代码已截断）...\n")
            truncated = True
            break
        chunks.append(piece)
        total += len(piece)

    return "".join(chunks).lstrip(), {
        "project_code_dir": str(project_dir),
        "context_mode": "all_project" if USE_ALL_PROJECT_CODE_CONTEXT else "single_case",
        "case_name": case_name or "",
        "st_file_count": len(st_files),
        "used_chars": total,
        "max_chars": max_chars,
        "truncated": truncated,
    }


def _answers_prompts_dir(run_id: str, project_name: str) -> Path:
    return DEFAULT_OUTPUT_DIR / run_id / "answers_prompts" / project_name


def _answers_results_dir(run_id: str, project_name: str) -> Path:
    return DEFAULT_OUTPUT_DIR / run_id / "answers" / project_name


def save_answer_prompt(run_id: str, project_name: str, case_id: str, prompt: str) -> Path:
    d = _answers_prompts_dir(run_id, project_name)
    d.mkdir(parents=True, exist_ok=True)
    safe = case_id.replace("/", "_").replace("\\", "_")
    path = d / f"{safe}.txt"
    path.write_text(prompt, encoding="utf-8")
    return path


def save_answer_result(run_id: str, project_name: str, case_id: str, result: Dict[str, Any]) -> Path:
    d = _answers_results_dir(run_id, project_name)
    d.mkdir(parents=True, exist_ok=True)
    safe = case_id.replace("/", "_").replace("\\", "_")
    path = d / f"{safe}.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_ambiguity_results(run_id: str, project_name: str) -> List[Dict[str, Any]]:
    """
    从 requirement_completion/output/<run_id>/results 读取 ambiguity_check 的结果。
    优先读批文件 results/<project>.json；否则读 results/<project>/*.json。
    """
    results_dir = DEFAULT_OUTPUT_DIR / run_id / "results"
    batch = results_dir / f"{project_name}.json"
    if batch.exists():
        try:
            data = json.loads(batch.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except Exception:
            return []
    per_dir = results_dir / project_name
    out: List[Dict[str, Any]] = []
    if per_dir.exists():
        for p in sorted(per_dir.glob("*.json")):
            try:
                obj = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
            if isinstance(obj, dict):
                out.append(obj)
    return out


def load_project_description(
    project_name: str,
    case_id: str,
    code_description_base: Path = CODE_DESCRIPTION_BASE,
) -> Optional[str]:
    """
    从 dataset/code_description/<子目录>/<对应项>.json 读取 description_en。
    子目录 = project_dir_to_code_name(project_name)，对应项 = case_id 最后一段（如 F_isScaleOutput）。
    若文件不存在或字段缺失，返回 None。
    """
    code_name = project_dir_to_code_name(project_name)
    case_stem = case_id.split("/")[-1] if "/" in case_id else case_id
    json_path = code_description_base / code_name / f"{case_stem}.json"
    if not json_path.exists():
        return None
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        return (data.get("description_cn") or "").strip() or None
    except Exception:
        return None


def build_answer_prompt(
    case_id: str,
    followups: List[Dict[str, Any]],
    project_code_text: str,
    project_code_meta: Dict[str, Any],
) -> str:
    """
    构造回答 prompt：让模型基于项目代码“理解约束”，但以“人类澄清需求”的口吻回答（避免代码细节），输出 JSON。
    """

    # 旧版 prompt（过于依赖代码细节，容易让回答看起来“像作弊”），按需求保留但不再使用：
    # return f"""你所要扮演的是一个解答疑问的人类。问题提问者的问题是基于项目待补全代码的模糊需求所提出的问题，而你有着完整的代码实现，因此你要让需求的模糊点明确化。
    # 请你基于「项目代码」提供的信息回答「追问列表」中的问题，但是注意实际的代码知识给你一个参考，你要想象你是还没有写出这个代码的人类，正在根据整个代码回答精确的需求问题。若项目代码中无法确定答案，请明确输出“无法从项目代码中确定”，并说明缺失的关键信息是什么。
    #
    # 【case_id】
    # {case_id}
    #
    # 【追问列表】
    # {json.dumps(followups, ensure_ascii=False, indent=2)}
    #
    # 【项目代码信息】
    # {json.dumps(project_code_meta, ensure_ascii=False, indent=2)}
    #
    # 【项目代码（Structured Text）】
    # ```st
    # {project_code_text}
    # ```
    #
    # 输出格式（严格 JSON，不要多余文字）： 
    # {{
    #   "回答列表": [
    #     {{
    #       "模糊点类型": "…原问题中的模糊点类型…",
    #       "追问问题": "…原问题…",
    #       "回答": "…基于项目代码的答案…"
    #     }}
    #   ]
    # }}
    # """

#old    3) 回答写成“人类澄清需求”的口吻，不引用文件名、函数名、变量名，不贴代码；用“通过…变量/输出…”“在…条件下…”“范围为…”“单位为…”等表述。

#     return f"""你扮演的是**回答需求追问的人类**。你心里清楚“待实现代码该做什么、不该做什么、具备哪些标准”，这些信息**全部且仅来自下面给出的项目代码**：代码里有的行为你才可以说，代码里没有的行为你绝不能编造。

# 核心规则（必须遵守）：
# 1) 只描述项目代码中实际存在的行为。若代码里没有实现某类行为（例如没有写日志、没有界面显示、没有错误码枚举、没有重试逻辑），则回答中**不得**提及该类行为；只用语义化、需求层面的说法描述代码里实际有的处理方式。
# 2) 若追问涉及“功能块/实例化/类型选择/调用方式”（如“是否独立实例化”“使用什么功能块控制”），回答中**必须包含代码里的具体类型名或功能块名**（例如 `MC_Power`），不能只写“独立实例化电源控制功能块”这类泛化表述。
# 3) 若追问涉及“范围约束/上下界/阈值/默认值/比例系数/偏移量”等数值约束，回答中必须写出代码里的具体数值常量，不能只写“动态调整”“由 CASE 决定”这类机制性表述。
# 4) 若追问涉及“计算公式”，回答需同时给出：使用哪些关键变量（可写变量名）+ 关键常量值（若有）+ 计算方向（如“物理量映射到终端量”），避免只给抽象描述。
# 5) 回答写成“人类澄清需求”的口吻，可以引用函数名、变量名、类型名（如 `MC_Power`），但是不贴代码。
# 6) 若某追问在项目代码中无法对应到任何实现，或代码未体现该方面信息，回答仅写"无需考虑"。
# 7) 会提供给你整个项目的代码，但是你只用关心 case_id 对应的函数/功能块代码。
# 8) 要回答的全面一点。
# 9) 输出严格 JSON，每个追问对应一个回答条目。

# 【case_id】
# {case_id}

# 【追问列表】
# {json.dumps(followups, ensure_ascii=False, indent=2)}

# 【项目代码（Structured Text）：你据此判断“该做/不该做/具备哪些标准”，回答时只描述其中实际有的行为】
# ```st
# {project_code_text}
# ```

# 输出格式（严格 JSON，不要多余文字）：
# {{
#   "回答列表": [
#     {{
#       "模糊点类型": "…原问题中的模糊点类型…",
#       "追问问题": "…原问题…",
#       "回答": "…仅基于项目代码实际行为的、需求澄清式表述…"
#     }}
#   ]
# }}
# """
    return f"""你扮演的是**回答需求追问的人类**。你心里清楚“待实现代码该做什么、不该做什么、具备哪些标准”，这些信息**全部且仅来自下面给出的项目代码**：代码里有的行为你才可以说，代码里没有的行为你绝不能编造。

核心规则（必须遵守）：
1) 只描述项目代码中实际存在的行为。若代码里没有实现某类行为（例如没有写日志、没有界面显示、没有错误码枚举、没有重试逻辑），则回答中**不得**提及该类行为；只用语义化、需求层面的说法描述代码里实际有的处理方式。
2) 若追问涉及“功能块/实例化/类型选择/调用方式”（如“是否独立实例化”“使用什么功能块控制”），回答中**必须包含代码里的具体类型名或功能块名**（例如 `MC_Power`），不能只写“独立实例化电源控制功能块”这类泛化表述。
3) 若追问涉及“范围约束/上下界/阈值/默认值/比例系数/偏移量”等数值约束，回答中必须写出代码里的具体数值常量，不能只写“动态调整”“由 CASE 决定”这类机制性表述。
4) 若追问涉及“计算公式”，回答需同时给出：使用哪些关键变量（可写变量名）+ 关键常量值（若有）+ 计算方向（如“物理量映射到终端量”），避免只给抽象描述。
5) 回答写成“人类澄清需求”的口吻，可以引用函数名、变量名、类型名（如 `MC_Power`），但是不贴代码。
6) 若某追问在项目代码中无法对应到任何实现，或代码未体现该方面信息，回答仅写"无需考虑"。
7) 会提供给你整个项目的代码，但是你只用关心 case_id 对应的函数/功能块代码。
8) 要回答的全面一点。
9) 输出严格 JSON，每个追问对应一个回答条目。
10) answer_en字段存储回答字段的同含义英文版本。

【case_id】
{case_id}

【追问列表】
{json.dumps(followups, ensure_ascii=False, indent=2)}

【项目代码（Structured Text）：你据此判断“该做/不该做/具备哪些标准”，回答时只描述其中实际有的行为】
```st
{project_code_text}
```

输出格式（严格 JSON，不要多余文字）：
{{
  "回答列表": [
    {{
      "模糊点类型": "…原问题中的模糊点类型…",
      "追问问题": "…原问题…",
      "回答": "…仅基于项目代码实际行为的、需求澄清式表述…",
      "answer_en": "…回答的同含义英文版本…"
    }}
  ]
}}
"""


def build_answer_prompt_with_project_description(
    case_id: str,
    followups: List[Dict[str, Any]],
    project_description: str,
    project_code_meta: Dict[str, Any],
) -> str:
    """
    构造回答 prompt 的「项目描述」版本：传入的是 project_description（来自 code_description 的 description_en），
    而非参考代码。让模型基于项目描述理解约束，以人类澄清需求的口吻回答，输出 JSON。
    """
    return f"""你扮演的是**回答需求追问的人类**。你心里清楚“待实现代码该做什么、不该做什么、具备哪些标准”，这些信息**全部且仅来自下面给出的待实现代码的参考逻辑描述**：描述里有的行为你才可以说，描述里没有的行为你绝不能编造。

核心规则（必须遵守）：
1) 只描述代码逻辑描述中实际存在的行为。若描述里没有某类行为，则回答中**不得**提及该类行为；只用语义化、需求层面的说法描述描述里实际有的处理方式。
2) 若追问涉及“功能块/实例化/类型选择/调用方式”，回答中**必须包含描述里的具体类型名或功能块名**（如 `MC_Power`），不能只写泛化表述。
3) 若追问涉及“范围约束/上下界/阈值/默认值/比例系数/偏移量”等数值约束，回答中必须写出描述里的具体数值常量。
4) 若追问涉及“计算公式”，回答需给出计算方法。
5) 回答写成“人类澄清需求”的口吻，可以引用函数名、类型名，但是不贴代码。
6) 若某追问在项目描述中无法对应到任何信息，则该条不输出任何信息。
7) 输出严格 JSON，每个追问对应一个回答条目。
8) answer_en字段存储回答字段的同含义英文版本。
【case_id】
{case_id}

【追问列表】
{json.dumps(followups, ensure_ascii=False, indent=2)}

【参考代码逻辑描述（英文）：你据此判断“该做/不该做/具备哪些标准”，回答时只描述其中实际有的行为】
{project_description}

输出格式（严格 JSON，不要多余文字）：
{{
  "回答列表": [
    {{
      "模糊点类型": "…原问题中的模糊点类型…",
      "追问问题": "…原问题…",
      "回答": "…仅基于代码逻辑描述实际行为的、需求澄清式表述…",
      "answer_en": "…回答的同含义英文版本…"
    }}
  ]
}}
"""


def parse_answer_json(text: str, case_id: str) -> Dict[str, Any]:
    if not text:
        return {"case_id": case_id, "回答列表": [], "error": "LLM 返回为空"}
    m = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if m:
        text = m.group(1).strip()
    try:
        data = json.loads(text)
        if not isinstance(data, dict):
            return {"case_id": case_id, "回答列表": [], "error": "LLM 返回非 JSON 对象"}
        data["case_id"] = case_id
        if "回答列表" not in data or not isinstance(data["回答列表"], list):
            data["回答列表"] = []
        return data
    except json.JSONDecodeError as e:
        return {"case_id": case_id, "回答列表": [], "error": f"JSON 解析失败: {e}", "raw": text[:800]}


def answer_followups_for_case(
    project_name: str,
    case_result: Dict[str, Any],
    project_code_text: str,
    project_code_meta: Dict[str, Any],
    api_key: str,
    base_url: str,
    model: str,
    run_id: str,
    use_project_description: bool = False,  #False 表示使用代码作为参考 True表示使用代码逻辑描述作为参考
) -> Dict[str, Any]:
    case_id = case_result.get("case_id") or f"{project_name}/unknown_case"
    followups = case_result.get("追问列表") or []
    if not followups:
        out = {"case_id": case_id, "回答列表": []}
        save_answer_result(run_id, project_name, case_id, out)
        return out

    if use_project_description:
        project_description = load_project_description(project_name, case_id)
        if project_description:
            print("使用代码描述回答追问")
            prompt = build_answer_prompt_with_project_description(
                case_id, followups, project_description, project_code_meta
            )
        else:
            print("使用参考代码回答追问")
            prompt = build_answer_prompt(case_id, followups, project_code_text, project_code_meta)
    else:
        print("使用参考代码回答追问")
        prompt = build_answer_prompt(case_id, followups, project_code_text, project_code_meta)
    save_answer_prompt(run_id, project_name, case_id, prompt)

    if openai is None:
        out = {"case_id": case_id, "回答列表": [], "error": "未安装 openai 库"}
        save_answer_result(run_id, project_name, case_id, out)
        return out

    try:
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        resp = client.chat.completions.create(
            model=model,
            # messages=[
            #     {
            #         "role": "system",
            #         "content": "你是回答需求追问的人类，认知全部来自给定项目代码。回答只描述代码里实际有的行为；绝不添加代码中未实现的行为。若无法从代码对应或代码未体现该方面，回答仅写「无需考虑」，不要写“需要人类补充”或“无法确定”等。输出严格 JSON。",
            #     },
            #     {"role": "user", "content": prompt},
            # ],
            messages=[
                {
                    "role": "system",
                    "content": "你是澄清需求的人类。回答必须严格参考项目代码，且输出严格 JSON。若追问涉及功能块/实例化/类型选择，必须写出具体类型名（如 MC_Power）。若涉及范围约束/上下界/阈值/默认值/偏移量/比例系数，必须写出代码中的具体数值常量（如 32768.0、-32768.0、0.0），禁止只说“动态调整”这类空泛机制描述。若代码未体现该方面信息，回答仅写「无需考虑」。",
                },
                {"role": "user", "content": prompt},
            ],
            
            temperature=0.2,
            max_tokens=1800,
        )
        text = (resp.choices[0].message.content or "").strip()
        out = parse_answer_json(text, case_id)
    except Exception as e:
        out = {"case_id": case_id, "回答列表": [], "error": str(e)}

    save_answer_result(run_id, project_name, case_id, out)
    return out


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="基于项目代码自动回答 ambiguity_check 的追问列表")
    parser.add_argument("--run-id", type=str, required=False, default=None, help="ambiguity_check 的 run_id（output/<run_id>）")
    parser.add_argument("--project", type=str, nargs="+", required=True, help="项目名（query 下目录名），可多个")
    parser.add_argument("--case", type=str, nargs="*", default=None, help="仅回答指定 case（JSON stem），与 --project 配合")
    parser.add_argument("--project-code-base", type=str, default=None, help=f"project_code 根目录（默认: {PROJECT_CODE_BASE}）")
    parser.add_argument("--model", type=str, default="gpt-4o", help="模型名（默认 gpt-4-turbo）")
    parser.add_argument("--max-chars", type=int, default=220000, help="项目代码最大字符数（超出截断）")
    parser.add_argument("--use-project-description", action="store_true", help="用 code_description 下对应 json 的 description_en 替代项目代码构造 prompt")
    args = parser.parse_args()

    run_id = args.run_id or make_run_id()
    projects = args.project
    case_filter = set(args.case) if args.case else None
    project_code_base = Path(args.project_code_base) if args.project_code_base else PROJECT_CODE_BASE

    api_key, base_url = get_api_config()

    for project_name in projects:
        print(f"\n项目: {project_name}")
        amb_results = load_ambiguity_results(run_id, project_name)
        if case_filter:
            amb_results = [r for r in amb_results if (str(r.get("case_id", "")).split("/")[-1] in case_filter)]
        if not amb_results:
            print("  ⚠ 未找到可回答的追问结果（可能该 run_id 下未生成 results，或被 --case 过滤）")
            continue

        shared_project_code_text = ""
        shared_project_code_meta: Dict[str, Any] = {}
        if USE_ALL_PROJECT_CODE_CONTEXT:
            shared_project_code_text, shared_project_code_meta = load_project_code(
                project_name=project_name,
                project_code_base=project_code_base,
                max_chars=args.max_chars,
            )
            if not shared_project_code_text:
                print(f"  ✗ 无法加载项目代码: {shared_project_code_meta.get('error')}")
                continue

        answers: List[Dict[str, Any]] = []
        for case_result in amb_results:
            if USE_ALL_PROJECT_CODE_CONTEXT:
                project_code_text, project_code_meta = shared_project_code_text, shared_project_code_meta
            else:
                case_name = str(case_result.get("case_id", "")).split("/")[-1]
                project_code_text, project_code_meta = load_project_code(
                    project_name=project_name,
                    project_code_base=project_code_base,
                    max_chars=args.max_chars,
                    case_name=case_name,
                )

            if not project_code_text:
                print(f"  ⚠ 无法加载项目代码（{case_result.get('case_id', 'unknown')}）: {project_code_meta.get('error')}")
                answers.append({
                    "case_id": case_result.get("case_id") or f"{project_name}/unknown_case",
                    "回答列表": [],
                    "error": project_code_meta.get("error") or "无法加载项目代码",
                })
                continue

            answers.append(
                answer_followups_for_case(
                    project_name=project_name,
                    case_result=case_result,
                    project_code_text=project_code_text,
                    project_code_meta=project_code_meta,
                    api_key=api_key,
                    base_url=base_url,
                    model=args.model,
                    run_id=run_id,
                    # use_project_description
                )
            )

        # 保存项目级汇总
        summary_path = DEFAULT_OUTPUT_DIR / run_id / "answers" / f"{project_name}.json"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(answers, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✓ 已保存: {summary_path}")

    print(f"\n全部完成。回答结果目录: {DEFAULT_OUTPUT_DIR / run_id / 'answers'}")


if __name__ == "__main__":
    main()

