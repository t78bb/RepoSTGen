#!/usr/bin/env python3
"""
需求模糊点识别：根据经验库分析原始需求是否存在未明确的模糊点，并生成追问列表。

- 经验库：requirement_completion/knowledge_base/total_knowledge.json
- 调用方：传入需求文本与 case_id，调用大模型，返回 JSON（是否需要追问、追问列表等）
"""
import json
import os
import re
import sys
import random
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# 保证同目录下 persist_io、knowledge_base_sampler 可被导入（无论从何路径运行脚本）
sys.path.insert(0, str(Path(__file__).resolve().parent))
from persist_io import save_result, save_user_prompt, save_results_batch, make_run_id
from knowledge_base_sampler import sample_knowledge_base_by_frequency

try:
    import openai
except ImportError:
    openai = None

# 模块所在目录与仓库根
REQUIREMENT_COMPLETION_DIR = Path(__file__).resolve().parent
REPO_ROOT = REQUIREMENT_COMPLETION_DIR.parent
DEFAULT_QUERY_BASE = REPO_ROOT / "dataset" / "query"
DEFAULT_KNOWLEDGE_BASE_PATH = REQUIREMENT_COMPLETION_DIR / "knowledge_base" / "total_knowledge.json"
# 测试集项目名单：经验库格式化时过滤掉 case_id 中包含这些项目名的项，避免泄露测试集
TEST_PROJECT_LIST_PATH = REQUIREMENT_COMPLETION_DIR / "dataset_seperate" / "part1_50case.txt"


def get_api_config() -> tuple:
    """从环境变量获取 API 配置 (api_key, base_url)"""
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
        raise RuntimeError(
            "未找到 API 密钥，请设置 ZHIZENGZENG_API_KEY / OPENAI_API_KEY / API_KEY"
        )
    return api_key, base_url


def load_knowledge_base(path: Optional[Path] = None) -> dict:
    """加载经验库 JSON，返回按「模糊点类型」分类的结构化字典。"""
    path = path or DEFAULT_KNOWLEDGE_BASE_PATH
    path = Path(path)
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_exclude_projects(path: Optional[Path] = None) -> Set[str]:
    """读取测试集项目名单，返回项目名集合。用于过滤经验库中来自这些 case 的项。"""
    path = path or TEST_PROJECT_LIST_PATH
    path = Path(path)
    if not path.exists():
        return set()
    projects = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        name = line.strip()
        if name:
            projects.add(name)
    return projects


def format_knowledge_for_prompt(
    knowledge_base: dict,
    exclude_projects: Optional[Set[str]] = None,
    exclude_projects_file: Optional[Path] = None,
) -> str:
    """将经验库格式化为 prompt 中「经验库」占位所需的一段文本。
    若提供 exclude_projects 或从 exclude_projects_file 读取到项目名，则过滤掉 case_id 中包含这些项目名的项。
    """
    if not knowledge_base:
        return "（当前经验库为空）"
    if exclude_projects is None and exclude_projects_file is not None:
        exclude_projects = load_exclude_projects(exclude_projects_file)
    if exclude_projects is None:
        exclude_projects = load_exclude_projects(TEST_PROJECT_LIST_PATH)
    lines = []
    for category, items in knowledge_base.items():
        if not isinstance(items, list):
            continue
        filtered = []
        for item in items:
            if isinstance(item, dict):
                case_id = item.get("case_id", "")
                if exclude_projects and case_id and any(p in case_id for p in exclude_projects):
                    continue
                filtered.append(item)
            else:
                filtered.append(item)
        if not filtered:
            continue
        lines.append(f"【{category}】")
        for i, item in enumerate(filtered, 1):
            if isinstance(item, dict):
                desc = item.get("模糊点描述", "")
                example = item.get("精准需求示例", "")
                lines.append(f"  {i}. 模糊点描述: {desc}")
                if example:
                    lines.append(f"     精准需求示例: {example}")
            else:
                lines.append(f"  {i}. {item}")
        lines.append("")
    return "\n".join(lines).strip()

