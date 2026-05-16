import json
from pathlib import Path
from typing import Dict, List, Tuple

# 硬编码：LITL 下两个评测结果名称（文件名或目录名）
FIRST_NAME = "0309_经验库_自增长实验_无经验库基线_44.44.json"
SECOND_NAME = "全流程1_61.62.json"
LITL_ROOT = Path(__file__).resolve().parent / "LITL"


def resolve_input_to_json(path_under_litl: str, litl_root: Path) -> List[Path]:
    """
    将用户输入解析为 JSON 文件列表。
    支持:
    1) 传入文件名: 全流程_51.52.json
    2) 传入目录名: 评测结果
    3) 传入相对路径: 评测结果/实验线结果.json
    """
    candidate = litl_root / path_under_litl
    if not candidate.exists():
        raise FileNotFoundError(f"在 LITL 下未找到: {path_under_litl}")

    if candidate.is_file():
        if candidate.suffix.lower() != ".json":
            raise ValueError(f"输入不是 JSON 文件: {candidate}")
        return [candidate]

    json_files = sorted(p for p in candidate.rglob("*.json") if p.is_file())
    if not json_files:
        raise ValueError(f"目录下没有 JSON 文件: {candidate}")
    return json_files


def load_results_map(json_files: List[Path]) -> Dict[str, Dict]:
    """
    从一个或多个 JSON 文件中读取 results，按 case_name 建立映射。
    若重复 case_name，后出现的会覆盖先出现的。
    """
    case_map: Dict[str, Dict] = {}
    for file_path in json_files:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        results = data.get("results", [])
        if not isinstance(results, list):
            raise ValueError(f"{file_path} 的 results 不是列表")
        for item in results:
            if not isinstance(item, dict):
                continue
            case_name = item.get("case_name")
            if not case_name:
                continue
            case_map[case_name] = item
    return case_map


def safe_float(value):
    try:
        if value is None:
            return None
        return float(value)
    except Exception:
        return None


def _row(project_name: str, case_name: str, base_score, target_score, delta_str: str, base_llm, target_llm, llm_changed: bool, missing: bool = False):
    """单行数据 (project_name, case_name, score_col, llm_col) 用于对齐输出。"""
    if missing:
        return (project_name or "", case_name, f"{base_score} -> N/A", f"{base_llm} -> N/A")
    return (
        project_name or "",
        case_name,
        f"{base_score} -> {target_score}  ({delta_str})",
        f"{base_llm} -> {target_llm}  ({'Y' if llm_changed else '-'})",
    )


def compare_cases(
    base_map: Dict[str, Dict], target_map: Dict[str, Dict]
) -> List[Tuple[str, str, str, str]]:
    """返回 [(project_name, case_name, score_col_text, llm_col_text), ...]"""
    rows: List[Tuple[str, str, str, str]] = []
    for case_name in sorted(base_map.keys(), key=lambda k: (base_map[k].get("project_name") or "", k)):
        base_item = base_map[case_name]
        target_item = target_map.get(case_name)

        project_name = base_item.get("project_name") or ""
        base_score = base_item.get("overall_score")
        base_llm = base_item.get("llm_assessment")

        if target_item is None:
            rows.append(_row(project_name, case_name, base_score, None, "N/A", base_llm, None, False, missing=True))
            continue

        target_score = target_item.get("overall_score")
        target_llm = target_item.get("llm_assessment")

        base_score_f = safe_float(base_score)
        target_score_f = safe_float(target_score)
        if base_score_f is not None and target_score_f is not None:
            delta = target_score_f - base_score_f
            delta_str = f"{delta:+.2f}"
        else:
            delta_str = "N/A"

        llm_changed = base_llm != target_llm
        score_changed = base_score != target_score

        if not score_changed and not llm_changed:
            continue

        rows.append(_row(project_name, case_name, base_score, target_score, delta_str, base_llm, target_llm, llm_changed))
    return rows


def main():
    if not LITL_ROOT.exists() or not LITL_ROOT.is_dir():
        raise FileNotFoundError(f"LITL 根目录不存在或不是目录: {LITL_ROOT}")

    first_json_files = resolve_input_to_json(FIRST_NAME, LITL_ROOT)
    second_json_files = resolve_input_to_json(SECOND_NAME, LITL_ROOT)

    first_map = load_results_map(first_json_files)
    second_map = load_results_map(second_json_files)

    diff_rows = compare_cases(first_map, second_map)

    print(f"[first]  {FIRST_NAME}  文件数: {len(first_json_files)}, case 数: {len(first_map)}")
    print(f"[second] {SECOND_NAME}  文件数: {len(second_json_files)}, case 数: {len(second_map)}")
    print()

    if not diff_rows:
        print("无差异 case。")
        return

    # 对齐列宽（按字符宽度，中文等宽 2）
    def width(s: str) -> int:
        return sum(2 if "\u4e00" <= c <= "\u9fff" else 1 for c in s)

    max_project = max(width(r[0]) for r in diff_rows)
    max_project = max(max_project, width("project_name"))
    max_case = max(width(r[1]) for r in diff_rows)
    max_case = max(max_case, width("case_name"))
    max_score = max(width(r[2]) for r in diff_rows)
    max_score = max(max_score, width("overall_score (first -> second)"))
    max_llm = max(width(r[3]) for r in diff_rows)
    max_llm = max(max_llm, width("llm_assessment (first -> second)"))

    def pad(s: str, w: int) -> str:
        return s + " " * (w - width(s))

    sep = "  "
    header_project = pad("project_name", max_project)
    header_case = pad("case_name", max_case)
    header_score = pad("overall_score (first -> second)", max_score)
    header_llm = pad("llm_assessment (first -> second)", max_llm)
    print(header_project + sep + header_case + sep + header_score + sep + header_llm)
    print("-" * (max_project + max_case + max_score + max_llm + 3 * len(sep)))
    for project_name, case_name, score_col, llm_col in diff_rows:
        print(pad(project_name, max_project) + sep + pad(case_name, max_case) + sep + pad(score_col, max_score) + sep + pad(llm_col, max_llm))
    print()
    print(f"差异 case 数: {len(diff_rows)}")


if __name__ == "__main__":
    main()
