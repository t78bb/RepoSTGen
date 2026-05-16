#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
上下文规划器模块
通过收集待补全函数块被调用位置的相关上下文，对待补全功能做出细致规划
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ContextWindow:
    """代码上下文窗口"""
    file_path: str  # 文件路径
    line_number: int  # 调用/定义所在行号（1-based）
    context_type: str  # 'call' 或 'definition'
    code_window: str  # 上下10行的代码窗口
    surrounding_lines: List[str]  # 原始代码行列表


@dataclass
class PlannerConfig:
    """规划器配置"""
    project_code_root: Path  # project_code 根目录路径
    context_window_size: int = 10  # 上下文窗口大小（上下各N行）
    project_name: Optional[str] = None  # 项目名称（如果为None，则需要在调用时指定）
    function_type: str = "function_block"  # 函数类型：'function_block' 或 'function'


def find_function_occurrences(
    function_name: str,
    project_code_dir: Path,
    function_type: str = "function_block",
    context_window_size: int = 10
) -> List[ContextWindow]:
    """
    在项目代码目录中查找函数的所有调用位置（不包括函数定义本身）
    并提取调用位置上下N行的代码窗口
    
    参数:
        function_name: 待查找的函数名
        project_code_dir: 项目代码目录路径（如 dataset/project_code/counter）
        function_type: 函数类型，'function_block' 或 'function'（默认 'function_block'）
        context_window_size: 上下文窗口大小（默认10行）
    
    返回:
        ContextWindow 对象列表，包含所有找到的调用位置及其上下文
    """
    contexts = []
    
    if not project_code_dir.exists():
        return contexts
    
    # 递归查找所有 .st 文件（排除函数定义所在的文件）
    st_files = list(project_code_dir.rglob("*.st"))
    
    for st_file in st_files:
        try:
            content = st_file.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # 跳过函数定义文件（不能看函数定义本身）
            if _contains_function_definition(lines, function_name):
                continue
            
            # 根据函数类型选择不同的查找策略
            if function_type.lower() == "function_block":
                # FUNCTION_BLOCK: 找到所有实例声明行（如 F1 : FB_Counter;），然后找到该实例的所有调用位置（如 F1(...)）
                instance_declarations = _find_instance_declarations(lines, function_name)
                
                for instance_name, decl_line_idx in instance_declarations:
                    call_positions = _find_instance_calls(lines, instance_name)
                    
                    for call_line_idx in call_positions:
                        # 提取上下文窗口
                        start_line = max(0, call_line_idx - context_window_size)
                        end_line = min(len(lines), call_line_idx + context_window_size + 1)
                        code_window = '\n'.join(lines[start_line:end_line])
                        surrounding_lines = lines[start_line:end_line]
                        
                        context = ContextWindow(
                            file_path=str(st_file.relative_to(project_code_dir.parent.parent)),
                            line_number=call_line_idx + 1,  # 1-based line number
                            context_type='call',
                            code_window=code_window,
                            surrounding_lines=surrounding_lines
                        )
                        contexts.append(context)
            
            elif function_type.lower() == "function":
                # FUNCTION: 直接找到所有函数调用位置（如 FunctionName(...)）
                function_calls = _find_function_calls(lines, function_name)
                
                for call_line_idx in function_calls:
                    # 提取上下文窗口
                    start_line = max(0, call_line_idx - context_window_size)
                    end_line = min(len(lines), call_line_idx + context_window_size + 1)
                    code_window = '\n'.join(lines[start_line:end_line])
                    surrounding_lines = lines[start_line:end_line]
                    
                    context = ContextWindow(
                        file_path=str(st_file.relative_to(project_code_dir.parent.parent)),
                        line_number=call_line_idx + 1,  # 1-based line number
                        context_type='call',
                        code_window=code_window,
                        surrounding_lines=surrounding_lines
                    )
                    contexts.append(context)
            else:
                raise ValueError(f"不支持的函数类型: {function_type}，必须是 'function_block' 或 'function'")
        
        except Exception as e:
            # 如果文件读取失败，跳过该文件
            print(f"警告: 无法读取文件 {st_file}: {e}")
            continue
    
    return contexts


