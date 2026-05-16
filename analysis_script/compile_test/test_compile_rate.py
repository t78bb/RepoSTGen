#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
编译通过率测试脚本
测试 ST 代码的编译通过率，不进行代码修复，只统计编译结果
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 添加项目根目录到路径
REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "verifier"))

from codesys_debug import CodesysCompiler, ResponseData

# CODESYS API 配置
CODESYS_API_URL = os.getenv("CODESYS_API_URL", "http://192.168.103.117:9000/api/v1/pou/workflow")


def extract_block_name_from_file(file_path: Path) -> str:
    """
    从文件路径提取块名称（去掉 .st 扩展名）
    """
    return file_path.stem


def test_single_file(
    st_file: Path,
    project_name: str,
    compiler: CodesysCompiler,
    ip_port: Optional[str] = None
) -> Dict:
    """
    测试单个 ST 文件的编译结果
    
    参数:
        st_file: ST 文件路径
        project_name: 项目名称
        compiler: CodesysCompiler 实例
        ip_port: API 地址（可选）
    
    返回:
        包含编译结果的字典
    """
    try:
        # 读取文件内容
        st_code = st_file.read_text(encoding='utf-8')
        
        # 提取块名称
        block_name = extract_block_name_from_file(st_file)
        
        # 调用编译检查
        check_result = compiler.syntax_check(
            project_name=project_name,
            block_name=block_name,
            st_code=st_code,
            ip_port=ip_port or CODESYS_API_URL
        )
        
        # 判断是否通过：Errors 字段为空则通过
        passed = check_result.success and (
            not check_result.errors or len(check_result.errors) == 0
        )
        
        # 构建结果
        result = {
            "file_path": str(st_file),
            "file_name": st_file.name,
            "block_name": block_name,
            "project_name": project_name,
            "passed": passed,
            "success": check_result.success,
            "errors_count": len(check_result.errors) if check_result.errors else 0,
            "errors": [error.to_dict() for error in check_result.errors] if check_result.errors else []
        }
        
        return result
        
    except Exception as e:
        return {
            "file_path": str(st_file),
            "file_name": st_file.name,
            "project_name": project_name,
            "passed": False,
            "success": False,
            "errors_count": 0,
            "errors": [],
            "exception": str(e)
        }


def test_directory(
    directory: Path,
    compiler: CodesysCompiler,
    ip_port: Optional[str] = None,
    result_subdir: str = "readful_result"
) -> Dict:
    """
    测试目录下所有 ST 文件的编译结果
    
    参数:
        directory: 包含 readful_result 或 full_result 的目录（项目目录）
        compiler: CodesysCompiler 实例
        ip_port: API 地址（可选）
        result_subdir: 要测试的子目录名称（默认：readful_result）
    
    返回:
        包含所有文件测试结果的字典
    """
    result_dir = directory / result_subdir
    
    if not result_dir.exists():
        return {
            "directory": str(directory),
            "project_name": directory.name,
            "error": f"{result_subdir} 目录不存在",
            "files": [],
            "total_files": 0,
            "passed_files": 0,
            "failed_files": 0,
            "pass_rate": 0.0
        }
    
    # 查找所有 .st 文件
    st_files = list(result_dir.glob("*.st"))
    
    if not st_files:
        return {
            "directory": str(directory),
            "project_name": directory.name,
            "error": "未找到 ST 文件",
            "files": [],
            "total_files": 0,
            "passed_files": 0,
            "failed_files": 0,
            "pass_rate": 0.0
        }
    
    # 测试每个文件
    file_results = []
    passed_count = 0
    
    print(f"\n  测试项目: {directory.name}")
    print(f"  找到 {len(st_files)} 个 ST 文件")
    
    for idx, st_file in enumerate(sorted(st_files), 1):
        print(f"    [{idx}/{len(st_files)}] 测试: {st_file.name}...", end=' ')
        
        result = test_single_file(st_file, directory.name, compiler, ip_port)
        file_results.append(result)
        
        if result["passed"]:
            print("✓ 通过")
            passed_count += 1
        else:
            print(f"✗ 失败 (错误数: {result['errors_count']})")
    
    pass_rate = (passed_count / len(st_files) * 100) if st_files else 0.0
    
    return {
        "directory": str(directory),
        "project_name": directory.name,
        "files": file_results,
        "total_files": len(st_files),
        "passed_files": passed_count,
        "failed_files": len(st_files) - passed_count,
        "pass_rate": round(pass_rate, 2)
    }


def test_output_directory(
    output_subdir: Path,
    compiler: CodesysCompiler,
    ip_port: Optional[str] = None
) -> List[Dict]:
    """
    测试 output 目录下指定子目录的所有项目
    
    参数:
        output_subdir: output 下的子目录（如 output/20260123_171908）
        compiler: CodesysCompiler 实例
        ip_port: API 地址（可选）
    
    返回:
        所有项目的测试结果列表
    """
    if not output_subdir.exists():
        print(f"错误: 目录不存在 - {output_subdir}")
        
        # 尝试列出父目录下的可用子目录
        parent_dir = output_subdir.parent
        if parent_dir.exists() and parent_dir.name == "output":
            available_dirs = [d.name for d in parent_dir.iterdir() if d.is_dir()]
            if available_dirs:
                print(f"\n可用的 output 子目录:")
                for dir_name in sorted(available_dirs):
                    print(f"  - {dir_name}")
                print(f"\n提示: 使用 --output-dir output/{available_dirs[0]} 来测试")
        
        return []
    
    # 查找所有包含 readful_result 的项目目录
    project_dirs = []
    for item in output_subdir.iterdir():
        if item.is_dir() and (item / "readful_result").exists():
            project_dirs.append(item)
    
    if not project_dirs:
        print(f"错误: 在 {output_subdir} 下未找到包含 readful_result 的项目目录")
        return []
    
    print(f"\n{'='*80}")
    print(f"测试 Output 目录: {output_subdir}")
    print(f"找到 {len(project_dirs)} 个项目")
    print(f"{'='*80}")
    
    results = []
    for idx, project_dir in enumerate(sorted(project_dirs), 1):
        print(f"\n[{idx}/{len(project_dirs)}] 处理项目: {project_dir.name}")
        result = test_directory(project_dir, compiler, ip_port)
        results.append(result)
    
    return results


