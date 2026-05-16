"""
CodeBLEU 评估器
用于评估生成代码与参考代码的相似度
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

# 添加 codebleu-main 到路径
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "codebleu-main"))

from codebleu import calc_codebleu


def get_original_project_name(repoeval_name: str) -> str:
    """
    从 repoeval_ 前缀的名称中提取原始项目名
    
    例如: repoeval_three-axis_CNC_motion -> three-axis_CNC_motion
          repoeval_readwriteFile -> readwriteFile
    """
    if repoeval_name.startswith("repoeval_"):
        return repoeval_name[len("repoeval_"):]
    return repoeval_name


def find_ground_truth_file(original_project_name: str, generated_filename: str, use_project_code: bool = False) -> Optional[Path]:
    """
    查找参考文件
    
    参数:
        original_project_name: 原始项目名（不含 repoeval_ 前缀）
        generated_filename: 生成的文件名
        use_project_code: 是否使用 project_code 目录（开关）
            - False（默认）: 使用 generation_context_ground_truth
            - True: 使用 project_code/[项目名]/FUN/
    
    返回:
        参考文件的路径，如果不存在则返回 None
    """
    if use_project_code:
        # 使用 project_code/[项目名]/FUN/ 路径（旧逻辑）
        dataset_base = REPO_ROOT / "dataset" / "project_code"
        project_dir = dataset_base / original_project_name
        
        if not project_dir.exists():
            return None
        
        # 在 FUN 目录下查找文件
        fun_dir = project_dir / "FUN"
        if not fun_dir.exists():
            return None
        
        ground_truth_file = fun_dir / generated_filename
        if ground_truth_file.exists():
            return ground_truth_file
    else:
        # 使用 generation_context_ground_truth 路径（新逻辑，默认）
        dataset_base = REPO_ROOT / "dataset" / "generation_context_ground_truth"
        project_dir = dataset_base / original_project_name
        
        if not project_dir.exists():
            return None
        
        # 直接在项目目录下查找文件
        ground_truth_file = project_dir / generated_filename
        if ground_truth_file.exists():
            return ground_truth_file
    
    return None


def evaluate_project_codebleu(
    project_dir: Path,
    lang: str = "python",
    weights: tuple = (0.25, 0.25, 0.25, 0.25),
    use_project_code: bool = False,
    readful_result_subdir: str = "readful_result"
) -> Optional[Dict]:
    """
    评估单个项目的 CodeBLEU 分数
    
    参数:
        project_dir: 项目目录路径（包含 readful_result/ 子目录）
        lang: 编程语言（默认 python，用于 ST 代码的近似评估）
        weights: CodeBLEU 各部分权重 (ngram, weighted_ngram, syntax, dataflow)
        use_project_code: 是否使用 project_code 作为参考（默认 False）
            - False: 使用 generation_context_ground_truth（默认）
            - True: 使用 project_code/[项目名]/FUN/
        readful_result_subdir: 要评估的代码子目录名（默认 "readful_result"）
            - "readful_result": 完整代码（包含 provide_code）
            - "readful_result_no_provide": 去除 provide_code 的代码
    
    返回:
        包含评估结果的字典，如果评估失败则返回 None
    """
    
    # 检查指定的代码目录是否存在
    readful_result_dir = project_dir / readful_result_subdir
    print(readful_result_dir)
    if not readful_result_dir.exists():
        print(f"  ⚠️  跳过评估: 未找到 {readful_result_subdir} 目录")
        return None
    
    # 获取原始项目名
    project_name = project_dir.name
    original_project_name = get_original_project_name(project_name)
    
    print(f"  项目名称: {project_name}")
    print(f"  原始项目: {original_project_name}")
    
    try:
        # 获取所有生成的 .st 文件
        generated_files = list(readful_result_dir.glob("*.st"))
        
        if not generated_files:
            print(f"  ⚠️  警告: readful_result 目录中没有找到 .st 文件")
            return None
        
        print(f"  📊 找到 {len(generated_files)} 个生成的 .st 文件，开始评估...")
        
        # 逐个评估每个文件
        case_results = []
        total_codebleu = 0.0
        total_ngram = 0.0
        total_weighted_ngram = 0.0
        total_syntax = 0.0
        total_dataflow = 0.0
        successful_cases = 0
        
        for idx, generated_file in enumerate(sorted(generated_files)):
            filename = generated_file.name
            print(f"\n    [{idx + 1}/{len(generated_files)}] 评估 {filename}...", end=' ')
            
            # 查找对应的参考文件
            ground_truth_file = find_ground_truth_file(original_project_name, filename, use_project_code)
            
            if ground_truth_file is None:
                print(f"❌ 未找到参考文件")
                case_results.append({
                    'filename': filename,
                    'case_id': idx,
                    'error': '未找到对应的参考文件'
                })
                continue
            
            # 读取生成代码和参考代码
            try:
                with open(generated_file, 'r', encoding='utf-8') as f:
                    generated_code = f.read()
                
                with open(ground_truth_file, 'r', encoding='utf-8') as f:
                    reference_code = f.read()
                
                # 计算 CodeBLEU
                result = calc_codebleu(
                    [reference_code],
                    [generated_code],
                    lang=lang,
                    weights=weights,
                    tokenizer=None
                )
                
                case_result = {
                    'filename': filename,
                    'case_id': idx,
                    'ground_truth_path': str(ground_truth_file),
                    'codebleu': result['codebleu'],
                    'ngram_match_score': result['ngram_match_score'],
                    'weighted_ngram_match_score': result['weighted_ngram_match_score'],
                    'syntax_match_score': result['syntax_match_score'],
                    'dataflow_match_score': result['dataflow_match_score'],
                    'reference_length': len(reference_code),
                    'prediction_length': len(generated_code)
                }
                
                case_results.append(case_result)
                
                total_codebleu += result['codebleu']
                total_ngram += result['ngram_match_score']
                total_weighted_ngram += result['weighted_ngram_match_score']
                total_syntax += result['syntax_match_score']
                total_dataflow += result['dataflow_match_score']
                successful_cases += 1
                
                print(f"✅ CodeBLEU={result['codebleu']:.4f}")
                
            except Exception as e:
                print(f"❌ 评估失败: {e}")
                case_results.append({
                    'filename': filename,
                    'case_id': idx,
                    'error': str(e)
                })
        
        if successful_cases == 0:
            print(f"\n  ⚠️  警告: 没有成功评估的文件")
            return None
        
        # 计算平均值
        avg_codebleu = total_codebleu / successful_cases
        avg_ngram = total_ngram / successful_cases
        avg_weighted_ngram = total_weighted_ngram / successful_cases
        avg_syntax = total_syntax / successful_cases
        avg_dataflow = total_dataflow / successful_cases
        
        # 构建评估结果
        evaluation_result = {
            'project_name': project_name,
            'original_project_name': original_project_name,
            'total_files': len(generated_files),
            'successful_evaluations': successful_cases,
            'language': lang,
            'weights': weights,
            'average_scores': {
                'codebleu': avg_codebleu,
                'ngram_match_score': avg_ngram,
                'weighted_ngram_match_score': avg_weighted_ngram,
                'syntax_match_score': avg_syntax,
                'dataflow_match_score': avg_dataflow
            },
            'file_results': case_results
        }
        
        print(f"\n  ✅ 评估完成:")
        print(f"     成功评估: {successful_cases}/{len(generated_files)} 个文件")
        print(f"     平均 CodeBLEU: {avg_codebleu:.4f}")
        print(f"     N-gram 匹配:   {avg_ngram:.4f}")
        print(f"     语法树匹配:    {avg_syntax:.4f}")
        print(f"     数据流匹配:    {avg_dataflow:.4f}")
        
        return evaluation_result
        
    except Exception as e:
        print(f"  ❌ 评估出错: {e}")
        import traceback
        traceback.print_exc()
        return None


def save_evaluation_result(evaluation_result: Dict, output_path: Path) -> bool:
    """
    保存评估结果到 JSON 文件
    
    参数:
        evaluation_result: 评估结果字典
        output_path: 输出文件路径
    
    返回:
        是否保存成功
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(evaluation_result, f, indent=2, ensure_ascii=False)
        print(f"  💾 评估结果已保存到: {output_path}")
        return True
    except Exception as e:
        print(f"  ❌ 保存评估结果失败: {e}")
        return False


