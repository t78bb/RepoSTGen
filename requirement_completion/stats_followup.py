#!/usr/bin/env python3
"""
统计指定 output 目录下 results 中各 JSON 的追问列表项数：
  追问项数之和 / case 数量 = 平均每 case 追问数。
支持 results 下项目级 JSON（数组）与子目录内单 case JSON，按 case_id 去重后统计。
"""
import json
import sys
from pathlib import Path

OUTPUT_BASE = Path(__file__).resolve().parent / "output"


def collect_cases_from_results(results_dir: Path) -> list:
    """从 results 目录收集所有 case（每个 case 为一个 dict，含 追问列表）。"""
    cases = []
    for p in results_dir.iterdir():
        if p.is_file() and p.suffix.lower() == ".json":
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
            if isinstance(data, list):
                cases.extend(data)
            elif isinstance(data, dict) and "追问列表" in data:
                cases.append(data)
    for sub in results_dir.iterdir():
        if not sub.is_dir():
            continue
        for j in sub.rglob("*.json"):
            try:
                data = json.loads(j.read_text(encoding="utf-8"))
            except Exception:
                continue
            if isinstance(data, dict) and "追问列表" in data:
                cases.append(data)
    # 按 case_id 去重（同一 case 可能既在 project.json 数组里又在 project/case.json 里）
    seen = set()
    unique = []
    for c in cases:
        cid = c.get("case_id", id(c))
        if cid not in seen:
            seen.add(cid)
            unique.append(c)
    return unique


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="统计 output 某次 run 的 results 下追问列表项数之和 / case 数")
    parser.add_argument(
        "run_dir",
        nargs="?",
        default=None,
        help="run 目录名，如 20260213_223537；不传则用 output 下最新目录",
    )
    parser.add_argument(
        "--output-base",
        type=str,
        default=None,
        help=f"output 根目录，默认: {OUTPUT_BASE}",
    )
    args = parser.parse_args()

    output_base = Path(args.output_base) if args.output_base else OUTPUT_BASE
    if not output_base.exists():
        print(f"目录不存在: {output_base}", file=sys.stderr)
        sys.exit(1)

    if args.run_dir:
        run_dir = output_base / args.run_dir
    else:
        dirs = [d for d in output_base.iterdir() if d.is_dir()]
        if not dirs:
            print("未找到 run 目录", file=sys.stderr)
            sys.exit(1)
        run_dir = max(dirs, key=lambda d: d.stat().st_mtime)
        print(f"使用最新目录: {run_dir.name}")

    results_dir = run_dir / "results"
    if not results_dir.exists():
        print(f"不存在 results 目录: {results_dir}", file=sys.stderr)
        sys.exit(1)

    cases = collect_cases_from_results(results_dir)
    total_followups = sum(len(c.get("追问列表") or []) for c in cases)
    n_cases = len(cases)
    avg = total_followups / n_cases if n_cases else 0

    print(f"Run 目录: {run_dir}")
    print(f"Results: {results_dir}")
    print(f"Case 数: {n_cases}")
    print(f"追问列表项数之和: {total_followups}")
    print(f"平均每 case 追问数: {avg:.2f}")


if __name__ == "__main__":
    main()