def gradually_expand_knowledge_for_prompt(
    knowledge_base: dict,
    case_id: str = "repoeval_",
    exclude_projects: Optional[Set[str]] = None,
    exclude_projects_file: Optional[Path] = None,
    percentage: float = 0.2,
) -> str:
    """将经验库格式化为 prompt 中「经验库」占位所需的一段文本。
    若提供 exclude_projects 或从 exclude_projects_file 读取到项目名，则过滤掉 case_id 中包含这些项目名的项。
    """
    if not knowledge_base:
        return "（当前经验库为空）"
    exclude_projects = {case_id} if case_id else set()
    lines = []
    for category, items in knowledge_base.items():
        if not isinstance(items, list):
            continue
        filtered = []
        # for item in items:
        #     if isinstance(item, dict):
        #         case_id = item.get("case_id", "")
        #         if exclude_projects and case_id and any(p in case_id for p in exclude_projects):
        #             continue
        #         filtered.append(item)
        #     else:
        #         filtered.append(item)
        for item in items:
            keep_item = True
            if isinstance(item, dict):
                item_case_id = item.get("case_id", "")
                # if exclude_projects and item_case_id and any(p in item_case_id for p in exclude_projects):
                if exclude_projects and item_case_id and any(p in item_case_id.split("/")[0] for p in exclude_projects):
                    keep_item = False
            if keep_item:
                if random.random() <= percentage:
                    filtered.append(item)

        if not filtered:
            continue
        lines.append(f"【{category}】")
        for i, item in enumerate(filtered, 1):
            if isinstance(item, dict):
                desc = item.get("模糊点描述", "")
                example = item.get("精准需求示例", "")
                lines.append(f"  {i}. 模糊点描述: {desc}")
                if example:
                    lines.append(f"     精准需求示例: {example}")
            else:
                lines.append(f"  {i}. {item}")
        lines.append("")
    return "\n".join(lines).strip()


def _is_low_value_followup(question: str) -> bool:
    """过滤泛化、低信息增益的追问。"""
    q = (question or "").strip()
    if not q:
        return True
    low_value_patterns = [
        r"^如何映射和处理输入和输出变量",
        r"^是否需要.*LED",
        r"^是否需要同时更新.*状态",
        r"^是否需要使用外部IO映射",
        r"^是否需要实现状态机来控制",
        r"^如何处理输入和输出变量",
        r"^还有其他需要补充",
    ]
    return any(re.search(p, q) for p in low_value_patterns)


def _postprocess_followups(data: dict) -> dict:
    """
    对 LLM 追问做后处理：去泛问、去重、限量，提升有效性。
    """
    if not isinstance(data, dict):
        return data
    followups = data.get("追问列表", [])
    if not isinstance(followups, list):
        data["追问列表"] = []
        data["是否需要追问"] = "否"
        return data

    seen = set()
    cleaned = []
    for item in followups:
        if not isinstance(item, dict):
            continue
        q_type = str(item.get("模糊点类型", "")).strip()
        q_text = str(item.get("追问问题", "")).strip()
        if not q_text or _is_low_value_followup(q_text):
            continue
        key = (q_type, q_text)
        if key in seen:
            continue
        seen.add(key)
        cleaned.append({"模糊点类型": q_type, "追问问题": q_text})

    # 控制问题数，避免噪声过多
    data["追问列表"] = cleaned[:5]
    data["是否需要追问"] = "是" if data["追问列表"] else "否"
    return data


