import argparse
import json
import os
import re
from pathlib import Path
from typing import Optional

from verifier.codesys_debug import CodesysCompiler


# 与 verifier/auto_fix_st_code.py 保持一致的默认地址
DEFAULT_CODESYS_API_URL = os.getenv(
    "CODESYS_API_URL",
    "http://192.168.2.112:9000/api/v1/pou/new_project_workflow",
)

# 与 full_process.py 中 run_fix 的默认工程根目录保持一致
DEFAULT_PROJECTS_ROOT = Path(r"F:\codesys_call\CODESYSCompileService-main\projects")


def extract_block_name(st_code: str) -> str:
    """
    按 auto_fix_st_code.py 的思路提取块名：
    - 先去掉 // 单行注释
    - 匹配 FUNCTION_BLOCK / PROGRAM / FUNCTION / METHOD 后的标识符
    """
    code_without_comments = re.sub(r"//.*?$", "", st_code, flags=re.MULTILINE | re.IGNORECASE)
    match = re.search(
        r"(?:FUNCTION_BLOCK|PROGRAM|FUNCTION|METHOD)\s+(?:PUBLIC\s+)?(\w+)(?=\s|[:;])",
        code_without_comments,
        re.IGNORECASE | re.MULTILINE,
    )
    return match.group(1) if match else "TestBlock"


def infer_codesys_project_name(output_project_dir_name: str) -> str:
    """仿照 full_process.py：repoeval_xxx -> xxx。"""
    if output_project_dir_name.startswith("repoeval_"):
        return output_project_dir_name[len("repoeval_") :]
    return output_project_dir_name


