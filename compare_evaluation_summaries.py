#!/usr/bin/env python3
"""
比较两个 evaluation_summary.json 文件中 CodeBLEU 相关指标的差异。

固定基线文件:
  F:\\项目级st补全\\repo_gen_project\\real_groud_truth最新\\evaluation_summary_20260123_160251.json

目标文件路径也在代码中硬编码，按需修改 SECOND_PATH 常量即可。
比较内容:
  - overall_statistics.average_scores 下的 5 个指标
  - project_statistics[project].average_scores 下的 5 个指标（按项目逐个对比）
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple


REPO_ROOT = Path(__file__).resolve().parent
BASELINE_PATH = REPO_ROOT / "real_groud_truth最新" / "evaluation_summary_20260123_160251.json"
# 目标文件：按需修改为你想对比的新结果
SECOND_PATH = REPO_ROOT / "output" / "20260228_全流程1" / "evaluation_summary_20260302_022406.json"

METRICS = [
    "codebleu",
    "ngram_match_score",
    "weighted_ngram_match_score",
    "syntax_match_score",
    "dataflow_match_score",
]


def load_summary(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_avg_scores(summary: Dict[str, Any]) -> Dict[str, float]:
    return summary.get("overall_statistics", {}).get("average_scores", {}) or {}


def get_project_scores(summary: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
    stats = summary.get("project_statistics", {}) or {}
    result: Dict[str, Dict[str, float]] = {}
    for proj, info in stats.items():
        avg = info.get("average_scores", {}) or {}
        result[proj] = avg
    return result


def fmt_float(val: Any) -> str:
    try:
        return f"{float(val):.4f}"
    except Exception:
        return "   N/A  "


def main() -> int:
    if not BASELINE_PATH.exists():
        print(f"基线文件不存在: {BASELINE_PATH}")
        return 1
    if not SECOND_PATH.exists():
        print(f"目标文件不存在: {SECOND_PATH}")
        return 1

    base = load_summary(BASELINE_PATH)
    other = load_summary(SECOND_PATH)

    base_overall = get_avg_scores(base)
    other_overall = get_avg_scores(other)

    base_projects = get_project_scores(base)
    other_projects = get_project_scores(other)

    print("=" * 96)
    print("整体平均分对比 (overall_statistics.average_scores)")
    print("=" * 96)

    # 表头
    col_metric = 28
    col_val = 12
    header = (
        f"{'metric':<{col_metric}}"
        f"{'baseline':>{col_val}}"
        f"{'target':>{col_val}}"
        f"{'diff':>{col_val}}"
    )
    print(header)
    print("-" * len(header))

    for m in METRICS:
        b = base_overall.get(m)
        o = other_overall.get(m)
        if b is not None and o is not None:
            diff = float(o) - float(b)
            diff_str = f"{diff:+.4f}"
        else:
            diff_str = "   N/A  "
        print(
            f"{m:<{col_metric}}"
            f"{fmt_float(b):>{col_val}}"
            f"{fmt_float(o):>{col_val}}"
            f"{diff_str:>{col_val}}"
        )

    print("\n" + "=" * 96)
    print("按项目的平均分对比 (project_statistics[project].average_scores)")
    print("=" * 96)

    all_projects = sorted(set(base_projects.keys()) | set(other_projects.keys()))
    for proj in all_projects:
        b_scores = base_projects.get(proj) or {}
        o_scores = other_projects.get(proj) or {}
        print(f"\n[项目] {proj}")
        header = (
            f"{'metric':<{col_metric}}"
            f"{'baseline':>{col_val}}"
            f"{'target':>{col_val}}"
            f"{'diff':>{col_val}}"
        )
        print(header)
        print("-" * len(header))
        for m in METRICS:
            b = b_scores.get(m)
            o = o_scores.get(m)
            if b is not None and o is not None:
                diff = float(o) - float(b)
                diff_str = f"{diff:+.4f}"
            else:
                diff_str = "   N/A  "
            print(
                f"{m:<{col_metric}}"
                f"{fmt_float(b):>{col_val}}"
                f"{fmt_float(o):>{col_val}}"
                f"{diff_str:>{col_val}}"
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