def analyze_requirement_ambiguity(
    requirement: str,
    case_id: str,
    knowledge_base: dict,
    api_key: str,
    base_url: str,
    model: str = "gpt-4o",
    run_id: Optional[str] = None,
    provide_code: str = "",
) -> dict:
    """
    接收需求文本，对照经验库调用大模型，返回「是否需要追问 + 追问列表」的 JSON 结构。

    Args:
        requirement: 原始需求文本
        case_id: 当前 case 标识，用于返回结果中的 case_id
        knowledge_base: 结构化经验库（与 total_knowledge.json 格式一致）
        api_key: 大模型 API Key
        base_url: 大模型 API Base URL
        model: 模型名称
        run_id: 可选，同一批落盘用同一 run_id，传入则落盘 user_prompt 与 result
        provide_code: 已提供的代码片段（补全时可见部分），供模型结合需求判断模糊点

    Returns:
        解析后的字典，包含 case_id, 是否需要追问, 追问列表 等；
        若 LLM 未返回合法 JSON 或调用失败，返回包含 error 或 fallback 的 dict。
    """
    project_name = case_id.split("/")[0] if "/" in case_id else case_id

    if openai is None:
        out = {
            "case_id": case_id,
            "是否需要追问": "否",
            "追问列表": [],
            "error": "未安装 openai 库",
        }
        if run_id:
            save_result(project_name, case_id, out, run_id=run_id)
        return out
    print("case_id: ", case_id)
    # knowledge_text = format_knowledge_for_prompt(knowledge_base)

    knowledge_text = gradually_expand_knowledge_for_prompt(knowledge_base, case_id=case_id)

    provide_code = provide_code or "（无）"

    # 原先的 prompt（追问易问偏、问泛，未紧扣经验库中的「模糊点描述」所针对的方面）：
    # prompt = f"""请严格按照以下规则完成任务：
    # 规则1：经验库提供的是「提问方式」的参考——包括哪些类型的模糊点值得追问（如报错机制、变量范围、IO映射等）以及如何用简洁具体的问题向人类追问；
    # 规则2：针对当前原始需求，参照经验库中的类型与提问方式，判断是否存在同类或类似的未明确之处；若需求中已明确则不必追问，若存在同类模糊点则按经验库的提问风格生成追问（可结合当前需求中的变量、场景做具体化），不必与经验库某条描述字面一致；
    # 规则3：追问问题必须简洁、具体，便于人类直接回答并补全需求；
    # 规则4：若经验库为空，或当前需求在经验库所涉类型上均已明确，则输出“无模糊点，无需追问”。
    # 规则5：要尽可能多的列出你认为需要追问的内容。
    # ...
    # """

    # prompt = f"""请严格按照以下规则完成任务（目标：问出会改变实现骨架的关键问题）：
    # 规则1：经验库提供「模糊点类型」及每条下的「模糊点描述」「精准需求示例」，用于指导追问应针对的**实现分叉点**（如控制原语选择、实例数量、执行顺序、范围约束等），而不是泛泛补充。
    # 规则2：每条追问必须紧扣经验库某条「模糊点描述」的同一维度；例如经验库描述“处理顺序”，则追问必须直接问先后关系；描述“范围约束”，则追问必须问上下限/单位。
    # 规则3：每条追问都应满足“回答不同会导致代码结构明显不同（例如是否实例化某功能块、实例个数、调用顺序变化）”。
    # 规则4：优先覆盖以下关键维度（按相关性选择）：
    #   - 控制原语/功能块选择（例如使用何种功能块实现控制，而不是仅做状态推断）
    #   - 实例数量与绑定关系（例如是否需要为每个轴/通道独立实例）
    #   - 执行顺序与失效策略（例如 Enable/Reset/故障时先后与复位策略）
    # 规则5：禁止低价值泛问，如“如何映射输入输出变量”“是否需要更新LED状态”等与主实现分叉弱相关的问题。
    # 规则6：先在内部对候选问题打分（不输出打分）：Impact(0-5) + Specificity(0-5) + Verifiability(0-5)，仅保留高分问题（总分>=11）。
    # 规则7：追问问题必须简洁、具体，可直接回答；输出 1~5 条即可，不追求数量。
    # 规则8：若经验库为空，或当前需求在经验库相关维度上均已明确，则输出“无模糊点，无需追问”。



    prompt = f"""请严格按照以下规则完成任务（目标：问出会改变实现骨架的关键问题）：
    规则1：经验库提供「模糊点类型」及每条下的「模糊点描述」「精准需求示例」，用于指导追问应针对的**实现分叉点**（如控制原语选择、实例数量、执行顺序、范围约束等），而不是泛泛补充。
    规则2：每条追问必须紧扣经验库某条「模糊点描述」的同一维度；例如经验库描述“处理顺序”，则追问必须直接问先后关系；描述“范围约束”，则追问必须问上下限/单位。
    规则3：每条追问都应满足“回答不同会导致代码结构明显不同（例如是否实例化某功能块、实例个数、调用顺序变化）”。
    规则4：优先覆盖以下关键维度（按相关性选择）：
      - 控制原语/功能块选择（例如使用何种功能块实现控制，而不是仅做状态推断）
      - 实例数量与绑定关系（例如是否需要为每个轴/通道独立实例）
      - 执行顺序与失效策略（例如 Enable/Reset/故障时先后与复位策略）
    规则5：禁止低价值泛问，如“如何映射输入输出变量”“是否需要更新LED状态”等与主实现分叉弱相关的问题。
    规则6：先在内部对候选问题打分（不输出打分）：Impact(0-5) + Specificity(0-5) + Verifiability(0-5)，仅保留高分问题（总分>=11）。
    规则7：追问问题必须简洁、具体，可直接回答；输出 1~5 条即可，不追求数量。
    规则8：若经验库为空，或当前需求在经验库相关维度上均已明确，则输出“无模糊点，无需追问”。

    【原始需求】
    {requirement}

    【已提供的代码（补全时可见部分）】
    ```
    {provide_code}
    ```

    【经验库（供参考提问类型与提问方式；生成追问时请对准各条「模糊点描述」所针对的实现分叉点）】
    {knowledge_text}

    输出格式参考：
    {{
    "是否需要追问": "是/否",
    "追问列表": [
        {{
        "模糊点类型": "",
        "追问问题": ""
        }}
    ]
    }}
    请只输出上述 JSON，不要输出其他内容。"""

    if run_id:
        save_user_prompt(project_name, case_id, prompt, run_id=run_id)

    try:
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        # 原 system：只要求“按经验库风格”生成追问，易导致追问与经验库关键维度不对齐
        # "content": "你参照经验库中的提问类型与提问方式，对当前需求判断是否存在未明确之处，若有则按经验库风格生成追问并输出指定格式的 JSON，若无则追问列表为空且是否需要追问为否。"
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "你是需求澄清专家。你的任务不是罗列泛化问题，而是识别会改变实现骨架的关键分叉点，并输出高价值追问。追问需与经验库描述同一维度，优先覆盖功能块/控制原语选择、实例数量与绑定关系、执行顺序与失效策略。禁止输出泛问。仅输出指定 JSON。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=2200,
        )
        text = (response.choices[0].message.content or "").strip()
        out = _parse_llm_json(text, case_id)
        out = _postprocess_followups(out)
    except Exception as e:
        out = {
            "case_id": case_id,
            "是否需要追问": "否",
            "追问列表": [],
            "error": str(e),
        }

    if run_id:
        save_result(project_name, case_id, out, run_id=run_id)
    return out


