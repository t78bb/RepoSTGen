"""
从经验库中按模糊类型频率统计，取频率最高的前 top_k 类，每类随机取 per_type 条，返回子集供追问使用。
"""
import random
from typing import Any, Dict, List, Optional


def sample_knowledge_base_by_frequency(
    knowledge_base: Dict[str, List[Dict[str, Any]]],
    top_k_types: int = 5,
    per_type_samples: int = 5,
    random_seed: Optional[int] = None,
) -> Dict[str, List[Dict[str, Any]]]:
    """
    统计 knowledge_base 中各模糊类型的数量，取频率最多的前 top_k_types 类，
    每类随机抽取 per_type_samples 条，返回与 knowledge_base 同结构的子集。

    Args:
        knowledge_base: 经验库，格式为 { "模糊类型名": [ {"模糊点描述", "精准需求示例", "case_id", ...}, ... ], ... }
        top_k_types: 取频率最高的前几类，默认 5
        per_type_samples: 每类随机取几条，默认 5
        random_seed: 随机种子，便于复现

    Returns:
        新字典，键为选中的类型名，值为该类型下随机抽取的条目列表（最多 per_type_samples 条）
    """
    if not knowledge_base:
        return {}

    if random_seed is not None:
        random.seed(random_seed)

    # 统计各类型数量（只统计非空列表）
    type_counts = [
        (t, len(items))
        for t, items in knowledge_base.items()
        if items and isinstance(items, list)
    ]
    if not type_counts:
        return {}

    # 按数量降序，取前 top_k_types 类
    type_counts.sort(key=lambda x: -x[1])
    top_types = [t for t, _ in type_counts[:top_k_types]]

    result: Dict[str, List[Dict[str, Any]]] = {}
    for t in top_types:
        items = knowledge_base[t]
        if len(items) <= per_type_samples:
            chosen = list(items)
        else:
            chosen = random.sample(items, per_type_samples)
        result[t] = chosen

    return result
