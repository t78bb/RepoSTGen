#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
输出 project_code 目录下各个子目录的子目录结构
"""

from pathlib import Path

# project_code 目录路径
project_code_base = Path(r"D:\graduate_project\项目级st补全\repo_gen_project\dataset\project_code")

if not project_code_base.exists():
    print(f"错误: 目录不存在 - {project_code_base}")
    exit(1)

print("=" * 80)
print("project_code 目录结构")
print("=" * 80)
print(f"基础目录: {project_code_base}\n")

# 获取所有项目目录
project_dirs = [d for d in project_code_base.iterdir() if d.is_dir()]
project_dirs.sort(key=lambda x: x.name)

if not project_dirs:
    print("未找到任何项目目录")
    exit(0)

print(f"找到 {len(project_dirs)} 个项目目录:\n")

# 遍历每个项目目录
for project_dir in project_dirs:
    print(f"项目: {project_dir.name}")
    print("-" * 80)
    
    # 获取项目目录下的所有子目录
    subdirs = [d for d in project_dir.iterdir() if d.is_dir()]
    subdirs.sort(key=lambda x: x.name)
    
    if subdirs:
        print("  子目录:")
        for subdir in subdirs:
            # 统计子目录下的文件数量
            file_count = len([f for f in subdir.iterdir() if f.is_file()])
            print(f"    - {subdir.name}/ ({file_count} 个文件)")
    else:
        print("  (无子目录)")
    
    print()

print("=" * 80)
print("统计信息")
print("=" * 80)

# 统计所有子目录类型
all_subdirs = {}
for project_dir in project_dirs:
    subdirs = [d.name for d in project_dir.iterdir() if d.is_dir()]
    for subdir_name in subdirs:
        if subdir_name not in all_subdirs:
            all_subdirs[subdir_name] = []
        all_subdirs[subdir_name].append(project_dir.name)

print(f"\n所有子目录类型及其出现的项目:")
for subdir_name in sorted(all_subdirs.keys()):
    projects = all_subdirs[subdir_name]
    print(f"  {subdir_name}: {len(projects)} 个项目")
    if len(projects) <= 10:
        print(f"    {', '.join(projects)}")
    else:
        print(f"    {', '.join(projects[:10])} ... (共 {len(projects)} 个)")