def test_ground_truth_directory(
    gt_root: Path,
    compiler: CodesysCompiler,
    ip_port: Optional[str] = None
) -> List[Dict]:
    """
    测试 real_groud_truth最新 目录下所有项目（使用 full_result 目录）
    
    参数:
        gt_root: real_groud_truth最新 目录
        compiler: CodesysCompiler 实例
        ip_port: API 地址（可选）
    
    返回:
        所有项目的测试结果列表
    """
    if not gt_root.exists():
        print(f"错误: 目录不存在 - {gt_root}")
        return []
    
    # 查找所有包含 full_result 的项目目录
    project_dirs = []
    for item in gt_root.iterdir():
        if item.is_dir() and (item / "full_result").exists():
            project_dirs.append(item)
    
    if not project_dirs:
        print(f"错误: 在 {gt_root} 下未找到包含 full_result 的项目目录")
        return []
    
    print(f"\n{'='*80}")
    print(f"测试 Ground Truth 目录: {gt_root}")
    print(f"找到 {len(project_dirs)} 个项目")
    print(f"{'='*80}")
    
    results = []
    for idx, project_dir in enumerate(sorted(project_dirs), 1):
        print(f"\n[{idx}/{len(project_dirs)}] 处理项目: {project_dir.name}")
        result = test_directory(project_dir, compiler, ip_port, result_subdir="full_result")
        results.append(result)
    
    return results


def main():
    parser = argparse.ArgumentParser(description="测试 ST 代码编译通过率")
    parser.add_argument(
        "--output-dir",
        type=str,
        help="output 目录下的子目录（例如：output/20260123_171908）"
    )
    parser.add_argument(
        "--gt-dir",
        type=str,
        default=None,
        help="ground truth 目录（可选，例如：real_groud_truth最新）"
    )
    parser.add_argument(
        "--ip-port",
        type=str,
        help="CODESYS API 地址（可选，默认使用环境变量或默认值）"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="输出 JSON 文件路径（可选，默认自动生成）"
    )
    
    args = parser.parse_args()
    
    # 检查至少指定了一个测试目录
    if not args.output_dir and not args.gt_dir:
        parser.error("必须至少指定 --output-dir 或 --gt-dir 中的一个")
    
    # 初始化编译器
    compiler = CodesysCompiler()
    ip_port = args.ip_port or CODESYS_API_URL
    
    # 收集所有结果
    all_results = {
        "test_time": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "output_results": [],
        "ground_truth_results": [],
        "summary": {}
    }
    
    # 测试 output 目录
    output_results = []
    if args.output_dir:
        output_subdir = Path(args.output_dir)
        # 如果是相对路径，相对于项目根目录
        if not output_subdir.is_absolute():
            output_subdir = REPO_ROOT / output_subdir
        output_results = test_output_directory(output_subdir, compiler, ip_port)
        all_results["output_results"] = output_results
    
    # 测试 ground truth 目录（仅当指定了 --gt-dir 时）
    gt_results = []
    if args.gt_dir:
        gt_root = REPO_ROOT / args.gt_dir
        gt_results = test_ground_truth_directory(gt_root, compiler, ip_port)
        all_results["ground_truth_results"] = gt_results
    
    # 计算总体统计
    all_projects = output_results + gt_results
    
    total_files = sum(r.get("total_files", 0) for r in all_projects)
    total_passed = sum(r.get("passed_files", 0) for r in all_projects)
    total_failed = sum(r.get("failed_files", 0) for r in all_projects)
    
    overall_pass_rate = (total_passed / total_files * 100) if total_files > 0 else 0.0
    
    all_results["summary"] = {
        "total_projects": len(all_projects),
        "total_files": total_files,
        "total_passed_files": total_passed,
        "total_failed_files": total_failed,
        "overall_pass_rate": round(overall_pass_rate, 2)
    }
    
    # 输出总结
    print("\n" + "="*80)
    print("测试完成 - 总体统计")
    print("="*80)
    print(f"总项目数: {len(all_projects)}")
    print(f"总文件数: {total_files}")
    print(f"通过文件数: {total_passed}")
    print(f"失败文件数: {total_failed}")
    print(f"总体编译通过率: {overall_pass_rate:.2f}%")
    print("="*80)
    
    # 保存结果
    if args.output:
        output_file = Path(args.output)
    else:
        # 自动生成文件名
        script_dir = Path(__file__).parent
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = script_dir / f"compile_test_result_{timestamp}.json"
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 结果已保存到: {output_file}")
    
    return 0


if __name__ == "__main__":
    exit(main())