def _parse_llm_json(text: str, case_id: str) -> dict:
    """从 LLM 输出中解析 JSON，兼容被 markdown 代码块包裹的情况。"""
    if not text:
        return {
            "case_id": case_id,
            "是否需要追问": "否",
            "追问列表": [],
            "error": "LLM 返回为空",
        }
    # 尝试去掉 ```json ... ``` 包裹
    m = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if m:
        text = m.group(1).strip()
    try:
        data = json.loads(text)
        if not isinstance(data, dict):
            return {"case_id": case_id, "是否需要追问": "否", "追问列表": [], "error": "LLM 返回非 JSON 对象"}
        # 统一字段名
        if "case_id" not in data:
            data["case_id"] = case_id
        if "追问列表" not in data:
            data["追问列表"] = []
        return data
    except json.JSONDecodeError as e:
        # 尝试修复因 LLM 输出被截断导致的未闭合 JSON（如 Unterminated string）
        repaired = _repair_truncated_followup_json(text)
        if repaired:
            try:
                data = json.loads(repaired)
                if isinstance(data, dict) and "追问列表" in data:
                    if "case_id" not in data:
                        data["case_id"] = case_id
                    data["_repaired"] = True  # 标记为截断修复结果
                    return data
            except json.JSONDecodeError:
                pass
        return {
            "case_id": case_id,
            "是否需要追问": "否",
            "追问列表": [],
            "error": f"JSON 解析失败: {e}",
            "raw": text[:500],
        }


