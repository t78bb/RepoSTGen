# -*- coding: utf-8 -*-
"""
批量重命名和复制目录脚本

功能：
1. 将 real_groud_truth最新 目录下所有子目录的 readful_result 改名为 origin_result_no_provide
2. 复制 full_result 目录并改名为 readful_result

使用方法：
    python 批量重命名目录.py
"""

import shutil
import sys
from pathlib import Path

# 设置输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 目标根目录
BASE_DIR = Path(r"D:\graduate_project\项目级st补全\repo_gen_project\real_groud_truth最新")

def main():
    if not BASE_DIR.exists():
        print(f"错误: 目录不存在: {BASE_DIR}")
        return
    
    print(f"处理目录: {BASE_DIR}")
    print("=" * 80)
    
    stats = {"renamed": 0, "copied": 0, "skipped_rename": 0, "skipped_copy": 0, "errors": 0}
    
    for subdir in sorted(BASE_DIR.iterdir()):
        if not subdir.is_dir():
            continue
        
        print(f"\n{subdir.name}:")
        
        # 步骤1: 重命名 readful_result 为 origin_result_no_provide
        rr = subdir / "readful_result"
        orn = subdir / "origin_result_no_provide"
        if rr.exists():
            if orn.exists():
                print("  [跳过] origin_result_no_provide 已存在")
                stats["skipped_rename"] += 1
            else:
                try:
                    rr.rename(orn)
                    print("  [OK] readful_result -> origin_result_no_provide")
                    stats["renamed"] += 1
                except Exception as e:
                    print(f"  [ERROR] 重命名失败: {e}")
                    stats["errors"] += 1
        else:
            print("  [跳过] readful_result 不存在")
        
        # 步骤2: 复制 full_result 为 readful_result
        fr = subdir / "full_result"
        new_rr = subdir / "readful_result"
        if fr.exists():
            if new_rr.exists():
                print("  [跳过] readful_result 已存在")
                stats["skipped_copy"] += 1
            else:
                try:
                    shutil.copytree(fr, new_rr)
                    print("  [OK] full_result -> readful_result (已复制)")
                    stats["copied"] += 1
                except Exception as e:
                    print(f"  [ERROR] 复制失败: {e}")
                    stats["errors"] += 1
        else:
            print("  [跳过] full_result 不存在")
    
    # 打印统计信息
    print("\n" + "=" * 80)
    print("处理完成！统计信息：")
    print("=" * 80)
    print(f"重命名成功:        {stats['renamed']}")
    print(f"复制成功:          {stats['copied']}")
    print(f"跳过重命名:        {stats['skipped_rename']}")
    print(f"跳过复制:          {stats['skipped_copy']}")
    print(f"错误数:            {stats['errors']}")
    print("=" * 80)

if __name__ == "__main__":
    main()

