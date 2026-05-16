#!/usr/bin/env python3
"""
从代码生成需求描述
遍历 BEIR_data 下的项目，读取 queries.jsonl，对每个文件生成需求描述
"""
import os
import json
import sys
from pathlib import Path
from typing import Dict, Optional
import time

# 尝试导入 openai 库
try:
    import openai
except ImportError:
    print("错误: 需要安装 openai 库")
    print("请运行: pip install openai")
    sys.exit(1)


def get_api_config():
    """从环境变量获取 API 配置"""
    api_key = os.getenv("ZHIZENGZENG_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL") or os.getenv("ZHIZENGZENG_BASE_URL") or "https://api.zhizengzeng.com/v1"
    
    if not api_key:
        print("错误: 未找到 API 密钥")
        print("请设置环境变量: ZHIZENGZENG_API_KEY 或 OPENAI_API_KEY 或 API_KEY")
        sys.exit(1)
    
    return api_key, base_url


def read_source_code(project_code_dir: Path, filename: str) -> Optional[str]:
    """
    从 project_code 目录读取源代码文件
    
    Args:
        project_code_dir: project_code 目录路径
        filename: 文件名（例如 "FB_DualAxisPower.st"）
    
    Returns:
        源代码内容，如果文件不存在返回 None
    """
    source_file = project_code_dir / "FUN" / filename
    if not source_file.exists():
        return None
    
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"  警告: 读取源代码文件失败 {source_file}: {e}")
        return None


def generate_requirement_with_llm(source_code: str, provide_code: str, api_key: str, base_url: str) -> Optional[str]:
    """
    调用大语言模型生成需求描述
    
    Args:
        source_code: 完整的源代码
        provide_code: 提供的代码片段（来自 queries.jsonl 的 text 字段）
        api_key: API 密钥
        base_url: API 基础 URL
    
    Returns:
        生成的需求描述，如果失败返回 None
    """
    # 构建提示词
    prompt = f"""你是一个代码分析专家。请根据以下代码，从需求的角度总结这个代码的功能。

完整的源代码：
```
{source_code}
```

请用一句话总结这个代码的需求，格式为："这个代码意在实现..."。

例如，如果代码实现了快速排序，你应该回答："这个代码意在实现针对数组的快速排序。"

只返回需求描述，不要返回其他内容。"""

    try:
        client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一个专业的代码分析专家，擅长从代码中提取功能需求。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        requirement = response.choices[0].message.content.strip()
        return requirement
    
    except Exception as e:
        print(f"    ✗ API 调用失败: {e}")
        return None


