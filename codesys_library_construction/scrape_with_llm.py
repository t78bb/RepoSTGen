"""
使用大模型从HTML中提取CODESYS库文档的结构化信息
递归提取Function、Struct、Enum等信息，并输出为JSON格式
"""

import os
import re
import json
import time
import requests
from pathlib import Path
from typing import Dict, Optional, List, Any
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup

# 配置
BASE_URL = "https://content.helpme-codesys.com"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "CODESYS_LIBRARIES")

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

session = requests.Session()
session.headers.update(HEADERS)

# 大模型API配置（从环境变量读取）
LLM_API_KEY = os.getenv("ZHIZENGZENG_API_KEY") or os.getenv("OPENAI_API_KEY")
LLM_BASE_URL = os.getenv("ZHIZENGZENG_BASE_URL", "https://api.zhizengzeng.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")


def sanitize_filename(name: str) -> str:
    """清理文件名，移除或替换不合法字符"""
    invalid_chars = r'[<>:"/\\|?*]'
    name = re.sub(invalid_chars, '_', name)
    name = name.strip()
    if not name:
        name = "unnamed"
    return name


def extract_clean_html_content(soup: BeautifulSoup) -> str:
    """
    从HTML中提取干净的内容，去除导航、菜单等无关信息
    
    返回: 清理后的HTML文本内容
    """
    # 移除script和style标签
    for script in soup(["script", "style", "nav", "header", "footer"]):
        script.decompose()
    
    # 查找主要内容区域
    main_content = soup.find('main') or soup.find('div', class_=re.compile(r'content', re.I))
    
    if not main_content:
        main_content = soup.find('body')
    
    if main_content:
        # 移除导航路径（包含»符号的元素）
        for elem in main_content.find_all(string=re.compile(r'»|Docs|Menu|Search')):
            parent = elem.parent
            if parent:
                parent.decompose()
        
        # 获取文本内容
        text = main_content.get_text(separator='\n', strip=True)
        
        # 清理多余的空行
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        # 移除只包含特殊符号的行
        cleaned_lines = []
        skip_patterns = ['¶', 'CODESYS', 'Group', 'We', 'software', 'Automation']
        
        for line in lines:
            # 跳过太短的行（可能是导航符号）
            if len(line) < 3:
                continue
            # 跳过只包含特殊符号的行
            if all(c in skip_patterns or c.isspace() or c in '»' for c in line.split()):
                continue
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    return ""


