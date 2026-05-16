import os
import json
import re
import shutil
from datetime import datetime
from codebleu import calc_codebleu
import editdistance
from pathlib import Path
from typing import List, Dict, Tuple
from fnmatch import fnmatch


# def extract_code_from_generation(text: str) -> str:
#     """从生成的文本中提取代码块"""
#     if not text or not isinstance(text, str):
#         return ""
    
#     # 尝试从markdown代码块中提取
#     CODE_BLOCK_PATTERN = r"```(?:\w*)?\n(.*?)\n```"
#     match = re.findall(CODE_BLOCK_PATTERN, text, flags=re.DOTALL)
#     if match:
#         return match[0]
#     # 如果没有代码块，返回原始文本
#     return text


def compute_edit_distance(reference: str, prediction: str) -> Tuple[int, float, float]:
    """计算编辑距离和相似度"""
    if not reference:
        reference = ""
    if not prediction:
        prediction = ""
    
    edit_dist = editdistance.eval(reference, prediction)
    max_len = max(len(reference), len(prediction))
    normalized_edit_dist = edit_dist / max_len if max_len > 0 else 0.0
    edit_similarity = 1 - normalized_edit_dist
    
    return edit_dist, normalized_edit_dist, edit_similarity


def evaluate_single_case(prediction: str, reference: str, lang: str = "python") -> Dict:
    """评估单个case的codebleu和编辑距离"""
    # 提取代码
    # pred_code = extract_code_from_generation(prediction)
    pred_code = prediction
    ref_code = reference
    
    # 计算CodeBLEU
    # print("定义部分 + 生成代码:\n")
    # print(pred_code)
    # print("\n\n\n参考代码:\n")
    # print(ref_code)



    try:
        codebleu_result = calc_codebleu(
            [ref_code],
            [pred_code],
            lang=lang,
            weights=(0.25, 0.25, 0.25, 0.25),
            tokenizer=None
        )
        codebleu_score = codebleu_result.get('codebleu', 0.0)
    except Exception as e:
        print(f"  Warning: CodeBLEU calculation failed: {e}")
        codebleu_score = 0.0
        codebleu_result = {}
    
    # 计算编辑距离
    edit_dist, normalized_edit_dist, edit_similarity = compute_edit_distance(ref_code, pred_code)
    
    return {
        'codebleu': codebleu_score,
        'codebleu_details': codebleu_result,
        'edit_distance': edit_dist,
        'normalized_edit_distance': normalized_edit_dist,
        'edit_similarity': edit_similarity,
        'reference_length': len(ref_code),
        'prediction_length': len(pred_code)
    }


