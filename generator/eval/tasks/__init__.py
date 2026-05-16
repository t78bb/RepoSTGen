import inspect
from pprint import pprint

from . import repoeval

# 精简版：仅保留 RepoEval 任务
TASK_REGISTRY = {
    **repoeval.create_all_tasks(),
}

ALL_TASKS = sorted(list(TASK_REGISTRY))


def get_task(task_name, args):
    kwargs = {}
    if args.dataset_path is not None:
        kwargs["dataset_path"] = args.dataset_path
    if args.dataset_name is not None:
        kwargs["dataset_name"] = args.dataset_name
    if args.data_files is not None:
        kwargs["data_files"] = args.data_files
    kwargs["cache_dir"] = args.cache_dir
    if task_name == "repoeval-function":
        kwargs["args"] = args
    kwargs["topk_docs"] = args.topk_docs
    kwargs["tokenizer"] = args.tokenizer if hasattr(args, "tokenizer") else None
    return TASK_REGISTRY[task_name](**kwargs)
