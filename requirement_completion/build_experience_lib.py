#!/usr/bin/env python3
"""
构建经验库：对比「模型生成代码」与「参考代码」，用 LLM 提取需求模糊点，得到每个 case 的 JSON。

输入：
- 指定目录（如 output/20260212_构建经验库）下各项目子目录的 readful_result/*.st（模型生成代码）
- dataset/query 下对应项目的 JSON（原始需求）
- dataset/project_code 下对应项目的 FUN/*.st（参考代码）

输出：
- requirement_completion/experience_build_output/{case_id}.json
- case_id = 项目名_任务名，如 repoeval_PID_controller_Tank
"""
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    import openai
except ImportError:
    openai = None

REQUIREMENT_COMPLETION_DIR = Path(__file__).resolve().parent
REPO_ROOT = REQUIREMENT_COMPLETION_DIR.parent
DEFAULT_INPUT_DIR = REPO_ROOT / "output" / "20260212_构建经验库"
DEFAULT_QUERY_BASE = REPO_ROOT / "dataset" / "query"
DEFAULT_PROJECT_CODE_BASE = REPO_ROOT / "dataset" / "project_code"
OUTPUT_DIR = REQUIREMENT_COMPLETION_DIR / "experience_build_output"


def get_api_config() -> tuple:
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
    """项目目录名 -> project_code 下目录名（去掉 repoeval_ 前缀）"""
    if project_name.startswith("repoeval_"):
        return project_name[len("repoeval_"):]
    return project_name


def load_reference_code(project_code_base: Path, project_name: str, task_name: str) -> Optional[str]:
    """加载参考代码：FUN/{task_name}.st 及 FUN/{task_name}_*.st 合并。"""
    code_name = project_dir_to_code_name(project_name)
    fun_dir = project_code_base / code_name / "FUN"
    if not fun_dir.exists() or not fun_dir.is_dir():
        return None
    parts: List[str] = []
    main_file = fun_dir / f"{task_name}.st"
    if main_file.exists():
        try:
            parts.append(main_file.read_text(encoding="utf-8"))
        except Exception:
            return None
    for p in sorted(fun_dir.iterdir()):
        if not p.is_file() or p.suffix.lower() != ".st":
            continue
        if p.name == f"{task_name}.st" or not p.name.startswith(f"{task_name}_"):
            continue
        try:
            parts.append(p.read_text(encoding="utf-8"))
        except Exception:
            continue
    if not parts:
        return None
    return "\n\n---\n\n".join(parts)


def load_requirement(query_base: Path, project_name: str, task_name: str) -> Optional[str]:
    """从 dataset/query/{project}/{task_name}.json 读取 requirement。"""
    json_path = query_base / project_name / f"{task_name}.json"
    if not json_path.exists():
        return None
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        return data.get("requirement") or data.get("requirement_cn") or ""
    except Exception:
        return None


def build_prompt(original_requirement: str, generated_code: str, reference_code: str) -> str:
    """构建给 LLM 的 user prompt。"""
    result = f"""请你完成以下任务：
1. 对比「模型生成代码」和「参考代码」，列出所有功能/逻辑差异（仅聚焦ST代码的项目级要求，如报错机制、变量范围、IO映射、循环周期等）；
2. 针对每个差异，分析：是「原始需求未明确说明」导致的，还是「模型生成错误」导致的？仅保留「需求未明确」的差异；
3. 对每个「需求未明确」的差异，提炼成「需求模糊点」（格式：模糊点类型+具体描述）；
4. 给出该模糊点对应的精准需求描述。你要想象能根据这个精准的描述让模型生成和参考代码相同的代码。但是不要直接复制参考代码的实现，要根据需求和模型生成代码的特性，给出精准的需求描述。

---

原始需求：
【{original_requirement}】

模型生成代码：
```
{generated_code}
```

参考代码：
```
{reference_code}
```

输出格式（JSON，不要输出 case_id）：
{{
  "模糊点列表": [
    {{
      "模糊点类型": "报错机制/变量范围/IO映射/循环周期等",
      "模糊点描述": "原始需求未说明电机转速报错的触发条件",
      "差异细节": "模型生成代码未实现转速超限时的报错逻辑，参考代码中转速>3000rpm时触发E-001报错",
      "精准需求描述": "电机转速超过3000rpm时，触发错误码E-001，报错信息包含当前转速值",
      "case_id": "repoeval_barrier/setButtonByDirect"
    }}
  ]
}}

若无「需求未明确」导致的差异，模糊点列表为空数组 []。请只输出上述 JSON，不要输出其他内容。"""
    print(result)
    return result


def parse_llm_json(text: str, case_id: str) -> dict:
    """从 LLM 输出解析 JSON，并注入 case_id。"""
    if not text:
        return {"case_id": case_id, "模糊点列表": []}
    m = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if m:
        text = m.group(1).strip()
    try:
        data = json.loads(text)
        if not isinstance(data, dict):
            return {"case_id": case_id, "模糊点列表": []}
        data["case_id"] = case_id
        if "模糊点列表" not in data:
            data["模糊点列表"] = []
        return data
    except json.JSONDecodeError:
        return {"case_id": case_id, "模糊点列表": [], "raw": text[:500]}