def call_llm_extract(content: str, content_type: str, url: str = "") -> Dict[str, Any]:
    """
    调用大模型提取结构化信息
    
    参数:
        content: HTML文本内容
        content_type: 内容类型（Function/Struct/Enum/Description）
        url: 页面URL
    
    返回:
        提取的结构化信息字典
    """
    if not LLM_API_KEY:
        raise ValueError("未配置LLM API密钥，请设置ZHIZENGZENG_API_KEY或OPENAI_API_KEY环境变量")
    
    try:
        import openai
        
        client = openai.OpenAI(
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL
        )
        
        # 构建提示词
        if content_type == "Function":
            system_prompt = """你是一个专业的CODESYS文档解析专家。从给定的HTML内容中提取Function的详细信息。

请提取以下信息并返回JSON格式：
{
  "name": "函数名称",
  "type": "Function",
  "signature": "完整的函数签名，如 FUNCTION 函数名 : 返回类型",
  "return_type": "返回类型",
  "description": "函数描述",
  "url": "页面URL",
  "parameters": [
    {
      "scope": "Return/Input/Output/InOut",
      "name": "参数名",
      "type": "参数类型",
      "comment": "参数注释"
    }
  ]
}

注意：
1. 字段名称必须完全一致
2. 如果遇到额外信息不属于上述字段，请放在"extra"字段中
3. 确保JSON格式正确，可以解析
4. 只返回JSON，不要其他文字说明"""
        
        elif content_type == "Struct":
            system_prompt = """你是一个专业的CODESYS文档解析专家。从给定的HTML内容中提取Struct的详细信息。

请提取以下信息并返回JSON格式：
{
  "name": "结构体名称",
  "type": "Struct",
  "description": "结构体描述",
  "url": "页面URL",
  "fields": [
    {
      "name": "字段名",
      "type": "字段类型",
      "comment": "字段注释"
    }
  ]
}

注意：
1. 字段名称必须完全一致
2. 如果遇到额外信息不属于上述字段，请放在"extra"字段中
3. 确保JSON格式正确，可以解析
4. 只返回JSON，不要其他文字说明"""
        
        elif content_type == "Enum":
            system_prompt = """你是一个专业的CODESYS文档解析专家。从给定的HTML内容中提取Enum的详细信息。

请提取以下信息并返回JSON格式：
{
  "name": "枚举名称",
  "type": "Enum",
  "description": "枚举描述",
  "url": "页面URL",
  "values": [
    {
      "name": "枚举值名称",
      "value": "枚举值（如果有）",
      "comment": "枚举值注释"
    }
  ]
}

注意：
1. 字段名称必须完全一致
2. 如果遇到额外信息不属于上述字段，请放在"extra"字段中
3. 确保JSON格式正确，可以解析
4. 只返回JSON，不要其他文字说明"""
        
        else:  # Description
            system_prompt = """你是一个专业的CODESYS文档解析专家。从给定的HTML内容中提取库的描述信息。

请提取以下信息并返回JSON格式：
{
  "description": "库的详细描述",
  "url": "页面URL"
}

注意：
1. 字段名称必须完全一致
2. 如果遇到额外信息不属于上述字段，请放在"extra"字段中
3. 确保JSON格式正确，可以解析
4. 只返回JSON，不要其他文字说明"""
        
        user_prompt = f"""请从以下HTML内容中提取{content_type}信息：

URL: {url}

内容：
{content[:8000]}  # 限制长度避免超出token限制

请返回JSON格式的提取结果。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=0.1  # 降低温度以获得更一致的结果
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # 尝试提取JSON（可能包含markdown代码块）
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', result_text, re.DOTALL)
        if json_match:
            result_text = json_match.group(1)
        else:
            # 尝试直接提取大括号内容
            json_match = re.search(r'(\{.*\})', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
        
        # 解析JSON
        try:
            result = json.loads(result_text)
            # 确保URL字段存在
            if "url" not in result:
                result["url"] = url
            return result
        except json.JSONDecodeError as e:
            print(f"    JSON解析失败: {e}")
            print(f"    原始响应: {result_text[:500]}")
            # 返回基本结构
            return {
                "name": "解析失败",
                "type": content_type,
                "url": url,
                "error": str(e),
                "raw_content": result_text[:1000]
            }
    
    except ImportError:
        raise ImportError("需要安装openai库: pip install openai")
    except Exception as e:
        print(f"    调用LLM API失败: {e}")
        return {
            "name": "API调用失败",
            "type": content_type,
            "url": url,
            "error": str(e)
        }


def get_current_version_url(lib_index_url: str) -> Optional[str]:
    """从库的版本页面获取Current版本的URL"""
    print(f"正在获取Current版本URL: {lib_index_url}")
    
    try:
        response = session.get(lib_index_url, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        current_url = None
        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            if text.strip().lower() == 'current':
                current_url = urljoin(lib_index_url, href)
                print(f"  找到Current版本: {current_url}")
                break
        
        if not current_url:
            # 尝试查找最新版本号
            version_urls = []
            for link in links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                if re.match(r'^\d+\.\d+\.\d+\.\d+$', text.strip()):
                    version_urls.append((text.strip(), urljoin(lib_index_url, href)))
            
            if version_urls:
                version_urls.sort(key=lambda x: tuple(map(int, x[0].split('.'))), reverse=True)
                current_url = version_urls[0][1]
                print(f"  使用最新版本: {version_urls[0][0]} -> {current_url}")
        
        return current_url
        
    except Exception as e:
        print(f"获取Current版本URL失败: {e}")
        return None


def extract_contents_links(soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
    """
    从页面中提取Contents部分的链接列表
    只提取带括号的链接，对于没有括号的链接，需要递归进入查找
    """
    contents = []
    seen_urls = set()
    
    # 查找Contents标题
    contents_heading = soup.find(['h1', 'h2', 'h3', 'h4'], string=re.compile(r'Contents', re.I))
    
    if contents_heading:
        # 从Contents标题开始，查找后续的所有链接
        all_next_elements = contents_heading.find_all_next(['ul', 'ol', 'div', 'li'])
        
        for elem in all_next_elements:
            # 如果遇到下一个主要标题（h1-h4），停止
            if elem.find(['h1', 'h2', 'h3', 'h4']):
                if not elem.find(string=re.compile(r'Contents', re.I)):
                    break
            
            # 查找该元素中的所有链接
            links = elem.find_all('a', href=True)
            for link in links:
                name = link.get_text(strip=True)
                href = link.get('href', '')
                
                if not name or not href:
                    continue
                
                # 处理相对路径
                if not href.startswith('http'):
                    href = urljoin(base_url, href)
                
                # 跳过外部链接
                if BASE_URL not in href:
                    continue
                
                # 跳过已处理的URL
                if href in seen_urls:
                    continue
                
                # 跳过主index.html
                if href == base_url or (href.endswith('/index.html') and base_url.endswith('/index.html') and href == base_url):
                    continue
                
                seen_urls.add(href)
                
                # 只提取带括号的链接（如 "CANopenDeviceSIL2 (FunctionBlock)"）
                if has_brackets_with_type(name):
                    link_type = extract_type_from_brackets(name)
                    contents.append({
                        "name": name,
                        "url": href,
                        "type": link_type
                    })
                else:
                    # 没有括号的链接，标记为需要递归查找
                    contents.append({
                        "name": name,
                        "url": href,
                        "type": "Recursive",  # 标记为需要递归
                        "needs_recursive": True
                    })
    
    # 如果还是没找到，尝试更宽松的搜索
    if not contents:
        for elem in soup.find_all(['div', 'section', 'article']):
            if elem.find(string=re.compile(r'Contents', re.I)):
                links = elem.find_all('a', href=True)
                for link in links:
                    name = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    if not name or not href:
                        continue
                    
                    if not href.startswith('http'):
                        href = urljoin(base_url, href)
                    
                    if BASE_URL not in href or href in seen_urls:
                        continue
                    
                    if href == base_url:
                        continue
                    
                    seen_urls.add(href)
                    
                    if has_brackets_with_type(name):
                        link_type = extract_type_from_brackets(name)
                        contents.append({
                            "name": name,
                            "url": href,
                            "type": link_type
                        })
                    else:
                        contents.append({
                            "name": name,
                            "url": href,
                            "type": "Recursive",
                            "needs_recursive": True
                        })
                
                if contents:
                    break
    
    return contents


def is_target_type_link(link_name: str, link_url: str) -> bool:
    """判断链接是否是目标类型（Function、Struct、Enum等）"""
    target_keywords = ['Function', 'Struct', 'Enum', 'FunctionBlock', 'Program', 
                       'Interface', 'Type', 'Var', 'Method', 'Property']
    
    link_name_lower = link_name.lower()
    for keyword in target_keywords:
        if keyword.lower() in link_name_lower:
            return True
    
    link_url_lower = link_url.lower()
    for keyword in target_keywords:
        if keyword.lower() in link_url_lower:
            return True
    
    return False


def has_brackets_with_type(name: str) -> bool:
    """
    检查链接名称是否包含括号和类型标识
    例如: "CANopenDeviceSIL2 (FunctionBlock)" -> True
    """
    # 匹配模式: 名称 (类型)
    pattern = r'\([^)]+\)'
    return bool(re.search(pattern, name))


def extract_type_from_brackets(name: str) -> str:
    """从括号中提取类型"""
    match = re.search(r'\(([^)]+)\)', name)
    if match:
        type_str = match.group(1).strip()
        type_lower = type_str.lower()
        
        if 'functionblock' in type_lower or 'fb' in type_lower:
            return "FunctionBlock"
        elif 'function' in type_lower:
            return "Function"
        elif 'struct' in type_lower:
            return "Struct"
        elif 'enum' in type_lower:
            return "Enum"
        elif 'program' in type_lower:
            return "Program"
        elif 'interface' in type_lower:
            return "Interface"
        elif 'type' in type_lower:
            return "Type"
        else:
            return type_str  # 返回原始类型字符串
    
    return "Unknown"


def extract_sub_links(soup: BeautifulSoup, base_url: str, recursive: bool = True) -> List[Dict[str, str]]:
    """
    从页面中提取子链接（只提取末尾带括号的链接）
    
    参数:
        soup: BeautifulSoup对象
        base_url: 基础URL
        recursive: 是否递归查找（对于没有括号的链接，递归进入查找）
    
    返回: 只返回带括号的链接列表
    """
    sub_links = []
    seen_urls = set()
    
    links = soup.find_all('a', href=True)
    
    for link in links:
        href = link.get('href', '')
        name = link.get_text(strip=True)
        
        if not name or not href:
            continue
        
        if href.startswith('http'):
            if BASE_URL not in href:
                continue
        else:
            href = urljoin(base_url, href)
        
        if href in seen_urls or 'index.html' in href.lower():
            continue
        seen_urls.add(href)
        
        # 只提取带括号的链接（如 "CANopenDeviceSIL2 (FunctionBlock)"）
        if has_brackets_with_type(name):
            link_type = extract_type_from_brackets(name)
            
            sub_links.append({
                "name": name,
                "url": href,
                "type": link_type
            })
    
    return sub_links


def scrape_and_extract_with_llm(url: str, content_type: str, extract_sub_links_flag: bool = False) -> tuple:
    """
    爬取页面并使用LLM提取结构化信息
    
    返回: (提取的JSON数据, 子链接列表)
    """
    try:
        print(f"    正在爬取: {url}")
        response = session.get(url, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取干净的内容
        clean_content = extract_clean_html_content(soup)
        
        if not clean_content:
            return None, []
        
        # 使用LLM提取结构化信息
        print(f"    使用LLM提取{content_type}信息...")
        extracted_info = call_llm_extract(clean_content, content_type, url)
        
        # 提取子链接
        sub_links = []
        if extract_sub_links_flag:
            sub_links = extract_sub_links(soup, url)
        
        return extracted_info, sub_links
        
    except Exception as e:
        print(f"    爬取失败: {e}")
        import traceback
        traceback.print_exc()
        return None, []


def scrape_library_with_llm(lib_index_url: str, lib_name: Optional[str] = None):
    """
    使用LLM爬取指定库的文档
    
    参数:
        lib_index_url: 库的版本页面URL
        lib_name: 库名称（可选）
    """
    print("=" * 60)
    print("使用LLM提取CODESYS库文档")
    print("=" * 60)
    print(f"库URL: {lib_index_url}")
    
    if not lib_name:
        match = re.search(r'/libs/([^/]+)/index\.html', lib_index_url)
        if match:
            lib_name = unquote(match.group(1))
        else:
            lib_name = "Unknown"
    
    print(f"库名: {lib_name}")
    
    # 检查API配置
    if not LLM_API_KEY:
        print("错误: 未配置LLM API密钥！")
        print("请设置环境变量: ZHIZENGZENG_API_KEY 或 OPENAI_API_KEY")
        return
    
    # 获取Current版本URL
    current_url = get_current_version_url(lib_index_url)
    if not current_url:
        print("无法获取Current版本URL，退出")
        return
    
    # 爬取Current版本页面
    print(f"\n正在爬取Current版本页面: {current_url}")
    try:
        response = session.get(current_url, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取Description
        print("\n提取库描述...")
        clean_content = extract_clean_html_content(soup)
        description_info = call_llm_extract(clean_content, "Description", current_url)
        
        # 提取Contents链接
        contents = extract_contents_links(soup, current_url)
        print(f"找到 {len(contents)} 个Contents链接")
        if contents:
            print("Contents链接列表:")
            for i, content in enumerate(contents[:10], 1):  # 只显示前10个
                print(f"  {i}. {content['name']} -> {content['url']}")
        
        # 创建输出目录
        lib_dir_name = sanitize_filename(lib_name)
        lib_dir = Path(OUTPUT_DIR) / lib_dir_name
        lib_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存库描述
        if description_info:
            description_file = lib_dir / "description.json"
            with open(description_file, 'w', encoding='utf-8') as f:
                json.dump(description_info, f, ensure_ascii=False, indent=2)
            print(f"已保存库描述: {description_file}")
        
        # 用于跟踪已处理的URL
        processed_urls = set()
        
        def process_content(content_item: dict, parent_name: str = "", depth: int = 0):
            """
            递归处理内容项及其子链接
            只提取带括号的链接，对于没有括号的链接递归进入查找
            """
            if depth > 5:  # 增加递归深度限制
                return
            
            func_name = content_item["name"]
            func_url = content_item["url"]
            
            if func_url in processed_urls:
                return
            processed_urls.add(func_url)
            
            indent = "  " * (depth + 1)
            
            # 检查是否需要递归查找（没有括号的链接）
            if content_item.get("needs_recursive", False):
                print(f"{indent}[深度{depth}] 递归进入: {func_name} (查找带括号的链接)")
                
                # 爬取页面并查找其中的带括号链接
                try:
                    response = session.get(func_url, timeout=30)
                    response.raise_for_status()
                    response.encoding = 'utf-8'
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 提取带括号的子链接
                    sub_links = extract_sub_links(soup, func_url, recursive=True)
                    
                    if sub_links:
                        print(f"{indent}  找到 {len(sub_links)} 个带括号的链接")
                        for sub_link in sub_links:
                            time.sleep(0.3)
                            process_content(sub_link, parent_name, depth + 1)
                    else:
                        # 如果没找到带括号的链接，继续递归查找（可能是目录页面）
                        # 查找Contents部分的链接
                        contents = extract_contents_links(soup, func_url)
                        if contents:
                            print(f"{indent}  找到 {len(contents)} 个Contents链接，继续递归")
                            for content in contents:
                                time.sleep(0.3)
                                process_content(content, parent_name, depth + 1)
                except Exception as e:
                    print(f"{indent}  递归查找失败: {e}")
                
                return
            
            # 处理带括号的链接（直接提取）
            print(f"{indent}[深度{depth}] 处理: {func_name}")
            
            # 确定内容类型
            content_type = content_item.get("type", "Function")
            if not content_type or content_type == "Unknown":
                # 从名称推断类型
                name_lower = func_name.lower()
                if 'function' in name_lower:
                    content_type = "Function"
                elif 'struct' in name_lower:
                    content_type = "Struct"
                elif 'enum' in name_lower:
                    content_type = "Enum"
                else:
                    content_type = "Function"  # 默认
            
            # 爬取并使用LLM提取
            extracted_info, sub_links = scrape_and_extract_with_llm(
                func_url, content_type, extract_sub_links_flag=False  # 不再递归提取子链接，因为已经在Contents中处理了
            )
            
            if not extracted_info:
                print(f"{indent}  警告: 未能提取信息")
                return
            
            # 构建文件名
            if parent_name:
                base_file_name = sanitize_filename(f"{parent_name}_{func_name}")
            else:
                base_file_name = sanitize_filename(func_name)
            
            json_file = lib_dir / (base_file_name + ".json")
            
            # 保存JSON
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(extracted_info, f, ensure_ascii=False, indent=2)
            
            print(f"{indent}  已保存: {json_file.name}")
            
            time.sleep(0.5)  # 添加延迟
        
        # 处理Contents中的每个链接
        for i, content in enumerate(contents, 1):
            print(f"\n[{i}/{len(contents)}] 处理主链接: {content['name']}")
            process_content(content, depth=0)
        
        print("\n" + "=" * 60)
        print("爬取完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"爬取失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python scrape_with_llm.py <库的版本页面URL> [库名]")
        print("示例: python scrape_with_llm.py \"https://content.helpme-codesys.com/en/libs/CAA%20Segmented%20Buffer%20Manager%20Extern/index.html\"")
        print("\n注意: 需要设置环境变量:")
        print("\nWindows CMD:")
        print("  set ZHIZENGZENG_API_KEY=你的API密钥")
        print("  set ZHIZENGZENG_BASE_URL=https://api.zhizengzeng.com/v1")
        print("  set LLM_MODEL=gpt-4o")
        print("\nWindows PowerShell:")
        print("  $env:ZHIZENGZENG_API_KEY=\"你的API密钥\"")
        print("  $env:ZHIZENGZENG_BASE_URL=\"https://api.zhizengzeng.com/v1\"")
        print("  $env:LLM_MODEL=\"gpt-4o\"")
        print("\nLinux/Mac:")
        print("  export ZHIZENGZENG_API_KEY=你的API密钥")
        print("  export ZHIZENGZENG_BASE_URL=https://api.zhizengzeng.com/v1")
        print("  export LLM_MODEL=gpt-4o")
        sys.exit(1)
    
    lib_url = sys.argv[1]
    lib_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    scrape_library_with_llm(lib_url, lib_name)

