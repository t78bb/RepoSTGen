"""
清空 output 下指定子目录中，每个项目 results.jsonl 里的 docs 字段，
并删除该项目目录下除 results.jsonl 外的所有文件和子目录。

用法:
  python clear_docs_in_results.py <output下子目录名>
  python clear_docs_in_results.py 20260228_全流程1
"""
import argparse
import json
import shutil
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="清空指定 output 子目录下各项目 results.jsonl 的 docs 字段"
    )
    parser.add_argument(
        "subdir",
        type=str,
        help="output 下的子目录名，例如 20260228_全流程1",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅打印会处理的文件，不实际修改",
    )
    parser.add_argument(
        "--keep-others",
        action="store_true",
        help="只清空 docs，不删除项目目录下其余文件和目录",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    output_dir = script_dir / "output"
    target_dir = output_dir / args.subdir

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"错误: 目录不存在或不是目录: {target_dir}", file=sys.stderr)
        return 1

    total_files = 0
    total_lines = 0

    # 递归查找所有 results.jsonl（兼容 子目录/results.jsonl 与 子目录/项目/results.jsonl）
    results_files = sorted(target_dir.rglob("results.jsonl"))
    results_files = [p for p in results_files if p.is_file()]

    for results_jsonl in results_files:
        rel = results_jsonl.relative_to(target_dir)

        if args.dry_run:
            print(f"[dry-run] 将处理: {results_jsonl}")
            total_files += 1
            continue

        lines_in = results_jsonl.read_text(encoding="utf-8").strip().splitlines()
        new_lines = []
        for line in lines_in:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                obj["docs"] = []
                new_lines.append(json.dumps(obj, ensure_ascii=False))
            except (json.JSONDecodeError, TypeError) as e:
                print(f"  警告: 跳过无效行 in {results_jsonl}: {e}", file=sys.stderr)
                new_lines.append(line)

        if new_lines:
            results_jsonl.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
            total_files += 1
            total_lines += len(new_lines)
            print(f"  已清空 docs: {rel} ({len(new_lines)} 条)")

        # 删除该项目目录下除 results.jsonl 外的所有文件和子目录
        if not args.keep_others:
            project_dir = results_jsonl.parent
            for item in sorted(project_dir.iterdir()):
                if item.name == "results.jsonl":
                    continue
                try:
                    if item.is_file():
                        item.unlink()
                        print(f"    已删除文件: {item.relative_to(target_dir)}")
                    elif item.is_dir():
                        shutil.rmtree(item)
                        print(f"    已删除目录: {item.relative_to(target_dir)}")
                except OSError as e:
                    print(f"    警告: 无法删除 {item}: {e}", file=sys.stderr)

    if args.dry_run:
        print(f"\n[dry-run] 将处理 {total_files} 个 results.jsonl 文件")
    else:
        print(f"\n完成: 共处理 {total_files} 个项目，{total_lines} 条记录已清空 docs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
