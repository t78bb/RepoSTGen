# -*- coding: utf-8 -*-
import os
import sys
import json
import argparse
import re
from pathlib import Path
from typing import Dict, Optional, Tuple

# UTF-8编码已在文件头声明


def extract_function_info(file_content: str) -> Dict:
    """
    从ST函数文件中提取函数信息
    
    返回:
        {
            'function_name': 函数名,
            'start_line': 函数定义行号（0-based）,
            'text_end_line': text结束后的行号（0-based），即VAR那一行
            'text': 查询文本（从开头到VAR之前的部分）,
            'ground_truth': 完整函数代码
        }
    """
    lines = file_content.split('\n')
    
    # 提取函数名（从FUNCTION或FUNCTION_BLOCK或METHOD行）
    function_name = None
    function_start_line = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('FUNCTION_BLOCK ') or stripped.startswith('FUNCTION ') or stripped.startswith('METHOD '):
            # 提取函数名
            if stripped.startswith('FUNCTION_BLOCK '):
                parts = stripped.split()
                if len(parts) >= 2:
                    # FUNCTION_BLOCK NAME 或 FUNCTION_BLOCK PUBLIC NAME
                    if parts[1].upper() == 'PUBLIC' and len(parts) >= 3:
                        function_name = parts[2].split(':')[0].strip()
                    else:
                        function_name = parts[1].split(':')[0].strip()
            elif stripped.startswith('FUNCTION '):
                parts = stripped.split()
                if len(parts) >= 2:
                    function_name = parts[1].split(':')[0].strip()
            elif stripped.startswith('METHOD '):
                parts = stripped.split()
                if len(parts) >= 2:
                    function_name = parts[1].split('(')[0].split(':')[0].strip()
            
            function_start_line = i
            break
    
    if not function_name:
        raise ValueError("无法找到函数定义")
    
    # 查找第一个VAR（局部变量定义）的位置
    # 注意：不包括VAR_INPUT, VAR_OUTPUT, VAR_IN_OUT等
    var_line = None
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 检测VAR段的开始
        if re.match(r'^VAR\s*$', stripped):  # 只匹配单独的VAR
            var_line = i
            break
        elif stripped.startswith('VAR_INPUT') or stripped.startswith('VAR_OUTPUT') or \
             stripped.startswith('VAR_IN_OUT') or stripped.startswith('VAR_TEMP'):
            # 这些是参数定义，不是局部变量
            continue
    
    # 提取text（从开头到VAR之前）
    text_end_line = None
    if var_line is not None:
        text_lines = lines[:var_line]
        text_end_line = var_line
    else:
        # 如果没有找到VAR，可能函数没有局部变量，提取到END_VAR或函数体开始
        # 寻找最后一个END_VAR
        last_end_var = None
        for i, line in enumerate(lines):
            if line.strip() == 'END_VAR':
                last_end_var = i
        
        if last_end_var is not None:
            text_lines = lines[:last_end_var + 1]
            text_end_line = last_end_var + 1
        else:
            text_lines = lines
            text_end_line = len(lines)
    
    text = '\n'.join(text_lines).strip()
    ground_truth = file_content.strip()
    
    return {
        'function_name': function_name,
        'start_line': function_start_line,
        'text_end_line': text_end_line,
        'text': text,
        'ground_truth': ground_truth
    }


def parse_file_path(file_path: Path, base_path: Path) -> Tuple[str, list]:
    """
    解析文件路径，提取项目名和文件路径元组
    
    Args:
        file_path: 完整文件路径
        base_path: 基础路径
    
    Returns:
        (project_name, fpath_tuple)
    """
    relative_path = file_path.relative_to(base_path)
    parts = relative_path.parts
    
    # 第一个部分通常是项目名
    project_name = parts[0] if parts else "unknown"
    
    # fpath_tuple包含项目名和文件相对路径
    fpath_tuple = [project_name] + list(parts[1:])
    
    return project_name, fpath_tuple


