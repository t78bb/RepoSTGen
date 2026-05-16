#!/usr/bin/env python3
"""
评估 ground_truth 目录下的 CodeBLEU 结果
仿照 full_process.py 的调用方式

参考代码来源: dataset/generation_context_ground_truth/[项目名]/*.st
生成代码来源: ground_truth/[项目目录]/readful_result/*.st
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# 添加 evaluate 目录到路径
sys.path.insert(0, str(Path(__file__).parent / "evaluate"))

from codebleu_evaluator import evaluate_and_save


def evaluate_ground_truth_project(project_dir: Path, lang: str = "python", use_project_code: bool = False) -> bool:
    """
    评估单个 ground_truth 项目的 CodeBLEU
    
    参数:
        project_dir: ground_truth 子目录路径
        lang: 编程语言（默认 python）
        use_project_code: 是否使用 project_code 作为参考（默认 False）
            - False: 使用 generation_context_ground_truth（默认）
            - True: 使用 project_code/[项目名]/FUN/
    
    返回:
        是否评估成功
    """
    print(f"\n{'='*80}")
    print(f"评估项目: {project_dir.name}")
    print(f"{'='*80}")
    
    # 检查 readful_result 目录是否存在
    readful_result_dir = project_dir / "readful_result"
    
    if not readful_result_dir.exists():
        print(f"  ⚠️  跳过: 未找到 readful_result 目录")
        return False
    
    # 检查是否有 ST 文件
    st_files = list(readful_result_dir.glob("*.st"))
    if not st_files:
        print(f"  ⚠️  跳过: readful_result 目录中没有 ST 文件")
        return False
    
    print(f"  ✓ 找到 {len(st_files)} 个 ST 文件")
    
    # 调用 evaluate_and_save 进行评估
    try:
        eval_success = evaluate_and_save(
            project_dir,
            output_filename="codebleu_evaluation.json",
            lang=lang,
            use_project_code=use_project_code
        )
        
        if eval_success:
            # 读取并显示评估结果摘要
            eval_file = project_dir / "codebleu_evaluation.json"
            if eval_file.exists():
                with open(eval_file, 'r', encoding='utf-8') as f:
                    result = json.load(f)
                
                print(f"\n  📊 评估摘要:")
                print(f"     项目名称: {result['project_name']}")
                print(f"     原始项目: {result['original_project_name']}")
                print(f"     评估文件数: {result['successful_evaluations']}/{result['total_files']}")
                print(f"     平均 CodeBLEU: {result['average_scores']['codebleu']:.4f}")
                
                print(f"\n  💾 结果已保存: {eval_file}")
            
            return True
        else:
            print(f"  ⚠️  评估未完成")
            return False
            
    except Exception as e:
        print(f"  ❌ 评估出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数：评估 ground_truth 目录下的所有项目"""
    import argparse
    
    parser = argparse.ArgumentParser(description="评估目录下的 CodeBLEU 结果")
    parser.add_argument(
        "--dir",
        type=str,
        default="ground_truth",
        help="指定要评估的目录路径（例如: ground_truth, after_gen_gt, ground_truth/repoeval_readwriteFile）"
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="python",
        help="编程语言（默认: python，用于 ST 代码的近似评估）"
    )
    parser.add_argument(
        "--use_project_code_gt",
        action="store_true",
        help="使用 project_code/[项目名]/FUN/ 作为参考代码（默认使用 generation_context_ground_truth）"
    )
    
    args = parser.parse_args()
    
    # 获取项目根目录
    repo_root = Path(__file__).parent
    target_root = repo_root / args.dir
    
    if not target_root.exists():
        print(f"❌ 目录不存在: {target_root}")
        return 1
    
    print("="*80)
    print("CodeBLEU 评估")
    print("="*80)
    print(f"目标目录: {target_root}")
    
    # 显示参考代码来源
    if args.use_project_code_gt:
        print(f"参考代码来源: dataset/project_code/[项目名]/FUN/")
    else:
        print(f"参考代码来源: dataset/generation_context_ground_truth/[项目名]/")
    
    # 确定要评估的项目
    if target_root.is_file() or (target_root / "readful_result").exists():
        # 如果目标是单个项目目录（包含 readful_result）
        project_dirs = [target_root]
        print(f"\n评估单个项目: {target_root.name}")
    else:
        # 否则，评估目录下所有包含 readful_result 的子目录
        project_dirs = [
            d for d in target_root.iterdir()
            if d.is_dir() and (d / "readful_result").exists()
        ]
        
        if not project_dirs:
            print(f"\n❌ ground_truth 目录下没有子目录")
            return 1
        
        print(f"\n找到 {len(project_dirs)} 个项目（使用 --all 评估所有项目）")
        print(f"默认评估所有项目...")
    
    # 记录评估结果
    results = {
        "success": [],
        "failed": [],
        "skipped": []
    }
    
    # 评估统计
    evaluation_stats = {}
    
    print(f"\n开始评估...")
    print("="*80)
    
    # 对每个项目进行评估
    for idx, project_dir in enumerate(sorted(project_dirs), 1):
        project_name = project_dir.name
        
        print(f"\n[{idx}/{len(project_dirs)}] 处理项目: {project_name}")
        
        success = evaluate_ground_truth_project(project_dir, lang=args.lang, use_project_code=args.use_project_code_gt)
        
        if success:
            results["success"].append(project_name)
            
            # 读取评估结果统计
            eval_file = project_dir / "codebleu_evaluation.json"
            if eval_file.exists():
                with open(eval_file, 'r', encoding='utf-8') as f:
                    eval_data = json.load(f)
                
                avg_scores = eval_data.get("average_scores", {})
                evaluation_stats[project_name] = {
                    "total_files": eval_data.get("total_files", 0),
                    "successful_evaluations": eval_data.get("successful_evaluations", 0),
                    "average_scores": {
                        "codebleu": avg_scores.get("codebleu", 0.0),
                        "ngram_match_score": avg_scores.get("ngram_match_score", 0.0),
                        "weighted_ngram_match_score": avg_scores.get("weighted_ngram_match_score", 0.0),
                        "syntax_match_score": avg_scores.get("syntax_match_score", 0.0),
                        "dataflow_match_score": avg_scores.get("dataflow_match_score", 0.0)
                    }
                }
        else:
            results["failed"].append(project_name)
    
    # 输出总结
    print("\n" + "="*80)
    print("评估总结")
    print("="*80)
    print(f"\n总项目数: {len(project_dirs)}")
    print(f"成功: {len(results['success'])}")
    print(f"失败: {len(results['failed'])}")
    
    if results["success"]:
        print(f"\n✅ 成功评估的项目 ({len(results['success'])}):")
        for project in results["success"]:
            stats = evaluation_stats.get(project, {})
            total = stats.get("total_files", 0)
            success_count = stats.get("successful_evaluations", 0)
            avg_scores = stats.get("average_scores", {})
            print(f"  - {project}: {success_count}/{total} 文件")
            print(f"      CodeBLEU: {avg_scores.get('codebleu', 0.0):.4f}")
            print(f"      N-gram: {avg_scores.get('ngram_match_score', 0.0):.4f}, "
                  f"Weighted N-gram: {avg_scores.get('weighted_ngram_match_score', 0.0):.4f}")
            print(f"      Syntax: {avg_scores.get('syntax_match_score', 0.0):.4f}, "
                  f"Dataflow: {avg_scores.get('dataflow_match_score', 0.0):.4f}")
    
    if results["failed"]:
        print(f"\n❌ 失败的项目 ({len(results['failed'])}):")
        for project in results["failed"]:
            print(f"  - {project}")
    
    # 计算总体统计
    overall_stats = {}
    if evaluation_stats:
        total_files = sum(s["successful_evaluations"] for s in evaluation_stats.values())
        
        # 计算各项指标的加权平均
        metrics = ["codebleu", "ngram_match_score", "weighted_ngram_match_score", 
                  "syntax_match_score", "dataflow_match_score"]
        
        overall_averages = {}
        for metric in metrics:
            total_weighted_score = sum(
                s["average_scores"][metric] * s["successful_evaluations"] 
                for s in evaluation_stats.values()
            )
            overall_averages[metric] = total_weighted_score / total_files if total_files > 0 else 0.0
        
        overall_stats = {
            "total_files": total_files,
            "total_projects": len(evaluation_stats),
            "average_scores": overall_averages
        }
        
        print(f"\n{'='*80}")
        print("总体统计")
        print(f"{'='*80}")
        print(f"总项目数: {len(evaluation_stats)}")
        print(f"总文件数: {total_files}")
        print(f"\n平均分数:")
        print(f"  CodeBLEU:               {overall_averages['codebleu']:.4f}")
        print(f"  N-gram Match:           {overall_averages['ngram_match_score']:.4f}")
        print(f"  Weighted N-gram Match:  {overall_averages['weighted_ngram_match_score']:.4f}")
        print(f"  Syntax Match:           {overall_averages['syntax_match_score']:.4f}")
        print(f"  Dataflow Match:         {overall_averages['dataflow_match_score']:.4f}")
    
    # 保存总结结果
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "language": args.lang,
        "total_projects": len(project_dirs),
        "success_count": len(results["success"]),
        "failed_count": len(results["failed"]),
        "overall_statistics": overall_stats,
        "results": results,
        "project_statistics": evaluation_stats
    }
    
    # 1. 保存固定名称的文件（会覆盖旧文件，方便查找最新结果）
    fixed_summary_file = target_root / "evaluation_results.json"
    with open(fixed_summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    print(f"\n💾 评估结果已保存到: {fixed_summary_file}")
    
    # 2. 同时保存带时间戳的文件（用于历史记录）
    timestamped_summary_file = target_root / f"evaluation_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(timestamped_summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    print(f"💾 历史记录已保存到: {timestamped_summary_file}")
    
    print(f"\n{'='*80}")
    if results["failed"]:
        print("评估完成（部分失败）")
        return 1
    else:
        print("✅ 评估完成（全部成功）")
        return 0


if __name__ == "__main__":
    sys.exit(main())

