#!/usr/bin/env python3
"""
清理 stable_data_back 目录下的指定文件和目录
删除每个子目录中的：
1. readful_result 子目录
2. evaluation_results.json 文件
3. generations_repoeval-function_repoeval-function.json 文件
"""
import os
import shutil
from pathlib import Path

def clean_stable_data_back(base_dir: str = r"D:\graduate_project\项目级st补全\repo_gen_project\output\stable_data_back"):
    """
    清理 stable_data_back 目录下的指定文件和目录
    
    Args:
        base_dir: 要清理的基础目录路径（可以是绝对路径或相对路径）
    """
    # 判断是绝对路径还是相对路径
    base_path = Path(base_dir)
    if base_path.is_absolute():
        target_dir = base_path
    else:
        script_dir = Path(__file__).resolve().parent
        target_dir = script_dir / base_dir
    
    if not target_dir.exists():
        print(f"错误: 目录不存在: {target_dir}")
        return
    
    if not target_dir.is_dir():
        print(f"错误: {target_dir} 不是一个目录")
        return
    
    print(f"开始清理目录: {target_dir}")
    print("=" * 80)
    
    # 获取所有子目录
    subdirs = [d for d in target_dir.iterdir() if d.is_dir()]
    
    if not subdirs:
        print(f"警告: {target_dir} 下没有子目录")
        return
    
    print(f"找到 {len(subdirs)} 个子目录")
    print()
    
    deleted_count = {
        "readful_result": 0,
        "evaluation_results.json": 0,
        "generations_repoeval-function_repoeval-function.json": 0
    }
    
    # 遍历每个子目录
    for subdir in subdirs:
        print(f"处理子目录: {subdir.name}")
        
        # 1. 删除 readful_result 目录
        readful_result_dir = subdir / "readful_result"
        if readful_result_dir.exists() and readful_result_dir.is_dir():
            try:
                shutil.rmtree(readful_result_dir)
                print(f"  ✓ 已删除: readful_result/")
                deleted_count["readful_result"] += 1
            except Exception as e:
                print(f"  ✗ 删除失败: readful_result/ - {e}")
        
        # 2. 删除 evaluation_results.json
        eval_json = subdir / "evaluation_results.json"
        if eval_json.exists() and eval_json.is_file():
            try:
                eval_json.unlink()
                print(f"  ✓ 已删除: evaluation_results.json")
                deleted_count["evaluation_results.json"] += 1
            except Exception as e:
                print(f"  ✗ 删除失败: evaluation_results.json - {e}")
        
        # 3. 删除 generations_repoeval-function_repoeval-function.json
        gen_json = subdir / "generations_repoeval-function_repoeval-function.json"
        if gen_json.exists() and gen_json.is_file():
            try:
                gen_json.unlink()
                print(f"  ✓ 已删除: generations_repoeval-function_repoeval-function.json")
                deleted_count["generations_repoeval-function_repoeval-function.json"] += 1
            except Exception as e:
                print(f"  ✗ 删除失败: generations_repoeval-function_repoeval-function.json - {e}")
        
        print()
    
    # 输出统计信息
    print("=" * 80)
    print("清理完成！统计信息:")
    print(f"  删除的 readful_result 目录数: {deleted_count['readful_result']}")
    print(f"  删除的 evaluation_results.json 文件数: {deleted_count['evaluation_results.json']}")
    print(f"  删除的 generations_repoeval-function_repoeval-function.json 文件数: {deleted_count['generations_repoeval-function_repoeval-function.json']}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="清理 stable_data_back 目录下的指定文件和目录")
    parser.add_argument(
        "--dir",
        type=str,
        default=r"D:\graduate_project\项目级st补全\repo_gen_project\output\stable_data_back",
        help="要清理的目录路径（可以是绝对路径或相对路径）"
    )
    args = parser.parse_args()
    
    clean_stable_data_back(args.dir)

