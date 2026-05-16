#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LITL 多实验最优结果合并脚本

根据多组 LITL 评估结果，按 project 粒度选择每个 project 的第 k 优结果，
并将对应 output 子目录中的 project 复制到新目录，保证数据一致性。

排序规则：通过数量（passed_cases）优先，其次平均得分（average_overall_score）降序。
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

# 项目路径
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
OUTPUT_BASE_DIR = REPO_ROOT / "output"


def load_litl_file(path: Path) -> dict:
    """加载 LITL 评估 JSON 文件"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_project_rankings(files_data: list) -> dict:
    """
    收集每个 project 在各文件中的表现，按 (passed_cases, average_overall_score) 降序排序。

    Returns:
        project_rankings: {
            project_name: [
                (file_idx, eval_dir, passed_cases, avg_score, proj_summary),
                ...  # 已按 passed_cases 降序、avg_score 降序排序
            ],
            ...
        }
    """
    project_rankings = {}

    for file_idx, data in enumerate(files_data):
        eval_dir = data.get("metadata", {}).get("eval_directory")
        if not eval_dir:
            print(f"警告: 文件 #{file_idx} 缺少 metadata.eval_directory，跳过")
            continue

        eval_path = Path(eval_dir).resolve()
        project_summary = data.get("project_summary", {})

        for project_name, proj in project_summary.items():
            passed_cases = proj.get("passed_cases", 0)
            avg_score = float(proj.get("average_overall_score", 0.0))

            entry = (file_idx, str(eval_path), passed_cases, avg_score, proj)

            if project_name not in project_rankings:
                project_rankings[project_name] = []
            project_rankings[project_name].append(entry)

    # 对每个 project 的条目排序：passed_cases 降序，average_overall_score 降序
    for project_name in project_rankings:
        project_rankings[project_name].sort(
            key=lambda x: (-x[2], -x[3])  # -passed_cases, -avg_score
        )

    return project_rankings


def select_and_copy(
    project_rankings: dict,
    file_paths: list,
    k: int,
    out_dir: Path,
) -> dict:
    """
    对每个 project 选择第 k 优结果，复制对应 project 子目录到 out_dir。

    Returns:
        selection_report: { project_name: { "source": ..., "rank": ..., "passed_cases": ..., "avg_score": ... } }
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    report = {}

    for project_name, entries in sorted(project_rankings.items()):
        if not entries:
            continue

        # k 超出范围时取最后一个
        idx = min(k, len(entries) - 1)
        file_idx, eval_dir, passed_cases, avg_score, _ = entries[idx]

        src_project = Path(eval_dir) / project_name
        dst_project = out_dir / project_name

        if not src_project.exists():
            print(f"警告: 源目录不存在，跳过 {project_name}: {src_project}")
            report[project_name] = {
                "source": str(src_project),
                "source_eval_dir": eval_dir,
                "file": str(file_paths[file_idx]) if file_idx < len(file_paths) else "?",
                "rank": idx,
                "total_entries": len(entries),
                "passed_cases": passed_cases,
                "average_overall_score": avg_score,
                "skipped": True,
                "reason": "source_dir_not_found",
            }
            continue

        if dst_project.exists():
            shutil.rmtree(dst_project)
        shutil.copytree(src_project, dst_project)
        print(f"  {project_name}: rank={idx} (passed={passed_cases}, avg={avg_score:.2f}) <- {Path(eval_dir).name}")

        report[project_name] = {
            "source": str(src_project),
            "source_eval_dir": eval_dir,
            "file": str(file_paths[file_idx]) if file_idx < len(file_paths) else "?",
            "rank": idx,
            "total_entries": len(entries),
            "passed_cases": passed_cases,
            "average_overall_score": avg_score,
            "skipped": False,
        }

    return report


def main():
    parser = argparse.ArgumentParser(
        description="根据多组 LITL 评估结果，按 project 选择第 k 优结果并复制到新目录",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 3 个评估文件，选择每个 project 的最优结果 (k=0)
  python merge_litl_best.py --files a.json b.json c.json --k 0

  # 选择第 2 优结果
  python merge_litl_best.py --files a.json b.json c.json --k 1

  # 指定输出目录名
  python merge_litl_best.py --files a.json b.json c.json -k 0 -o merge_best
        """,
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="LITL 评估结果 JSON 文件路径（可多个）",
    )
    parser.add_argument(
        "-k", "--rank",
        type=int,
        default=0,
        help="选择排序位次，0=最优，1=次优，以此类推（默认: 0）",
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=None,
        help="新目录名称，置于 output 下（默认: merge_best_k{k}_{timestamp}）",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="将选择报告保存为 JSON 文件",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅打印选择结果，不实际复制",
    )
    args = parser.parse_args()

    if args.rank < 0:
        print("错误: -k 必须 >= 0")
        sys.exit(1)

    # 加载所有文件
    files_data = []
    for p in args.files:
        if not p.exists():
            print(f"错误: 文件不存在: {p}")
            sys.exit(1)
        files_data.append(load_litl_file(p))
    print(f"已加载 {len(files_data)} 个评估文件")

    # 收集并按 project 排序
    project_rankings = collect_project_rankings(files_data)
    all_projects = sorted(project_rankings.keys())
    print(f"共 {len(all_projects)} 个 project")

    # 确定输出目录
    if args.output_dir:
        out_dir = OUTPUT_BASE_DIR / args.output_dir
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = OUTPUT_BASE_DIR / f"merge_best_k{args.rank}_{ts}"
    print(f"输出目录: {out_dir}")

    # 选择并复制
    print("\n开始复制...")
    report = select_and_copy(
        project_rankings,
        [p.resolve() for p in args.files],
        args.rank,
        out_dir,
    )

    # 保存报告
    if args.report:
        report_path = Path(args.report)
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "k": args.rank,
                    "output_dir": str(out_dir),
                    "input_files": [str(p) for p in args.files],
                    "project_count": len(report),
                    "selection_report": report,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
        print(f"\n选择报告已保存: {report_path}")

    print(f"\n完成。共处理 {len(report)} 个 project，输出目录: {out_dir}")


if __name__ == "__main__":
    main()
