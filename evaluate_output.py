#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量评估 output 目录下项目的 CodeBLEU 脚本
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
from evaluate.codebleu_evaluator import evaluate_and_save


def main():
    parser = argparse.ArgumentParser(description="批量评估 output 目录下的项目")
    parser.add_argument(
        "--dir",
        type=str,
        required=True,
        help="output 目录路径（例如：output/20260121_155341_fixed）"
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="python",
        help="编程语言（默认：python）"
    )
    parser.add_argument(
        "--use_project_code_gt",
        action="store_true",
        help="使用 project_code/[项目名]/FUN/ 作为参考代码（默认使用 generation_context_ground_truth）"
    )
    
    args = parser.parse_args()
    
    # 获取目录
    output_dir = Path(args.dir)
    
    if not output_dir.exists():
        print(f"错误: 目录不存在 - {output_dir}")
        return 1
    
    if not output_dir.is_dir():
        print(f"错误: 不是目录 - {output_dir}")
        return 1
    
    # 查找所有项目子目录（包含 readful_result 的目录）
    project_dirs = []
    for item in output_dir.iterdir():
        if item.is_dir() and (item / "readful_result").exists():
            project_dirs.append(item)
    
    if not project_dirs:
        print(f"错误: 在 {output_dir} 下未找到包含 readful_result 的项目目录")
        return 1
    
    print("="*80)
    print("批量 CodeBLEU 评估")
    print("="*80)
    print(f"Output 目录: {output_dir}")
    print(f"找到 {len(project_dirs)} 个项目")
    
    # 根据开关选择评测策略
    if args.use_project_code_gt:
        # 开关打开：评估完整代码
        readful_result_subdir = "readful_result"
        print(f"评测模式: 完整代码评估")
        print(f"  参考代码: dataset/project_code/[项目名]/FUN/")
        print(f"  评测代码: {readful_result_subdir}/")
    else:
        # 开关关闭：评估实现逻辑
        readful_result_subdir = "readful_result_no_provide"
        print(f"评测模式: 实现逻辑评估")
        print(f"  参考代码: dataset/generation_context_ground_truth/[项目名]/")
        print(f"  评测代码: {readful_result_subdir}/")
    
    print("="*80)
    
    # 统计
    success_count = 0
    failed_count = 0
    results = []
    evaluation_stats = {}  # 用于存储每个项目的详细统计
    
    # 对每个项目进行评估
    for idx, project_dir in enumerate(sorted(project_dirs), 1):
        project_name = project_dir.name
        
        print(f"\n[{idx}/{len(project_dirs)}] 处理项目: {project_name}")
        print("-"*80)
        
        try:
            success = evaluate_and_save(
                project_dir,
                output_filename="codebleu_evaluation.json",
                lang=args.lang,
                use_project_code=args.use_project_code_gt,
                readful_result_subdir=readful_result_subdir
            )
            
            if success:
                print(f"✓ {project_name} 评估完成")
                success_count += 1
                results.append((project_name, "成功"))
                
                # 读取评估结果并收集统计信息
                eval_file = project_dir / "codebleu_evaluation.json"
                if eval_file.exists():
                    with open(eval_file, 'r', encoding='utf-8') as f:
                        eval_data = json.load(f)
                        
                        # 计算平均分数
                        file_results = eval_data.get('file_results', [])
                        if file_results:
                            avg_scores = {
                                'codebleu': 0.0,
                                'ngram_match_score': 0.0,
                                'weighted_ngram_match_score': 0.0,
                                'syntax_match_score': 0.0,
                                'dataflow_match_score': 0.0,
                            }
                            
                            for file_result in file_results:
                                avg_scores['codebleu'] += file_result.get('codebleu', 0.0)
                                avg_scores['ngram_match_score'] += file_result.get('ngram_match_score', 0.0)
                                avg_scores['weighted_ngram_match_score'] += file_result.get('weighted_ngram_match_score', 0.0)
                                avg_scores['syntax_match_score'] += file_result.get('syntax_match_score', 0.0)
                                avg_scores['dataflow_match_score'] += file_result.get('dataflow_match_score', 0.0)
                            
                            # 计算平均值
                            num_files = len(file_results)
                            for key in avg_scores:
                                avg_scores[key] /= num_files
                            
                            evaluation_stats[project_name] = {
                                'total_files': num_files,
                                'successful_evaluations': num_files,
                                'average_scores': avg_scores
                            }
            else:
                print(f"⚠ {project_name} 评估未完成")
                failed_count += 1
                results.append((project_name, "未完成"))
                
        except Exception as e:
            print(f"✗ {project_name} 评估失败: {e}")
            failed_count += 1
            results.append((project_name, f"失败: {e}"))
    
    # 计算总体统计
    overall_avg_scores = {
        "codebleu": 0.0,
        "ngram_match_score": 0.0,
        "weighted_ngram_match_score": 0.0,
        "syntax_match_score": 0.0,
        "dataflow_match_score": 0.0,
    }
    
    total_files_evaluated = sum(stats["successful_evaluations"] for stats in evaluation_stats.values())
    
    if total_files_evaluated > 0:
        # 加权平均：按每个项目的文件数量加权
        for project_name, stats in evaluation_stats.items():
            weight = stats["successful_evaluations"] / total_files_evaluated
            for metric in overall_avg_scores:
                overall_avg_scores[metric] += stats["average_scores"].get(metric, 0.0) * weight
    
    # 输出总结
    print("\n" + "="*80)
    print("评估完成")
    print("="*80)
    print(f"总计: {len(project_dirs)} 个项目")
    print(f"成功: {success_count} 个")
    print(f"失败: {failed_count} 个")
    print(f"总文件数: {total_files_evaluated}")
    print("\n平均分数:")
    for metric, score in overall_avg_scores.items():
        print(f"  {metric.replace('_', ' ').title():<30}: {score:.4f}")
    print("="*80)
    
    # 输出详细结果
    print("\n详细结果:")
    print("-"*80)
    for project_name, status in results:
        print(f"  {project_name}: {status}")
    print("="*80)
    
    # 保存总结文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 成功和失败的项目列表
    successful_projects = [name for name, status in results if status == "成功"]
    failed_projects = [name for name, status in results if status != "成功"]
    
    summary = {
        "evaluation_time": timestamp,
        "output_directory": str(output_dir),
        "evaluation_mode": "完整代码评估" if args.use_project_code_gt else "实现逻辑评估",
        "reference_source": "dataset/project_code/[项目名]/FUN/" if args.use_project_code_gt else "dataset/generation_context_ground_truth/[项目名]/",
        "evaluated_code_source": readful_result_subdir + "/",
        "total_projects": len(project_dirs),
        "successful_projects_count": success_count,
        "failed_projects_count": failed_count,
        "total_files_evaluated": total_files_evaluated,
        "overall_average_scores": overall_avg_scores,
        "successful_projects": successful_projects,
        "failed_projects": failed_projects,
        "project_details": evaluation_stats
    }
    
    # 保存两个版本：固定名称 + 带时间戳
    summary_file_fixed = output_dir / "evaluation_summary.json"
    summary_file_timestamped = output_dir / f"evaluation_summary_{timestamp}.json"
    
    for summary_file in [summary_file_fixed, summary_file_timestamped]:
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"✓ 总结文件已保存: {summary_file}")
    
    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    exit(main())


