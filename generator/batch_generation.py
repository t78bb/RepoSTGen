#!/usr/bin/env python3
"""
批量执行代码生成脚本
对 codesys_result 下的每个数据集目录执行代码生成
"""
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def remove_repoeval_prefix(dataset_name):
    """移除 repoeval 前缀，返回用于 dataset_path 的名称"""
    if dataset_name.startswith("repoeval_"):
        name = dataset_name[len("repoeval_"):]
        if name.startswith("_"):
            name = name[1:]
        if name.endswith("_"):
            name = name[:-1]
        return name
    return dataset_name

def main():
    import argparse
    parser = argparse.ArgumentParser(description="批量执行代码生成脚本")
    parser.add_argument(
        "--result_dir",
        type=str,
        default=None,
        help="Directory name under output to save results. If not provided, will use timestamp."
    )
    parser.add_argument(
        "--project",
        type=str,
        default=None,
        help="只处理 `result_dir` 下的某个子目录，直接写目录名，例如 `repoeval_counter`。",
    )
    args = parser.parse_args()
    
    # 如果没有提供 result_dir，生成统一的时间戳（确保所有任务使用同一个目录）
    if not args.result_dir:
        args.result_dir = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"未指定 --result_dir，使用时间戳: {args.result_dir}")
    
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    main_py = script_dir / "main.py"

    output_dir = repo_root / "output"
    result_dir = os.path.join(output_dir, args.result_dir)
    
    if not output_dir.exists():
        print(f"错误: {output_dir} 目录不存在")
        sys.exit(1)
    
    # 检查结果目录是否存在
    if not os.path.exists(result_dir):
        print(f"错误: 结果目录不存在: {result_dir}")
        print(f"请先运行 retrieval 生成结果目录")
        sys.exit(1)
    
    # 获取结果目录下的所有子目录（这些是数据集目录）
    all_dirs = [d for d in os.listdir(result_dir)
                 if os.path.isdir(os.path.join(result_dir, d))]
    all_dirs.sort()
    if args.project:
        all_dirs = [d for d in all_dirs if d == args.project]
        if not all_dirs:
            print(f"错误: 没有找到项目 {args.project}，请确认目录名是否正确。")
            sys.exit(1)
    
    print("="*80)
    print("批量执行代码生成")
    print("="*80)
    print(f"\n结果目录: {args.result_dir}")
    print(f"待处理数据集数: {len(all_dirs)}")
    print(f"\n数据集列表:")
    for i, d in enumerate(all_dirs, 1):
        print(f"  {i}. {d}")
    
    # 记录结果
    results = {
        "success": [],
        "failed": [],
        "skipped": []
    }
    
    print(f"\n开始执行...")
    print("="*80)
    
    for idx, dataset_dir in enumerate(all_dirs, 1):
        print(f"\n[{idx}/{len(all_dirs)}] 处理数据集: {dataset_dir}")
        print("-" * 80)
        
        # 在结果目录下查找对应的项目目录
        project_dir = os.path.join(result_dir, dataset_dir)
        data_files_test = os.path.join(project_dir, "results.jsonl")
        
        # 检查 data_files_test 文件是否存在
        if not os.path.exists(data_files_test):
            print(f"  ⚠ 跳过: data_files_test 文件不存在: {data_files_test}")
            results["skipped"].append({
                "dataset": dataset_dir,
                "reason": f"data_files_test 文件不存在: {data_files_test}"
            })
            continue
        
        # 构建命令（始终传递 result_dir，确保所有任务使用同一个目录）
        cmd = [
            sys.executable or "python",
            str(main_py),
            "--tasks", "repoeval-function",
            "--model", "gpt-4o",
            "--dataset_path", "json",
            "--data_files_test", data_files_test,
            "--topk_docs", "5",  #前5个匹配retrieval
            "--max_length_input", "2048",
            "--max_length_generation", "1024",
            "--model_backend", "api",
            "--temperature", "0.2",
            "--top_p", "0.95",
            "--save_generations",
            "--result_dir", args.result_dir
        ]
        
        # 打印完整命令（用于调试）
        cmd_str = ' '.join(cmd)
        print(f"  命令: {cmd_str}")
        print(f"  data_files_test: {data_files_test}")
        
        # 执行命令（实时输出）
        try:
            # 使用 Popen 实现实时输出
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # 将 stderr 合并到 stdout
                text=True,
                bufsize=1,  # 行缓冲
                universal_newlines=True
            )
            
            # 实时读取并打印输出
            output_lines = []
            import time
            
            start_time = time.time()
            timeout_seconds = 7200  # 2小时超时
            
            # 实时读取并打印输出
            try:
                for line in process.stdout:
                    # 检查超时
                    if time.time() - start_time > timeout_seconds:
                        process.kill()
                        raise subprocess.TimeoutExpired(cmd, timeout_seconds)
                    
                    line = line.rstrip()
                    print(f"    {line}")  # 添加缩进以便区分
                    output_lines.append(line)
                    sys.stdout.flush()  # 确保实时输出
                
                # 等待进程完成
                returncode = process.wait()
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                raise
            
            # 合并所有输出
            full_output = '\n'.join(output_lines)
            
            if returncode == 0:
                print(f"  ✓ 成功")
                results["success"].append(dataset_dir)
            else:
                print(f"  ✗ 失败 (返回码: {returncode})")
                # 显示完整的错误信息（去除 FutureWarning 等警告）
                if full_output:
                    # 过滤掉 FutureWarning，显示实际错误
                    error_lines = full_output.split('\n')
                    important_errors = [line for line in error_lines 
                                       if 'Error' in line or 'Exception' in line or 'Traceback' in line
                                       or (line.strip() and 'FutureWarning' not in line and 'Warning' not in line)]
                    if important_errors:
                        error_display = '\n'.join(important_errors[-10:])  # 显示最后10行重要错误
                    else:
                        error_display = full_output[-1000:]  # 显示最后1000字符
                    print(f"  错误信息:\n{error_display}")
                else:
                    print(f"  无错误信息输出")
                
                results["failed"].append({
                    "dataset": dataset_dir,
                    "returncode": returncode,
                    "error": full_output[:2000] if full_output else "无错误信息"
                })
        
        except subprocess.TimeoutExpired:
            if 'process' in locals():
                process.kill()
                process.wait()
            print(f"  ✗ 超时（超过2小时）")
            results["failed"].append({
                "dataset": dataset_dir,
                "returncode": -1,
                "error": "执行超时（超过2小时）"
            })
        
        except Exception as e:
            if 'process' in locals():
                try:
                    process.kill()
                    process.wait()
                except:
                    pass
            print(f"  ✗ 异常: {str(e)}")
            results["failed"].append({
                "dataset": dataset_dir,
                "returncode": -1,
                "error": str(e)
            })
    
    # 输出总结
    print("\n" + "="*80)
    print("执行总结")
    print("="*80)
    print(f"\n总数据集数: {len(all_dirs)}")
    print(f"成功: {len(results['success'])}")
    print(f"失败: {len(results['failed'])}")
    print(f"跳过: {len(results['skipped'])}")
    
    if results["success"]:
        print(f"\n✓ 成功的数据集 ({len(results['success'])}):")
        for d in results["success"]:
            print(f"  - {d}")
    
    if results["skipped"]:
        print(f"\n⚠ 跳过的数据集 ({len(results['skipped'])}):")
        for item in results["skipped"]:
            print(f"  - {item['dataset']}: {item['reason']}")
    
    if results["failed"]:
        print(f"\n✗ 失败的数据集 ({len(results['failed'])}):")
        for item in results["failed"]:
            print(f"\n  数据集: {item['dataset']}")
            print(f"  返回码: {item['returncode']}")
            print(f"  错误信息:")
            print(f"    {item['error']}")
            print("-" * 80)
    
    # 保存结果到文件
    import json
    result_file = f"batch_generation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n详细结果已保存到: {result_file}")
    
    # 如果有失败，返回非零退出码
    if results["failed"]:
        sys.exit(1)

if __name__ == "__main__":
    main()

