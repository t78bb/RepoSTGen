from pathlib import Path
import argparse
import sys


def get_subdir_names(dir_path: Path) -> set[str]:
    if not dir_path.exists():
        raise FileNotFoundError(f"目录不存在: {dir_path}")
    if not dir_path.is_dir():
        raise NotADirectoryError(f"不是目录: {dir_path}")
    return {p.name for p in dir_path.iterdir() if p.is_dir()}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="比较两个目录的子目录集合，并输出前者减后者的结果。"
    )
    parser.add_argument(
        "--query_dir",
        type=str,
        default=r"dataset/query",
        help="前一个目录（默认: dataset/query）",
    )
    parser.add_argument(
        "--target_dir",
        type=str,
        required=True,
        help="后一个目录（例如: output/20260226_40case_无plan_barrier）",
    )
    args = parser.parse_args()

    query_dir = Path(args.query_dir)
    target_dir = Path(args.target_dir)

    try:
        query_set = get_subdir_names(query_dir)
        target_set = get_subdir_names(target_dir)
    except Exception as exc:
        print(f"路径检查失败: {exc}")
        return 1

    remain = sorted(query_set - target_set)
    print("  ".join(remain))
    return 0


if __name__ == "__main__":
    sys.exit(main())
