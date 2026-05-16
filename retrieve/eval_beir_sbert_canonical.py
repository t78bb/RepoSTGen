import os
# 在导入任何 HuggingFace 相关模块之前，先设置离线模式（如果模型已缓存）
# 这样可以避免在导入时就开始网络请求
cache_dir = os.path.expanduser('~/.cache/huggingface/hub')
if os.path.exists(cache_dir):
    # 检查是否有模型缓存（简单检查：如果缓存目录存在，可能已有模型）
    # 更精确的检查会在 main 函数中进行
    if os.getenv('OFFLINE_MODE') == '1':
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
        os.environ['HF_HUB_OFFLINE'] = '1'

import json
import logging
import argparse
from datetime import datetime
from time import time
from typing import List, Dict
from pathlib import Path
from beir import LoggingHandler
from beir.retrieval import models
from beir.datasets.data_loader import GenericDataLoader
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.dense import DenseRetrievalExactSearch as DRES
from tqdm import tqdm

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
        
def get_top_docs(results: Dict, corpus: Dict, task_id: str, topk: int = 20) -> List[str]:
    if task_id not in results: return []
    doc_scores = results[task_id]
    doc_scores_sorted = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)
    doc_scores_sorted = doc_scores_sorted[:topk]
    doc_code_snippets = [corpus[code_id] for code_id, score in doc_scores_sorted]
    return doc_code_snippets


def find_query_dir_for_dataset(dataset_name: str, base_query_dir: str = "dataset/query") -> str:
    """
    根据数据集名称查找对应的 query 目录
    
    Args:
        dataset_name: 数据集名称，例如 "repoeval_四层电梯控制实训"
        base_query_dir: query 基础目录，默认 "dataset/query"
    
    Returns:
        query 目录路径，如果找不到返回 None
    """
    from pathlib import Path
    base_path = Path(base_query_dir)
    if not base_path.exists():
        return None
    
    # 尝试直接匹配
    query_dir = base_path / dataset_name
    if query_dir.exists():
        return str(query_dir)
    
    # 尝试匹配所有可能的变体
    for subdir in base_path.iterdir():
        if not subdir.is_dir():
            continue
        # 完全匹配
        if subdir.name == dataset_name:
            return str(subdir)
        # 去掉前缀匹配（处理 repoeval_ 前缀）
        if dataset_name.startswith("repoeval_"):
            name_without_prefix = dataset_name[9:]  # 去掉 "repoeval_"
            if subdir.name == dataset_name or subdir.name.endswith(name_without_prefix):
                return str(subdir)
            # 处理双下划线的情况
            if subdir.name.startswith("repoeval__") and name_without_prefix in subdir.name:
                return str(subdir)
    
    return None


def load_queries_from_query_dir(query_dir: str) -> Dict[str, Dict]:
    """
    从 query 目录加载新格式的查询文件
    
    Args:
        query_dir: query 目录路径，例如 "dataset/query/repoeval_四层电梯控制实训"
    
    Returns:
        字典，格式为 {task_id: {"requirement": "...", "provide_code": "..."}}
        task_id 是文件名（去掉 .json 扩展名）
    """
    from pathlib import Path
    query_path = Path(query_dir)
    if not query_path.exists():
        logging.warning(f"Query directory does not exist: {query_dir}")
        return {}
    
    queries = {}
    json_files = list(query_path.glob("*.json"))
    if not json_files:
        logging.warning(f"No JSON files found in query directory: {query_dir}")
        return {}
    
    for json_file in json_files:
        task_id = json_file.stem  # 文件名去掉 .json
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                queries[task_id] = {
                    "requirement": data.get("requirement", ""),
                    "provide_code": data.get("provide_code", ""),
                    "function_name": data.get("function_name", task_id)  # 保存 function_name，如果没有则使用 task_id
                }
        except Exception as e:
            logging.warning(f"Failed to load {json_file}: {e}")
            continue
    
    logging.info(f"Loaded {len(queries)} queries from {query_dir}")
    return queries


