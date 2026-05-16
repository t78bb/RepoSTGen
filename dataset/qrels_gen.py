# -*- coding: utf-8 -*-
"""
生成 BEIR 格式的 qrels 文件
根据 queries 中的 fpath_tuple 匹配 corpus 中的文档
"""

import json
import os
from pathlib import Path
import argparse


def generate_qrels(queries_file: str, corpus_file: str, output_file: str):
    """
    生成 qrels 文件
    
    Args:
        queries_file: queries.jsonl 文件路径
        corpus_file: corpus.jsonl 文件路径
        output_file: 输出的 qrels 文件路径
    """
    # 读取 queries
    queries = []
    with open(queries_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.strip():
                queries.append(json.loads(line))
    
    print(f"读取了 {len(queries)} 个查询")
    
    # 读取 corpus
    corpus_entries = []
    with open(corpus_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.strip():
                corpus_entries.append(json.loads(line))
    
    print(f"读取了 {len(corpus_entries)} 个语料库条目")
    
    # 生成 qrels
    qrels = []
    
    for query in queries:
        query_id = query['_id']
        fpath_tuple = query['metadata'].get('fpath_tuple', [])
        
        if not fpath_tuple:
            print(f"警告: 查询 {query_id} 没有 fpath_tuple")
            continue
        
        # 获取文件名（最后一个元素）
        filename = fpath_tuple[-1]
        print(f"\n处理查询 {query_id}, 文件名: {filename}")
        
        # 在 corpus 中查找包含该文件名的所有条目
        matched_count = 0
        for corpus_entry in corpus_entries:
            corpus_id = corpus_entry['_id']
            
            # 检查 corpus_id 是否包含文件名（去除扩展名进行匹配）
            filename_without_ext = filename.rsplit('.', 1)[0] if '.' in filename else filename
            
            if filename_without_ext in corpus_id:
                qrels.append({
                    'query_id': query_id,
                    'corpus_id': corpus_id,
                    'score': 1
                })
                matched_count += 1
        
        print(f"  匹配到 {matched_count} 个语料库条目")
    
    print(f"\n总共生成 {len(qrels)} 条关联关系")
    
    # 创建输出目录
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 写入 TSV 文件（制表符分隔）
    with open(output_file, 'w', encoding='utf-8') as f:
        # 写入表头
        f.write("query-id\tcorpus-id\tscore\n")
        
        # 写入数据
        for qrel in qrels:
            f.write(f"{qrel['query_id']}\t{qrel['corpus_id']}\t{qrel['score']}\n")
    
    print(f"\nqrels 文件已保存到: {output_file}")


def generate_qrels_for_project(project_dir: str):
    """
    为指定项目生成 qrels
    
    Args:
        project_dir: 项目目录路径（例如 beir_dataset/modbus）
    """
    project_path = Path(project_dir)
    
    if not project_path.exists():
        raise FileNotFoundError(f"项目目录不存在: {project_dir}")
    
    # 确定文件路径
    queries_file = project_path / "queries.jsonl"
    corpus_file = project_path / "corpus.jsonl"
    qrels_file = project_path / "qrels" / "test.tsv"
    
    # 检查必要文件是否存在
    if not queries_file.exists():
        raise FileNotFoundError(f"queries 文件不存在: {queries_file}")
    
    if not corpus_file.exists():
        raise FileNotFoundError(f"corpus 文件不存在: {corpus_file}")
    
    print(f"为项目生成 qrels: {project_path.name}")
    print(f"  Queries: {queries_file}")
    print(f"  Corpus:  {corpus_file}")
    print(f"  Output:  {qrels_file}")
    print()
    
    generate_qrels(
        queries_file=str(queries_file),
        corpus_file=str(corpus_file),
        output_file=str(qrels_file)
    )


def main():
    parser = argparse.ArgumentParser(
        description='生成 BEIR 格式的 qrels 文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 为单个项目生成 qrels
  python qrels_gen.py -p beir_dataset/modbus
  
  # 为所有项目生成 qrels
  python qrels_gen.py --all
  
  # 手动指定文件路径
  python qrels_gen.py -q queries.jsonl -c corpus.jsonl -o qrels/test.tsv
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--project', type=str,
                       help='项目目录路径（例如 beir_dataset/modbus）')
    group.add_argument('--all', action='store_true',
                       help='为 beir_dataset 下的所有项目生成 qrels')
    group.add_argument('-q', '--queries', type=str,
                       help='queries.jsonl 文件路径')
    
    parser.add_argument('-c', '--corpus', type=str,
                        help='corpus.jsonl 文件路径（与 -q 一起使用）')
    parser.add_argument('-o', '--output', type=str,
                        help='输出的 qrels 文件路径（与 -q 一起使用）')
    
    args = parser.parse_args()
    
    try:
        if args.all:
            # 处理所有项目
            beir_dataset_dir = Path("beir_dataset")
            if not beir_dataset_dir.exists():
                print("错误: beir_dataset 目录不存在")
                return
            
            project_dirs = [d for d in beir_dataset_dir.iterdir() if d.is_dir()]
            
            if not project_dirs:
                print("错误: beir_dataset 目录下没有找到项目")
                return
            
            print(f"找到 {len(project_dirs)} 个项目\n")
            
            for project_dir in project_dirs:
                try:
                    generate_qrels_for_project(str(project_dir))
                    print()
                except Exception as e:
                    print(f"错误: 处理项目 {project_dir.name} 时出错: {e}\n")
                    continue
            
        elif args.project:
            # 处理单个项目
            generate_qrels_for_project(args.project)
            
        else:
            # 手动指定文件
            if not args.corpus or not args.output:
                print("错误: 使用 -q 参数时，必须同时指定 -c 和 -o 参数")
                return
            
            generate_qrels(
                queries_file=args.queries,
                corpus_file=args.corpus,
                output_file=args.output
            )
    
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

