#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成所有项目的BEIR数据集和RepoEval格式
对st项目代码提取目录下的所有子目录进行处理
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Tuple
import argparse

# 导入生成模块（用于直接调用，避免subprocess编码问题）
from corpus_gen import generate_corpus
from queries_gen import generate_query_entry
from qrels_gen import generate_qrels as qrels_generate_qrels


class BatchDatasetGenerator:
    """批量数据集生成器"""
    
    def __init__(self, 
                 projects_dir: str = "st项目代码提取",
                 function_lists_dir: str = "function_lists",
                 output_base_dir: str = None,
                 window_size: int = 20,
                 slice_size: int = 10,
                 quiet: bool = False):
        """
        初始化批量生成器
        
        Args:
            projects_dir: 项目源代码根目录
            function_lists_dir: 函数列表文件目录
            output_base_dir: 输出根目录（默认使用时间戳命名）
            window_size: corpus生成的滑动窗口大小
            slice_size: corpus生成的滑动步长
            quiet: 安静模式，只输出错误信息（默认False）
        """
        self.projects_dir = Path(projects_dir)
        self.function_lists_dir = Path(function_lists_dir)
        
        # 如果未指定输出目录，使用时间戳
        if output_base_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_base_dir = Path(f"datasets_{timestamp}")
        else:
            self.output_base_dir = Path(output_base_dir)
        
        self.window_size = window_size
        self.slice_size = slice_size
        self.quiet = quiet
        
        # 统计信息
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'details': []
        }
    
    def print_info(self, message: str):
        """打印信息（只在非quiet模式下）"""
        if not self.quiet:
            print(message)
    
    def print_error(self, message: str):
        """打印错误（始终输出）"""
        print(f"错误: {message}", file=sys.stderr)
    
    def find_projects(self) -> List[Tuple[str, Path, Path]]:
        """
        查找所有项目及其对应的函数列表文件
        
        Returns:
            [(项目名, 项目路径, 函数列表文件路径), ...]
        """
        if not self.projects_dir.exists():
            self.print_error(f"项目目录不存在: {self.projects_dir}")
            return []
        
        if not self.function_lists_dir.exists():
            self.print_error(f"函数列表目录不存在: {self.function_lists_dir}")
            return []
        
        projects = []
        
        # 遍历所有子目录
        for project_path in sorted(self.projects_dir.iterdir()):
            if not project_path.is_dir():
                continue
            
            project_name = project_path.name
            
            # 查找对应的函数列表文件
            function_list_file = self.function_lists_dir / f"{project_name}.txt"
            
            if function_list_file.exists():
                projects.append((project_name, project_path, function_list_file))
            else:
                self.print_info(f"警告: 项目 '{project_name}' 没有对应的函数列表文件")
                projects.append((project_name, project_path, None))
        
        return projects
    
    def generate_project_dataset(self, 
                                 project_name: str, 
                                 project_path: Path, 
                                 function_list_file: Path = None) -> bool:
        """
        为单个项目生成完整数据集
        
        Args:
            project_name: 项目名称
            project_path: 项目路径
            function_list_file: 函数列表文件路径（可选）
            
        Returns:
            是否成功
        """
        self.print_info(f"\n{'='*80}")
        self.print_info(f"正在处理项目: {project_name}")
        self.print_info(f"项目路径: {project_path}")
        if function_list_file:
            self.print_info(f"函数列表: {function_list_file}")
        self.print_info(f"{'='*80}")
        
        try:
            # 创建项目输出目录
            project_output_dir = self.output_base_dir / "beir_dataset" / project_name
            project_output_dir.mkdir(parents=True, exist_ok=True)
            
            repoeval_output_dir = self.output_base_dir / "repoeval"
            repoeval_output_dir.mkdir(parents=True, exist_ok=True)
            
            # 1. 生成 corpus.jsonl
            self.print_info(f"\n[1/4] 生成 corpus.jsonl...")
            corpus_file = project_output_dir / "corpus.jsonl"
            
            try:
                generate_corpus(
                    project_path=str(project_path),
                    output_file=str(corpus_file),
                    window_size=self.window_size,
                    slice_size=self.slice_size,
                    project_name=project_name,
                    file_suffix='.st'
                )
                self.print_info(f"✓ corpus.jsonl 生成成功")
            except Exception as e:
                self.print_error(f"corpus生成失败 [{project_name}] - {e}")
                return False
            
            # 2. 生成 queries.jsonl
            self.print_info(f"\n[2/4] 生成 queries.jsonl...")
            queries_file = project_output_dir / "queries.jsonl"
            
            if not (function_list_file and function_list_file.exists()):
                self.print_error(f"没有函数列表文件，跳过queries生成 [{project_name}]")
                self.stats['skipped'] += 1
                return False
            
            try:
                # 读取函数列表文件
                with open(function_list_file, 'r', encoding='utf-8') as f:
                    function_files = [line.strip() for line in f if line.strip()]
                
                # 生成queries
                queries = []
                for i, func_file in enumerate(function_files):
                    # 构造完整路径
                    if not Path(func_file).is_absolute():
                        func_path = project_path / func_file
                    else:
                        func_path = Path(func_file)
                    
                    if not func_path.exists():
                        self.print_info(f"  警告: 文件不存在 - {func_file}")
                        continue
                    
                    try:
                        query_entry = generate_query_entry(
                            file_path=str(func_path),
                            base_path=str(project_path),
                            index=i,
                            project_name=project_name
                        )
                        queries.append(query_entry)
                    except Exception as e:
                        self.print_info(f"  警告: 处理 {func_file} 时出错: {e}")
                        continue
                
                # 写入文件
                with open(queries_file, 'w', encoding='utf-8') as f:
                    for query in queries:
                        f.write(json.dumps(query, ensure_ascii=False) + '\n')
                
                self.print_info(f"✓ queries.jsonl 生成成功 ({len(queries)} 条)")
            except Exception as e:
                self.print_error(f"queries生成失败 [{project_name}] - {e}")
                return False
            
            # 3. 生成 qrels/test.tsv
            self.print_info(f"\n[3/4] 生成 qrels/test.tsv...")
            qrels_dir = project_output_dir / "qrels"
            qrels_dir.mkdir(exist_ok=True)
            qrels_file = qrels_dir / "test.tsv"
            
            try:
                qrels_generate_qrels(
                    queries_file=str(queries_file),
                    corpus_file=str(corpus_file),
                    output_file=str(qrels_file)
                )
                self.print_info(f"✓ qrels/test.tsv 生成成功")
            except Exception as e:
                self.print_error(f"qrels生成失败 [{project_name}] - {e}")
                return False
            
            # 4. 生成 repoeval 格式
            self.print_info(f"\n[4/4] 生成 repoeval 格式...")
            repoeval_file = repoeval_output_dir / f"{project_name}.jsonl"
            
            try:
                # 读取 queries 并转换为 repoeval 格式
                with open(queries_file, 'r', encoding='utf-8') as f:
                    queries = [json.loads(line) for line in f if line.strip()]
                
                # 转换格式
                repoeval_entries = []
                for query in queries:
                    repoeval_entry = {
                        'prompt': query['text'],
                        'metadata': query.get('metadata', {})
                    }
                    repoeval_entries.append(repoeval_entry)
                
                # 写入文件
                with open(repoeval_file, 'w', encoding='utf-8') as f:
                    for entry in repoeval_entries:
                        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                
                self.print_info(f"✓ repoeval/{project_name}.jsonl 生成成功 ({len(repoeval_entries)} 条)")
            except Exception as e:
                self.print_error(f"repoeval生成失败 [{project_name}] - {e}")
                return False
            
            self.print_info(f"\n✓✓✓ 项目 '{project_name}' 处理完成！")
            return True
            
        except Exception as e:
            self.print_error(f"项目处理失败 [{project_name}]: {e}")
            if not self.quiet:
                import traceback
                traceback.print_exc()
            return False
    
    def run(self):
        """执行批量生成"""
        self.print_info("="*80)
        self.print_info("批量生成BEIR数据集和RepoEval格式")
        self.print_info("="*80)
        self.print_info(f"项目目录: {self.projects_dir.absolute()}")
        self.print_info(f"函数列表目录: {self.function_lists_dir.absolute()}")
        self.print_info(f"输出目录: {self.output_base_dir.absolute()}")
        self.print_info(f"窗口大小: {self.window_size}")
        self.print_info(f"滑动步长: {self.slice_size}")
        self.print_info("="*80)
        
        # 查找所有项目
        projects = self.find_projects()
        self.stats['total'] = len(projects)
        
        if not projects:
            self.print_error("未找到任何项目！")
            return
        
        self.print_info(f"\n找到 {len(projects)} 个项目")
        self.print_info("\n项目列表:")
        for i, (name, path, func_file) in enumerate(projects, 1):
            status = "✓" if func_file else "✗"
            self.print_info(f"  {i:2d}. [{status}] {name}")
        
        # 确认开始
        self.print_info(f"\n准备开始批量处理...")
        
        # 创建输出目录
        self.output_base_dir.mkdir(parents=True, exist_ok=True)
        
        # 处理每个项目
        for i, (project_name, project_path, function_list_file) in enumerate(projects, 1):
            self.print_info(f"\n\n进度: [{i}/{len(projects)}]")
            
            success = self.generate_project_dataset(
                project_name, 
                project_path, 
                function_list_file
            )
            
            if success:
                self.stats['success'] += 1
                self.stats['details'].append({
                    'project': project_name,
                    'status': 'success'
                })
            else:
                self.stats['failed'] += 1
                self.stats['details'].append({
                    'project': project_name,
                    'status': 'failed'
                })
        
        # 生成总结报告
        self.generate_summary_report()
    
    def generate_summary_report(self):
        """生成总结报告"""
        # 总结始终输出
        print("\n\n" + "="*80)
        print("批量处理完成！")
        print("="*80)
        
        print(f"\n统计信息:")
        print(f"  总项目数: {self.stats['total']}")
        print(f"  成功: {self.stats['success']}")
        print(f"  失败: {self.stats['failed']}")
        print(f"  跳过: {self.stats['skipped']}")
        
        if self.stats['failed'] > 0:
            print(f"\n失败的项目:")
            for detail in self.stats['details']:
                if detail['status'] == 'failed':
                    print(f"  ✗ {detail['project']}")
        
        print(f"\n输出目录: {self.output_base_dir.absolute()}")
        print(f"  ├── beir_dataset/")
        print(f"  │   ├── {self.stats['success']} 个项目")
        print(f"  │   │   ├── corpus.jsonl")
        print(f"  │   │   ├── queries.jsonl")
        print(f"  │   │   └── qrels/test.tsv")
        print(f"  └── repoeval/")
        print(f"      └── {self.stats['success']} 个 .jsonl 文件")
        
        # 保存统计信息到文件
        report_file = self.output_base_dir / "generation_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'parameters': {
                    'window_size': self.window_size,
                    'slice_size': self.slice_size,
                    'projects_dir': str(self.projects_dir),
                    'function_lists_dir': str(self.function_lists_dir)
                },
                'statistics': self.stats
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n详细报告已保存到: {report_file}")
        print("="*80)