def evaluate_and_save(
    project_dir: Path,
    output_filename: str = "codebleu_evaluation.json",
    lang: str = "python",
    use_project_code: bool = False,
    readful_result_subdir: str = "readful_result"
) -> bool:
    """
    评估项目并保存结果
    
    参数:
        project_dir: 项目目录
        output_filename: 输出文件名
        lang: 编程语言
        use_project_code: 是否使用 project_code 作为参考（默认 False）
            - False: 使用 generation_context_ground_truth（默认）
            - True: 使用 project_code/[项目名]/FUN/
        readful_result_subdir: 要评估的代码子目录名（默认 "readful_result"）
            - "readful_result": 完整代码（包含 provide_code）
            - "readful_result_no_provide": 去除 provide_code 的代码
    
    返回:
        是否成功
    """
    print(f"\n📊 开始评估: {project_dir.name}")
    print(f"{'='*80}")
    
    # 显示参考代码来源和评测代码来源
    if use_project_code:
        print(f"  参考代码来源: dataset/project_code/[项目名]/FUN/")
        print(f"  评测代码来源: {readful_result_subdir}/")
    else:
        print(f"  参考代码来源: dataset/generation_context_ground_truth/[项目名]/")
        print(f"  评测代码来源: {readful_result_subdir}/")
    
    # 执行评估
    result = evaluate_project_codebleu(
        project_dir, 
        lang=lang, 
        use_project_code=use_project_code,
        readful_result_subdir=readful_result_subdir
    )
    
    if result is None:
        return False
    
    # 保存结果
    output_path = project_dir / output_filename
    return save_evaluation_result(result, output_path)


if __name__ == "__main__":
    # 测试代码
    import argparse
    
    parser = argparse.ArgumentParser(description="CodeBLEU 评估工具")
    parser.add_argument("project_dir", type=str, help="项目目录路径")
    parser.add_argument("--lang", type=str, default="python", help="编程语言（默认: python）")
    parser.add_argument("--output", type=str, default="codebleu_evaluation.json", help="输出文件名")
    parser.add_argument(
        "--use_project_code_gt",
        action="store_true",
        help="使用 project_code/[项目名]/FUN/ 作为参考代码（默认使用 generation_context_ground_truth）"
    )
    
    args = parser.parse_args()
    
    project_dir = Path(args.project_dir)
    if not project_dir.exists():
        print(f"❌ 目录不存在: {project_dir}")
        sys.exit(1)
    
    success = evaluate_and_save(project_dir, args.output, args.lang, use_project_code=args.use_project_code_gt)
    sys.exit(0 if success else 1)

