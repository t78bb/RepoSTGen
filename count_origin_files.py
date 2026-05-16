# -*- coding: utf-8 -*-
import sys
from pathlib import Path
import json

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TARGET_DIR = Path(r"D:\graduate_project\项目级st补全\repo_gen_project\real_groud_truth最新")

if not TARGET_DIR.exists():
    print(f"目录不存在: {TARGET_DIR}")
    exit(1)

print(f"统计目录: {TARGET_DIR}")
print("=" * 80)

stats = {
    "total_subdirs": 0,
    "subdirs_with_origin_result": 0,
    "subdirs_without_origin_result": 0,
    "total_files": 0,
    "details": []
}

for subdir in sorted(TARGET_DIR.iterdir()):
    if not subdir.is_dir():
        continue
    
    stats["total_subdirs"] += 1
    origin_result_dir = subdir / "origin_result_no_provide"
    
    if origin_result_dir.exists() and origin_result_dir.is_dir():
        files = [f for f in origin_result_dir.iterdir() if f.is_file()]
        file_count = len(files)
        
        stats["subdirs_with_origin_result"] += 1
        stats["total_files"] += file_count
        
        stats["details"].append({
            "subdir": subdir.name,
            "file_count": file_count,
            "files": [f.name for f in files]
        })
        
        print(f"{subdir.name:50} {file_count:4} 个文件")
    else:
        stats["subdirs_without_origin_result"] += 1
        print(f"{subdir.name:50} {'无origin_result_no_provide目录':<20}")

print("\n" + "=" * 80)
print("统计结果:")
print("=" * 80)
print(f"总子目录数:                    {stats['total_subdirs']}")
print(f"有origin_result_no_provide:   {stats['subdirs_with_origin_result']}")
print(f"无origin_result_no_provide:   {stats['subdirs_without_origin_result']}")
print(f"总文件数:                      {stats['total_files']}")
print("=" * 80)

output_file = TARGET_DIR.parent / "origin_result_file_count.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

print(f"\n详细结果已保存到: {output_file}")