def process_project(project_dir: Path) -> Dict:
    """处理单个项目的所有cases"""
    project_name = project_dir.name
    print(f"\n{'='*80}")
    print(f"处理项目: {project_name}")
    print(f"{'='*80}")
    
    # 文件路径
    generations_file = project_dir / "generations_repoeval-function_repoeval-function.json"
    results_file = project_dir / "results.jsonl"
    
    # 检查文件是否存在
    if not generations_file.exists():
        print(f"  跳过: {generations_file} 不存在")
        return None
    
    if not results_file.exists():
        print(f"  跳过: {results_file} 不存在")
        return None
    
    # 读取generations文件
    try:
        with open(generations_file, 'r', encoding='utf-8') as f:
            generations_data = json.load(f)
    except Exception as e:
        print(f"  错误: 无法读取 {generations_file}: {e}")
        return None
    
    # 读取results.jsonl
    references = []
    prompts = []
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line.strip())
                    ground_truth = data.get('metadata', {}).get('ground_truth', '')
                    references.append(ground_truth)
                    prompt = data.get('prompt', '')
                    prompts.append(prompt)
    except Exception as e:
        print(f"  错误: 无法读取 {results_file}: {e}")
        return None
    
    # 提取predictions
    predictions = []
    for gen_list in generations_data:
        if gen_list and len(gen_list) > 0:
            # 取第一个生成结果
            predictions.append(gen_list[0])
        else:
            predictions.append("")
    
    # 确保数量一致
    min_len = min(len(predictions), len(references), len(prompts))
    predictions = predictions[:min_len]
    references = references[:min_len]
    prompts = prompts[:min_len]
    
    if min_len == 0:
        print(f"  警告: 没有找到有效的cases")
        return None
    
    print(f"  找到 {min_len} 个cases")
    
    # 评估每个case
    case_results = []
    total_codebleu = 0.0
    total_edit_distance = 0
    total_edit_similarity = 0.0
    
    for idx, (pred, ref, prompt) in enumerate(zip(predictions, references, prompts)):
        print(f"  处理 case {idx + 1}/{min_len}...", end=' ')
        prefixed_pred = f"{prompt}\n{pred}" if prompt else pred
        result = evaluate_single_case(prefixed_pred, ref)
        case_results.append(result)
        
        total_codebleu += result['codebleu']
        total_edit_distance += result['edit_distance']
        total_edit_similarity += result['edit_similarity']
        
        print(f"CodeBLEU: {result['codebleu']:.4f}, ES: {result['edit_similarity']:.4f}")
    
    # 计算平均值
    avg_codebleu = total_codebleu / min_len
    avg_edit_distance = total_edit_distance / min_len
    avg_edit_similarity = total_edit_similarity / min_len
    
    project_result = {
        'project_name': project_name,
        'num_cases': min_len,
        'average_codebleu': avg_codebleu,
        'average_edit_distance': avg_edit_distance,
        'average_edit_similarity': avg_edit_similarity,
        'case_results': case_results
    }
    
    print(f"\n  项目统计:")
    print(f"    平均 CodeBLEU: {avg_codebleu:.4f}")
    print(f"    平均编辑距离: {avg_edit_distance:.2f}")
    print(f"    平均编辑相似度 (ES): {avg_edit_similarity:.4f}")
    
    return project_result


