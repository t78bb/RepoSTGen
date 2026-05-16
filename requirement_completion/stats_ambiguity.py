#!/usr/bin/env python3
"""
统计 experience_build_output 下各子目录中 JSON 的：
1. 模糊点类型分布（各类型出现次数）
2. 各 case 的模糊点列表中条目数量
"""
import json
from pathlib import Path
from collections import defaultdict

EXPERIENCE_OUTPUT_DIR = Path(__file__).resolve().parent / "experience_build_output"


def main() -> None:
    if not EXPERIENCE_OUTPUT_DIR.exists():
        print(f"目录不存在: {EXPERIENCE_OUTPUT_DIR}")
        return

    type_counts: dict = defaultdict(int)
    case_counts: list = []  # (case_id, count)
    project_case_counts: dict = defaultdict(list)  # project -> [(case_id, count)]

    for json_path in sorted(EXPERIENCE_OUTPUT_DIR.rglob("*.json")):
        # 只统计项目子目录下的 json，跳过 code 等子目录里的非结果文件（若有）
        rel = json_path.relative_to(EXPERIENCE_OUTPUT_DIR)
        parts = rel.parts
        if len(parts) < 2 or parts[-1].startswith("."):
            continue
        # 项目名 = 第一层子目录
        project_name = parts[0]
        if "code" in parts:
            continue

        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"跳过无效 JSON: {json_path} ({e})")
            continue

        case_id = data.get("case_id", str(rel.with_suffix("")))
        items = data.get("模糊点列表", [])
        if not isinstance(items, list):
            items = []

        n = len(items)
        case_counts.append((case_id, n))
        project_case_counts[project_name].append((case_id, n))

        for item in items:
            if isinstance(item, dict):
                t = item.get("模糊点类型", "").strip() or "（未标注类型）"
                type_counts[t] += 1

    # 输出
    print("=" * 60)
    print("模糊点类型统计（全局）")
    print("=" * 60)
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")
    print(f"  合计: {sum(type_counts.values())} 条")
    print()

    print("=" * 60)
    print("各 case 模糊点数量（按项目）")
    print("=" * 60)
    for project in sorted(project_case_counts.keys()):
        pairs = project_case_counts[project]
        total_items = sum(n for _, n in pairs)
        print(f"\n  [{project}] 共 {len(pairs)} 个 case，模糊点合计 {total_items}")
        for cid, n in sorted(pairs, key=lambda x: -x[1]):
            print(f"    {cid}: {n}")
    print()

    print("=" * 60)
    print("汇总")
    print("=" * 60)
    total_cases = len(case_counts)
    total_items = sum(n for _, n in case_counts)
    zero_count = sum(1 for _, n in case_counts if n == 0)
    print(f"  总 case 数: {total_cases}")
    print(f"  总模糊点条数: {total_items}")
    print(f"  无模糊点 case 数: {zero_count}")
    print(f"  有模糊点 case 数: {total_cases - zero_count}")
    if total_cases > 0:
        print(f"  平均每 case 模糊点数: {total_items / total_cases:.2f}")


if __name__ == "__main__":
    main()
