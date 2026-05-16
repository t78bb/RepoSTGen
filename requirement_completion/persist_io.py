#!/usr/bin/env python3
"""
落盘中间结果：所有写入 requirement_completion 下的逻辑集中在此文件。

主要落盘内容：
1. user_prompt — 发给模型的用户侧 prompt（按 case 或按项目保存）
2. result — 单条或整批的解析结果（是否需要追问、追问列表等）

目录约定（均在 requirement_completion 下）：
  output/
    [run_id]/                    # 可选，同一批用同一 run_id 便于对齐
      prompts/
        {project_name}/
          {case_id}.txt          # 单 case 的 user_prompt
        {project_name}.txt       # 或整项目一个 prompt 文件（按需）
      results/
        {project_name}/
          {case_id}.json         # 单 case 的结果
        {project_name}.json      # 或整项目一批 results 列表
  若未传 run_id，则使用 output/default/ 或 output/ 下直接 prompts/results。
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 模块所在目录
REQUIREMENT_COMPLETION_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = REQUIREMENT_COMPLETION_DIR / "output"


def _run_subdir(run_id: Optional[str]) -> Path:
    """返回 output 下的子目录，带或不带 run_id。"""
    if run_id:
        return DEFAULT_OUTPUT_DIR / run_id
    return DEFAULT_OUTPUT_DIR / "default"


def get_prompts_dir(project_name: str, run_id: Optional[str] = None) -> Path:
    """返回某项目下 prompts 的落盘目录（不创建）。"""
    return _run_subdir(run_id) / "prompts" / project_name


def get_results_dir(project_name: str, run_id: Optional[str] = None) -> Path:
    """返回某项目下 results 的落盘目录（不创建）。"""
    return _run_subdir(run_id) / "results" / project_name


def _safe_case_id(case_id: str) -> str:
    """将 case_id 转为可作文件名的字符串（如 project/name -> project_name）。"""
    return case_id.replace("/", "_").replace("\\", "_")


def save_user_prompt(
    project_name: str,
    case_id: str,
    user_prompt: str,
    run_id: Optional[str] = None,
) -> Path:
    """
    保存发给模型的 user_prompt（单条 case）。

    Args:
        project_name: 项目名，如 repoeval_isScaleOutput
        case_id: 如 repoeval_isScaleOutput/F_isScaleOutput
        user_prompt: 完整用户侧 prompt 文本
        run_id: 可选，同一批运行共用一个 run_id

    Returns:
        落盘文件的路径
    """
    base = get_prompts_dir(project_name, run_id)
    base.mkdir(parents=True, exist_ok=True)
    safe = _safe_case_id(case_id)
    path = base / f"{safe}.txt"
    path.write_text(user_prompt, encoding="utf-8")
    return path


def save_user_prompt_project(
    project_name: str,
    prompts: Dict[str, str],
    run_id: Optional[str] = None,
) -> Path:
    """
    批量保存同一项目下多个 case 的 user_prompt。
    prompts: { case_id -> user_prompt 文本 }
    落盘为同一目录下多个 .txt，或一个 JSON（key 为 case_id）。这里采用每个 case 一个 .txt，便于单条查看。
    """
    base = get_prompts_dir(project_name, run_id)
    base.mkdir(parents=True, exist_ok=True)
    for cid, text in prompts.items():
        safe = _safe_case_id(cid)
        (base / f"{safe}.txt").write_text(text, encoding="utf-8")
    return base


def save_result(
    project_name: str,
    case_id: str,
    result: Dict[str, Any],
    run_id: Optional[str] = None,
) -> Path:
    """
    保存单条 case 的解析结果（是否需要追问、追问列表等）。

    Args:
        project_name: 项目名
        case_id: case 标识
        result: 解析后的 dict（可含 case_id, 是否需要追问, 追问列表 等）
        run_id: 可选

    Returns:
        落盘 JSON 路径
    """
    base = get_results_dir(project_name, run_id)
    base.mkdir(parents=True, exist_ok=True)
    safe = _safe_case_id(case_id)
    path = base / f"{safe}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return path


def save_results_batch(
    project_name: str,
    results: List[Dict[str, Any]],
    run_id: Optional[str] = None,
) -> Path:
    """
    保存整批 results（如 run_for_project 返回的 list）为一个 JSON 文件。

    Returns:
        落盘 JSON 路径，如 output/[run_id]/results/repoeval_xxx/repoeval_xxx.json
    """
    base = _run_subdir(run_id) / "results"
    base.mkdir(parents=True, exist_ok=True)
    path = base / f"{project_name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return path


def make_run_id() -> str:
    """生成一次运行 ID（时间戳），便于同一批 prompt 与 result 对齐。"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")
