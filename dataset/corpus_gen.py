# -*- coding: utf-8 -*-
import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict

# UTF-8编码已在文件头声明


def read_file_lines(file_path: str) -> List[str]:
    """读取文件的所有行"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.readlines()
    except Exception as e:
        print(f"Warning: 无法读取文件 {file_path}: {e}")
        return []


def generate_sliding_windows(lines: List[str], window_size: int, slice_size: int) -> List[Dict]:
    """
    使用滑动窗口生成代码片段
    
    策略：
    1. 第一个窗口从 0 到 window_size/2
    2. 逐步增长到完整窗口大小（每次增加 slice_size）
    3. 之后正常滑动
    
    Args:
        lines: 文件的所有行
        window_size: 窗口大小（行数）
        slice_size: 滑动步长（行数）
    
    Returns:
        窗口列表，每个窗口包含起始行号、结束行号和内容
    """
    windows = []
    total_lines = len(lines)
    
    if total_lines == 0:
        return windows
    
    # 第一阶段：从窗口大小的一半开始，逐步增长到完整窗口
    half_window = window_size // 2
    current_window_size = half_window
    start_line = 0
    line_no = 0  # 初始化line_no
    
    # 生成从半窗口逐步增长到完整窗口的窗口
    while current_window_size <= window_size:
        end_line = min(start_line + current_window_size, total_lines)
        
        # 提取窗口内容
        window_content = ''.join(lines[start_line:end_line])
        
        windows.append({
            'line_no': line_no,  # 使用递增的line_no
            'start_line_no': start_line,
            'end_line_no': end_line,
            'content': window_content
        })
        
        # 如果已经到达文件末尾，停止
        if end_line >= total_lines:
            return windows
        
        # 增长窗口大小，同时line_no也增加
        current_window_size += slice_size
        line_no += slice_size
    
    # 第二阶段：正常滑动窗口
    # 重置line_no为slice_size，这样窗口从[slice_size, window_size+slice_size]开始
    line_no = slice_size
    
    while line_no < total_lines:
        start_line = line_no
        end_line = min(line_no + window_size, total_lines)
        
        # 提取窗口内容
        window_content = ''.join(lines[start_line:end_line])
        
        windows.append({
            'line_no': line_no,
            'start_line_no': start_line,
            'end_line_no': end_line,
            'content': window_content
        })
        
        # 移动窗口
        line_no += slice_size
        
        # 如果已经到达文件末尾，停止
        if end_line >= total_lines:
            break
    
    return windows


def collect_files(project_path: str, file_suffix: str) -> List[tuple]:
    """
    收集项目中所有指定后缀的文件
    
    Returns:
        List of (file_path, relative_path) tuples
    """
    project_path = Path(project_path)
    files = []
    
    for root, dirs, filenames in os.walk(project_path):
        for filename in filenames:
            if filename.endswith(file_suffix):
                full_path = Path(root) / filename
                relative_path = full_path.relative_to(project_path)
                files.append((str(full_path), str(relative_path)))
    
    return files


def generate_corpus(
    project_path: str,
    file_suffix: str = '.st',
    window_size: int = 50,
    slice_size: int = 5,
    output_file: str = 'corpus.jsonl',
    project_name: str = None
):
    """
    生成BEIR格式的corpus文件
    
    Args:
        project_path: 项目路径
        file_suffix: 文件后缀，例如 '.st' 或 '.py'
        window_size: 窗口大小（行数）
        slice_size: 滑动步长（行数）
        output_file: 输出文件路径
        project_name: 项目名称（如果不指定，从路径提取）
    """
    project_path = Path(project_path)
    if project_name is None:
        project_name = project_path.name
    
    # 收集所有符合条件的文件
    files = collect_files(str(project_path), file_suffix)
    print(f"找到 {len(files)} 个 {file_suffix} 文件")
    
    corpus_entries = []
    
    for file_path, relative_path in files:
        # 读取文件内容
        lines = read_file_lines(file_path)
        if not lines:
            continue
        
        # 生成滑动窗口
        windows = generate_sliding_windows(lines, window_size, slice_size)
        
        if not windows:
            continue
        
        print(f"处理文件: {relative_path} ({len(lines)} 行, {len(windows)} 个窗口)")
        
        # 为每个窗口生成corpus条目
        for window in windows:
            # 生成唯一ID
            doc_id = f"{project_name}_{relative_path}_{window['start_line_no']}-{window['end_line_no']}"
            # 清理ID中的特殊字符
            doc_id = doc_id.replace('\\', '_').replace('/', '_').replace(' ', '_')
            
            # 生成title
            title = f"{project_name}-{relative_path}"
            
            # 构建metadata
            metadata_entry = {
                "fpath_tuple": [project_name, relative_path],
                "repo": project_name,
                "line_no": window['line_no'],
                "start_line_no": window['start_line_no'],
                "end_line_no": window['end_line_no'],
                "window_size": window_size,
                "slice_size": slice_size,
            }
            
            # 构建corpus条目
            corpus_entry = {
                "_id": doc_id,
                "title": title,
                "text": window['content'],
                "metadata": [metadata_entry]  # 按照格式要求，metadata是一个列表
            }
            
            corpus_entries.append(corpus_entry)
    
    # 写入jsonl文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in corpus_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"\n[OK] 成功生成corpus文件: {output_file}")
    print(f"- 处理文件数: {len(files)}")
    print(f"- 生成corpus条目数: {len(corpus_entries)}")
    print(f"- 窗口大小: {window_size} 行")
    print(f"- 滑动步长: {slice_size} 行")


def main():
    parser = argparse.ArgumentParser(
        description='生成BEIR格式的corpus语料库文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 使用默认参数处理.st文件
  python corpus_gen.py -p "path/to/project"
  
  # 处理Python文件，自定义窗口大小和步长
  python corpus_gen.py -p "path/to/project" -s .py -w 100 -l 10
  
  # 指定输出文件
  python corpus_gen.py -p "path/to/project" -o my_corpus.jsonl
        """
    )
    
    parser.add_argument(
        '-p', '--project',
        type=str,
        required=True,
        help='项目路径'
    )
    
    parser.add_argument(
        '-s', '--suffix',
        type=str,
        default='.st',
        help='文件后缀，例如 .st 或 .py (默认: .st)'
    )
    
    parser.add_argument(
        '-w', '--window-size',
        type=int,
        default=50,
        help='窗口大小（行数），默认: 50'
    )
    
    parser.add_argument(
        '-l', '--slice-size',
        type=int,
        default=5,
        help='滑动步长（行数），默认: 5'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='corpus.jsonl',
        help='输出文件路径 (默认: corpus.jsonl)'
    )
    
    parser.add_argument(
        '-n', '--name',
        type=str,
        default=None,
        help='项目名称（如果不指定，从路径提取）'
    )
    
    args = parser.parse_args()
    
    # 验证参数
    if not os.path.exists(args.project):
        print(f"Error: 项目路径不存在: {args.project}")
        return
    
    if args.window_size <= 0:
        print(f"Error: 窗口大小必须大于0")
        return
    
    if args.slice_size <= 0:
        print(f"Error: 滑动步长必须大于0")
        return
    
    # 生成corpus
    generate_corpus(
        project_path=args.project,
        file_suffix=args.suffix,
        window_size=args.window_size,
        slice_size=args.slice_size,
        output_file=args.output,
        project_name=args.name
    )


if __name__ == "__main__":
    main()