def main(args=None):
    """
    主函数
    
    Args:
        args: argparse.Namespace 对象，如果为 None 则从命令行解析
    """
    # 如果没有提供 args，从命令行解析
    if args is None:
        parser = argparse.ArgumentParser()
        parser.add_argument("--dataset", type=str, required=True,
                            help="Dataset to use for evaluation (must start with 'repoeval')")
        parser.add_argument("--model", type=str, default="BAAI/bge-base-en-v1.5", help="Sentence-BERT model to use")
        parser.add_argument("--batch_size", type=int, default=64, help="Batch size for retrieval")
        parser.add_argument("--dataset_path", type=str, default="output/origin_repoeval/datasets/function_level_completion_2k_context_codex.test.clean.jsonl", help="Dataset path for evaluation")
        parser.add_argument("--output_file", type=str, default="outputs.json",
                            help="Specify the filepath if you want to save the retrieval (evaluation) results.")
        parser.add_argument("--results_file", type=str, default="results.jsonl",
                            help="Specify the filepath if you want to save the retrieval results (JSONL format, one JSON object per line).")
        parser.add_argument("--result_dir", type=str, default=None,
                            help="Directory name under codesys_result to save results. If not provided, will use timestamp.")
        parser.add_argument("--query_dir", type=str, default=None,
                            help="Directory path for new format query files (e.g., 'dataset/query/repoeval_xxx'). If not provided, will auto-detect from dataset name. If auto-detection fails, will use BEIR queries.jsonl format.")
        parser.add_argument("--output_base_dir", type=str, default=None,
                            help="Base output directory. If not provided, will use default '../codesys_result'.")
        parser.add_argument("--data_base_dir", type=str, default=None,
                            help="Base directory for corpus data (containing corpus.jsonl, queries.jsonl, qrels.jsonl). If not provided, will use 'output' relative to project root.")
        args = parser.parse_args()
    
    # 根据数据集名称创建输出目录
    # 如果提供了 --output_base_dir 则使用它，否则使用默认路径
    if args.output_base_dir:
        base_output_dir = args.output_base_dir
    else:
        base_output_dir = "../codesys_result"
    
    # 确定结果目录名称：如果提供了 --result_dir 则使用它，否则使用时间戳
    if args.result_dir:
        result_dir_name = args.result_dir
    else:
        result_dir_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 创建结果目录
    result_dir = os.path.join(base_output_dir, result_dir_name)
    os.makedirs(result_dir, exist_ok=True)
    
    # 在结果目录下创建数据集目录
    dataset_name = args.dataset  # 例如: repoeval__assembly-station
    output_dir = os.path.join(result_dir, dataset_name)
    
    # 创建目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    # 修改输出文件路径，使其保存到数据集目录下
    args.output_file = os.path.join(output_dir, "outputs.json")
    args.results_file = os.path.join(output_dir, "results.jsonl")
    
    logging.info(f"Result directory: {result_dir}")
    logging.info(f"Output directory: {output_dir}")
    logging.info(f"Output file: {args.output_file}")
    logging.info(f"Results file: {args.results_file}")
    
    # 如果文件已存在则删除（准备覆盖）
    if os.path.exists(args.results_file):
        os.remove(args.results_file)

    logging.info("Loading SentenceBERT model...")
    logging.info(f"Model: {args.model}, Batch size: {args.batch_size}")
    
    # 配置 HuggingFace 下载（支持镜像站和离线模式）
    # 1. 检查是否应该使用离线模式（在设置镜像之前）
    cache_dir = os.path.expanduser('~/.cache/huggingface/hub')
    model_cache_name = args.model.replace('/', '--')
    model_cache_path = os.path.join(cache_dir, f'models--{model_cache_name}')
    
    use_offline = False
    local_model_path = None
    
    if os.getenv('OFFLINE_MODE') == '1':
        use_offline = True
        logging.info(f"强制离线模式（OFFLINE_MODE=1）")
    elif os.path.exists(model_cache_path):
        # 检查缓存目录是否包含必要的文件（snapshots 目录）
        snapshots_dir = os.path.join(model_cache_path, 'snapshots')
        if os.path.exists(snapshots_dir) and os.listdir(snapshots_dir):
            use_offline = True
            logging.info(f"检测到模型缓存，使用离线模式: {args.model}")
    
    # 2. 如果使用离线模式，尝试找到本地模型路径
    if use_offline:
        # 设置离线模式环境变量（必须在导入 SentenceTransformer 之前）
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
        os.environ['HF_HUB_OFFLINE'] = '1'
        # 确保不会尝试网络请求
        os.environ['HF_HUB_DISABLE_EXPERIMENTAL_WARNING'] = '1'
        
        # 查找本地模型路径（使用 snapshots 目录中的实际路径）
        if os.path.exists(model_cache_path):
            snapshots_dir = os.path.join(model_cache_path, 'snapshots')
            if os.path.exists(snapshots_dir):
                snapshot_dirs = [d for d in os.listdir(snapshots_dir) 
                               if os.path.isdir(os.path.join(snapshots_dir, d))]
                if snapshot_dirs:
                    # 使用最新的快照目录
                    local_model_path = os.path.join(snapshots_dir, snapshot_dirs[0])
                    logging.info(f"使用本地模型路径: {local_model_path}")
                else:
                    logging.warning(f"快照目录为空，将使用模型名称（可能触发网络请求）")
            else:
                logging.warning(f"快照目录不存在，将使用模型名称（可能触发网络请求）")
        else:
            logging.warning(f"模型缓存目录不存在，将使用模型名称（可能触发网络请求）")
    else:
        # 如果没有设置镜像，使用默认镜像站（国内用户友好）
        if not os.getenv('HF_ENDPOINT'):
            os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
        logging.info(f"从 {os.getenv('HF_ENDPOINT', 'huggingface.co')} 下载模型: {args.model}")
    
    # 3. 现在才初始化模型（此时环境变量已设置）
    try:
        # 如果找到了本地路径，优先使用本地路径（完全避免网络请求）
        model_name_or_path = local_model_path if local_model_path else args.model
        model = DRES(
            models.SentenceBERT(model_name_or_path),
            batch_size=args.batch_size,
            corpus_chunk_size=512*9999
        )
        if use_offline and local_model_path:
            logging.info(f"✓ 已从本地路径加载模型，无网络请求")
    except Exception as e:
        if use_offline:
            logging.error(f"离线模式加载失败: {e}")
            logging.error("可能原因：模型缓存不完整，请重新下载模型")
            logging.error("解决方法：运行 'python retrieve/download_model_complete.py' 完整下载模型")
            logging.error("或者删除缓存目录或设置 OFFLINE_MODE=0 重新下载")
        raise
    retriever = EvaluateRetrieval(model, score_function="dot")
    logging.info("Model loaded successfully")

    # 只处理 repoeval 数据集
    if not args.dataset.startswith("repoeval"):
        raise ValueError(f"`dataset` should start with 'repoeval', got: {args.dataset}")
    
    all_eval_results = []
    
    # 自动查找 query 目录（如果未指定）
    query_dir = args.query_dir
    if not query_dir:
        query_dir = find_query_dir_for_dataset(args.dataset)
        if query_dir:
            logging.info(f"Auto-detected query directory: {query_dir}")
        else:
            logging.info(f"No query directory found for dataset: {args.dataset}, will use BEIR format")
    
    # 确定数据基础目录
    if args.data_base_dir:
        data_base_dir = args.data_base_dir
    else:
        # 默认使用项目根目录下的 dataset/BEIR_data（包含 corpus.jsonl 等 BEIR 文件）
        script_dir = Path(__file__).resolve().parent
        project_root = script_dir.parent
        beir_data_dir = project_root / "dataset" / "BEIR_data"
        if beir_data_dir.exists():
            data_base_dir = str(beir_data_dir)
        else:
            # 如果 BEIR_data 不存在，尝试 output/stable_data
            stable_data_dir = project_root / "output" / "stable_data"
            if stable_data_dir.exists():
                data_base_dir = str(stable_data_dir)
            else:
                data_base_dir = str(project_root / "output")
    
    logging.info(f"Data base directory: {data_base_dir}")
    
    # 检查数据目录是否存在
    if not os.path.exists(data_base_dir):
        raise FileNotFoundError(f"Data base directory does not exist: {data_base_dir}")
    
    # 匹配逻辑：支持完全匹配或以下划线开头
    # 如果 args.dataset 本身已经以下划线结尾，则完全匹配；否则匹配 args.dataset_ 开头的目录
    instance_list = [i for i in os.listdir(data_base_dir) 
                     if os.path.isdir(os.path.join(data_base_dir, i)) and 
                     (i == args.dataset or i.startswith(f"{args.dataset.rstrip('_')}_"))]
    
    if not instance_list:
        # 尝试在其他可能的位置查找
        script_dir = Path(__file__).resolve().parent
        project_root = script_dir.parent
        
        # 如果当前不在 BEIR_data 下，尝试 BEIR_data
        if "BEIR_data" not in data_base_dir:
            beir_data_dir = project_root / "dataset" / "BEIR_data"
            if beir_data_dir.exists():
                logging.info(f"No matching directories in {data_base_dir}, trying BEIR_data: {beir_data_dir}")
                instance_list = [i for i in os.listdir(beir_data_dir) 
                               if os.path.isdir(beir_data_dir / i) and 
                               (i == args.dataset or i.startswith(f"{args.dataset.rstrip('_')}_"))]
                if instance_list:
                    data_base_dir = str(beir_data_dir)
                    logging.info(f"Found matching directories in BEIR_data: {data_base_dir}")
        
        # 如果还是找不到，尝试在 output/stable_data 下查找
        if not instance_list and "stable_data" not in data_base_dir:
            stable_data_dir = project_root / "output" / "stable_data"
            if stable_data_dir.exists():
                logging.info(f"No matching directories, trying stable_data: {stable_data_dir}")
                instance_list = [i for i in os.listdir(stable_data_dir) 
                               if os.path.isdir(stable_data_dir / i) and 
                               (i == args.dataset or i.startswith(f"{args.dataset.rstrip('_')}_"))]
                if instance_list:
                    data_base_dir = str(stable_data_dir)
                    logging.info(f"Found matching directories in stable_data: {data_base_dir}")
        
        if not instance_list:
            # 列出所有可用的目录，帮助调试
            available_dirs = [d for d in os.listdir(data_base_dir) if os.path.isdir(os.path.join(data_base_dir, d))]
            logging.error(f"Available directories in {data_base_dir}: {available_dirs[:10]}...")  # 只显示前10个
            raise ValueError(f"No matching data directories found in {data_base_dir} for dataset: {args.dataset}")
    
    processed_instances = 0  # 记录成功处理的实例数
    
    for ins_dir in tqdm(instance_list):
        logging.info("Instance Repo: {}".format(ins_dir))
        
        # 加载数据
        data_folder = os.path.join(data_base_dir, ins_dir)
        logging.info(f"Loading data from: {data_folder}")
        
        # 检查必要的 BEIR 文件是否存在
        corpus_file = os.path.join(data_folder, "corpus.jsonl")
        if not os.path.exists(corpus_file):
            error_msg = f"Corpus file not found: {corpus_file}. BEIR format files (corpus.jsonl, queries.jsonl, qrels.jsonl) are required for retrieval."
            logging.error(error_msg)
            # 如果使用新格式查询，必须要有 corpus.jsonl，否则抛出异常
            if query_dir:
                raise FileNotFoundError(error_msg)
            else:
                # 旧格式：只记录警告并跳过
                logging.warning(f"Skipping instance {ins_dir}")
                continue
        
        try:
            corpus, queries_beir, qrels = GenericDataLoader(
                data_folder=data_folder
            ).load(split="test")
        except Exception as e:
            logging.error(f"Failed to load BEIR data from {data_folder}: {e}")
            logging.error(f"Required files: corpus.jsonl, queries.jsonl, qrels.jsonl")
            raise
        
        # 根据是否找到 query_dir 决定使用哪种格式
        use_new_format = False
        query_data = {}
        
        if query_dir:
            # 新格式：从 query 目录加载
            query_data = load_queries_from_query_dir(query_dir)
            if not query_data:
                logging.warning(f"No query data loaded from {query_dir}, falling back to BEIR format")
                queries = queries_beir
            else:
                # 新格式：分别用 provide_code 和 requirement 做两次检索，合并结果并去重
                queries_provide = {task_id: data["provide_code"] for task_id, data in query_data.items()}
                queries_requirement = {task_id: data["requirement"] for task_id, data in query_data.items()}
                use_new_format = True
                logging.info(f"Instance #{ins_dir}: #{len(corpus)} corpus, #{len(queries_provide)} queries (new format, dual retrieval)")
        else:
            # 旧格式：使用 BEIR queries
            queries = queries_beir
            logging.info(f"Instance #{ins_dir}: #{len(corpus)} corpus, #{len(queries)} queries (BEIR format)")

        logging.info("Starting retrieval...")
        start_time = time()
        if use_new_format:
            # 两次检索：provide_code 与 requirement
            for q_dict in (queries_provide, queries_requirement):
                if len(q_dict) == 1:
                    q_dict.update({"dummy": "dummy"})
            logging.info(f"Retrieving by provide_code for {len(queries_provide)} queries...")
            results_provide = retriever.retrieve(corpus, queries_provide)
            logging.info(f"Retrieving by requirement for {len(queries_requirement)} queries...")
            results_requirement = retriever.retrieve(corpus, queries_requirement)
            for q_dict in (queries_provide, queries_requirement):
                if "dummy" in q_dict:
                    q_dict.pop("dummy")
                    results_provide.pop("dummy", None)
                    results_requirement.pop("dummy", None)
            # 合并两次检索结果并去重（同一 doc_id 保留较高分）
            results = {}
            for task_id in query_data:
                rp = results_provide.get(task_id, {})
                rq = results_requirement.get(task_id, {})
                merged = dict(rp)
                for doc_id, score in rq.items():
                    merged[doc_id] = max(merged.get(doc_id, 0), score)
                results[task_id] = merged
        else:
            if len(queries) == 1:
                queries.update({"dummy": "dummy"})
            logging.info(f"Retrieving for {len(queries)} queries against {len(corpus)} documents...")
            results = retriever.retrieve(corpus, queries)
            if "dummy" in queries:
                queries.pop("dummy")
                results.pop("dummy")
        end_time = time()
        logging.info("Retrieval completed. Time taken: {:.2f} seconds".format(end_time - start_time))

        # 根据格式处理检索结果
        if use_new_format:
            # 新格式：直接从 query_data 构建结果
            logging.info(f"Processing {len(query_data)} queries...")
            dataset = []
            for idx, (task_id, data) in enumerate(query_data.items(), 1):
                # 检查 task_id 是否在检索结果中（get_top_docs 内部也会检查，但这里提前过滤）
                if task_id not in results:
                    logging.warning(f"Task {task_id} not found in retrieval results, skipping")
                    continue
                docs = get_top_docs(results=results, corpus=corpus, task_id=task_id)
                dataset.append({
                    "requirement": data["requirement"],
                    "provide_code": data["provide_code"],
                    "function_name": data.get("function_name", task_id),  # 保存 function_name 字段
                    "docs": docs,
                    "task_id": task_id
                })
                if idx % 10 == 0:
                    logging.info(f"Processed {idx}/{len(query_data)} queries...")
            logging.info(f"Processed all {len(dataset)} queries successfully")
        else:
            # 旧格式：从 dataset_path 读取 tasks
            tasks = [json.loads(line.strip()) for line in open(args.dataset_path, 'r')]
            prompts, references, docs, metadatas = [], [], [], []
            for task in tasks:
                if task["metadata"]["task_id"] not in queries: continue
                prompts.append(task["prompt"]) # save full prompt
                references.append(task["metadata"]["ground_truth"])
                docs.append(get_top_docs(
                    results=results, corpus=corpus, task_id=task["metadata"]["task_id"],
                ))
                metadatas.append(task["metadata"])
            assert len(prompts) == len(references) == len(docs)
            dataset = [
                {"prompt": p, "reference": r, "docs": d, "metadata":m}
                for p,r,d,m in zip(prompts, references, docs, metadatas)
            ]
        
        with open(args.results_file, "a") as fout:
            for curr in dataset:
                fout.write(json.dumps(curr) + "\n")

        # evaluate retrieval results
        # 如果使用新格式，qrels 中的 query_id 可能与 task_id 不匹配，跳过评估
        if use_new_format:
            logging.info("Using new format - skipping evaluation (qrels may not match task_ids)")
            # 对于新格式，不进行评估，只记录检索时间
            eval_results = {
                "time": end_time - start_time,
                "note": "New format - evaluation skipped"
            }
            logging.info(f"Instance #{ins_dir}: Retrieval completed in {end_time - start_time:.2f} seconds")
        elif len(qrels) == 0:
            logging.info("No qrels found for this dataset - skipping evaluation")
            eval_results = {
                "time": end_time - start_time,
                "note": "No qrels - evaluation skipped"
            }
        else:
            logging.info("Retriever evaluation for k in: {}".format(retriever.k_values))
            try:
                ndcg, _map, recall, precision = retriever.evaluate(qrels, results, retriever.k_values)
                mrr = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="mrr")
                eval_results = {
                    "ndcg": ndcg, "mrr": mrr,
                    "recall": recall, "precision": precision,
                    "time": end_time - start_time
                }
                logging.info(f"Instance #{ins_dir}: {eval_results}")
            except Exception as e:
                logging.warning(f"Evaluation failed: {e}, skipping evaluation")
                eval_results = {
                    "time": end_time - start_time,
                    "note": f"Evaluation failed: {str(e)}"
                }
        
        all_eval_results.append(eval_results)
        processed_instances += 1  # 记录成功处理的实例
        
        with open(args.output_file + "_all", "w") as f:
            json.dump(all_eval_results, f)

    # 检查是否有实例被成功处理
    if processed_instances == 0:
        error_msg = f"No instances were successfully processed. Check if corpus.jsonl files exist in the data directories."
        logging.error(error_msg)
        raise RuntimeError(error_msg)
    
    # 计算平均评估结果（只计算有评估指标的结果）
    if all_eval_results:
        # 过滤出有评估指标的结果（排除只有 time 和 note 的结果）
        eval_results_with_metrics = [e for e in all_eval_results if "ndcg" in e or "recall" in e]
        
        if eval_results_with_metrics:
            avg_eval_results = {}
            for k,v_dict in eval_results_with_metrics[0].items():
                if k in ["time", "note"]:
                    continue  # 跳过时间和备注
                if isinstance(v_dict, dict):
                    avg_v_dict = {}
                    for vk,vv in v_dict.items():
                        avg_vv = sum([e[k][vk] for e in eval_results_with_metrics])/len(eval_results_with_metrics)
                        avg_v_dict[vk] = avg_vv
                    avg_eval_results.update(avg_v_dict)
                elif isinstance(v_dict, (int, float)):
                    avg_v = sum([e[k] for e in eval_results_with_metrics])/len(eval_results_with_metrics)
                    avg_eval_results[k] = avg_v
            
            # 添加平均时间
            avg_time = sum([e.get("time", 0) for e in all_eval_results])/len(all_eval_results)
            avg_eval_results["avg_time"] = avg_time
            
            print("Average Eval Results: ", avg_eval_results)
            with open(args.output_file, "w") as f:
                json.dump(avg_eval_results, f)
        else:
            # 如果没有评估指标，只保存时间统计
            avg_time = sum([e.get("time", 0) for e in all_eval_results])/len(all_eval_results)
            summary = {
                "avg_time": avg_time,
                "total_instances": len(all_eval_results),
                "note": "No evaluation metrics available (using new format or no qrels)"
            }
            print("Summary: ", summary)
            with open(args.output_file, "w") as f:
                json.dump(summary, f)

if __name__ == "__main__":
    main()
