#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
评估修复历史中每个版本的 CodeBLEU 分数
用于分析修复过程中的代码质量变化
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# 添加项目根目录和 codebleu 目录到 Python 路径
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(repo_root / "codebleu-main"))

from codebleu import calc_codebleu


def get_ground_truth_file(project_name: str, filename: str, use_project_code: bool = False) -> Path:
    """
    获取 ground truth 文件路径
    
    参数:
        project_name: 项目名称（如 repoeval_readwriteFile）
        filename: 文件名（如 ReadFile.st）
        use_project_code: 是否使用 project_code 作为参考
    
    返回:
        ground truth 文件路径
    """
    repo_root = Path(__file__).parent.parent
    
    # 去除 repoeval_ 前缀
    original_name = project_name
    if original_name.startswith('repoeval_'):
        original_name = original_name[9:]
    
    if use_project_code:
        # 使用 project_code/FUN 作为参考
        gt_path = repo_root / "dataset" / "project_code" / original_name / "FUN" / filename
    else:
        # 使用 generation_context_ground_truth 作为参考
        gt_path = repo_root / "dataset" / "generation_context_ground_truth" / original_name / filename
    
    return gt_path if gt_path.exists() else None


def extract_version_number(filename: str) -> int:
    """
    从文件名中提取版本号
    
    例如:
        ReadFile_0.st -> 0
        ReadFile_1.st -> 1
        WriteFile_2.st -> 2
    """
    stem = Path(filename).stem  # 去除扩展名
    if '_' in stem:
        parts = stem.split('_')
        try:
            return int(parts[-1])
        except ValueError:
            return -1
    return -1


def get_base_filename(history_filename: str) -> str:
    """
    从历史文件名获取基础文件名
    
    例如:
        ReadFile_0.st -> ReadFile.st
        WriteFile_2.st -> WriteFile.st
    """
    stem = Path(history_filename).stem
    if '_' in stem:
        parts = stem.split('_')
        base_name = '_'.join(parts[:-1])  # 去掉最后的版本号
        return f"{base_name}.st"
    return history_filename


def remove_declaration_part(code: str) -> str:
    """
    去除 ST 代码的声明部分，只保留实现逻辑
    
    规则:
    1. 如果找到 VAR（独立一行），从该行开始保留
    2. 如果没有 VAR，找到最后一个 END_VAR，从其后一行开始保留
    3. 如果既没有 VAR 也没有 END_VAR，保留原内容
    
    参数:
        code: 原始代码字符串
    
    返回:
        处理后的代码字符串
    """
    lines = code.splitlines()
    
    # 规则1: 查找第一个独立的 VAR 行
    var_start_index = -1
    for i, line in enumerate(lines):
        if line.strip().upper() == "VAR":
            var_start_index = i
            break
    
    if var_start_index != -1:
        # 找到了 VAR，从该行开始保留
        processed_lines = lines[var_start_index:]
    else:
        # 规则2: 没有 VAR，找最后一个 END_VAR
        last_end_var_index = -1
        for i, line in enumerate(reversed(lines)):
            if line.strip().upper() == "END_VAR":
                last_end_var_index = len(lines) - 1 - i
                break
        
        if last_end_var_index != -1:
            # 找到了 END_VAR，从其后一行开始保留
            processed_lines = lines[last_end_var_index + 1:]
        else:
            # 规则3: 既没有 VAR 也没有 END_VAR，保留原内容
            processed_lines = lines
    
    return "\n".join(processed_lines)