def syntax_check_one_file(
    compiler: CodesysCompiler,
    st_file: Path,
    codesys_project_path: Path,
    ip_port: str,
) -> dict:
    st_code = st_file.read_text(encoding="utf-8")
    block_name = extract_block_name(st_code)
    check_result = compiler.syntax_check(str(codesys_project_path), block_name, st_code, ip_port)

    # 参考 auto_fix_st_code.py：success=True 或 errors=[] 视为通过
    no_error = bool(check_result.success) or len(check_result.errors or []) == 0

    error_items = []
    for err in check_result.errors or []:
        error_items.append(
            {
                "error_type": getattr(err, "error_type", None),
                "error_desc": getattr(err, "error_desc", None),
                "line_no": getattr(err, "line_no", None),
                "line_content": getattr(err, "line_content", None),
            }
        )

    return {
        "st_file": str(st_file),
        "block_name": block_name,
        "success": no_error,
        "raw_success": bool(check_result.success),
        "error_count": len(error_items),
        "errors": error_items,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "对 output 下指定子目录的各项目 readful_result/*.st 做 syntax_check，"
            "仅检查是否有编译错误，不做修复。"
        )
    )
    parser.add_argument("output_subdir", type=str, help="output 下的子目录名，如 20260301_全流程消融retrieve")
    parser.add_argument(
        "--output-root",
        type=str,
        default="output",
        help="output 根目录（默认: output）",
    )
    parser.add_argument(
        "--projects-root",
        type=str,
        default=str(DEFAULT_PROJECTS_ROOT),
        help="Codesys .project 根目录（默认: F:\\codesys_call\\CODESYSCompileService-main\\projects）",
    )
    parser.add_argument(
        "--ip-port",
        type=str,
        default=DEFAULT_CODESYS_API_URL,
        help=f"Codesys API 地址（默认: {DEFAULT_CODESYS_API_URL}）",
    )
    parser.add_argument(
        "--save-report",
        action="store_true",
        default=True,
        help="将检查结果保存为 JSON 报告到 output 子目录下（默认开启）",
    )
    parser.add_argument(
        "--no-save-report",
        dest="save_report",
        action="store_false",
        help="不保存 JSON 报告",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    output_root = Path(args.output_root)
    if not output_root.is_absolute():
        output_root = script_dir / output_root
    target_root = output_root / args.output_subdir
    projects_root = Path(args.projects_root)

    if not target_root.exists() or not target_root.is_dir():
        print(f"错误: 指定目录不存在或不是目录: {target_root}")
        return 1

    compiler = CodesysCompiler()
    report = {
        "target_root": str(target_root),
        "projects_root": str(projects_root),
        "ip_port": args.ip_port,
        "projects": [],
    }

    total_projects = 0
    checked_projects = 0
    total_files = 0
    failed_files = 0

    project_dirs = sorted([p for p in target_root.iterdir() if p.is_dir()], key=lambda p: p.name)
    if not project_dirs:
        print(f"警告: 目录下没有项目子目录: {target_root}")
        return 0

    print("=" * 80)
    print("批量 syntax_check（仅检查，不修复）")
    print("=" * 80)
    print(f"目标目录: {target_root}")
    print(f"项目目录数: {len(project_dirs)}")
    print(f"Codesys API: {args.ip_port}")
    print(f"Codesys 工程根目录: {projects_root}")

    for project_dir in project_dirs:
        total_projects += 1
        readful_result_dir = project_dir / "readful_result"
        if not readful_result_dir.exists() or not readful_result_dir.is_dir():
            print(f"\n[跳过] {project_dir.name}: 缺少 readful_result 目录")
            report["projects"].append(
                {
                    "project_dir": str(project_dir),
                    "skipped": True,
                    "reason": "missing readful_result",
                    "files": [],
                }
            )
            continue

        st_files = sorted(readful_result_dir.glob("*.st"), key=lambda p: p.name)
        if not st_files:
            print(f"\n[跳过] {project_dir.name}: readful_result 下没有 .st 文件")
            report["projects"].append(
                {
                    "project_dir": str(project_dir),
                    "skipped": True,
                    "reason": "no .st files",
                    "files": [],
                }
            )
            continue

        checked_projects += 1
        inferred_project = infer_codesys_project_name(project_dir.name)
        codesys_project_path = projects_root / f"{inferred_project}.project"
        print(f"\n[{checked_projects}] 项目: {project_dir.name}")
        print(f"    Codesys 工程: {codesys_project_path}")
        if not codesys_project_path.exists():
            print("    ⚠ 警告: 对应 .project 文件不存在，仍将继续调用 syntax_check")

        project_result = {
            "project_dir": str(project_dir),
            "codesys_project_path": str(codesys_project_path),
            "skipped": False,
            "files": [],
        }

        project_fail_count = 0
        for st_file in st_files:
            total_files += 1
            file_result = syntax_check_one_file(
                compiler=compiler,
                st_file=st_file,
                codesys_project_path=codesys_project_path,
                ip_port=args.ip_port,
            )
            project_result["files"].append(file_result)

            if file_result["success"]:
                print(f"    ✓ {st_file.name} 通过")
            else:
                failed_files += 1
                project_fail_count += 1
                print(f"    ✗ {st_file.name} 失败（错误数: {file_result['error_count']}）")
                for idx, err in enumerate(file_result["errors"], 1):
                    print(f"      [{idx}] {err.get('error_type')}: {err.get('error_desc')}")

        print(f"    项目结果: {len(st_files) - project_fail_count}/{len(st_files)} 通过")
        report["projects"].append(project_result)

    report["summary"] = {
        "total_projects": total_projects,
        "checked_projects": checked_projects,
        "total_files": total_files,
        "passed_files": total_files - failed_files,
        "failed_files": failed_files,
    }

    print("\n" + "=" * 80)
    print("检查完成")
    print("=" * 80)
    print(f"项目: 已检查 {checked_projects}/{total_projects}")
    print(f"文件: 通过 {total_files - failed_files}/{total_files}，失败 {failed_files}")

    if args.save_report:
        report_path = target_root / "syntax_check_report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"报告已保存: {report_path}")

    return 0 if failed_files == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
