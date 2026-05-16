#!/usr/bin/env python3
"""
为 dataset/query 目录下所有子目录中的 JSON 文件添加 function_name 字段
字段值为 JSON 文件名（不含 .json 后缀）
"""
import json
from pathlib import Path
from typing import Dict, Any


def add_function_name_to_json(json_file: Path) -> bool:
    """
    为单个 JSON 文件添加 function_name 字段
    
    Args:
        json_file: JSON 文件路径
        
    Returns:
        是否成功处理
    """
    try:
        # 读取 JSON 文件
        with open(json_file, 'r', encoding='utf-8') as f:
            data: Dict[str, Any] = json.load(f)
        
        # 获取文件名（不含 .json 后缀）
        function_name = json_file.stem
        
        # 添加或更新 function_name 字段
        data['function_name'] = function_name
        
        # 保存回文件（保持原有格式，使用 indent=2）
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except json.JSONDecodeError as e:
        print(f"  [ERROR] JSON 解析错误 {json_file.name}: {e}")
        return False
    except Exception as e:
        print(f"  [ERROR] 处理失败 {json_file.name}: {e}")
        return False


def main():
    """主函数"""
    # 确定 query 目录路径
    script_dir = Path(__file__).resolve().parent
    query_dir = script_dir / "query"
    
    if not query_dir.exists():
        print(f"[ERROR] query 目录不存在: {query_dir}")
        return
    
    print(f"处理目录: {query_dir}")
    print("=" * 80)
    
    # 统计信息
    total_files = 0
    success_count = 0
    failed_count = 0
    
    # 遍历所有子目录
    subdirs = sorted([d for d in query_dir.iterdir() if d.is_dir()])
    
    if not subdirs:
        print("  [WARN] 没有找到子目录")
        return
    
    print(f"找到 {len(subdirs)} 个子目录\n")
    
    for subdir in subdirs:
        print(f"处理子目录: {subdir.name}")
        
        # 查找所有 JSON 文件
        json_files = sorted(subdir.glob("*.json"))
        
        if not json_files:
            print(f"  [WARN] 没有找到 JSON 文件")
            continue
        
        print(f"  找到 {len(json_files)} 个 JSON 文件")
        
        # 处理每个 JSON 文件
        for json_file in json_files:
            total_files += 1
            if add_function_name_to_json(json_file):
                success_count += 1
                print(f"    [OK] {json_file.name}")
            else:
                failed_count += 1
        
        print()
    
    # 输出统计
    print("=" * 80)
    print("处理完成")
    print(f"总文件数: {total_files}")
    print(f"成功: {success_count}")
    print(f"失败: {failed_count}")


if __name__ == "__main__":
    main()