def evaluate_history_file(history_file: Path, gt_file: Path, lang: str = "python") -> dict:
    """
    评估单个历史文件
    
    参数:
        history_file: 历史版本文件路径
        gt_file: ground truth 文件路径
        lang: 编程语言
    
    返回:
        评估结果字典
    """
    try:
        # 读取文件内容
        with open(history_file, 'r', encoding='utf-8') as f:
            generated_code = f.read()
        
        with open(gt_file, 'r', encoding='utf-8') as f:
            reference_code = f.read()
        
        # 去除 history 文件的声明部分（动态处理，不创建新文件）
        generated_code_no_decl = remove_declaration_part(generated_code)
        
        # 计算 CodeBLEU
        result = calc_codebleu(
            [reference_code],
            [generated_code_no_decl],
            lang=lang,
            weights=(0.25, 0.25, 0.25, 0.25),
            tokenizer=None
        )
        
        return {
            'filename': history_file.name,
            'version': extract_version_number(history_file.name),
            'codebleu': result.get('codebleu', 0.0),
            'ngram_match_score': result.get('ngram_match_score', 0.0),
            'weighted_ngram_match_score': result.get('weighted_ngram_match_score', 0.0),
            'syntax_match_score': result.get('syntax_match_score', 0.0),
            'dataflow_match_score': result.get('dataflow_match_score', 0.0),
            'success': True
        }
    
    except Exception as e:
        return {
            'filename': history_file.name,
            'version': extract_version_number(history_file.name),
            'error': str(e),
            'success': False
        }


def evaluate_history_directory(history_dir: Path, project_name: str, lang: str = "python", 
                               use_project_code: bool = False) -> dict:
    """
    评估历史目录中的所有文件
    
    参数:
        history_dir: readful_result_history 目录路径
        project_name: 项目名称
        lang: 编程语言
        use_project_code: 是否使用 project_code 作为参考
    
    返回:
        评估结果字典
    """
    if not history_dir.exists():
        print(f"❌ 历史目录不存在: {history_dir}")
        return None
    
    # 获取所有 ST 文件
    history_files = list(history_dir.glob("*.st"))
    
    if not history_files:
        print(f"⚠️  历史目录中没有 ST 文件: {history_dir}")
        return None
    
    print(f"\n📂 历史目录: {history_dir}")
    print(f"   找到 {len(history_files)} 个历史版本文件")
    print(f"   参考代码来源: {'project_code/FUN' if use_project_code else 'generation_context_ground_truth'}")
    
    # 按基础文件名分组
    files_by_base = defaultdict(list)
    for hf in history_files:
        base_name = get_base_filename(hf.name)
        files_by_base[base_name].append(hf)
    
    # 评估结果
    results = {
        'project_name': project_name,
        'history_dir': str(history_dir),
        'total_files': len(history_files),
        'files_by_function': {}
    }
    
    total_evaluated = 0
    total_failed = 0
    
    # 对每个基础文件的所有版本进行评估
    for base_name, version_files in sorted(files_by_base.items()):
        print(f"\n  📄 评估 {base_name} 的 {len(version_files)} 个版本...")
        
        # 获取 ground truth
        gt_file = get_ground_truth_file(project_name, base_name, use_project_code)
        
        if not gt_file:
            print(f"    ⚠️  未找到 ground truth: {base_name}")
            results['files_by_function'][base_name] = {
                'error': 'Ground truth not found',
                'versions': []
            }
            total_failed += len(version_files)
            continue
        
        print(f"    Ground truth: {gt_file}")
        
        # 按版本号排序
        version_files.sort(key=lambda f: extract_version_number(f.name))
        
        # 评估每个版本
        version_results = []
        for vf in version_files:
            version_num = extract_version_number(vf.name)
            print(f"    评估版本 {version_num}...", end=' ')
            
            result = evaluate_history_file(vf, gt_file, lang)
            version_results.append(result)
            
            if result['success']:
                print(f"✓ CodeBLEU: {result['codebleu']:.4f}")
                total_evaluated += 1
            else:
                print(f"✗ {result.get('error', 'Unknown error')}")
                total_failed += 1
        
        # 计算改进趋势
        successful_versions = [v for v in version_results if v['success']]
        if len(successful_versions) > 1:
            first_score = successful_versions[0]['codebleu']
            last_score = successful_versions[-1]['codebleu']
            improvement = last_score - first_score
            improvement_percent = (improvement / first_score * 100) if first_score > 0 else 0
            
            results['files_by_function'][base_name] = {
                'versions': version_results,
                'total_versions': len(version_results),
                'first_version_score': first_score,
                'last_version_score': last_score,
                'improvement': improvement,
                'improvement_percent': improvement_percent
            }
            
            if improvement > 0:
                print(f"    📈 改进: {first_score:.4f} → {last_score:.4f} (+{improvement:.4f}, +{improvement_percent:.2f}%)")
            elif improvement < 0:
                print(f"    📉 下降: {first_score:.4f} → {last_score:.4f} ({improvement:.4f}, {improvement_percent:.2f}%)")
            else:
                print(f"    ➡️  不变: {first_score:.4f}")
        else:
            results['files_by_function'][base_name] = {
                'versions': version_results,
                'total_versions': len(version_results)
            }
    
    # 统计信息
    results['summary'] = {
        'total_evaluated': total_evaluated,
        'total_failed': total_failed,
        'success_rate': total_evaluated / len(history_files) if history_files else 0
    }
    
    return results


