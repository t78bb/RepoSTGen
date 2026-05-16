#!/usr/bin/env python3
"""
批量执行 retrieval 脚本
处理 dataset/query 目录下的所有子目录，对每个项目执行检索
"""
import os
import sys
from pathlib import Path
from datetime import datetime
import argparse

# 导入检索模块
from eval_beir_sbert_canonical import main as retrieval_main

def main():
    parser = argparse.ArgumentParser(description="批量执行 retrieval 脚本")
    parser.add_argument(
        "--project",
        type=str,
        nargs="+",
        default=None,
        help="指定要处理的项目名称（可以指定多个，例如：--project repoeval_四层电梯控制实训 repoeval_交通信号灯控制实训）。如果不指定，则处理所有项目。"
    )
    parser.add_argument(
        "--result-dir",
        type=str,
        default=None,
        help="结果目录名称（如果不指定，将使用时间戳）"
    )
    args = parser.parse_args()
    
    # 获取脚本所在目录
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    
    # 设置路径
    query_base_dir = project_root / "dataset" / "query"
    output_base_dir = project_root / "output"
    
    # 检查目录是否存在
    if not query_base_dir.exists():
        print(f"错误: query 目录不存在: {query_base_dir}")
        sys.exit(1)
    
    # 创建输出目录
    output_base_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成时间戳或使用指定的结果目录
    if args.result_dir:
        result_dir_name = args.result_dir
        timestamp = args.result_dir
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_dir_name = timestamp
    
    # 获取要处理的 query 子目录
    if args.project:
        # 指定了项目，只处理这些项目
        query_dirs = []
        for project_name in args.project:
            project_path = query_base_dir / project_name
            if project_path.exists() and project_path.is_dir():
                query_dirs.append(project_path)
            else:
                print(f"⚠ 警告: 项目目录不存在: {project_path}")
        query_dirs.sort(key=lambda x: x.name)
        if not query_dirs:
            print(f"错误: 没有找到任何指定的项目目录")
            sys.exit(1)
        print(f"\n指定处理 {len(query_dirs)} 个项目: {[p.name for p in query_dirs]}")
    else:
        # 未指定项目，处理所有项目
        query_dirs = [d for d in query_base_dir.iterdir() if d.is_dir()]
        query_dirs.sort(key=lambda x: x.name)
        if not query_dirs:
            print(f"警告: {query_base_dir} 下没有子目录")
            sys.exit(0)
    
    print("=" * 80)
    print("批量执行 Retrieval")
    print("=" * 80)
    print(f"\nQuery 基础目录: {query_base_dir}")
    print(f"输出基础目录: {output_base_dir}")
    print(f"结果目录名称: {result_dir_name}")
    print(f"待处理项目数: {len(query_dirs)}")
    print(f"\n项目列表:")
    for i, d in enumerate(query_dirs, 1):
        print(f"  {i}. {d.name}")
    
    # 记录结果
    results = {
        "success": [],
        "failed": [],
        "skipped": []
    }
    
    print(f"\n开始执行...")
    print("=" * 80)
    
    for idx, query_dir in enumerate(query_dirs, 1):
        project_name = query_dir.name
        
        # 检查是否有 JSON 文件
        json_files = list(query_dir.glob("*.json"))
        if not json_files:
            print(f"\n[{idx}/{len(query_dirs)}] ⚠ 跳过项目 {project_name}: 没有 JSON 文件")
            results["skipped"].append({
                "project": project_name,
                "reason": "没有 JSON 文件"
            })
            continue
        
        print(f"\n[{idx}/{len(query_dirs)}] 处理项目: {project_name}")
        print(f"  找到 {len(json_files)} 个查询文件")
        print("-" * 80)
        
        # 从项目名提取 dataset 名称（query 目录名就是 dataset 名）
        dataset_name = project_name
        
        # 构建参数对象
        print(f"  开始执行...")
        try:
            # 确定数据目录（BEIR 数据在 dataset/BEIR_data 下）
            beir_data_dir = project_root / "dataset" / "BEIR_data"
            if not beir_data_dir.exists():
                print(f"  ⚠ 警告: BEIR_data 目录不存在: {beir_data_dir}")
                print(f"  将使用 output 目录作为数据目录")
                beir_data_dir = output_base_dir  # 如果不存在，使用 output
            else:
                print(f"  使用 BEIR 数据目录: {beir_data_dir}")
            
            # 创建参数对象
            retrieval_args = argparse.Namespace(
                dataset=dataset_name,
                query_dir=str(query_dir),
                result_dir=result_dir_name,
                output_base_dir=str(output_base_dir),
                data_base_dir=str(beir_data_dir),  # BEIR 数据目录
                model="BAAI/bge-base-en-v1.5",
                batch_size=64,
                dataset_path="output/origin_repoeval/datasets/function_level_completion_2k_context_codex.test.clean.jsonl",
                output_file="outputs.json",
                results_file="results.jsonl"
            )
            
            # 直接调用函数
            retrieval_main(retrieval_args)
            
            print(f"  ✓ 成功")
            results["success"].append(project_name)
        
        except KeyboardInterrupt:
            print(f"\n  ✗ 用户中断")
            raise
        except Exception as e:
            print(f"  ✗ 异常: {str(e)}")
            import traceback
            error_msg = traceback.format_exc()
            results["failed"].append({
                "project": project_name,
                "returncode": -1,
                "error": str(e) + "\n" + error_msg[:500]
            })
            print(f"  错误信息:")
            print(f"    {str(e)}")
    
    # 输出总结
    print("\n" + "=" * 80)
    print("执行总结")
    print("=" * 80)
    print(f"\n总项目数: {len(query_dirs)}")
    print(f"成功: {len(results['success'])}")
    print(f"失败: {len(results['failed'])}")
    print(f"跳过: {len(results['skipped'])}")
    
    if results["success"]:
        print(f"\n✓ 成功的项目 ({len(results['success'])}):")
        for p in results["success"]:
            print(f"  - {p}")
    
    if results["skipped"]:
        print(f"\n⚠ 跳过的项目 ({len(results['skipped'])}):")
        for item in results["skipped"]:
            print(f"  - {item['project']}: {item['reason']}")
    
    if results["failed"]:
        print(f"\n✗ 失败的项目 ({len(results['failed'])}):")
        for item in results["failed"]:
            print(f"\n  项目: {item['project']}")
            print(f"  返回码: {item['returncode']}")
            print(f"  错误信息:")
            print(f"    {item['error']}")
            print("-" * 80)
    
    # 保存结果到文件
    import json
    result_file = output_base_dir / result_dir_name / f"batch_retrieval_results_{timestamp}.json"
    result_file.parent.mkdir(parents=True, exist_ok=True)
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n详细结果已保存到: {result_file}")
    
    # 输出最终结果目录
    final_output_dir = output_base_dir / result_dir_name
    print(f"\n所有检索结果保存在: {final_output_dir}")
    
    # 如果有失败，返回非零退出码
    if results["failed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()

