#!/usr/bin/env python3
"""
将 dataset/query 下各 case 的 requirement 字段填入 total_knowledge_req.json 的每一项。
每项的 case_id 格式为 "项目名/case名"，对应 dataset/query/项目名/case名.json 的 requirement。
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_FILE = Path(__file__).resolve().parent / "knowledge_base" / "total_knowledge_req.json"
QUERY_BASE = REPO_ROOT / "dataset" / "query"


def main() -> int:
    if not KNOWLEDGE_FILE.exists():
        print(f"错误: 经验库不存在 {KNOWLEDGE_FILE}", file=sys.stderr)
        return 1
    if not QUERY_BASE.exists():
        print(f"错误: query 目录不存在 {QUERY_BASE}", file=sys.stderr)
        return 1

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    filled = 0
    missing = []

    for category, items in data.items():
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            case_id = item.get("case_id")
            if not case_id or "/" not in case_id:
                missing.append((category, case_id or "(无 case_id)"))
                continue
            project, case_name = case_id.split("/", 1)
            query_file = QUERY_BASE / project / f"{case_name}.json"
            if not query_file.exists():
                missing.append((category, case_id))
                continue
            try:
                q = json.loads(query_file.read_text(encoding="utf-8"))
            except Exception as e:
                missing.append((category, f"{case_id} (读文件失败: {e})"))
                continue
            req = q.get("requirement") or q.get("requirement_cn") or ""
            item["requirement"] = req
            filled += 1

    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"已填入 requirement: {filled} 项")
    if missing:
        print(f"未找到或失败: {len(missing)} 项")
        for cat, cid in missing[:20]:
            print(f"  [{cat}] {cid}")
        if len(missing) > 20:
            print(f"  ... 共 {len(missing)} 项")
    return 0


if __name__ == "__main__":
    sys.exit(main())
