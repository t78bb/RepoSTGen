#!/usr/bin/env python3
"""
根据 project_code 中的参考代码，调用大语言模型生成“补全所需的功能描述”，
写入 dataset/query 下对应 JSON 的 requirement 与 requirement_cn 字段。

目录对应关系：
- dataset/query/<repoeval_项目名>/ 下有若干 .json
- dataset/project_code/<项目名>/FUN/ 下有对应的 .st 参考代码（项目名 = 去掉 repoeval_ 前缀）
- 每个 JSON 的 function_name 对应 FUN 下的 <function_name>.st（及同名前缀的 _xxx.st 方法文件）

用法：
  python generate_requirements_from_code.py
  python generate_requirements_from_code.py --project repoeval_isScaleOutput
  python generate_requirements_from_code.py --project repoeval_Command1 repoeval_counter
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple

try:
    import openai
except ImportError:
    print("错误: 需要安装 openai 库。请运行: pip install openai")
    sys.exit(1)


# 默认路径（以项目仓库根为准）
REPO_ROOT = Path(__file__).resolve().parent.parent
QUERY_BASE = REPO_ROOT / "dataset" / "query"
PROJECT_CODE_BASE = REPO_ROOT / "dataset" / "project_code"


def get_api_config() -> Tuple[str, str]:
    """从环境变量获取 API 配置"""
    api_key = (
        os.getenv("ZHIZENGZENG_API_KEY")
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("API_KEY")
    )
    base_url = (
        os.getenv("BASE_URL")
        or os.getenv("ZHIZENGZENG_BASE_URL")
        or "https://api.zhizengzeng.com/v1"
    )
    if not api_key:
        print("错误: 未找到 API 密钥")
        print("请设置环境变量: ZHIZENGZENG_API_KEY 或 OPENAI_API_KEY 或 API_KEY")
        sys.exit(1)
    return api_key, base_url


def query_dir_to_project_code_name(query_dir_name: str) -> str:
    """query 子目录名 -> project_code 下的项目名（去掉 repoeval_ 前缀）"""
    if query_dir_name.startswith("repoeval_"):
        return query_dir_name[len("repoeval_"):]
    return query_dir_name


def find_fun_code(project_code_dir: Path, function_name: str) -> Optional[str]:
    """
    在 project_code/<项目>/FUN 下查找与 function_name 对应的实现代码。
    先找 FUN/<function_name>.st，再找 FUN/<function_name>_*.st（方法/子实现），合并后返回。
    """
    fun_dir = project_code_dir / "FUN"
    if not fun_dir.exists() or not fun_dir.is_dir():
        return None

    # 主文件：FUN/<function_name>.st
    main_file = fun_dir / f"{function_name}.st"
    parts: List[str] = []

    if main_file.exists():
        try:
            parts.append(main_file.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"    警告: 读取失败 {main_file}: {e}")
            return None

    # 同名前缀的方法文件：FUN/<function_name>_*.st（排除已读的主文件）
    for p in sorted(fun_dir.iterdir()):
        if not p.is_file() or p.suffix.lower() != ".st":
            continue
        if p.name == f"{function_name}.st":
            continue
        if p.name.startswith(f"{function_name}_"):
            try:
                parts.append(p.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"    警告: 读取失败 {p}: {e}")

    if not parts:
        return None
    return "\n\n---\n\n".join(parts)


def generate_requirement_and_cn(
    source_code: str,
    provide_code: str,
    function_name: str,
    api_key: str,
    base_url: str,
    model: str = "gpt-4-turbo",
) -> Tuple[Optional[str], Optional[str]]:
    """
    调用大模型根据完整参考代码生成：
    1) 补全所需的功能描述（英文）-> requirement
    2) 中文版功能描述 -> requirement_cn
    """
    prompt = f"""下面是一段 CODESYS/Structured Text 的完整参考实现（正确无误）。请根据该实现，写出补全时若只看到provide_code，为复现该实现所需的功能描述。

**英文描述（REQUIREMENT_EN）要求：**
- 以 "This code should implement ..." 开头，用需求口吻描述“应实现什么”，不要用“这段代码实现了”的陈述口吻。
- 一段话写清：做什么、关键输入/输出与类型、主要分支或枚举的语义（例如不同 case 下的取值）、边界与异常处理（如除零、空范围时的行为）。
- 尽量使用代码中的变量名、类型名，用 where 等从句把返回值/分支含义说具体。但是注意：单独的VAR（并非VAR_INPUT VAR_OUTPUT这种）相当于局部变量，这也是补全的一部分，所以不要直接提到它们。
- 不要概括性废话，不要“便于补全”等元描述，只写可直接指导实现的技术需求，用确定性的语言，不要用“可能”、“应该”等模糊词汇。

**中文描述（REQUIREMENT_CN）要求：**
- 与英文同一含义，内容翻译成中文就行。

**输出格式（严格照做）：**
先写一行：REQUIREMENT_EN:
换行后写英文描述（一段）。
再写一行：REQUIREMENT_CN:
换行后写中文描述（一段）。
不要其他解释或标题。

完整参考代码：
```
{source_code}
```

补全时已提供的代码片段（仅作上下文）：
```
{provide_code}
```

