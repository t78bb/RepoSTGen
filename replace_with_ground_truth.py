# -*- coding: utf-8 -*-
"""
用 ground_truth 替换 readful_result 中的文件内容

功能：
1. 遍历 groud_truthcopy自project_code 目录下的所有项目
2. 对每个项目的 readful_result 目录中的文件
3. 找到对应的 ground_truth（从 dataset/project_code/{project}/FUN/{case}.st）
4. 用 ground_truth 的内容覆盖 readful_result 中的文件
"""

import sys
from pathlib import Path
import json

# 设置输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 基础目录
TARGET_DIR = Path(r"D:\graduate_project\项目级st补全\repo_gen_project\groud_truthcopy自project_code")
PROJECT_CODE_DIR = Path(r"D:\graduate_project\项目级st补全\repo_gen_project\dataset\project_code")

def replace_with_ground_truth():
    """用 ground_truth 替换 readful_result 中的文件"""
    
    if not TARGET_DIR.exists():
        print(f"错误: 目录不存在: {TARGET_DIR}")
        return
    
    if not PROJECT_CODE_DIR.exists():
        print(f"错误: project_code目录不存在: {PROJECT_CODE_DIR}")
        return
    
    print(f"处理目录: {TARGET_DIR}")
    print("=" * 80)
    
    stats = {
        "total_subdirs": 0,
        "processed": 0,
        "skipped_no_readful_result": 0,
        "files_replaced": 0,
        "files_not_found": 0,
        "errors": 0,
        "details": []
    }
    
    # 遍历所有子目录
    for subdir in sorted(TARGET_DIR.iterdir()):
        if not subdir.is_dir():
            continue
        
        stats["total_subdirs"] += 1
        project_name = subdir.name
        
        readful_result_dir = subdir / "readful_result"
        
        # 检查 readful_result 目录是否存在
        if not readful_result_dir.exists():
            print(f"\n{project_name}: 跳过（无readful_result目录）")
            stats["skipped_no_readful_result"] += 1
            continue
        
        # 获取所有ST文件
        st_files = list(readful_result_dir.glob("*.st"))
        if not st_files:
            print(f"\n{project_name}: 跳过（readful_result目录为空）")
            continue
        
        print(f"\n{project_name}: 处理 {len(st_files)} 个文件")
        stats["processed"] += 1
        
        project_detail = {
            "project": project_name,
            "files_replaced": 0,
            "files_not_found": [],
            "files": []
        }
        
        # 处理每个文件
        for st_file in sorted(st_files):
            case_name = st_file.stem  # 文件名（不含扩展名）
            
            try:
                # 找到对应的 ground truth
                # 去掉 "repoeval_" 前缀
                dataset_project_name = project_name.replace("repoeval_", "")
                ground_truth_file = PROJECT_CODE_DIR / dataset_project_name / "FUN" / f"{case_name}.st"
                
                if not ground_truth_file.exists():
                    print(f"  [跳过] {case_name}.st (找不到ground truth: {ground_truth_file})")
                    stats["files_not_found"] += 1
                    project_detail["files_not_found"].append(case_name)
                    continue
                
                # 读取 ground truth 内容
                ground_truth_content = ground_truth_file.read_text(encoding='utf-8')
                
                # 覆盖 readful_result 中的文件
                with open(st_file, 'w', encoding='utf-8') as f:
                    f.write(ground_truth_content)
                
                stats["files_replaced"] += 1
                project_detail["files_replaced"] += 1
                project_detail["files"].append(case_name)
                print(f"  [替换] {case_name}.st")
                
            except Exception as e:
                print(f"  [错误] {case_name}.st: {e}")
                stats["errors"] += 1
                project_detail["files"].append({
                    "filename": case_name,
                    "status": "error",
                    "error": str(e)
                })
        
        stats["details"].append(project_detail)
    
    # 打印统计信息
    print("\n" + "=" * 80)
    print("处理完成！统计信息：")
    print("=" * 80)
    print(f"总子目录数:              {stats['total_subdirs']}")
    print(f"已处理:                  {stats['processed']}")
    print(f"跳过（无readful_result）: {stats['skipped_no_readful_result']}")
    print(f"文件已替换:              {stats['files_replaced']}")
    print(f"文件未找到:              {stats['files_not_found']}")
    print(f"错误数:                  {stats['errors']}")
    print("=" * 80)
    
    # 保存详细结果
    output_file = TARGET_DIR.parent / "replace_ground_truth_log.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细日志已保存到: {output_file}")

if __name__ == "__main__":
    replace_with_ground_truth()