def call_llm_extract(
    prompt: str,
    case_id: str,
    api_key: str,
    base_url: str,
    model: str = "gpt-4-turbo",
) -> dict:
    """调用 LLM 得到模糊点 JSON。"""
    if not openai:
        return {"case_id": case_id, "模糊点列表": [], "error": "未安装 openai"}
    try:
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "你对比模型生成代码与参考代码，仅保留「原始需求未明确」导致的差异，并提炼为需求模糊点与精准需求描述。输出指定格式的 JSON，不要输出 case_id。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=2000,
        )
        text = (response.choices[0].message.content or "").strip()
        return parse_llm_json(text, case_id)
    except Exception as e:
        return {"case_id": case_id, "模糊点列表": [], "error": str(e)}


def collect_cases(input_dir: Path) -> List[tuple]:
    """收集所有 (project_name, task_name) 且存在 readful_result 与参考代码。"""
    cases = []
    for project_dir in sorted(input_dir.iterdir()):
        if not project_dir.is_dir():
            continue
        project_name = project_dir.name
        readful_dir = project_dir / "readful_result"
        if not readful_dir.exists() or not readful_dir.is_dir():
            continue
        for st_path in sorted(readful_dir.glob("*.st")):
            task_name = st_path.stem
            cases.append((project_name, task_name))
    return cases


def process_one_case(
    project_name: str,
    task_name: str,
    input_dir: Path,
    query_base: Path,
    project_code_base: Path,
    api_key: str,
    base_url: str,
    output_dir: Path,
) -> Optional[Path]:
    """
    处理单个 case：读取需求与代码，调 LLM，落盘 JSON。
    返回落盘路径，失败返回 None。
    """
    case_id = f"{project_name}/{task_name}"

    requirement = load_requirement(query_base, project_name, task_name)
    if not requirement:
        print(f"  [跳过] {case_id}: 未找到原始需求")
        return None

    generated_path = input_dir / project_name / "readful_result" / f"{task_name}.st"
    if not generated_path.exists():
        print(f"  [跳过] {case_id}: 未找到模型生成代码")
        return None
    generated_code = generated_path.read_text(encoding="utf-8")

    reference_code = load_reference_code(project_code_base, project_name, task_name)
    if not reference_code:
        print(f"  [跳过] {case_id}: 未找到参考代码")
        return None

    # 落盘目录：JSON 在项目子目录下，参考/生成代码放在项目子目录下的 code 子目录
    out_path = output_dir / f"{case_id}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    code_dir = out_path.parent / "code"
    code_dir.mkdir(parents=True, exist_ok=True)
    (code_dir / f"{task_name}_reference.st").write_text(reference_code, encoding="utf-8")
    (code_dir / f"{task_name}_generated.st").write_text(generated_code, encoding="utf-8")

    prompt = build_prompt(requirement, generated_code, reference_code)
    result = call_llm_extract(prompt, case_id, api_key, base_url)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return out_path


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="从 readful_result 与参考代码构建经验库 JSON")
    parser.add_argument(
        "--input-dir",
        type=str,
        default=None,
        help=f"构建经验库的根目录（各项目下含 readful_result），默认: {DEFAULT_INPUT_DIR}",
    )
    parser.add_argument(
        "--query-base",
        type=str,
        default=None,
        help=f"query 根目录，默认: {DEFAULT_QUERY_BASE}",
    )
    parser.add_argument(
        "--project-code-base",
        type=str,
        default=None,
        help=f"project_code 根目录，默认: {DEFAULT_PROJECT_CODE_BASE}",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help=f"结果输出目录，默认: {OUTPUT_DIR}",
    )
    parser.add_argument(
        "--project",
        type=str,
        nargs="*",
        default=None,
        help="只处理指定项目（可多个）；不指定则处理所有项目",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="最多处理多少个 case（用于调试）",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir) if args.input_dir else DEFAULT_INPUT_DIR
    query_base = Path(args.query_base) if args.query_base else DEFAULT_QUERY_BASE
    project_code_base = Path(args.project_code_base) if args.project_code_base else DEFAULT_PROJECT_CODE_BASE
    output_dir = Path(args.output_dir) if args.output_dir else OUTPUT_DIR

    if not input_dir.exists():
        print(f"错误: 输入目录不存在: {input_dir}", file=sys.stderr)
        sys.exit(1)

    try:
        api_key, base_url = get_api_config()
    except RuntimeError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

    cases = collect_cases(input_dir)
    if args.project:
        allowed = set(args.project)
        cases = [(p, t) for p, t in cases if p in allowed]
    if not cases:
        print("没有可处理的 case")
        sys.exit(0)

    if args.limit:
        cases = cases[: args.limit]

    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print(f"待处理 case 数: {len(cases)}\n")

    ok, skip = 0, 0
    for i, (project_name, task_name) in enumerate(cases, 1):
        print(f"[{i}/{len(cases)}] {project_name}/{task_name}")
        path = process_one_case(
            project_name=project_name,
            task_name=task_name,
            input_dir=input_dir,
            query_base=query_base,
            project_code_base=project_code_base,
            api_key=api_key,
            base_url=base_url,
            output_dir=output_dir,
        )
        if path:
            ok += 1
            print(f"  -> {path.name}")
        else:
            skip += 1
        time.sleep(0.3)

    print(f"\n完成: 成功 {ok}, 跳过 {skip}")
    print(f"结果目录: {output_dir}")


if __name__ == "__main__":
    main()
