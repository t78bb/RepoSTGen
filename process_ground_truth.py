#!/usr/bin/env python3
"""
处理 ground_truth 目录下的 generations 文件
仿照 full_process 中的 readful_result 处理逻辑
并添加 provide_code 到文件头部
"""

import sys
import json
from pathlib import Path
from types import SimpleNamespace

# 添加 generator 目录到路径
sys.path.insert(0, str(Path(__file__).parent / "generator"))

from process_generations import process_project


def get_original_project_name(dir_name: str) -> str:
    """
    从目录名提取原始项目名
    repoevalreadwriteFile -> repoeval_readwriteFile
    """
    # 如果目录名是 repoevalXXX 格式，转换为 repoeval_XXX
    if dir_name.startswith("repoeval") and not dir_name.startswith("repoeval_"):
        return "repoeval_" + dir_name[8:]  # 添加下划线
    return dir_name


def add_provide_code_to_st_files(ground_truth_dir: Path, readful_result_dir: Path) -> bool:
    """
    为 readful_result 目录中的每个 ST 文件添加 provide_code 到头部
    
    参数:
        ground_truth_dir: ground_truth 子目录路径
        readful_result_dir: readful_result 目录路径
    
    返回:
        是否处理成功
    """
    # 获取原始项目名
    dir_name = ground_truth_dir.name
    project_name = get_original_project_name(dir_name)
    
    # dataset/query 目录
    query_dir = Path(__file__).parent / "dataset" / "query" / project_name
    
    if not query_dir.exists():
        print(f"  ⚠️  未找到对应的 query 目录: {query_dir}")
        return False
    
    print(f"\n  添加 provide_code 到文件头部...")
    print(f"  Query 目录: {query_dir.name}")
    
    # 获取所有 ST 文件
    st_files = list(readful_result_dir.glob("*.st"))
    
    if not st_files:
        print(f"  ⚠️  readful_result 目录中没有 ST 文件")
        return False
    
    success_count = 0
    
    for st_file in sorted(st_files):
        # 获取文件名（不含扩展名）
        file_stem = st_file.stem
        
        # 在 query 目录中查找对应的 JSON 文件
        json_file = query_dir / f"{file_stem}.json"
        
        if not json_file.exists():
            print(f"    ⚠️  {file_stem}.st: 未找到对应的 JSON 文件")
            continue
        
        try:
            # 读取 JSON 文件获取 provide_code
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            provide_code = json_data.get('provide_code', '')
            
            if not provide_code:
                print(f"    ⚠️  {file_stem}.st: JSON 文件中没有 provide_code 字段")
                continue
            
            # 读取当前 ST 文件内容
            with open(st_file, 'r', encoding='utf-8') as f:
                st_content = f.read()
            
            # 拼接：provide_code + 空行 + 原内容
            new_content = f"{provide_code}\n\n{st_content}"
            
            # 写回文件
            with open(st_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"    ✅ {file_stem}.st: 已添加 provide_code ({len(provide_code)} 字符)")
            success_count += 1
            
        except Exception as e:
            print(f"    ❌ {file_stem}.st: 处理失败 - {e}")
    
    print(f"\n  完成: {success_count}/{len(st_files)} 个文件已添加 provide_code")
    
    return success_count > 0


def process_ground_truth_dir(ground_truth_dir: Path) -> bool:
    """
    处理 ground_truth 目录，生成 readful_result
    
    参数:
        ground_truth_dir: ground_truth 子目录路径
    
    返回:
        是否处理成功
    """
    print(f"\n{'='*80}")
    print(f"处理 Ground Truth 目录: {ground_truth_dir.name}")
    print(f"{'='*80}")
    
    # 检查必要文件
    generations_file = ground_truth_dir / "generations_repoeval-function_repoeval-function.json"
    results_file = ground_truth_dir / "results.jsonl"
    
    if not generations_file.exists():
        print(f"  ❌ 未找到文件: {generations_file.name}")
        return False
    
    if not results_file.exists():
        print(f"  ❌ 未找到文件: {results_file.name}")
        return False
    
    print(f"  ✓ 找到 generations 文件: {generations_file.name}")
    print(f"  ✓ 找到 results 文件: {results_file.name}")
    
    # 调用 process_project 生成 readful_result
    print(f"\n  开始处理生成结果，转换为 ST 文件...")
    
    try:
        # 创建参数对象
        process_args = SimpleNamespace(verbose=True, dry_run=False)
        
        # 调用 process_project
        process_project(ground_truth_dir, process_args, add_head=False)
        
        # 检查 readful_result 目录是否创建成功
        readful_result_dir = ground_truth_dir / "readful_result"
        
        if readful_result_dir.exists():
            st_files = list(readful_result_dir.glob("*.st"))
            print(f"\n  ✅ 成功生成 readful_result 目录")
            print(f"     包含 {len(st_files)} 个 ST 文件:")
            for st_file in sorted(st_files):
                print(f"       - {st_file.name}")
            
            # 添加 provide_code 到每个 ST 文件头部
            #add_success = add_provide_code_to_st_files(ground_truth_dir, readful_result_dir)
            
            # if add_success:
            #     print(f"\n  ✅ 处理完成")
            # else:
            #     print(f"\n  ⚠️  provide_code 添加未完全成功")
            
            return True
        else:
            print(f"\n  ⚠️  警告: readful_result 目录未创建")
            return False
            
    except Exception as e:
        print(f"\n  ❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="处理 ground_truth 目录下的 generations 文件")
    parser.add_argument(
        "--dir",
        type=str,
        default="ground_truth",
        help="要处理的目录路径（例如：ground_truth, after_gen_gt）"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="处理指定目录下的所有子目录"
    )
    
    args = parser.parse_args()
    
    # 获取项目根目录
    repo_root = Path(__file__).parent
    
    if args.all:
        # 处理指定目录下的所有子目录
        target_root = repo_root / args.dir
        
        if not target_root.exists():
            print(f"❌ 目录不存在: {target_root}")
            return 1
        
        # 获取所有子目录
        subdirs = [d for d in target_root.iterdir() if d.is_dir()]
        
        if not subdirs:
            print(f"❌ 目录下没有子目录: {target_root}")
            return 1
        
        print(f"\n找到 {len(subdirs)} 个子目录")
        
        success_count = 0
        for subdir in sorted(subdirs):
            if process_ground_truth_dir(subdir):
                success_count += 1
        
        print(f"\n{'='*80}")
        print(f"处理完成: 成功 {success_count}/{len(subdirs)}")
        print(f"{'='*80}")
        
        return 0 if success_count == len(subdirs) else 1
    
    else:
        # 处理单个目录
        target_dir = repo_root / args.dir
        
        if not target_dir.exists():
            print(f"❌ 目录不存在: {target_dir}")
            print(f"\n提示: 使用 --dir [目录] --all 处理目录下的所有子目录")
            return 1
        
        if not target_dir.is_dir():
            print(f"❌ 不是目录: {target_dir}")
            return 1
        
        success = process_ground_truth_dir(target_dir)
        
        return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