def main():
    parser = argparse.ArgumentParser(
        description='批量生成所有项目的BEIR数据集和RepoEval格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 使用默认参数
  python batch_generate_all.py
  
  # 安静模式（只显示错误和最终报告）
  python batch_generate_all.py -q
  
  # 自定义窗口参数
  python batch_generate_all.py -w 30 -s 15
  
  # 指定输出目录
  python batch_generate_all.py -o my_datasets
  
  # 完整参数
  python batch_generate_all.py -p st项目代码提取 -f function_lists -w 20 -s 10 -q -o datasets_20240101
        """
    )
    
    parser.add_argument('-p', '--projects-dir',
                       default='st项目代码提取',
                       help='项目源代码根目录 (默认: st项目代码提取)')
    
    parser.add_argument('-f', '--function-lists-dir',
                       default='function_lists',
                       help='函数列表文件目录 (默认: function_lists)')
    
    parser.add_argument('-o', '--output-dir',
                       default=None,
                       help='输出根目录 (默认: datasets_时间戳)')
    
    parser.add_argument('-w', '--window-size',
                       type=int,
                       default=20,
                       help='corpus滑动窗口大小 (默认: 20)')
    
    parser.add_argument('-s', '--slice-size',
                       type=int,
                       default=10,
                       help='corpus滑动步长 (默认: 10)')
    
    parser.add_argument('-q', '--quiet',
                       action='store_true',
                       help='安静模式，只输出错误信息和最终报告 (默认: False)')
    
    args = parser.parse_args()
    
    # 创建生成器并执行
    generator = BatchDatasetGenerator(
        projects_dir=args.projects_dir,
        function_lists_dir=args.function_lists_dir,
        output_base_dir=args.output_dir,
        window_size=args.window_size,
        slice_size=args.slice_size,
        quiet=args.quiet
    )
    
    generator.run()


if __name__ == "__main__":
    main()