def main():
    parser = argparse.ArgumentParser(description="评估修复历史中每个版本的 CodeBLEU")
    parser.add_argument(
        "--timestamp",
        type=str,
        required=True,
        help="时间戳目录（例如：20260122_163745）"
    )
    parser.add_argument(
        "--project",
        type=str,
        required=True,
        help="项目名称（例如：repoeval_readwriteFile）"
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
        help="使用 project_code/FUN 作为参考（默认使用 generation_context_ground_truth）"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="输出 JSON 文件路径（默认：history_evaluation_[timestamp].json）"
    )
    
    args = parser.parse_args()
    
    # 构建路径
    repo_root = Path(__file__).parent.parent
    history_dir = repo_root / "output" / args.timestamp / args.project / "readful_result_history"
    
    print("="*80)
    print("评估修复历史版本")
    print("="*80)
    print(f"时间戳目录: {args.timestamp}")
    print(f"项目名称:   {args.project}")
    print(f"历史目录:   {history_dir}")
    print("="*80)
    
    # 评估
    results = evaluate_history_directory(
        history_dir,
        args.project,
        lang=args.lang,
        use_project_code=args.use_project_code_gt
    )
    
    if results is None:
        return 1
    
    # 保存结果
    if args.output:
        output_file = Path(args.output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = Path(__file__).parent / f"history_evaluation_{timestamp}.json"
    
    print(f"\n💾 保存结果到: {output_file}")
    
    # 添加元数据
    results['metadata'] = {
        'timestamp': datetime.now().isoformat(),
        'args': vars(args)
    }
    
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print("✓ 保存成功")
    except Exception as e:
        print(f"✗ 保存失败: {e}")
        return 1
    
    # 打印总结
    summary = results['summary']
    print("\n" + "="*80)
    print("评估总结")
    print("="*80)
    print(f"总文件数:     {results['total_files']}")
    print(f"成功评估:     {summary['total_evaluated']}")
    print(f"失败:         {summary['total_failed']}")
    print(f"成功率:       {summary['success_rate']*100:.2f}%")
    
    # 打印改进趋势
    print("\n改进趋势:")
    print("-"*80)
    for base_name, data in sorted(results['files_by_function'].items()):
        if 'improvement' in data:
            imp = data['improvement']
            imp_pct = data['improvement_percent']
            symbol = "📈" if imp > 0 else "📉" if imp < 0 else "➡️"
            print(f"  {symbol} {base_name:30s}: {data['first_version_score']:.4f} → {data['last_version_score']:.4f} ({imp:+.4f}, {imp_pct:+.2f}%)")
    
    print("="*80)
    
    return 0


if __name__ == "__main__":
    exit(main())

