#!/usr/bin/env python3
"""
按固定 project 顺序比较两个 LITL 评测结果中的 project_summary。

比较字段：
- average_overall_score
- passed_cases

project 顺序直接硬编码自：
output/20260309_200325/full_process_results_20260309_213659.json
中的 self_growing_kb.project_generation_order。
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


LITL_ROOT = Path(__file__).resolve().parent / "LITL"


PROJECT_ORDER: List[str] = [
    "repoeval_Builder_Application_RPI",
    "repoeval_Command1",
    "repoeval_Decorator_Application",
    "repoeval_GreatExampleOfAdvantages",
    "repoeval_Interation_HowTo",
    "repoeval_PID_controller",
    "repoeval_PT1Filter",
    "repoeval_ProductionLine",
    "repoeval_Proxy_Application",
    "repoeval_Robotics_DynamicModel",
    "repoeval_VisuElements",
    "repoeval_Wrappers",
    "repoeval_assembly-station",
    "repoeval_counter",
    "repoeval_electronic_cam_motion",
    "repoeval_electronic_gear_motion",
    "repoeval_elevator",
    "repoeval_four-level_elevator_control",
    "repoeval_isScaleOutput",
    "repoeval_barrier",
    "repoeval_measurement_control",
    "repoeval_open-type_dual-axis_winding_machine",
    "repoeval_plc_hello_mixing_tank",
    "repoeval_readwriteFile",
    "repoeval_three-axis_CNC_motion",
    "repoeval_traffic_light",
]


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"JSON 根节点不是对象: {path}")
    return data


def resolve_input_json_path(path_str: str) -> Path:
    """
    解析输入 JSON 路径：
    - 若传入绝对路径/当前可访问路径，直接使用
    - 否则默认到 LITL 目录下查找
    """
    raw_path = Path(path_str)
    if raw_path.exists():
        return raw_path

    litl_path = LITL_ROOT / path_str
    if litl_path.exists():
        return litl_path

    raise FileNotFoundError(f"文件不存在: {raw_path}，且在 LITL 下也未找到: {litl_path}")


def safe_float(value: Any) -> Optional[float]:
    try:
        if value is None:
            return None
        return float(value)
    except Exception:
        return None


def safe_int(value: Any) -> Optional[int]:
    try:
        if value is None:
            return None
        return int(value)
    except Exception:
        return None


def format_float(value: Optional[float]) -> str:
    return "N/A" if value is None else f"{value:.2f}"


def format_int(value: Optional[int]) -> str:
    return "N/A" if value is None else str(value)


def compare_project_summary(
    first_data: Dict[str, Any],
    second_data: Dict[str, Any],
) -> List[Dict[str, Any]]:
    first_summary = first_data.get("project_summary") or {}
    second_summary = second_data.get("project_summary") or {}
    if not isinstance(first_summary, dict) or not isinstance(second_summary, dict):
        raise ValueError("project_summary 不是对象")

    rows: List[Dict[str, Any]] = []
    for project_name in PROJECT_ORDER:
        first_item = first_summary.get(project_name) or {}
        second_item = second_summary.get(project_name) or {}

        first_score = safe_float(first_item.get("average_overall_score"))
        second_score = safe_float(second_item.get("average_overall_score"))
        first_passed = safe_int(first_item.get("passed_cases"))
        second_passed = safe_int(second_item.get("passed_cases"))

        score_delta = None
        if first_score is not None and second_score is not None:
            score_delta = second_score - first_score

        passed_delta = None
        if first_passed is not None and second_passed is not None:
            passed_delta = second_passed - first_passed

        rows.append(
            {
                "project_name": project_name,
                "first_average_overall_score": first_score,
                "second_average_overall_score": second_score,
                "average_overall_score_delta": score_delta,
                "first_passed_cases": first_passed,
                "second_passed_cases": second_passed,
                "passed_cases_delta": passed_delta,
            }
        )
    return rows


def display_rows(rows: List[Dict[str, Any]], first_label: str, second_label: str) -> None:
    def width(text: str) -> int:
        return sum(2 if "\u4e00" <= c <= "\u9fff" else 1 for c in text)

    # header = [
    #     "project_name",
    #     f"avg_score ({first_label})",
    #     f"avg_score ({second_label})",
    #     "score_delta",
    #     f"passed ({first_label})",
    #     f"passed ({second_label})",
    #     "passed_delta",
    # ]

    header = [
        "project_name   ",
        f"avg_score1    ",
        f"avg_score2    ",
        "score_delta    ",
        f"passed1   ",
        f"passed2   ",
        "passed_delta",
    ]


    table_rows: List[List[str]] = []
    for row in rows:
        table_rows.append(
            [
                row["project_name"],
                format_float(row["first_average_overall_score"]),
                format_float(row["second_average_overall_score"]),
                format_float(row["average_overall_score_delta"]),
                format_int(row["first_passed_cases"]),
                format_int(row["second_passed_cases"]),
                format_int(row["passed_cases_delta"]),
            ]
        )

    widths = [width(col) for col in header]
    for row in table_rows:
        for i, col in enumerate(row):
            widths[i] = max(widths[i], width(col))

    def pad(text: str, target: int) -> str:
        return text + " " * (target - width(text))

    sep = "  "
    print(sep.join(pad(header[i], widths[i]) for i in range(len(header))))
    print("-" * (sum(widths) + len(sep) * (len(header) - 1)))
    for row in table_rows:
        print(sep.join(pad(row[i], widths[i]) for i in range(len(row))))


def build_output_payload(
    first_path: Path,
    second_path: Path,
    rows: List[Dict[str, Any]],
) -> Dict[str, Any]:
    comparable_score_rows = [r for r in rows if r["average_overall_score_delta"] is not None]
    comparable_pass_rows = [r for r in rows if r["passed_cases_delta"] is not None]

    return {
        "first_file": str(first_path),
        "second_file": str(second_path),
        "project_order": PROJECT_ORDER,
        "summary": {
            "project_count_in_order": len(PROJECT_ORDER),
            "comparable_average_overall_score_projects": len(comparable_score_rows),
            "comparable_passed_cases_projects": len(comparable_pass_rows),
            "score_improved_projects": sum(1 for r in comparable_score_rows if r["average_overall_score_delta"] > 0),
            "score_declined_projects": sum(1 for r in comparable_score_rows if r["average_overall_score_delta"] < 0),
            "passed_improved_projects": sum(1 for r in comparable_pass_rows if r["passed_cases_delta"] > 0),
            "passed_declined_projects": sum(1 for r in comparable_pass_rows if r["passed_cases_delta"] < 0),
        },
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="按固定 project 顺序比较两个 LITL 结果中的 average_overall_score 与 passed_cases"
    )
    parser.add_argument("first_file", type=str, help="第一个 LITL 评测结果 JSON")
    parser.add_argument("second_file", type=str, help="第二个 LITL 评测结果 JSON")
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="可选，保存比较结果到 JSON 文件",
    )
    args = parser.parse_args()

    first_path = resolve_input_json_path(args.first_file)
    second_path = resolve_input_json_path(args.second_file)

    first_data = load_json(first_path)
    second_data = load_json(second_path)
    rows = compare_project_summary(first_data, second_data)

    print(f"first : {first_path}")
    print(f"second: {second_path}")
    print()
    display_rows(rows, first_path.stem, second_path.stem)

    if args.output:
        output_path = Path(args.output)
        payload = build_output_payload(first_path, second_path, rows)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print()
        print(f"已保存比较结果: {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
