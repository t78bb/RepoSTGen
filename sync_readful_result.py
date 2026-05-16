# -*- coding: utf-8 -*-
"""
同步 readful_result 目录

功能：
1. 清空 real_groud_truth最新 下所有子目录的 readful_result 内容
2. 把 full_result 所有文件复制到 readful_result
"""

import sys
import shutil
from pathlib import Path

# 设置输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 基础目录
BASE_DIR = Path(r"D:\graduate_project\项目级st补全\repo_gen_project\real_groud_truth最新")

def sync_readful_result():
    """同步 readful_result 目录"""
    
    if not BASE_DIR.exists():
        print(f"错误: 目录不存在: {BASE_DIR}")
        return
    
    print(f"处理目录: {BASE_DIR}")
    print("=" * 80)
    
    stats = {
        "total_subdirs": 0,
        "processed": 0,
        "skipped_no_full_result": 0,
        "skipped_no_readful_result": 0,
        "files_copied": 0,
        "errors": 0,
        "details": []
    }
    
    # 遍历所有子目录
    for subdir in sorted(BASE_DIR.iterdir()):
        if not subdir.is_dir():
            continue
        
        stats["total_subdirs"] += 1
        project_name = subdir.name
        
        full_dir = subdir / "full_result"
        readful_dir = subdir / "readful_result"
        
        # 检查 full_result 目录是否存在
        if not full_dir.exists():
            print(f"\n{project_name}: 跳过（无full_result目录）")
            stats["skipped_no_full_result"] += 1
            continue
        
        # 获取 full_result 中的所有文件
        full_files = [f for f in full_dir.iterdir() if f.is_file()]
        
        if not full_files:
            print(f"\n{project_name}: 跳过（full_result目录为空）")
            continue
        
        # 创建或清空 readful_result 目录
        if readful_dir.exists():
            # 清空目录
            for item in readful_dir.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                except Exception as e:
                    print(f"  [警告] 删除 {item.name} 失败: {e}")
        else:
            # 创建目录
            readful_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{project_name}: 处理 {len(full_files)} 个文件")
        stats["processed"] += 1
        
        project_detail = {
            "project": project_name,
            "files_copied": 0,
            "files": []
        }
        
        # 复制所有文件
        for full_file in sorted(full_files):
            try:
                readful_file = readful_dir / full_file.name
                shutil.copy2(full_file, readful_file)
                stats["files_copied"] += 1
                project_detail["files_copied"] += 1
                project_detail["files"].append(full_file.name)
                print(f"  [复制] {full_file.name}")
            except Exception as e:
                print(f"  [错误] {full_file.name}: {e}")
                stats["errors"] += 1
        
        stats["details"].append(project_detail)
    
    # 打印统计信息
    print("\n" + "=" * 80)
    print("处理完成！统计信息：")
    print("=" * 80)
    print(f"总子目录数:              {stats['total_subdirs']}")
    print(f"已处理:                  {stats['processed']}")
    print(f"跳过（无full_result）:   {stats['skipped_no_full_result']}")
    print(f"跳过（无readful_result）:{stats['skipped_no_readful_result']}")
    print(f"文件已复制:              {stats['files_copied']}")
    print(f"错误数:                  {stats['errors']}")
    print("=" * 80)

if __name__ == "__main__":
    sync_readful_result()

