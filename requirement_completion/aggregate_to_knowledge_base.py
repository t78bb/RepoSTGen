#!/usr/bin/env python3
"""
将 experience_build_output 下各项目子目录中的 JSON（模糊点列表）按类型整合，
写入 knowledge_base 目录，格式与 total_knowledge.json 一致，每条记录带 case_id。

输出文件：knowledge_base/aggregated_knowledge.json
格式：{ "模糊点类型": [ { "模糊点描述", "精准需求示例", "case_id" }, ... ], ... }
"""
import json
from pathlib import Path
from collections import defaultdict

REQUIREMENT_COMPLETION_DIR = Path(__file__).resolve().parent
EXPERIENCE_OUTPUT_DIR = REQUIREMENT_COMPLETION_DIR / "experience_build_output"
KNOWLEDGE_BASE_DIR = REQUIREMENT_COMPLETION_DIR / "knowledge_base"
OUTPUT_FILE = KNOWLEDGE_BASE_DIR / "aggregated_knowledge.json"


def main() -> None:
    if not EXPERIENCE_OUTPUT_DIR.exists():
        print(f"目录不存在: {EXPERIENCE_OUTPUT_DIR}")
        return

    # 按类型聚合：类型 -> [ { 模糊点描述, 精准需求示例, case_id }, ... ]
    by_type: dict = defaultdict(list)

    for json_path in sorted(EXPERIENCE_OUTPUT_DIR.rglob("*.json")):
        rel = json_path.relative_to(EXPERIENCE_OUTPUT_DIR)
        parts = rel.parts
        if len(parts) < 2 or "code" in parts:
            continue

        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"跳过无效 JSON: {json_path} ({e})")
            continue

        case_id = data.get("case_id", str(rel.with_suffix("")).replace("\\", "/"))
        items = data.get("模糊点列表", [])
        if not isinstance(items, list):
            continue

        for item in items:
            if not isinstance(item, dict):
                continue
            type_name = (item.get("模糊点类型") or "").strip() or "未分类"
            desc = (item.get("模糊点描述") or "").strip()
            # 经验库格式用「精准需求示例」，experience JSON 里是「精准需求描述」
            example = (item.get("精准需求示例") or item.get("精准需求描述") or "").strip()
            by_type[type_name].append({
                "模糊点描述": desc,
                "精准需求示例": example,
                "case_id": case_id,
            })

    # 转为普通 dict，键按字母排序（可选），列表保持插入顺序
    result = {k: by_type[k] for k in sorted(by_type.keys())}

    KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"已整合到: {OUTPUT_FILE}")
    print("按类型统计:")
    for t, arr in result.items():
        print(f"  {t}: {len(arr)} 条")
    print(f"  合计: {sum(len(arr) for arr in result.values())} 条")


if __name__ == "__main__":
    main()