def main():
    """主函数：处理所有项目"""
    import argparse
    from datetime import datetime
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="CodeBLEU评估脚本")
    parser.add_argument(
        "--result_dir",
        type=str,
        default=None,
        help="Directory name under codesys_result to read results. If not provided, will use timestamp."
    )
    parser.add_argument(
        "--project",
        action="append",
        help=(
            "只评估指定项目，可传多次，格式是 codesys_result/<result_dir>/repoeval_xxx "
            "中的目录名。多个项目时重复此参数即可。"
        ),
    )
    parser.add_argument(
        "--project-pattern",
        type=str,
        help=(
            "（可选）用 glob 模式筛选项目目录，"
            "例如 --project-pattern 'repoeval_2025*'。"
        ),
    )
    args = parser.parse_args()
    
    # 基础目录
    base_codesys_result = Path("/root/code_rag_bench/code-rag-bench/codesys_result")
    
    # 确定结果目录名称：如果提供了 --result_dir 则使用它，否则尝试查找最新的目录
    if args.result_dir:
        result_dir_name = args.result_dir
    else:
        # 如果没有提供 result_dir，尝试查找最新的目录
        if base_codesys_result.exists():
            all_dirs = [d for d in base_codesys_result.iterdir() 
                       if d.is_dir() and not d.name.startswith('.')]
            if all_dirs:
                # 按修改时间排序，取最新的
                all_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                result_dir_name = all_dirs[0].name
                print(f"未指定 --result_dir，使用最新的目录: {result_dir_name}")
            else:
                result_dir_name = datetime.now().strftime("%Y%m%d_%H%M%S")
                print(f"未指定 --result_dir 且未找到现有目录，使用时间戳: {result_dir_name}")
        else:
            result_dir_name = datetime.now().strftime("%Y%m%d_%H%M%S")
            print(f"未指定 --result_dir，使用时间戳: {result_dir_name}")
    
    # 构建基础目录路径
    base_dir = base_codesys_result / result_dir_name
    
    if not base_dir.exists():
        print(f"错误: 目录不存在: {base_dir}")
        print(f"提示: 请使用 --result_dir 参数指定正确的结果目录")
        print(f"可用的目录:")
        if base_codesys_result.exists():
            for d in sorted(base_codesys_result.iterdir()):
                if d.is_dir() and not d.name.startswith('.'):
                    print(f"  - {d.name}")
        return
    
    # 获取所有项目目录
    project_dirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith('repoeval_')]
    project_dirs.sort()

    if args.project:
        project_set = set(args.project)
        project_dirs = [d for d in project_dirs if d.name in project_set]

    if args.project_pattern:
        project_dirs = [d for d in project_dirs if fnmatch(d.name, args.project_pattern)]
    
    print(f"找到 {len(project_dirs)} 个项目")
    
    # 处理所有项目
    all_project_results = []
    total_cases = 0
    total_codebleu = 0.0
    total_edit_distance = 0
    total_edit_similarity = 0.0
    
    for project_dir in project_dirs:
        result = process_project(project_dir)
        if result:
            all_project_results.append(result)
            total_cases += result['num_cases']
            total_codebleu += result['average_codebleu'] * result['num_cases']
            total_edit_distance += result['average_edit_distance'] * result['num_cases']
            total_edit_similarity += result['average_edit_similarity'] * result['num_cases']
    
    # 计算总体统计
    if total_cases > 0:
        overall_codebleu = total_codebleu / total_cases
        overall_edit_distance = total_edit_distance / total_cases
        overall_edit_similarity = total_edit_similarity / total_cases
    else:
        overall_codebleu = 0.0
        overall_edit_distance = 0.0
        overall_edit_similarity = 0.0
    
    # 打印最终统计
    print(f"\n{'='*80}")
    print("最终统计结果")
    print(f"{'='*80}")
    print(f"总项目数: {len(all_project_results)}")
    print(f"总cases数: {total_cases}")
    print(f"总体平均 CodeBLEU: {overall_codebleu:.4f}")
    print(f"总体平均编辑距离: {overall_edit_distance:.2f}")
    print(f"总体平均编辑相似度 (ES): {overall_edit_similarity:.4f}")
    print(f"{'='*80}")
    
    # 保存详细结果
    output_file = base_dir / "evaluation_summary.json"
    summary = {
        'overall_statistics': {
            'num_projects': len(all_project_results),
            'total_cases': total_cases,
            'overall_codebleu': overall_codebleu,
            'overall_edit_distance': overall_edit_distance,
            'overall_edit_similarity': overall_edit_similarity
        },
        'project_results': all_project_results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n详细结果已保存到: {output_file}")
    
    # 归档评估结果到 evaluate_result 目录
    try:
        # 创建 evaluate_result 目录
        evaluate_result_dir = Path("/root/code-rag-bench/codebleu/evaluate_result")
        evaluate_result_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamp_dir = evaluate_result_dir / timestamp
        timestamp_dir.mkdir(parents=True, exist_ok=True)
        
        # 复制 result_dir 目录到时间戳目录（base_dir 就是 result_dir）
        dest_result_dir = timestamp_dir / result_dir_name
        if dest_result_dir.exists():
            shutil.rmtree(dest_result_dir)
        shutil.copytree(base_dir, dest_result_dir)
        
        # 复制 evaluation_summary.json 到时间戳目录
        dest_summary = timestamp_dir / "evaluation_summary.json"
        shutil.copy2(output_file, dest_summary)
        
        print(f"\n评估结果已归档到: {timestamp_dir}")
        print(f"  - {result_dir_name} 目录已复制")
        print(f"  - evaluation_summary.json 已复制")
    except Exception as e:
        print(f"\n警告: 归档评估结果时出错: {e}")
    
    return summary


if __name__ == "__main__":
    main()