def _contains_function_definition(lines: List[str], function_name: str) -> bool:
    """
    检查文件是否包含函数定义（需要跳过，因为不能看函数定义本身）
    
    参数:
        lines: 文件的所有行
        function_name: 函数名
    
    返回:
        是否包含函数定义
    """
    for line in lines:
        stripped = line.strip()
        
        # 检查 FUNCTION_BLOCK
        if re.match(rf'^\s*FUNCTION_BLOCK\s+{re.escape(function_name)}\b', stripped, re.IGNORECASE):
            return True
        
        # 检查 FUNCTION
        if re.match(rf'^\s*FUNCTION\s+{re.escape(function_name)}\b', stripped, re.IGNORECASE):
            return True
        
        # 检查 METHOD
        if re.match(rf'^\s*METHOD\s+{re.escape(function_name)}\b', stripped, re.IGNORECASE):
            return True
    
    return False


def _find_instance_declarations(lines: List[str], function_name: str) -> List[Tuple[str, int]]:
    """
    找到所有 FUNCTION_BLOCK 的实例声明行
    例如：F1 : FB_Counter; 或 FB_Counter_0:FB_Counter;
    
    参数:
        lines: 文件的所有行
        function_name: 函数名（FUNCTION_BLOCK 名称）
    
    返回:
        (实例名, 行号) 元组列表，行号是 0-based
    """
    declarations = []
    
    for line_idx, line in enumerate(lines):
        # 去掉所有空格后再匹配，应对各种格式
        # 例如：F1 : FB_Counter; 或 F1:FB_Counter; 或 F1 :FB_Counter; 等
        line_no_spaces = re.sub(r'\s+', '', line)
        
        # 匹配模式：instance_name:function_name;
        pattern = rf'(\w+):{re.escape(function_name)};'
        match = re.search(pattern, line_no_spaces, re.IGNORECASE)
        
        if match:
            instance_name = match.group(1)
            declarations.append((instance_name, line_idx))
    
    return declarations


def _find_instance_calls(lines: List[str], instance_name: str) -> List[int]:
    """
    在文件中找到实例的所有调用位置
    例如：F1(...) 或 F1(param1 := value1, param2 := value2);
    
    参数:
        lines: 文件的所有行
        instance_name: 实例名
    
    返回:
        调用位置的行号列表（0-based）
    """
    call_positions = []
    
    for line_idx, line in enumerate(lines):
        stripped = line.strip()
        
        # 匹配模式：instance_name(...)
        # 例如：F1(...) 或 FB_Counter_0(param1 := value1);
        pattern = rf'\b{re.escape(instance_name)}\s*\('
        if re.search(pattern, stripped, re.IGNORECASE):
            call_positions.append(line_idx)
    
    return call_positions


def _find_function_calls(lines: List[str], function_name: str) -> List[int]:
    """
    找到函数的直接调用位置（用于 FUNCTION 类型）
    例如：FunctionName(...) 或 result := FunctionName(param1, param2);
    
    参数:
        lines: 文件的所有行
        function_name: 函数名
    
    返回:
        调用位置的行号列表（0-based）
    """
    call_positions = []
    
    for line_idx, line in enumerate(lines):
        stripped = line.strip()
        
        # 匹配模式：function_name(...)
        # 但不能是方法调用（instance.function_name(...)）
        # 也不能是声明（: function_name）
        pattern = rf'\b{re.escape(function_name)}\s*\('
        if re.search(pattern, stripped, re.IGNORECASE):
            # 排除方法调用（前面有点号）
            if not re.search(rf'\.\s*{re.escape(function_name)}\s*\(', stripped, re.IGNORECASE):
                call_positions.append(line_idx)
    
    return call_positions


def collect_contexts(
    function_name: str,
    config: PlannerConfig,
    project_name: Optional[str] = None
) -> List[ContextWindow]:
    """
    收集函数的所有上下文（对外暴露的主接口）
    
    参数:
        function_name: 待补全函数的名称
        config: 规划器配置对象
        project_name: 项目名称（可选，如果提供则覆盖 config 中的 project_name）
    
    返回:
        ContextWindow 对象列表，包含所有找到的调用和定义位置及其上下文
    """
    # 确定使用的项目名称
    used_project_name = project_name if project_name is not None else config.project_name
    
    if not used_project_name:
        raise ValueError("必须指定 project_name（通过参数或 config）")
    
    # 构建项目代码目录路径：project_code_root / project_name
    project_code_dir = config.project_code_root / used_project_name
    
    if not project_code_dir.exists():
        raise ValueError(f"项目目录不存在: {project_code_dir}")
    
    contexts = find_function_occurrences(
        function_name=function_name,
        project_code_dir=project_code_dir,
        function_type=config.function_type,
        context_window_size=config.context_window_size
    )
    # print(f"找到 {len(contexts)} 个上下文位置:")
    # for ctx in contexts:
    #     print(f"\n类型: {ctx.context_type}, 文件: {ctx.file_path}, 行号: {ctx.line_number}")
    #     print("代码窗口:")
    #     print(ctx.code_window)
    #     print("-" * 80)
    return contexts


