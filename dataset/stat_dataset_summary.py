import argparse
import json
import re
from pathlib import Path
from typing import DefaultDict, Dict, List, Set, Tuple


def tokenize(text: str) -> List[str]:
    """
    使用通用正则切分 token：
    - 连续字母/数字/下划线作为一个 token
    - 标点符号作为独立 token
    """
    if not text:
        return []
    return re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)


def average(values: List[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def count_file_lines(file_path: Path) -> int:
    # 采用二进制读取，按换行符统计行数，避免编码差异影响
    with file_path.open("rb") as f:
        content = f.read()
    if not content:
        return 0
    return content.count(b"\n") + (0 if content.endswith(b"\n") else 1)


_VAR_BLOCK_RE = re.compile(
    r"(?ims)^\s*(VAR_INPUT|VAR_OUTPUT)\s*$([\s\S]*?)^\s*END_VAR\s*$"
)


def _count_st_decl_lines(block_body: str) -> int:
    """
    统计 ST 变量声明行数（近似参数个数）。

    规则（偏鲁棒，适配当前数据集 provide_code）：
    - 按行处理，去掉行内注释 (* ... *) 与 // ...
    - 忽略空行、仅包含分号/逗号的行
    - 认为包含 ':' 且以 ';' 结束的行是一个声明（如 a: INT;）
    - 不尝试展开同一行多变量（数据集中通常一行一个声明）
    """

    def strip_inline_comments(line: str) -> str:
        line = re.sub(r"\(\*.*?\*\)", "", line)
        line = re.sub(r"//.*$", "", line)
        return line

    count = 0
    for raw in block_body.splitlines():
        line = strip_inline_comments(raw).strip()
        if not line:
            continue
        if line in {";", ","}:
            continue
        if ":" in line and line.endswith(";"):
            count += 1
    return count


def count_st_io_params(provide_code: str) -> Tuple[int, int]:
    """
    从 provide_code 中提取 VAR_INPUT / VAR_OUTPUT 的参数个数。
    未出现的区块按 0 处理。
    """
    if not provide_code:
        return 0, 0

    input_count = 0
    output_count = 0
    for m in _VAR_BLOCK_RE.finditer(provide_code):
        block_type = m.group(1).upper()
        body = m.group(2) or ""
        if block_type == "VAR_INPUT":
            input_count += _count_st_decl_lines(body)
        elif block_type == "VAR_OUTPUT":
            output_count += _count_st_decl_lines(body)

    return input_count, output_count


def resolve_effective_gt_files(query_dir: Path, gt_dir: Path) -> Tuple[List[Path], List[str]]:
    """
    基于 query 文件确定需要纳入统计的 ground truth 文件：
    query/repoeval_xxx/Func.json -> generation_context_ground_truth/xxx/Func.st
    """
    matched: Set[Path] = set()
    missing: List[str] = []

    for query_path in query_dir.rglob("*.json"):
        if not query_path.is_file():
            continue

        rel = query_path.relative_to(query_dir)
        if not rel.parts:
            continue
        category = rel.parts[0]
        if category.startswith("repoeval_"):
            category = category[len("repoeval_") :]

        expected_gt = gt_dir / category / f"{query_path.stem}.st"
        if expected_gt.exists():
            matched.add(expected_gt.resolve())
        else:
            missing.append(str(rel))

    return sorted(matched), sorted(missing)


def stats_generation_context_by_query(query_dir: Path, gt_dir: Path) -> Dict[str, object]:
    effective_gt_files, missing_query_files = resolve_effective_gt_files(query_dir, gt_dir)
    line_counts = [count_file_lines(path) for path in effective_gt_files]

    from collections import defaultdict

    per_project_line_counts: DefaultDict[str, List[int]] = defaultdict(list)
    for gt_path in effective_gt_files:
        try:
            rel = gt_path.relative_to(gt_dir)
            project = rel.parts[0] if rel.parts else "unknown"
        except Exception:
            project = "unknown"
        per_project_line_counts[project].append(count_file_lines(gt_path))

    lines_by_project: Dict[str, Dict[str, object]] = {}
    for project in sorted(per_project_line_counts.keys()):
        counts = per_project_line_counts[project]
        lines_by_project[project] = {
            "file_count": len(counts),
            "lines_total": int(sum(counts)) if counts else 0,
            "lines_avg_per_file": average([float(x) for x in counts]),
        }

    return {
        "effective_file_count": len(effective_gt_files),
        "average_lines_per_file": average([float(x) for x in line_counts]),
        "effective_lines_by_project": lines_by_project,
        "missing_match_count": len(missing_query_files),
        "missing_query_files": missing_query_files,
    }


def stats_query(query_dir: Path) -> Dict[str, object]:
    token_lengths: List[int] = []
    colon_counts: List[int] = []
    input_param_counts: List[int] = []
    output_param_counts: List[int] = []
    json_file_count = 0

    from collections import defaultdict

    per_project_inputs: DefaultDict[str, List[int]] = defaultdict(list)
    per_project_outputs: DefaultDict[str, List[int]] = defaultdict(list)
    per_project_requirement_token_lengths: DefaultDict[str, List[int]] = defaultdict(list)

    for path in query_dir.rglob("*.json"):
        if not path.is_file():
            continue
        json_file_count += 1
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            # 遇到无法解析的文件时跳过，保证统计脚本可持续运行
            continue

        # 兼容 requirement 以及拼写错误 rquirement
        requirement = data.get("requirement", data.get("rquirement", ""))
        provide_code = data.get("provide_code", "")

        if isinstance(requirement, str):
            req_tokens = len(tokenize(requirement))
            token_lengths.append(req_tokens)
        if isinstance(provide_code, str):
            colon_counts.append(provide_code.count(":"))
            in_cnt, out_cnt = count_st_io_params(provide_code)
            input_param_counts.append(in_cnt)
            output_param_counts.append(out_cnt)

            rel = path.relative_to(query_dir)
            project = rel.parts[0] if rel.parts else "unknown"
            if project.startswith("repoeval_"):
                project = project[len("repoeval_") :]
            per_project_inputs[project].append(in_cnt)
            per_project_outputs[project].append(out_cnt)
            if isinstance(requirement, str):
                per_project_requirement_token_lengths[project].append(req_tokens)

    provide_code_params_by_project: Dict[str, Dict[str, object]] = {}
    for project in sorted(set(per_project_inputs.keys()) | set(per_project_outputs.keys())):
        ins = per_project_inputs.get(project, [])
        outs = per_project_outputs.get(project, [])
        file_count = max(len(ins), len(outs))
        avg_in = average([float(x) for x in ins])
        avg_out = average([float(x) for x in outs])
        in_total = int(sum(ins)) if ins else 0
        out_total = int(sum(outs)) if outs else 0
        provide_code_params_by_project[project] = {
            "file_count": file_count,
            "avg_input_param_count": avg_in,
            "avg_output_param_count": avg_out,
            "avg_param_count": avg_in + avg_out,
            "input_param_total": in_total,
            "output_param_total": out_total,
            "param_total": in_total + out_total,
        }

    requirement_tokens_by_project: Dict[str, Dict[str, object]] = {}
    for project in sorted(per_project_requirement_token_lengths.keys()):
        lens = per_project_requirement_token_lengths[project]
        requirement_tokens_by_project[project] = {
            "file_count": len(lens),
            "token_total": int(sum(lens)) if lens else 0,
            "token_avg_length": average([float(x) for x in lens]),
        }

    avg_input = average([float(x) for x in input_param_counts])
    avg_output = average([float(x) for x in output_param_counts])
    return {
        "query_json_file_count": json_file_count,
        "requirement_token_avg_length": average([float(x) for x in token_lengths]),
        "requirement_token_total": int(sum(token_lengths)) if token_lengths else 0,
        "requirement_sample_count": len(token_lengths),
        "requirement_tokens_by_project": requirement_tokens_by_project,
        "provide_code_colon_avg_count": average([float(x) for x in colon_counts]),
        "provide_code_sample_count": len(colon_counts),
        "provide_code_input_param_avg_count": avg_input,
        "provide_code_output_param_avg_count": avg_output,
        "provide_code_param_avg_count": avg_input + avg_output,
        "provide_code_params_by_project": provide_code_params_by_project,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="统计 dataset 目录的基础指标并输出为 JSON")
    parser.add_argument(
        "--dataset-dir",
        default=str(Path(__file__).resolve().parent),
        help="dataset 根目录，默认是当前脚本所在目录",
    )
    parser.add_argument(
        "--output",
        default="dataset_stats_summary.json",
        help="输出 JSON 文件名（相对 --dataset-dir）或绝对路径",
    )
    args = parser.parse_args()

    dataset_dir = Path(args.dataset_dir).resolve()
    gt_dir = dataset_dir / "generation_context_ground_truth"
    query_dir = dataset_dir / "query"

    gt_stats = stats_generation_context_by_query(query_dir, gt_dir)
    query_stats = stats_query(query_dir)

    result = {
        "dataset_dir": str(dataset_dir),
        "generation_context_ground_truth": {
            "directory": str(gt_dir),
            **gt_stats,
        },
        "query": {
            "directory": str(query_dir),
            **query_stats,
        },
    }

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = dataset_dir / output_path

    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"统计完成，结果已写入: {output_path}")


if __name__ == "__main__":
    main()