函数/功能块名：{function_name}
"""

    try:
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "你根据参考实现写出补全任务所需的功能需求。英文用 This code should implement... 开头的单段技术描述，包含变量名、分支语义和边界行为；中文同义同密度。只输出 REQUIREMENT_EN: 与 REQUIREMENT_CN: 两段，无多余内容。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1500,
        )
        text = (response.choices[0].message.content or "").strip()
        en, cn = None, None
        if "REQUIREMENT_EN:" in text:
            a = text.split("REQUIREMENT_EN:", 1)[1]
            if "REQUIREMENT_CN:" in a:
                en_part, cn_part = a.split("REQUIREMENT_CN:", 1)
                en = en_part.strip()
                cn = cn_part.strip()
            else:
                en = a.strip()
        if not en:
            en = text
        return en, cn
    except Exception as e:
        print(f"    ✗ API 调用失败: {e}")
        return None, None


def process_one_json(
    json_path: Path,
    project_code_dir: Path,
    api_key: str,
    base_url: str,
    dry_run: bool,
) -> bool:
    """
    处理单个 query 下的 JSON 文件：读 function_name，找 FUN 代码，调 LLM 写回 requirement / requirement_cn。
    返回是否成功。
    """
    try:
        raw = json_path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except Exception as e:
        print(f"  ⚠ 读取 JSON 失败 {json_path}: {e}")
        return False

    function_name = data.get("function_name")
    if not function_name:
        print(f"  ⚠ 缺少 function_name: {json_path}")
        return False

    provide_code = data.get("provide_code", "")

    source_code = find_fun_code(project_code_dir, function_name)
    if not source_code:
        print(f"  ⚠ 未找到 FUN 代码: {function_name} in {project_code_dir / 'FUN'}")
        return False

    if dry_run:
        print(f"    [dry-run] 将生成 requirement/requirement_cn 并写回: {json_path.name}")
        return True

    requirement_en, requirement_cn = generate_requirement_and_cn(
        source_code, provide_code, function_name, api_key, base_url
    )
    if requirement_en is None:
        return False

    data["requirement"] = requirement_en
    if requirement_cn:
        data["requirement_cn"] = requirement_cn
    else:
        data["requirement_cn"] = ""

    try:
        json_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception as e:
        print(f"    ✗ 写回 JSON 失败: {e}")
        return False

    print(f"    ✓ {json_path.name} (requirement + requirement_cn)")
    return True


def process_project(
    query_project_dir: Path,
    project_code_dir: Path,
    api_key: str,
    base_url: str,
    dry_run: bool,
) -> Tuple[int, int]:
    """处理 query 下的一个项目子目录。返回 (成功数, 失败/跳过数)。"""
    success, fail = 0, 0
    for j in sorted(query_project_dir.iterdir()):
        if not j.is_file() or j.suffix.lower() != ".json":
            continue
        if process_one_json(j, project_code_dir, api_key, base_url, dry_run):
            success += 1
        else:
            fail += 1
        time.sleep(0.3)
    return success, fail


def main() -> None:
    parser = argparse.ArgumentParser(
        description="根据 project_code 参考代码生成 query 下 JSON 的 requirement 与 requirement_cn"
    )
    parser.add_argument(
        "--project",
        type=str,
        nargs="+",
        default=None,
        help="只处理指定的 query 项目（目录名，可多个），例如 --project repoeval_isScaleOutput repoeval_Command1",
    )
    parser.add_argument(
        "--query-base",
        type=str,
        default=None,
        help=f"query 根目录（默认: {QUERY_BASE}）",
    )
    parser.add_argument(
        "--project-code-base",
        type=str,
        default=None,
        help=f"project_code 根目录（默认: {PROJECT_CODE_BASE}）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只扫描并打印将要处理的文件，不调用 API、不写回",
    )
    args = parser.parse_args()

    query_base = Path(args.query_base) if args.query_base else QUERY_BASE
    project_code_base = Path(args.project_code_base) if args.project_code_base else PROJECT_CODE_BASE

    if not query_base.exists():
        print(f"错误: query 目录不存在: {query_base}")
        sys.exit(1)
    if not project_code_base.exists():
        print(f"错误: project_code 目录不存在: {project_code_base}")
        sys.exit(1)

    if args.project:
        project_dirs = []
        for name in args.project:
            d = query_base / name
            if d.exists() and d.is_dir():
                project_dirs.append(d)
            else:
                print(f"⚠ 项目目录不存在，已跳过: {d}")
        project_dirs.sort(key=lambda x: x.name)
    else:
        project_dirs = [d for d in query_base.iterdir() if d.is_dir()]
        project_dirs.sort(key=lambda x: x.name)

    if not project_dirs:
        print("没有可处理的项目目录。")
        sys.exit(0)

    api_key, base_url = get_api_config()
    print(f"API: base_url={base_url}, api_key={api_key[:20]}...")
    if args.dry_run:
        print("（dry-run 模式，不调用 API、不写回文件）")
    print()

    total_ok, total_fail = 0, 0
    for query_project_dir in project_dirs:
        name = query_project_dir.name
        project_code_name = query_dir_to_project_code_name(name)
        project_code_dir = project_code_base / project_code_name
        if not project_code_dir.exists():
            # 不区分大小写再试一次
            lower_name = project_code_name.lower()
            match = next(
                (d for d in project_code_base.iterdir() if d.is_dir() and d.name.lower() == lower_name),
                None,
            )
            if match:
                project_code_dir = match
            else:
                print(f"⚠ 跳过 {name}: project_code 中无对应目录 {project_code_name}")
                continue

        print(f"处理项目: {name} -> {project_code_dir.name}")
        ok, fail = process_project(
            query_project_dir, project_code_dir, api_key, base_url, args.dry_run
        )
        total_ok += ok
        total_fail += fail
        print(f"  本项: 成功 {ok}, 失败/跳过 {fail}\n")

    print("=" * 60)
    print(f"合计: 成功 {total_ok}, 失败/跳过 {total_fail}")


if __name__ == "__main__":
    main()
