"""
占位模块：用于基于 Codesys 报错收集并推荐库函数描述，供后续集成到提示中。

后续计划（待实现）：
- 解析编译错误中的库/函数名称。
- 从已构建的库信息目录（如 codesys_library_construction/infos）提取相应描述。
- 输出可拼接到 prompt 的文本片段。
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable, List, Tuple, Optional

# 默认库目录（仓库根下 codesys_library_construction/infos）
DEFAULT_INFOS_DIR = (
    Path(__file__).resolve().parent.parent / "codesys_library_construction" / "infos"
)


def load_library_index(infos_dir: Optional[Path] = None) -> List[str]:
    """
    从 infos 目录收集所有库函数文件名，返回名称列表。
    名称使用文件 stem 及其左括号前缀（如 "Foo (Method)" -> "Foo" 和 "Foo (Method)" 均可匹配）。
    仅关注文件名本身，不读取 JSON 内容。
    """
    if infos_dir is None:
        infos_dir = DEFAULT_INFOS_DIR
    names: List[str] = []
    if not infos_dir.exists():
        return names

    for jf in infos_dir.glob("*.json"):
        stem = jf.stem
        base = stem.split(" (", 1)[0]
        for key in {stem, base}:
            if key and key not in names:
                names.append(key)
    return names


def _build_path_index(infos_dir: Optional[Path] = None) -> dict:
    """
    内部工具：构建 {名称: 文件路径字符串} 映射，供推荐时按需读取 JSON 内容。
    """
    if infos_dir is None:
        infos_dir = DEFAULT_INFOS_DIR
    index: dict = {}
    if not infos_dir.exists():
        return index

    for jf in infos_dir.glob("*.json"):
        stem = jf.stem
        base = stem.split(" (", 1)[0]
        for key in {stem, base}:
            if key and key not in index:
                index[key] = str(jf)
    return index


def extract_library_names(error_messages: Iterable[str]) -> List[str]:
    """
    从报错信息中解析出疑似库/函数名，保持去重后的出现顺序。
    当前重点匹配两类报错：
    1) 参数数量错误："requires exactly"
       例: Function 'SysFileOpen' requires exactly '3' inputs
    2) 参数名错误："is no input of"
       例: szFileName is no input of function 'SysFileOpen'

    兜底：继续匹配 "Function 'Name'"、"Function \"Name\""、"object Name"。

    另外，如果错误对象中带有 line_content 字段（单行源码），
    还会从该行中额外提取形如 funcName(...) 的函数名。
    """
    # 兼容单个字符串或结构化错误列表
    if isinstance(error_messages, str):
        msg_strings = error_messages.splitlines()
        structured_errors: List[object] = []
    else:
        structured_errors = list(error_messages)
        msg_strings = [str(e) for e in structured_errors]

    # 优先针对 requires exactly / is no input of 的函数名提取（在字符串视图上）
    patterns = [
        r"[Ff]unction\s+[\"']?([A-Za-z_][A-Za-z0-9_]*)[\"']?.*requires exactly",
        r"is no input of\s+[Ff]unction\s+[\"']?([A-Za-z_][A-Za-z0-9_]*)[\"']?",
        # 兜底
        r"[Ff]unction\s+'([A-Za-z_][A-Za-z0-9_]*)'",
        r"[Ff]unction\s+\"([A-Za-z_][A-Za-z0-9_]*)\"",
        r"object\s+([A-Za-z_][A-Za-z0-9_]*)",
    ]
    seen = set()
    ordered: List[str] = []
    for msg in msg_strings:
        if not msg:
            continue
        for pat in patterns:
            for name in re.findall(pat, msg):
                if name not in seen:
                    seen.add(name)
                    ordered.append(name)

    # 额外：从 line_content 中提取 funcName(...) 形式的调用
    func_call_pattern = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(")
    for err in structured_errors:

        line_content = None
        if isinstance(err, dict):
            line_content = err.get("line_content")
        else:
            line_content = getattr(err, "line_content", None)
            
        if not isinstance(line_content, str) or not line_content.strip():
            continue
        
        # 输出 line_content 用于调试
        print(f"line_content: {line_content}")
        
        for fn in func_call_pattern.findall(line_content):
            if fn not in seen:
                seen.add(fn)
                ordered.append(fn)

    
    print(ordered)
    return ordered


def recommend_library_snippets(
    error_messages: Iterable[str],
    infos_dir: Optional[Path] = None
) -> List[Tuple[str, str]]:
    """
    根据报错提取库/函数名，匹配 infos 描述并返回 (name, snippet) 列表。
    这里在真正命中时才按路径读取 JSON 文件内容：
    直接把对应文件的全文作为 snippet 返回（不再解析内部结构）。
    """
    index = _build_path_index(infos_dir)
    # print(error_messages)
    names = extract_library_names(error_messages)
    results: List[Tuple[str, str]] = []
    for name in names:
        path_str = index.get(name)
        if not path_str:
            continue
        try:
            p = Path(path_str)
            snippet = p.read_text(encoding="utf-8")
            results.append((name, snippet))
        except Exception:
            continue·
    return results

