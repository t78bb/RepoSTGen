import os
import re
import json
import shutil
from pathlib import Path
from typing import Optional
import sys

# 添加verifier目录到路径，以便导入模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'verifier'))
from auto_fix_st_code import auto_fix_st_code

# 智增增API配置 - 从环境变量读取
ZHIZENGZENG_API_KEY = os.getenv("ZHIZENGZENG_API_KEY")
ZHIZENGZENG_BASE_URL = os.getenv("ZHIZENGZENG_BASE_URL", "https://api.zhizengzeng.com/v1")

# CODESYS API 配置
CODESYS_API_URL = os.getenv("CODESYS_API_URL", "http://192.168.103.117:9000/api/v1/pou/workflow")


def extract_code_from_markdown(content: str) -> str:
    """
    如果存在两个```，截取这两个```中间的行
    如果没有则返回原内容
    """
    # 查找第一个```和最后一个```
    first_idx = content.find('```')
    if first_idx == -1:
        return content
    
    # 从第一个```之后查找下一个```
    second_idx = content.find('```', first_idx + 3)
    if second_idx == -1:
        return content
    
    # 提取中间的内容
    extracted = content[first_idx + 3:second_idx].strip()
    
    # 移除可能的语言标识（如```st）
    if extracted.startswith('st\n') or extracted.startswith('st\r\n'):
        extracted = extracted[3:].lstrip()
    elif extracted.startswith('ST\n') or extracted.startswith('ST\r\n'):
        extracted = extracted[3:].lstrip()
    
    return extracted


def extract_function_name_from_filename(filename: str) -> str:
    """
    从文件名提取function_name
    例如: HeatExchanger.st -> HeatExchanger
    """
    # 移除.st扩展名
    name = os.path.splitext(filename)[0]
    return name


def load_results_jsonl(jsonl_path: str) -> list:
    """
    加载results.jsonl文件，返回所有JSON对象的列表
    """
    results = []
    if not os.path.exists(jsonl_path):
        return results
    
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"警告: 解析JSON失败: {e}")
                    continue
    
    return results


def find_prompt_by_function_name(results: list, function_name: str) -> Optional[str]:
    """
    在results.jsonl的JSON对象中找到function_name字段匹配的prompt
    """
    for result in results:
        # 检查metadata中的function_name
        if 'metadata' in result:
            metadata = result['metadata']
            if 'function_name' in metadata and metadata['function_name'] == function_name:
                if 'prompt' in result:
                    return result['prompt']
    
    return None


def process_prompt_text(prompt: str) -> str:
    """
    处理prompt中的\t和\n，把它们换成真正的缩进和换行
    """
    # 将\t替换为实际的制表符（或4个空格）
    processed = prompt.replace('\\t', '\t')
    # 将\n替换为实际的换行符
    processed = processed.replace('\\n', '\n')
    return processed


def process_st_file(st_file_path: str, results_jsonl_path: str, output_file_path: str) -> bool:
    """
    处理单个ST文件：
    1. 读取st文件内容
    2. 如果存在两个```，截取中间的内容
    3. 从文件名提取function_name
    4. 在results.jsonl中找到对应的prompt
    5. 处理prompt（\t和\n转换）
    6. 将prompt粘贴到st文件头部（换行隔开）
    7. 保存到输出文件
    
    返回: 是否成功找到prompt
    """
    # 读取st文件
    with open(st_file_path, 'r', encoding='utf-8') as f:
        st_content = f.read()
    
    # 提取```中间的内容（如果有）
    st_content = extract_code_from_markdown(st_content)
    
    # 从文件名提取function_name
    filename = os.path.basename(st_file_path)
    function_name = extract_function_name_from_filename(filename)
    
    # 加载results.jsonl
    results = load_results_jsonl(results_jsonl_path)
    
    # 查找对应的prompt
    prompt = find_prompt_by_function_name(results, function_name)
    
    if prompt is None:
        print(f"  警告: 未找到 {function_name} 对应的prompt，跳过添加prompt")
        # 即使没有prompt，也保存处理后的内容  详情见process_generaiton
        final_content = st_content
    else:
        # 处理prompt
        processed_prompt = process_prompt_text(prompt)

        # 如果 prompt 以 FUNCTION / FUNCTION_BLOCK 开头（忽略大小写），在 st_content 后补对应 END_
        lower_prompt = processed_prompt.lstrip().lower()
        end_suffix = ""
        st_body = st_content.rstrip()
        if lower_prompt.startswith("function "):
            if not st_body.lower().endswith("end_function"):
                end_suffix = "END_FUNCTION"
        elif lower_prompt.startswith("function_block "):
            if not st_body.lower().endswith("end_function_block"):
                end_suffix = "END_FUNCTION_BLOCK"
        
        # prompt 放前，st 内容在后，二者间空一行；END_XXX 追加在 st_content 后再空一行
        parts = [processed_prompt.rstrip(), st_body]
        if end_suffix:
            parts.append(end_suffix)
        final_content = "\n\n".join(parts) + "\n"

    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    # 保存到输出文件
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    return prompt is not None