def generate_query_entry(file_path: str, base_path: str = None, index: int = None, project_name: str = None) -> Dict:
    """
    从单个ST文件生成一个query条目
    
    Args:
        file_path: ST函数文件路径
        base_path: 基础路径（用于生成相对路径）
        index: 查询序号（可选，如果提供则使用 项目名/序号 格式）
        project_name: 项目名称（如果提供，使用此名称而不是从路径提取）
    
    Returns:
        符合BEIR格式的query字典
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 提取函数信息
    func_info = extract_function_info(content)
    
    # 解析路径，获取fpath_tuple
    if base_path:
        base_path = Path(base_path)
        extracted_project_name, fpath_tuple = parse_file_path(file_path, base_path)
        # 如果没有显式提供project_name，使用提取的
        if project_name is None:
            project_name = extracted_project_name
    else:
        # 如果没有提供base_path，使用文件名作为项目名
        if project_name is None:
            project_name = file_path.stem
        fpath_tuple = [project_name, file_path.name]
    
    # 生成ID - 根据是否提供index使用不同格式
    if index is not None:
        query_id = f"{project_name}/{index}"
        task_id = query_id
    else:
        query_id = f"{project_name}_{func_info['function_name']}_query"
        task_id = query_id
    
    # lineno应该是text结束后的行号（即VAR那一行，1-based）
    lineno = func_info['text_end_line'] + 1  # 转换为1-based
    
    # 构建query条目
    query_entry = {
        "_id": query_id,
        "text": func_info['text'],
        "metadata": {
            "task_id": task_id,
            "ground_truth": func_info['ground_truth'],
            "fpath_tuple": fpath_tuple,
            "context_start_lineno": 0,  # ST文件通常从第0行开始
            "lineno": lineno,
            "function_name": func_info['function_name'],
            "line_no": lineno
        }
    }
    
    return query_entry


def generate_queries_from_directory(directory: str, output_file: str, file_suffix: str = '.st', base_path: str = None, project_name: str = None):
    """
    从目录中的所有ST文件批量生成queries
    
    Args:
        directory: 包含ST文件的目录
        output_file: 输出的queries.jsonl文件路径
        file_suffix: 文件后缀（默认.st）
        base_path: 基础路径（用于生成相对路径）
        project_name: 项目名称（如果提供，使用此名称而不是从路径提取）
    """
    directory = Path(directory)
    
    if not directory.exists():
        raise FileNotFoundError(f"目录不存在: {directory}")
    
    # 如果没有指定base_path，使用directory的父目录
    if base_path is None:
        base_path = directory.parent
    else:
        base_path = Path(base_path)
    
    # 如果没有指定project_name，从directory提取
    if project_name is None:
        project_name = directory.name
    
    queries = []
    
    # 收集所有ST文件并排序（保证序号稳定）
    st_files = sorted(directory.rglob(f'*{file_suffix}'))
    
    # 遍历目录下所有ST文件，使用序号
    for index, file_path in enumerate(st_files):
        try:
            print(f"处理文件 {index}: {file_path.name}")
            query_entry = generate_query_entry(str(file_path), str(base_path), index=index, project_name=project_name)
            queries.append(query_entry)
        except Exception as e:
            print(f"警告: 处理文件 {file_path} 时出错: {e}")
            continue
    
    # 写入jsonl文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for query in queries:
            f.write(json.dumps(query, ensure_ascii=False) + '\n')
    
    print(f"\n成功生成 {len(queries)} 条查询")
    print(f"输出文件: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='生成BEIR格式的queries.jsonl文件')
    parser.add_argument('-f', '--file', type=str, help='单个ST函数文件路径')
    parser.add_argument('-d', '--directory', type=str, help='包含ST文件的目录路径')
    parser.add_argument('-o', '--output', type=str, default='queries.jsonl', help='输出文件路径（默认: queries.jsonl）')
    parser.add_argument('-s', '--suffix', type=str, default='.st', help='文件后缀（默认: .st）')
    parser.add_argument('-b', '--base-path', type=str, help='基础路径（用于生成相对路径）')
    parser.add_argument('-n', '--name', type=str, help='项目名称（用于生成ID，默认从路径提取）')
    
    args = parser.parse_args()
    
    if args.file:
        # 处理单个文件
        try:
            query_entry = generate_query_entry(args.file, args.base_path, project_name=args.name)
            
            # 写入jsonl文件
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(json.dumps(query_entry, ensure_ascii=False) + '\n')
            
            print(f"成功生成查询: {query_entry['_id']}")
            print(f"输出文件: {args.output}")
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)
    
    elif args.directory:
        # 处理目录
        try:
            generate_queries_from_directory(args.directory, args.output, args.suffix, args.base_path, project_name=args.name)
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)
    
    else:
        parser.print_help()
        print("\n错误: 必须指定 -f/--file 或 -d/--directory 参数")
        sys.exit(1)


if __name__ == '__main__':
    main()