def process_project(beir_project_dir: Path, project_code_dir: Path, output_dir: Path, api_key: str, base_url: str):
    """
    处理一个项目，生成所有文件的需求
    
    Args:
        beir_project_dir: BEIR_data 下的项目目录
        project_code_dir: project_code 下的对应项目目录
        output_dir: 输出目录（query 下的项目目录）
        api_key: API 密钥
        base_url: API 基础 URL
    """
    project_name = beir_project_dir.name
    print(f"\n处理项目: {project_name}")
    print("-" * 80)
    
    # 读取 queries.jsonl
    queries_file = beir_project_dir / "queries.jsonl"
    if not queries_file.exists():
        print(f"  ⚠ 跳过: queries.jsonl 不存在")
        return
    
    # 检查 project_code 目录是否存在
    if not project_code_dir.exists():
        print(f"  ⚠ 跳过: project_code 目录不存在: {project_code_dir}")
        return
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 读取 queries.jsonl
    queries = []
    with open(queries_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    queries.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"  ⚠ 跳过无效的 JSON 行: {e}")
                    continue
    
    print(f"  找到 {len(queries)} 个查询")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for idx, query in enumerate(queries, 1):
        # 提取文件名（从 metadata 中获取 fpath_tuple）
        metadata = query.get("metadata", {})
        fpath_tuple = metadata.get("fpath_tuple", [])
        
        # 如果 metadata 中没有，尝试从顶层获取（兼容性处理）
        if not fpath_tuple:
            fpath_tuple = query.get("fpath_tuple", [])
        
        if not fpath_tuple:
            print(f"  [{idx}/{len(queries)}] ⚠ 跳过: fpath_tuple 为空")
            skip_count += 1
            continue
        
        filename = fpath_tuple[-1]  # 最后一个元素是文件名
        provide_code = query.get("text", "")
        
        print(f"  [{idx}/{len(queries)}] 处理文件: {filename}")
        
        # 读取源代码
        source_code = read_source_code(project_code_dir, filename)
        if source_code is None:
            print(f"    ⚠ 跳过: 源代码文件不存在")
            skip_count += 1
            continue
        
        # 生成需求（仍然使用 LLM 生成 requirement）
        requirement = generate_requirement_with_llm(source_code, provide_code, api_key, base_url)
        if requirement is None:
            print(f"    ✗ 生成需求失败")
            error_count += 1
            continue
        
        # 保存结果
        # provide_code 直接使用原始值，不经过 LLM 处理
        output_file = output_dir / f"{Path(filename).stem}.json"
        result = {
            "requirement": requirement,
            "provide_code": provide_code  # 直接使用原始值
        }
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"    ✓ 已保存: {output_file.name}")
            success_count += 1
        except Exception as e:
            print(f"    ✗ 保存失败: {e}")
            error_count += 1
        
        # 避免 API 调用过快
        time.sleep(0.5)
    
    print(f"\n  完成统计:")
    print(f"    成功: {success_count}")
    print(f"    跳过: {skip_count}")
    print(f"    失败: {error_count}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="从代码生成需求描述")
    parser.add_argument(
        "--project",
        type=str,
        nargs="+",
        default=None,
        help="指定要处理的项目名称（可以指定多个，例如：--project repoeval_四层电梯控制实训 repoeval_交通信号灯控制实训）。如果不指定，则处理所有项目。"
    )
    parser.add_argument(
        "--beir-data-dir",
        type=str,
        default=None,
        help="BEIR_data 目录路径（默认：脚本所在目录/BEIR_data）"
    )
    parser.add_argument(
        "--project-code-dir",
        type=str,
        default=None,
        help="project_code 目录路径（默认：脚本所在目录/project_code）"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="输出目录路径（默认：脚本所在目录/query）"
    )
    
    args = parser.parse_args()
    
    # 获取脚本所在目录
    script_dir = Path(__file__).resolve().parent
    dataset_dir = script_dir
    
    # 目录路径
    beir_data_dir = Path(args.beir_data_dir) if args.beir_data_dir else dataset_dir / "BEIR_data"
    project_code_dir = Path(args.project_code_dir) if args.project_code_dir else dataset_dir / "project_code"
    output_base_dir = Path(args.output_dir) if args.output_dir else dataset_dir / "query"
    
    # 检查目录
    if not beir_data_dir.exists():
        print(f"错误: BEIR_data 目录不存在: {beir_data_dir}")
        sys.exit(1)
    
    if not project_code_dir.exists():
        print(f"错误: project_code 目录不存在: {project_code_dir}")
        sys.exit(1)
    
    # 获取 API 配置
    api_key, base_url = get_api_config()
    print(f"API 配置:")
    print(f"  Base URL: {base_url}")
    print(f"  API Key: {api_key[:20]}...")
    
    # 创建输出目录
    output_base_dir.mkdir(parents=True, exist_ok=True)
    
    # 获取要处理的项目
    if args.project:
        # 指定了项目，只处理这些项目
        beir_projects = []
        for project_name in args.project:
            project_path = beir_data_dir / project_name
            if project_path.exists() and project_path.is_dir():
                beir_projects.append(project_path)
            else:
                print(f"⚠ 警告: 项目目录不存在: {project_path}")
        beir_projects.sort(key=lambda x: x.name)
        print(f"\n指定处理 {len(beir_projects)} 个项目: {[p.name for p in beir_projects]}")
    else:
        # 未指定项目，处理所有项目
        beir_projects = [d for d in beir_data_dir.iterdir() if d.is_dir()]
        beir_projects.sort(key=lambda x: x.name)
        print(f"\n找到 {len(beir_projects)} 个项目，将处理所有项目")
    
    print("=" * 80)
    
    # 处理每个项目
    for beir_project_dir in beir_projects:
        project_name = beir_project_dir.name  # BEIR_data 中的项目名（带 repoeval_ 前缀）
        
        # 查找对应的 project_code 目录
        # BEIR_data 中的项目名都有 repoeval_ 前缀，需要去掉前缀来匹配 project_code
        project_code_name = project_name
        
        # 处理 repoeval_ 前缀（所有 BEIR_data 项目都有这个前缀）
        if project_name.startswith("repoeval_"):
            project_code_name = project_name[9:]  # 去掉 "repoeval_" 前缀
        
        # 查找 project_code 目录
        project_code_project_dir = project_code_dir / project_code_name
        
        # 如果找不到，尝试直接匹配（以防万一）
        if not project_code_project_dir.exists():
            project_code_project_dir = project_code_dir / project_name
        
        # 如果还是找不到，尝试模糊匹配（不区分大小写）
        if not project_code_project_dir.exists():
            # 尝试在 project_code 下查找包含项目名的目录（不区分大小写）
            project_code_name_lower = project_code_name.lower()
            matching_dirs = [d for d in project_code_dir.iterdir() 
                           if d.is_dir() and (
                               project_code_name_lower == d.name.lower() or
                               project_code_name_lower in d.name.lower() or 
                               d.name.lower() in project_code_name_lower
                           )]
            if matching_dirs:
                project_code_project_dir = matching_dirs[0]
                print(f"  使用模糊匹配的目录: {project_code_project_dir.name} (匹配: {project_code_name})")
        
        # 最终检查
        if not project_code_project_dir.exists():
            # 列出所有可用的 project_code 目录，帮助调试
            available_dirs = [d.name for d in project_code_dir.iterdir() if d.is_dir()]
            print(f"\n⚠ 跳过项目 {project_name}: 在 project_code 中找不到对应目录")
            print(f"  尝试匹配的名称: {project_code_name}")
            print(f"  可用的 project_code 目录: {', '.join(available_dirs[:10])}{'...' if len(available_dirs) > 10 else ''}")
            continue
        
        # 输出目录
        output_project_dir = output_base_dir / project_name
        
        # 处理项目
        process_project(beir_project_dir, project_code_project_dir, output_project_dir, api_key, base_url)
    
    print("\n" + "=" * 80)
    print("所有项目处理完成！")


if __name__ == "__main__":
    main()

