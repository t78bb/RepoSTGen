# -*- coding: utf-8 -*-
"""
同步 full_result 目录中的文件

功能：
1. 比较 origin_result_no_provide 和 full_result 的文件数量
2. 如果数量相同则跳过
3. 如果不同，对于缺失的文件：
   - 从 origin_result_no_provide 复制到 full_result
   - 从 dataset/query 中找到对应的 JSON 文件
   - 将 provide_code 字段内容添加到文件头部
"""

import sys
import json
import shutil
from pathlib import Path

# 设置输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 基础目录
BASE_DIR = Path(r"D:\graduate_project\项目级st补全\repo_gen_project\real_groud_truth最新")
QUERY_DIR = Path(r"D:\graduate_project\项目级st补全\repo_gen_project\dataset\query")

def sync_full_result():
    """同步 full_result 目录"""
    
    if not BASE_DIR.exists():
        print(f"错误: 目录不存在: {BASE_DIR}")
        return
    
    print(f"处理目录: {BASE_DIR}")
    print("=" * 80)
    
    stats = {
        "total_subdirs": 0,
        "skipped": 0,
        "processed": 0,
        "files_copied": 0,
        "files_updated": 0,
        "errors": 0,
        "details": []
    }
    
    # 遍历所有子目录
    for subdir in sorted(BASE_DIR.iterdir()):
        if not subdir.is_dir():
            continue
        
        stats["total_subdirs"] += 1
        project_name = subdir.name
        
        origin_dir = subdir / "origin_result_no_provide"
        full_dir = subdir / "full_result"
        
        # 检查目录是否存在
        if not origin_dir.exists():
            print(f"\n{project_name}: 跳过（无origin_result_no_provide目录）")
            continue
        
        if not full_dir.exists():
            print(f"\n{project_name}: 创建full_result目录")
            full_dir.mkdir(parents=True, exist_ok=True)
        
        # 获取文件列表
        origin_files = {f.name for f in origin_dir.iterdir() if f.is_file() and f.suffix == '.st'}
        full_files = {f.name for f in full_dir.iterdir() if f.is_file() and f.suffix == '.st'}
        
        # 比较文件数量
        if len(origin_files) == len(full_files):
            print(f"\n{project_name}: 跳过（文件数量相同: {len(origin_files)}）")
            stats["skipped"] += 1
            continue
        
        # 找出缺失的文件
        missing_files = origin_files - full_files
        
        if not missing_files:
            print(f"\n{project_name}: 跳过（full_result文件更多或相同）")
            stats["skipped"] += 1
            continue
        
        print(f"\n{project_name}: 处理 {len(missing_files)} 个缺失文件")
        stats["processed"] += 1
        
        project_detail = {
            "project": project_name,
            "missing_files": len(missing_files),
            "files": []
        }
        
        # 处理每个缺失的文件
        for filename in sorted(missing_files):
            try:
                origin_file = origin_dir / filename
                full_file = full_dir / filename
                
                # 1. 复制文件
                shutil.copy2(origin_file, full_file)
                stats["files_copied"] += 1
                print(f"  [复制] {filename}")
                
                # 2. 查找对应的 JSON 文件
                # 文件名（不含扩展名）
                case_name = filename[:-3]  # 去掉 .st
                json_file = QUERY_DIR / project_name / f"{case_name}.json"
                
                if json_file.exists():
                    # 读取 JSON 文件
                    with open(json_file, 'r', encoding='utf-8') as f:
                        query_data = json.load(f)
                    
                    provide_code = query_data.get("provide_code", "")
                    
                    if provide_code:
                        # 读取原文件内容
                        with open(full_file, 'r', encoding='utf-8') as f:
                            original_content = f.read()
                        
                        # 将 provide_code 添加到文件头部
                        new_content = provide_code + "\n\n" + original_content
                        
                        # 写回文件
                        with open(full_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        stats["files_updated"] += 1
                        print(f"  [更新] {filename} (已添加provide_code)")
                        project_detail["files"].append({
                            "filename": filename,
                            "status": "copied_and_updated",
                            "provide_code_length": len(provide_code)
                        })
                    else:
                        print(f"  [警告] {filename} (JSON中无provide_code字段)")
                        project_detail["files"].append({
                            "filename": filename,
                            "status": "copied_only",
                            "reason": "no_provide_code"
                        })
                else:
                    print(f"  [警告] {filename} (找不到JSON文件: {json_file})")
                    project_detail["files"].append({
                        "filename": filename,
                        "status": "copied_only",
                        "reason": "json_not_found"
                    })
                
            except Exception as e:
                print(f"  [错误] {filename}: {e}")
                stats["errors"] += 1
                project_detail["files"].append({
                    "filename": filename,
                    "status": "error",
                    "error": str(e)
                })
        
        stats["details"].append(project_detail)
    
    # 打印统计信息
    print("\n" + "=" * 80)
    print("处理完成！统计信息：")
    print("=" * 80)
    print(f"总子目录数:        {stats['total_subdirs']}")
    print(f"跳过（数量相同）:  {stats['skipped']}")
    print(f"已处理:            {stats['processed']}")
    print(f"文件已复制:        {stats['files_copied']}")
    print(f"文件已更新:        {stats['files_updated']}")
    print(f"错误数:            {stats['errors']}")
    print("=" * 80)
    
    # 保存详细结果
    output_file = BASE_DIR.parent / "sync_full_result_log.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细日志已保存到: {output_file}")

if __name__ == "__main__":
    sync_full_result()

