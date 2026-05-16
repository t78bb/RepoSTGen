#!/usr/bin/env python3
"""
统计 query 目录下各个子目录的 JSON 文件总数
"""
import os
import sys
from pathlib import Path
from collections import defaultdict


def count_json_files_in_query_dir():
    """统计 query 目录下各个子目录的 JSON 文件总数"""
    # 获取脚本所在目录
    script_dir = Path(__file__).resolve().parent
    query_dir = script_dir / "query"
    
    # 检查目录是否存在
    if not query_dir.exists():
        print(f"错误: query 目录不存在: {query_dir}")
        sys.exit(1)
    
    # 统计结果
    stats = {}
    total_files = 0
    
    # 获取所有子目录
    subdirs = [d for d in query_dir.iterdir() if d.is_dir()]
    subdirs.sort(key=lambda x: x.name)
    
    if not subdirs:
        print(f"警告: {query_dir} 下没有子目录")
        return
    
    print("=" * 80)
    print("Query 目录 JSON 文件统计")
    print("=" * 80)
    print(f"\nQuery 目录: {query_dir}")
    print(f"子目录数量: {len(subdirs)}")
    print("\n" + "-" * 80)
    
    # 统计每个子目录的 JSON 文件数
    for subdir in subdirs:
        json_files = list(subdir.glob("*.json"))
        file_count = len(json_files)
        stats[subdir.name] = file_count
        total_files += file_count
        print(f"{subdir.name:50s} : {file_count:4d} 个文件")
    
    print("-" * 80)
    print(f"{'总计':50s} : {total_files:4d} 个文件")
    print("=" * 80)
    
    # 输出统计摘要
    print("\n统计摘要:")
    print(f"  子目录数: {len(subdirs)}")
    print(f"  总文件数: {total_files}")
    if subdirs:
        avg_files = total_files / len(subdirs)
        print(f"  平均每个子目录: {avg_files:.1f} 个文件")
        
        # 找出文件数最多和最少的子目录
        max_dir = max(stats.items(), key=lambda x: x[1])
        min_dir = min(stats.items(), key=lambda x: x[1])
        print(f"  最多文件: {max_dir[0]} ({max_dir[1]} 个)")
        print(f"  最少文件: {min_dir[0]} ({min_dir[1]} 个)")
    
    return stats


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="统计 query 目录下各个子目录的 JSON 文件总数")
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="输出统计结果到 JSON 文件（可选）"
    )
    args = parser.parse_args()
    
    # 执行统计
    stats = count_json_files_in_query_dir()
    
    # 如果指定了输出文件，保存结果
    if args.output:
        import json
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        result = {
            "total_directories": len(stats),
            "total_files": sum(stats.values()),
            "statistics": stats
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n统计结果已保存到: {output_path}")


if __name__ == "__main__":
    main()