def run_for_project(
    project_name: str,
    query_base: Path,
    knowledge_base_path: Path,
    api_key: str,
    base_url: str,
    run_id: Optional[str] = None,
    case_filter: Optional[List[str]] = None,
) -> Tuple[List[dict], str]:
    """
    对 query 目录下指定项目的 case 执行模糊点分析，返回结果列表及本批使用的 run_id。
    若 case_filter 非空，仅处理 JSON 文件名（stem）在该列表中的 case；否则处理该项目下全部 .json。
    若未传 run_id 则自动生成，本批会落盘 user_prompt 与 result 到 requirement_completion/output/[run_id]/。
    """
    project_dir = query_base / project_name
    if not project_dir.exists() or not project_dir.is_dir():
        raise FileNotFoundError(f"项目目录不存在: {project_dir}")

    if run_id is None:
        run_id = make_run_id()
    knowledge_base = load_knowledge_base(knowledge_base_path)
    # 按模糊类型数量取频率最高的前 5 类，每类随机 5 条，作为本批使用的经验库子集
    # knowledge_base = sample_knowledge_base_by_frequency(
    #     knowledge_base, top_k_types=5, per_type_samples=5
    # )
    results = []

    json_paths = sorted(project_dir.glob("*.json"))
    if case_filter:
        case_set = set(case_filter)
        json_paths = [p for p in json_paths if p.stem in case_set]
        if not json_paths:
            print(f"  警告: 指定 case {case_filter} 在该项目下无匹配（该项目有: {[p.stem for p in sorted(project_dir.glob('*.json'))]}），未生成任何结果，输出目录可能未创建。")
            return results, run_id

    for json_path in json_paths:
        case_id = f"{project_name}/{json_path.stem}"
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as e:
            results.append({
                "case_id": case_id,
                "是否需要追问": "否",
                "追问列表": [],
                "error": f"读取 JSON 失败: {e}",
            })
            continue

        requirement = data.get("requirement") or data.get("requirement_cn") or ""
        if not requirement:
            results.append({
                "case_id": case_id,
                "是否需要追问": "否",
                "追问列表": [],
                "error": "该 case 无 requirement 字段",
            })
            continue

        provide_code = data.get("provide_code", "") or ""

        out = analyze_requirement_ambiguity(
            requirement=requirement,
            case_id=case_id,
            knowledge_base=knowledge_base,
            api_key=api_key,
            base_url=base_url,
            run_id=run_id,
            provide_code=provide_code,
        )
        results.append(out)

    save_results_batch(project_name, results, run_id=run_id)
    return results, run_id


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="对 query 下指定项目进行需求模糊点识别，输出追问列表（JSON）"
    )
    parser.add_argument(
        "--project",
        type=str,
        nargs="+",
        required=True,
        help="query 下的项目目录名，可多个，例如 --project repoeval_isScaleOutput repoeval_traffic_light",
    )
    parser.add_argument(
        "--case",
        type=str,
        nargs="*",
        default=None,
        help="仅执行指定的 case（JSON 文件名不含扩展名），与 --project 配合；不传则执行该项目下全部 case。例如 --project repoeval_counter --case FB_counter",
    )
    parser.add_argument(
        "--query-base",
        type=str,
        default=None,
        help=f"query 根目录（默认: {DEFAULT_QUERY_BASE}）",
    )
    parser.add_argument(
        "--knowledge-base",
        type=str,
        default=None,
        help=f"经验库 JSON 路径（默认: {DEFAULT_KNOWLEDGE_BASE_PATH}）",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="将结果写入该 JSON 文件；不指定则只打印到 stdout",
    )
    parser.add_argument(
        "--run-id",
        type=str,
        default=None,
        help="落盘 run_id，与 persist_io 对齐；不指定则自动生成，中间结果写入 requirement_completion/output/[run_id]/",
    )
    parser.add_argument(
        "--auto-answer",
        action="store_true",
        help="在提问完成后自动调用 answer_followups.py 基于项目代码回答追问",
    )
    args = parser.parse_args()

    query_base = Path(args.query_base) if args.query_base else DEFAULT_QUERY_BASE
    knowledge_base_path = Path(args.knowledge_base) if args.knowledge_base else DEFAULT_KNOWLEDGE_BASE_PATH

    if not query_base.exists():
        print(f"错误: query 目录不存在: {query_base}", file=sys.stderr)
        sys.exit(1)
    if not knowledge_base_path.exists():
        print(f"警告: 经验库不存在，将使用空经验库: {knowledge_base_path}", file=sys.stderr)

    try:
        api_key, base_url = get_api_config()
    except RuntimeError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

    projects = args.project if isinstance(args.project, list) else [args.project]
    case_list = args.case if isinstance(args.case, list) else ([args.case] if args.case else None)
    print(f"项目: {projects}")
    if case_list:
        print(f"仅 case: {case_list}")
    print(f"Query 根目录: {query_base}")
    print(f"经验库: {knowledge_base_path}")
    print()

    from persist_io import DEFAULT_OUTPUT_DIR
    used_run_id = args.run_id or make_run_id()
    all_results = []

    for idx, project_name in enumerate(projects, 1):
        print(f"\n[{idx}/{len(projects)}] {project_name}")
        try:
            results, _ = run_for_project(
                project_name=project_name,
                query_base=query_base,
                knowledge_base_path=knowledge_base_path,
                api_key=api_key,
                base_url=base_url,
                run_id=used_run_id,
                case_filter=case_list,
            )
            all_results.extend(results)
        except FileNotFoundError as e:
            print(f"  错误: {e}", file=sys.stderr)

    # print(f"\n中间结果已落盘: {DEFAULT_OUTPUT_DIR / used_run_id}")
    print()

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"已写入 {len(all_results)} 条结果到: {out_path}")

    for r in all_results:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        print("-" * 60)

    # 可选：自动调用 answer_followups.py 基于项目代码回答追问
    if args.auto_answer and all_results:
        cmd = [
            sys.executable,
            str(REQUIREMENT_COMPLETION_DIR / "answer_followups.py"),
            "--run-id",
            used_run_id,
        ]
        # 项目列表
        cmd += ["--project"]
        cmd.extend(projects)
        # case 过滤（如果有）
        if case_list:
            cmd += ["--case"]
            cmd.extend(case_list)
        print("\n开始自动调用 answer_followups.py 回答追问…")
        print("命令:", " ".join(map(str, cmd)))
        try:
            subprocess.run(cmd, check=False)
        except Exception as e:
            print(f"自动调用 answer_followups 失败: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
