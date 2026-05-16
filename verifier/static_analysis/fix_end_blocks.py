"""
简单的 ST 结构检查/修复脚本：
- 每个 IF…THEN 需要 END_IF
- 每个 CASE 需要 END_CASE

策略（轻量级启发式，未做完整语法解析）：
1. 顺序扫描每行，忽略 // 之后的注释内容。
2. 遇到 IF…THEN（且不是 ELSIF/ELSE）入栈；遇到 CASE 入栈。
3. 遇到 END_IF / END_CASE 出栈，若类型不匹配则先补齐缺失的 END_* 再消费当前结束标记。
4. 文件末尾若栈里还有未闭合的块，按栈序追加对应 END_*。

使用方法：
    python verifier/static_analysis/fix_end_blocks.py <input.st> [--output <out.st>] [--inplace]
优先级：--output > --inplace（若两者都不给，则打印到 stdout）。
"""

from __future__ import annotations

import argparse
import os
import re
from typing import List, Tuple, Optional


END_MAP = {"IF": "END_IF;", "CASE": "END_CASE;"}


def _strip_inline_comment(line: str) -> str:
    """去掉 // 后的内容，仅用于简化匹配。"""
    if "//" in line:
        return line.split("//", 1)[0]
    return line


def _is_if_start(text: str) -> bool:
    """
    判断是否是 IF…THEN 的起始行（排除 ELSIF/ELSE）。
    仅按关键词判断，不做完整语法解析。
    """
    # 需要含 IF 和 THEN，且不以 ELSIF/ELSE 开头
    upper = text.strip().upper()
    return (
        upper.startswith("IF ")
        or upper.startswith("IF(")
        or upper.startswith("IF\t")
    ) and " THEN" in upper and not upper.startswith("ELSIF") and not upper.startswith("ELSE")


def _is_case_start(text: str) -> bool:
    upper = text.strip().upper()
    return upper.startswith("CASE ")


def _match_end_keyword(text: str) -> Optional[str]:
    upper = text.strip().upper()
    if upper.startswith("END_IF"):
        return "IF"
    if upper.startswith("END_CASE"):
        return "CASE"
    return None


def fix_missing_end_blocks(code: str) -> Tuple[str, List[str]]:
    """
    尝试修复缺失的 END_IF / END_CASE，返回 (新代码, 插入记录)。
    插入记录例子：["补齐 END_IF; 于第 10 行前", "文件末尾补齐 END_CASE;"]
    """
    lines = code.splitlines()
    stack: List[Tuple[str, str]] = []  # (type, indent)
    new_lines: List[str] = []
    inserts: List[str] = []

    for idx, raw_line in enumerate(lines, start=1):
        line_no_comment = _strip_inline_comment(raw_line)
        token_end = _match_end_keyword(line_no_comment)
        indent = re.match(r"\s*", raw_line).group(0)

        if token_end:
            # 先把栈顶收敛到匹配类型
            while stack and stack[-1][0] != token_end:
                missing_type, missing_indent = stack.pop()
                insert_line = f"{missing_indent}{END_MAP[missing_type]}"
                new_lines.append(insert_line)
                inserts.append(f"补齐 {END_MAP[missing_type]} 于第 {idx} 行前")
            if stack and stack[-1][0] == token_end:
                stack.pop()
            new_lines.append(raw_line)
            continue

        # 起始块检测
        if _is_if_start(line_no_comment):
            stack.append(("IF", indent))
        elif _is_case_start(line_no_comment):
            stack.append(("CASE", indent))

        new_lines.append(raw_line)

    # 文件末尾补齐未闭合的块（按后进先出）
    while stack:
        missing_type, missing_indent = stack.pop()
        insert_line = f"{missing_indent}{END_MAP[missing_type]}"
        new_lines.append(insert_line)
        inserts.append(f"文件末尾补齐 {END_MAP[missing_type]}")

    return "\n".join(new_lines), inserts


def main():
    parser = argparse.ArgumentParser(description="修复 ST 代码中缺失的 END_IF / END_CASE。")
    parser.add_argument("input", help="输入 ST 文件路径")
    parser.add_argument("--output", help="输出文件路径（如不指定且 --inplace 未开，则打印到 stdout）")
    parser.add_argument("--inplace", action="store_true", help="就地覆盖输入文件（无 --output 时生效）")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"未找到文件: {args.input}")

    with open(args.input, "r", encoding="utf-8") as f:
        code = f.read()

    fixed, inserts = fix_missing_end_blocks(code)

    if args.output:
        out_path = args.output
    elif args.inplace:
        out_path = args.input
    else:
        out_path = None

    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(fixed)
        print(f"已写入: {out_path}")
    else:
        print(fixed)

    if inserts:
        print("\n插入记录:")
        for item in inserts:
            print(f"- {item}")
    else:
        print("\n无缺失的 END_IF/END_CASE。")


if __name__ == "__main__":
    main()