def collect_similar_contexts(
    function_name: str,
    results_jsonl_path: Path,
    project_code_dir: Path,
) -> List[str]:
    """
    基于检索结果收集“相似函数”的源码内容列表。

    逻辑：
    1. 在指定目录的 results.jsonl 中，找到 function_name 对应的条目（通过 metadata.function_name / function_name / task_id 匹配）；
    2. 从该条目的 docs 字段中读取 title，取最后一个以 .st 结尾的部分作为文件名，收集为集合；
    3. 去掉集合中与 function_name 同名的项（忽略大小写与 .st 扩展名差异）；
    4. 在 project_code_dir 下查找这些文件名对应的 .st 文件，读取其内容，组成 List 返回。

    返回：
        List[str]，每个元素是一个相似函数文件的完整 ST 源码内容。
    """

    def _normalize_name(name: Optional[str]) -> str:
        if not name:
            return ""
        n = name.strip().lower()
        if n.endswith(".st"):
            n = n[:-3]
        return n

    similar_sources: List[str] = []

    if not results_jsonl_path.exists():
        return similar_sources

    target_docs = None
    target_fn_norm = _normalize_name(function_name)

    # 1. 从 results.jsonl 中找到与 function_name 匹配的条目，并取出 docs
    with results_jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue

            metadata = obj.get("metadata") or {}
            cand_fn = None
            if isinstance(metadata, dict):
                cand_fn = metadata.get("function_name") or metadata.get("task_id")
            cand_fn = cand_fn or obj.get("function_name") or obj.get("task_id")

            if _normalize_name(str(cand_fn)) != target_fn_norm:
                continue

            docs = obj.get("docs")
            if isinstance(docs, list):
                target_docs = docs
            break

    if not target_docs:
        return similar_sources

    # 2. 从 docs.title 中提取 .st 文件名集合
    filename_set = set()
    for d in target_docs:
        if not isinstance(d, dict):
            continue
        title = d.get("title")
        if not isinstance(title, str):
            continue
        # 取路径最后一段
        last_part = title.replace("\\", "/").split("/")[-1]
        if last_part.lower().endswith(".st"):
            filename_set.add(last_part)

    # 3. 去掉与 function_name 同名的文件（忽略大小写与 .st 扩展名）
    filtered_filenames = []
    for fname in filename_set:
        if _normalize_name(fname) == target_fn_norm:
            continue
        filtered_filenames.append(fname)
    if not project_code_dir.exists():
        return similar_sources

    # 4. 在 project_code_dir 下查找对应文件，并读取内容
    for fname in filtered_filenames:
        # 允许任意子目录匹配
        matched_files = list(project_code_dir.rglob(fname))
        if not matched_files:
            continue
        # 如果有多个同名文件，当前简单地取第一个
        try:
            content = matched_files[0].read_text(encoding="utf-8")
            similar_sources.append(content)
        except Exception:
            continue
    print(similar_sources)
    return similar_sources



                

# 示例使用
if __name__ == "__main__":
    # 测试代码
    from pathlib import Path
    
    # 创建配置
    config = PlannerConfig(
        project_code_root=Path(__file__).parent.parent / "dataset" / "project_code",
        context_window_size=10,
        function_type="function_block"  # FB_Counter 是 FUNCTION_BLOCK
    )
    
    # 通过参数指定项目名称和函数名（方便调试时修改）
    function_name = "readFile"
    project_name = "readwriteFile"
    
    contexts = collect_contexts(function_name, config, project_name=project_name)
    
    print(f"找到 {len(contexts)} 个上下文位置:")
    for ctx in contexts:
        print(f"\n类型: {ctx.context_type}, 文件: {ctx.file_path}, 行号: {ctx.line_number}")
        print("代码窗口:")
        print(ctx.code_window)
        print("-" * 80)

