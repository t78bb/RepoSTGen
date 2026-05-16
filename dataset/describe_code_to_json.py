#!/usr/bin/env python3
"""
根据 dataset/query 下的项目与文件名，在 dataset/project_code 中查找对应 FUN（或 PRG）下的 .st 文件，
用 LLM 生成代码逻辑的自然语言描述（中英文），写入 dataset/code_description/[项目名]/[文件名].json。

用法:
  python dataset/describe_code_to_json.py
  python dataset/describe_code_to_json.py --subdir repoeval_readwriteFile
"""
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
QUERY_BASE = REPO_ROOT / "dataset" / "query"
PROJECT_CODE_BASE = REPO_ROOT / "dataset" / "project_code"
CODE_DESCRIPTION_BASE = REPO_ROOT / "dataset" / "code_description"


def get_api_config() -> Tuple[str, str]:
    api_key = (
        os.getenv("ZHIZENGZENG_API_KEY")
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("API_KEY")
    )
    base_url = (
        os.getenv("ZHIZENGZENG_BASE_URL")
        or os.getenv("BASE_URL")
        or "https://api.zhizengzeng.com/v1"
    )
    if not api_key:
        raise RuntimeError(
            "请设置环境变量 ZHIZENGZENG_API_KEY 或 OPENAI_API_KEY"
        )
    return api_key, base_url


def find_st_file(project_code_dir: Path, stem: str) -> Optional[Path]:
    """在 project_code 项目目录下查找 FUN/<stem>.st 或 PRG/<stem>.st。"""
    for sub in ("FUN", "PRG"):
        p = project_code_dir / sub / f"{stem}.st"
        if p.exists():
            return p
    return None


def describe_code_with_llm(
    source_code: str,
    function_name: str,
    api_key: str,
    base_url: str,
    model: str = "gpt-4o",
) -> Tuple[Optional[str], Optional[str]]:
    """调用 LLM 生成代码逻辑的中英文自然语言描述。"""
    try:
        import openai
    except ImportError:
        print("请安装 openai: pip install openai", file=sys.stderr)
        return None, None

    prompt = f"""下面是一段 IEC 61131-3 Structured Text (ST) 代码。请用自然语言详细描述其代码逻辑。

函数/功能块名：{function_name}

代码：
```
{source_code}
```

请严格按以下格式输出两段（不要其他内容）：
DESCRIPTION_EN:
（这里写英文描述，一段话）

DESCRIPTION_CN:
（这里写中文描述，一段话）
"""

    try:
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "你根据ST代码写出其逻辑的自然语言描述。输出仅包含 DESCRIPTION_EN: 与 DESCRIPTION_CN: 两段，无多余内容。描述要详细，不要遗漏关键信息。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1200,
        )
        text = (response.choices[0].message.content or "").strip()
        en, cn = None, None
        if "DESCRIPTION_EN:" in text:
            rest = text.split("DESCRIPTION_EN:", 1)[1]
            if "DESCRIPTION_CN:" in rest:
                en_part, cn_part = rest.split("DESCRIPTION_CN:", 1)
                en = en_part.strip()
                cn = cn_part.strip()
            else:
                en = rest.strip()
        if not en:
            en = text
        return en, cn
    except Exception as e:
        print(f"  LLM 调用失败: {e}", file=sys.stderr)
        return None, None


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(
        description="从 query 与 project_code 生成 code_description（LLM 描述 ST 代码逻辑，中英文 JSON）"
    )
    parser.add_argument(
        "--subdir",
        type=str,
        default=None,
        help="仅处理 query 下该子目录，例如 repoeval_readwriteFile；不传则处理全部",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印将要处理的文件，不调用 LLM、不写入",
    )
    args = parser.parse_args()

    if not QUERY_BASE.exists():
        print(f"错误: query 目录不存在 {QUERY_BASE}", file=sys.stderr)
        return 1
    if not PROJECT_CODE_BASE.exists():
        print(f"错误: project_code 目录不存在 {PROJECT_CODE_BASE}", file=sys.stderr)
        return 1

    CODE_DESCRIPTION_BASE.mkdir(parents=True, exist_ok=True)

    if args.subdir:
        query_subdirs = [QUERY_BASE / args.subdir]
        if not query_subdirs[0].exists():
            print(f"错误: 子目录不存在 {query_subdirs[0]}", file=sys.stderr)
            return 1
    else:
        query_subdirs = [d for d in sorted(QUERY_BASE.iterdir()) if d.is_dir()]

    api_key, base_url = get_api_config()
    total = 0
    ok = 0

    for query_dir in query_subdirs:
        project_name = (
            query_dir.name[9:] if query_dir.name.startswith("repoeval_") else query_dir.name
        )
        project_code_dir = PROJECT_CODE_BASE / project_name
        if not project_code_dir.exists():
            print(f"[跳过] 无 project_code: {project_name}")
            continue

        out_dir = CODE_DESCRIPTION_BASE / project_name
        if not args.dry_run:
            out_dir.mkdir(parents=True, exist_ok=True)

        json_files = list(query_dir.glob("*.json"))
        for json_path in sorted(json_files):
            stem = json_path.stem
            st_path = find_st_file(project_code_dir, stem)
            if not st_path:
                print(f"  未找到 .st: {project_name}/{stem}")
                continue
            total += 1
            if args.dry_run:
                print(f"  将处理: {st_path} -> {out_dir / (stem + '.json')}")
                ok += 1
                continue

            try:
                code = st_path.read_text(encoding="utf-8")
            except Exception as e:
                print(f"  读取失败 {st_path}: {e}", file=sys.stderr)
                continue

            desc_en, desc_cn = describe_code_with_llm(
                code, stem, api_key, base_url
            )
            if desc_en is None and desc_cn is None:
                continue
            out_file = out_dir / f"{stem}.json"
            data = {
                "description_en": desc_en or "",
                "description_cn": desc_cn or "",
            }
            out_file.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"  已写: {out_file.relative_to(REPO_ROOT)}")
            ok += 1

    print(f"\n完成: 成功 {ok}/{total} 个文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
