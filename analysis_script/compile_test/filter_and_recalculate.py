#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从编译测试结果中过滤指定项目并重新统计
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict

# 要过滤的项目名称（不含 repoeval_ 前缀）
FILTER_PROJECTS = ['can', 'healthydata', 'modbus', 'core']


def filter_projects(results: List[Dict], filter_list: List[str]) -> List[Dict]:
    """
    从结果列表中过滤掉指定的项目
    
    参数:
        results: 项目结果列表
        filter_list: 要过滤的项目名称列表（不含 repoeval_ 前缀）
    
    返回:
        过滤后的结果列表
    """
    filtered = []
    filtered_names = []
    
    for result in results:
        project_name = result.get('project_name', '')
        
        # 检查是否在过滤列表中
        should_filter = False
        for filter_name in filter_list:
            # 匹配 repoeval_xxx 或 xxx
            if project_name == f'repoeval_{filter_name}' or project_name == filter_name:
                should_filter = True
                filtered_names.append(project_name)
                break
        
        if not should_filter:
            filtered.append(result)
    
    return filtered, filtered_names


def recalculate_summary(output_results: List[Dict], gt_results: List[Dict]) -> Dict:
    """
    重新计算总体统计信息
    
    参数:
        output_results: output 结果列表
        gt_results: ground truth 结果列表
    
    返回:
        统计信息字典
    """
    all_projects = output_results + gt_results
    
    total_files = sum(r.get("total_files", 0) for r in all_projects)
    total_passed = sum(r.get("passed_files", 0) for r in all_projects)
    total_failed = sum(r.get("failed_files", 0) for r in all_projects)
    
    overall_pass_rate = (total_passed / total_files * 100) if total_files > 0 else 0.0
    
    return {
        "total_projects": len(all_projects),
        "total_files": total_files,
        "total_passed_files": total_passed,
        "total_failed_files": total_failed,
        "overall_pass_rate": round(overall_pass_rate, 2)
    }


def main():
    parser = argparse.ArgumentParser(description="从编译测试结果中过滤指定项目并重新统计")
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="输入的 JSON 文件路径"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="输出的 JSON 文件路径（可选，默认添加 _filtered 后缀）"
    )
    parser.add_argument(
        "--filter",
        type=str,
        nargs='+',
        default=FILTER_PROJECTS,
        help=f"要过滤的项目名称列表（默认：{' '.join(FILTER_PROJECTS)}）"
    )
    
    args = parser.parse_args()
    
    # 读取输入文件
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"错误: 输入文件不存在 - {input_file}")
        return 1
    
    print(f"读取文件: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n原始统计:")
    print(f"  output_results: {len(data.get('output_results', []))} 个项目")
    print(f"  ground_truth_results: {len(data.get('ground_truth_results', []))} 个项目")
    
    # 过滤项目
    filter_list = args.filter
    print(f"\n过滤项目: {', '.join([f'repoeval_{name}' for name in filter_list])}")
    
    output_results = data.get('output_results', [])
    gt_results = data.get('ground_truth_results', [])
    
    filtered_output, filtered_output_names = filter_projects(output_results, filter_list)
    filtered_gt, filtered_gt_names = filter_projects(gt_results, filter_list)
    
    all_filtered_names = filtered_output_names + filtered_gt_names
    
    if all_filtered_names:
        print(f"\n已过滤的项目:")
        for name in all_filtered_names:
            print(f"  - {name}")
    else:
        print(f"\n未找到需要过滤的项目")
    
    # 重新计算统计
    new_summary = recalculate_summary(filtered_output, filtered_gt)
    
    print(f"\n过滤后统计:")
    print(f"  output_results: {len(filtered_output)} 个项目")
    print(f"  ground_truth_results: {len(filtered_gt)} 个项目")
    print(f"  总项目数: {new_summary['total_projects']}")
    print(f"  总文件数: {new_summary['total_files']}")
    print(f"  通过文件数: {new_summary['total_passed_files']}")
    print(f"  失败文件数: {new_summary['total_failed_files']}")
    print(f"  总体通过率: {new_summary['overall_pass_rate']}%")
    
    # 构建新的数据
    new_data = {
        "test_time": data.get("test_time", ""),
        "filtered_projects": all_filtered_names,
        "output_results": filtered_output,
        "ground_truth_results": filtered_gt,
        "summary": new_summary
    }
    
    # 确定输出文件路径
    if args.output:
        output_file = Path(args.output)
    else:
        # 自动生成文件名
        output_file = input_file.parent / f"{input_file.stem}_filtered{input_file.suffix}"
    
    # 保存结果
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到: {output_file}")
    
    return 0


if __name__ == "__main__":
    exit(main())

