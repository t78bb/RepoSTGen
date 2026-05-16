#!/usr/bin/env python3
"""
对指定根目录下每个子目录调用 create_no_provide_version：
从 readful_result 中去掉 query 中对应的 provide_code 部分，写入 readful_result_no_provide。

使用 full_process.create_no_provide_version 的已有实现。
"""
import sys
from pathlib import Path

# 项目根目录
REPO_ROOT = Path(__file__).resolve().parent
# 要处理的根目录（其下每个子目录视为一个项目，含 readful_result）
TARGET_ROOT = REPO_ROOT / "output" / "20260306_vanilla"

sys.path.insert(0, str(REPO_ROOT))
from full_process import create_no_provide_version


def main() -> int:
    print(1)
    if not TARGET_ROOT.exists() or not TARGET_ROOT.is_dir():
        print(f"错误: 目录不存在或不是目录: {TARGET_ROOT}")
        return 1

    ok = 0
    skip = 0
    for subdir in sorted(TARGET_ROOT.iterdir()):
        if not subdir.is_dir():
            continue
        readful = subdir / "readful_result"
        if not readful.exists() or not readful.is_dir():
            print(f"[跳过] {subdir.name}: 无 readful_result")
            skip += 1
            continue
        print(f"\n处理: {subdir.name}")
        if create_no_provide_version(subdir):
            ok += 1
        else:
            print(f"  ⚠ 未生成或失败")

    print(f"\n完成: 成功 {ok} 个项目，跳过 {skip} 个")
    return 0


if __name__ == "__main__":
    sys.exit(main())