def process_directory(source_dir: str, output_dir: str):
    """
    处理整个目录结构：
    1. 遍历source_dir下的每个子目录
    2. 对每个子目录的readful_result中的st文件进行处理
    3. 创建对应的输出目录结构
    4. 对处理后的文件进行自动修复
    """
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    
    # 遍历所有子目录
    for subdir in source_path.iterdir():
        if not subdir.is_dir():
            continue
        
        subdir_name = subdir.name
        readful_result_dir = subdir / 'readful_result'
        results_jsonl_path = subdir / 'results.jsonl'
        
        if not readful_result_dir.exists():
            print(f"跳过 {subdir_name}: 未找到readful_result目录")
            continue
        
        if not results_jsonl_path.exists():
            print(f"跳过 {subdir_name}: 未找到results.jsonl文件")
            continue
        
        print(f"\n处理项目: {subdir_name}")
        print("=" * 60)
        
        # 创建对应的输出目录结构
        output_subdir = output_path / subdir_name
        output_readful_result = output_subdir / 'readful_result'
        output_readful_result.mkdir(parents=True, exist_ok=True)
        
        # 复制其他文件（如果需要）
        for file in subdir.iterdir():
            if file.is_file() and file.name != 'results.jsonl':
                shutil.copy2(file, output_subdir / file.name)
        
        # 复制results.jsonl
        shutil.copy2(results_jsonl_path, output_subdir / 'results.jsonl')
        
        # 处理readful_result中的所有st文件
        st_files = list(readful_result_dir.glob('*.st'))
        print(f"找到 {len(st_files)} 个ST文件")

        # 历史版本目录（与 readful_result 同级）
        history_dir = output_subdir / 'readful_result_history'
        history_dir.mkdir(parents=True, exist_ok=True)
        
        for st_file in st_files:
            filename = st_file.name
            print(f"\n处理文件: {filename}")
            
            # 处理st文件（添加prompt）
            output_st_file = output_readful_result / filename
            found_prompt = process_st_file(
                str(st_file),
                str(results_jsonl_path),
                str(output_st_file)
            )
            
            if found_prompt:
                print(f"  ✓ 已添加prompt")
            else:
                print(f"  ⚠ 未找到prompt，仅处理了代码内容")
            
            # 进行自动修复
            print(f"  开始自动修复...")
            try:

                # output_st_file = """
                # FUNCTION_BLOCK WriteFile
                # VAR
                #     a: INT;
                #     b: INT;
                #     resweult: INT;
                # END_VAR
                # result := a + b;
                # """
                

                fixed_code, success, count = auto_fix_st_code(
                    str(output_st_file),
                    max_verify_count=3,
                    ip_port=CODESYS_API_URL,
                    use_openai=True,
                    openai_api_key=ZHIZENGZENG_API_KEY,
                    base_url=ZHIZENGZENG_BASE_URL,
                    model="gpt-4o",
                    version_save_dir=str(history_dir)
                )
                
                if success:
                    print(f"  ✓ 修复成功！共尝试 {count} 次")
                    # 保存修复后的代码
                    with open(output_st_file, 'w', encoding='utf-8') as f:
                        f.write(fixed_code)
                else:
                    print(f"  ✗ 修复失败，已达到最大尝试次数 ({count})")
                    # 即使失败也保存当前代码
                    with open(output_st_file, 'w', encoding='utf-8') as f:
                        f.write(fixed_code)
            
            except Exception as e:
                print(f"  ✗ 修复过程出错: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n完成项目: {subdir_name}")


if __name__ == "__main__":
    # 默认根目录指向仓库下的 output，可通过环境变量 RESULT_ROOT 覆盖
    script_dir = Path(__file__).resolve().parent
    default_root = Path(os.getenv("RESULT_ROOT", script_dir / "output"))

    # 硬编码源/输出子目录（可根据需要修改）
    SOURCE_SUBDIR = "20251219_gen"
    OUTPUT_SUBDIR = "20251219_gen_fixed"

    source_path = Path(SOURCE_SUBDIR)
    output_path = Path(OUTPUT_SUBDIR)
    if not source_path.is_absolute():
        source_path = default_root / source_path
    if not output_path.is_absolute():
        output_path = default_root / output_path

    # 检查API配置
    if not ZHIZENGZENG_API_KEY:
        print("错误: 未配置API密钥！")
        print("请在CMD中设置环境变量:")
        print("  set ZHIZENGZENG_API_KEY=你的API密钥")
        print("  set ZHIZENGZENG_BASE_URL=https://api.zhizengzeng.com/v1")
        exit(1)
    
    if not source_path.exists():
        print(f"源目录不存在: {source_path}")
        exit(1)

    print("=" * 60)
    print("批量处理ST文件并自动修复")
    print("=" * 60)
    print(f"源目录: {source_path}")
    print(f"输出目录: {output_path}")
    print(f"API地址: {ZHIZENGZENG_BASE_URL}")
    print("=" * 60)
    
    # 开始处理
    process_directory(str(source_path), str(output_path))
    
    print("\n" + "=" * 60)
    print("所有处理完成！")
    print("=" * 60)

