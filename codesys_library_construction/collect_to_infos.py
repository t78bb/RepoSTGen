"""
从 SCRIPT_LIBRARY 的所有子目录收集文件到 infos 目录。
默认路径：
- 源：codesys_library_construction/SCRIPT_LIBRARY
- 目标：codesys_library_construction/infos

行为：
- 递归遍历 SCRIPT_LIBRARY 下的所有文件，平铺复制到目标目录。
- 如目标已存在同名文件，保留原文件并为后续重复文件追加编号（_1, _2, ...）。
- 运行结束打印重复文件名及最终落盘名的对应关系。

用法：
    python collect_to_infos.py
    python collect_to_infos.py --src SCRIPT_LIBRARY --dst infos
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Tuple


def collect_files(src_root: Path, dst_root: Path) -> List[str]:
    """
    返回值：发生重名而被跳过的原始文件名列表（不去重，以出现顺序记录）。
    """
    if not src_root.exists():
        raise FileNotFoundError(f"源目录不存在: {src_root}")
    dst_root.mkdir(parents=True, exist_ok=True)

    skipped: List[str] = []

    for file in sorted(src_root.rglob("*")):
        if not file.is_file():
            continue

        base_name = file.name
        target = dst_root / base_name
        # 若已存在同名文件，则跳过并记录
        if target.exists():
            skipped.append(base_name)
            continue
        shutil.copy2(file, target)

    return skipped


def main() -> None:
    parser = argparse.ArgumentParser(description="收集 SCRIPT_LIBRARY 子目录文件到 infos（检测重名并提示）")
    parser.add_argument("--src", default="SCRIPT_LIBRARY", help="源目录，默认 SCRIPT_LIBRARY")
    parser.add_argument("--dst", default="infos", help="目标目录，默认 infos")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    src_root = (script_dir / args.src).resolve()
    dst_root = (script_dir / args.dst).resolve()

    skipped = collect_files(src_root, dst_root)

    print(f"收集完成，输出目录: {dst_root}")
    if skipped:
        print("\n发现同名文件，已跳过：")
        for name in skipped:
            print(f"  {name}")
    else:
        print("\n未发现重名文件。")


if __name__ == "__main__":
    main()

