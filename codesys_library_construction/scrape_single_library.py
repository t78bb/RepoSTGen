"""
爬取指定CODESYS库的文档
从库的版本页面提取Current版本并爬取内容
"""

import os
import re
import time
import requests
from pathlib import Path
from typing import Dict, Optional
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


def sanitize_filename(name: str) -> str:
    """清理文件名，移除或替换不合法字符"""
    invalid_chars = r'[<>:"/\\|?*]'
    name = re.sub(invalid_chars, '_', name)
    name = name.strip()
    if not name:
        name = "unnamed"
    return name


def get_current_version_url(lib_index_url: str) -> Optional[str]:
    """
    从库的版本页面获取Current版本的URL
    
    参数:
        lib_index_url: 库的版本页面URL，如 https://content.helpme-codesys.com/en/libs/CAA%20Segmented%20Buffer%20Manager%20Extern/index.html
    
    返回:
        Current版本的URL，如 https://content.helpme-codesys.com/en/libs/CAA%20Segmented%20Buffer%20Manager%20Extern/Current/index.html
    """
    print(f"正在获取Current版本URL: {lib_index_url}")
    
    try:
        response = session.get(lib_index_url, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有链接
        links = soup.find_all('a', href=True)
        
        current_url = None
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # 查找Current链接
            if text.strip().lower() == 'current':
                # 构建完整URL
                current_url = urljoin(lib_index_url, href)
                print(f"  找到Current版本: {current_url}")
                break
        
        if not current_url:
            print("  警告: 未找到Current版本链接")
            # 尝试查找最新版本号
            version_urls = []
            for link in links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                # 匹配版本号格式（如 3.5.17.0）
                if re.match(r'^\d+\.\d+\.\d+\.\d+$', text.strip()):
                    version_urls.append((text.strip(), urljoin(lib_index_url, href)))
            
            if version_urls:
                # 按版本号排序（降序）
                version_urls.sort(key=lambda x: tuple(map(int, x[0].split('.'))), reverse=True)
                current_url = version_urls[0][1]
                print(f"  使用最新版本: {version_urls[0][0]} -> {current_url}")
        
        return current_url
        
    except Exception as e:
        print(f"获取Current版本URL失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def extract_description(soup: BeautifulSoup) -> str:
    """从页面中提取Description部分的内容"""
    description = ""
    
    # 方法1: 查找Description标题
    desc_heading = soup.find(['h1', 'h2', 'h3', 'h4'], string=re.compile(r'Description', re.I))
    
    if desc_heading:
        # 查找Description后面的所有兄弟元素，直到遇到下一个标题
        current = desc_heading.find_next_sibling()
        while current:
            if current.name in ['h1', 'h2', 'h3', 'h4']:
                break
            
            if current.name in ['p', 'div', 'span']:
                text = current.get_text(separator=' ', strip=True)
                if text:
                    description += text + "\n"
            elif isinstance(current, str):
                text = current.strip()
                if text:
                    description += text + "\n"
            
            current = current.find_next_sibling()
    
    # 方法2: 如果还没找到，尝试查找包含"Description"文本的元素
    if not description.strip():
        for elem in soup.find_all(['div', 'section', 'article']):
            if elem.find(string=re.compile(r'Description', re.I)):
                paragraphs = elem.find_all(['p', 'div'])
                for p in paragraphs:
                    text = p.get_text(separator=' ', strip=True)
                    if text and 'Description' not in text:
                        description += text + "\n"
                if description.strip():
                    break
    
    # 方法3: 查找id或class包含"description"的元素
    if not description.strip():
        desc_elem = soup.find(id=re.compile(r'description', re.I)) or \
                    soup.find(class_=re.compile(r'description', re.I))
        if desc_elem:
            description = desc_elem.get_text(separator='\n', strip=True)
    
    return description.strip()


def extract_contents_links(soup: BeautifulSoup, base_url: str) -> list:
    """从页面中提取Contents部分的链接列表"""
    contents = []
    
    # 方法1: 查找Contents标题
    contents_heading = soup.find(['h1', 'h2', 'h3', 'h4'], string=re.compile(r'Contents', re.I))
    
    if contents_heading:
        # 查找Contents后面的列表元素
        list_elem = contents_heading.find_next(['ul', 'ol', 'div'])
        
        if not list_elem:
            parent = contents_heading.parent
            if parent:
                list_elem = parent.find_next(['ul', 'ol', 'div'])
        
        if list_elem:
            links = list_elem.find_all('a', href=True)
            for link in links:
                name = link.get_text(strip=True)
                href = link.get('href', '')
                if name and href:
                    full_url = urljoin(base_url, href)
                    contents.append({
                        "name": name,
                        "url": full_url
                    })
    
    # 方法2: 查找id或class包含"contents"的元素
    if not contents:
        contents_elem = soup.find(id=re.compile(r'contents', re.I)) or \
                       soup.find(class_=re.compile(r'contents', re.I))
        if contents_elem:
            links = contents_elem.find_all('a', href=True)
            for link in links:
                name = link.get_text(strip=True)
                href = link.get('href', '')
                if name and href:
                    full_url = urljoin(base_url, href)
                    contents.append({
                        "name": name,
                        "url": full_url
                    })
    
    # 方法3: 查找所有指向库内函数的链接
    if not contents:
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            href = link.get('href', '')
            name = link.get_text(strip=True)
            if name and href and not href.startswith('http') and \
               'index.html' not in href and '.' in href:
                full_url = urljoin(base_url, href)
                contents.append({
                    "name": name,
                    "url": full_url
                })
    
    return contents


def is_target_type_link(link_name: str, link_url: str) -> bool:
    """
    判断链接是否是目标类型（Function、Struct、Enum等）
    
    参数:
        link_name: 链接文本
        link_url: 链接URL
    
    返回:
        如果是目标类型返回True
    """
    # 检查链接文本中是否包含类型关键词
    target_keywords = ['Function', 'Struct', 'Enum', 'FunctionBlock', 'Program', 
                       'Interface', 'Type', 'Var', 'Method', 'Property']
    
    link_name_lower = link_name.lower()
    for keyword in target_keywords:
        if keyword.lower() in link_name_lower:
            return True
    
    # 检查URL中是否包含类型关键词
    link_url_lower = link_url.lower()
    for keyword in target_keywords:
        if keyword.lower() in link_url_lower:
            return True
    
    return False


def extract_sub_links(soup: BeautifulSoup, base_url: str) -> list:
    """
    从页面中提取子链接（Function、Struct、Enum等）
    
    返回: [{"name": "链接名", "url": "链接URL", "type": "类型"}, ...]
    """
    sub_links = []
    seen_urls = set()  # 用于去重
    
    # 查找所有链接
    links = soup.find_all('a', href=True)
    
    for link in links:
        href = link.get('href', '')
        name = link.get_text(strip=True)
        
        if not name or not href:
            continue
        
        # 跳过外部链接（除非是同一个域名）
        if href.startswith('http'):
            if BASE_URL not in href:
                continue
        else:
            # 相对路径，构建完整URL
            href = urljoin(base_url, href)
        
        # 跳过已处理的URL
        if href in seen_urls:
            continue
        seen_urls.add(href)
        
        # 跳过index.html和当前页面
        if 'index.html' in href.lower():
            continue
        
        # 判断是否是目标类型
        if is_target_type_link(name, href):
            # 提取类型
            link_type = "Unknown"
            name_lower = name.lower()
            href_lower = href.lower()
            
            # 优先从名称中提取类型
            if 'functionblock' in name_lower or 'fb' in name_lower or '(functionblock)' in name_lower:
                link_type = "FunctionBlock"
            elif 'function' in name_lower and 'functionblock' not in name_lower or '(function)' in name_lower:
                link_type = "Function"
            elif 'struct' in name_lower or '(struct)' in name_lower:
                link_type = "Struct"
            elif 'enum' in name_lower or '(enum)' in name_lower:
                link_type = "Enum"
            elif 'program' in name_lower or '(program)' in name_lower:
                link_type = "Program"
            elif 'interface' in name_lower or '(interface)' in name_lower:
                link_type = "Interface"
            elif 'type' in name_lower or '(type)' in name_lower:
                link_type = "Type"
            # 如果名称中没有，尝试从URL中提取
            elif '/function/' in href_lower or '/functions/' in href_lower:
                link_type = "Function"
            elif '/struct/' in href_lower or '/structs/' in href_lower:
                link_type = "Struct"
            elif '/enum/' in href_lower or '/enums/' in href_lower:
                link_type = "Enum"
            elif '/functionblock/' in href_lower or '/functionblocks/' in href_lower:
                link_type = "FunctionBlock"
            
            sub_links.append({
                "name": name,
                "url": href,
                "type": link_type
            })
    
    return sub_links


def parse_function_info(content_text: str) -> dict:
    """
    解析Function页面的结构化信息
    
    返回: {
        "name": "函数名",
        "type": "Function",
        "signature": "FUNCTION 函数名 : 返回类型",
        "return_type": "返回类型",
        "description": "描述",
        "parameters": [
            {"scope": "Return/Input/Output/InOut", "name": "参数名", "type": "类型", "comment": "注释"},
            ...
        ]
    }
    """
    info = {
        "name": "",
        "type": "Function",
        "signature": "",
        "return_type": "",
        "description": "",
        "parameters": []
    }
    
    lines = [line.strip() for line in content_text.split('\n') if line.strip()]
    
    # 查找函数名（如 "GetBufferSize (FUN)"）
    for i, line in enumerate(lines):
        if '(FUN)' in line or '(Function)' in line:
            # 提取函数名
            match = re.search(r'([^(]+)\s*\(FUN\)|([^(]+)\s*\(Function\)', line)
            if match:
                info["name"] = (match.group(1) or match.group(2)).strip()
            break
    
    # 查找函数签名（如 "FUNCTION GetBufferSize : CAA.SIZE"）
    for i, line in enumerate(lines):
        if line.startswith('FUNCTION'):
            info["signature"] = line
            # 提取返回类型
            match = re.search(r'FUNCTION\s+\w+\s*:\s*(.+)', line)
            if match:
                info["return_type"] = match.group(1).strip()
            # 下一行通常是描述
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if next_line and not next_line.startswith('InOut:') and not next_line.startswith('Scope'):
                    info["description"] = next_line
            break
    
    # 查找参数表格
    # 查找 "InOut:" 标记
    inout_start = -1
    for i, line in enumerate(lines):
        if line == 'InOut:' or line.startswith('InOut:'):
            inout_start = i
            break
    
    if inout_start >= 0:
        # 查找表格标题行（包含 Scope, Name, Type, Comment）
        table_start = -1
        for i in range(inout_start, min(inout_start + 10, len(lines))):
            if 'Scope' in lines[i] and 'Name' in lines[i] and 'Type' in lines[i]:
                table_start = i + 1
                break
        
        if table_start >= 0:
            # 解析表格数据
            i = table_start
            current_scope = None
            
            while i < len(lines):
                line = lines[i]
                
                # 检查是否是Scope行（Return, Input, Output, InOut）
                if line in ['Return', 'Input', 'Output', 'InOut']:
                    current_scope = line
                    i += 1
                    continue
                
                # 跳过空行和标题行
                if not line or line in ['Scope', 'Name', 'Type', 'Comment']:
                    i += 1
                    continue
                
                # 参数名（第一行）
                param_name = line
                i += 1
                
                # 类型（下一行，可能跨多行）
                param_type_parts = []
                while i < len(lines):
                    type_line = lines[i]
                    
                    # 如果遇到新的Scope，停止
                    if type_line in ['Return', 'Input', 'Output', 'InOut']:
                        break
                    
                    # 如果下一行看起来像参数名（短且不包含类型关键词），可能是下一个参数
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        if next_line and next_line not in ['Return', 'Input', 'Output', 'InOut'] and \
                           len(next_line) < 50 and not any(keyword in next_line for keyword in 
                           ['TO', 'POINTER', 'HANDLE', 'SIZE', 'ERROR', 'BOOL', 'INT', 'REAL', 'STRING', 'DINT', 'WORD', 'BYTE', 'ARRAY']):
                            # 可能是下一个参数，停止读取类型
                            break
                    
                    # 判断是否是类型行（包含类型关键词）
                    if any(keyword in type_line for keyword in 
                          ['TO', 'POINTER', 'HANDLE', 'SIZE', 'ERROR', 'BOOL', 'INT', 'REAL', 'STRING', 
                           'DINT', 'WORD', 'BYTE', 'ARRAY', 'OF', 'REF', 'VAR', 'CONST', '.']):
                        param_type_parts.append(type_line)
                        i += 1
                    else:
                        # 可能是注释，停止读取类型
                        break
                
                param_type = ' '.join(param_type_parts).strip()
                
                # 注释（剩余行，直到遇到新的Scope或参数）
                param_comment_parts = []
                while i < len(lines):
                    comment_line = lines[i]
                    
                    # 如果遇到新的Scope，停止
                    if comment_line in ['Return', 'Input', 'Output', 'InOut']:
                        break
                    
                    # 如果下一行看起来像参数名，停止
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        if next_line and next_line not in ['Return', 'Input', 'Output', 'InOut'] and \
                           len(next_line) < 50 and not any(keyword in next_line for keyword in 
                           ['TO', 'POINTER', 'HANDLE', 'SIZE', 'ERROR', 'BOOL', 'INT', 'REAL', 'STRING', 'DINT', 'WORD', 'BYTE', 'ARRAY']):
                            # 可能是下一个参数，停止读取注释
                            break
                    
                    param_comment_parts.append(comment_line)
                    i += 1
                
                param_comment = ' '.join(param_comment_parts).strip()
                
                # 保存参数
                if current_scope and param_name:
                    info["parameters"].append({
                        "scope": current_scope,
                        "name": param_name,
                        "type": param_type,
                        "comment": param_comment
                    })
    
    return info


def format_function_info(info: dict) -> str:
    """
    将解析的Function信息格式化为清晰的文本
    """
    lines = []
    
    # 基本信息
    if info["name"]:
        lines.append(f"名称: {info['name']}")
    if info["type"]:
        lines.append(f"类型: {info['type']}")
    if info["signature"]:
        lines.append(f"函数签名: {info['signature']}")
    if info["return_type"]:
        lines.append(f"返回类型: {info['return_type']}")
    if info["description"]:
        lines.append(f"描述: {info['description']}")
    
    lines.append("")
    lines.append("=" * 80)
    lines.append("")
    
    # 参数表格
    if info["parameters"]:
        lines.append("参数列表:")
        lines.append("")
        # 表头
        lines.append(f"{'Scope':<12} {'Name':<30} {'Type':<40} {'Comment'}")
        lines.append("-" * 120)
        
        for param in info["parameters"]:
            scope = param.get("scope", "")
            name = param.get("name", "")
            param_type = param.get("type", "")
            comment = param.get("comment", "")
            
            # 处理多行注释（如果类型或注释太长，可能需要换行）
            if len(param_type) > 40:
                # 类型太长，需要换行
                type_lines = [param_type[i:i+40] for i in range(0, len(param_type), 40)]
                # 第一行
                lines.append(f"{scope:<12} {name:<30} {type_lines[0]:<40} {comment[:50] if comment else ''}")
                # 后续类型行
                for type_line in type_lines[1:]:
                    lines.append(f"{'':<12} {'':<30} {type_line:<40}")
            elif len(comment) > 50:
                # 注释太长，可能需要换行
                comment_lines = comment.split()
                first_comment = ' '.join(comment_lines[:10])  # 前10个词
                lines.append(f"{scope:<12} {name:<30} {param_type:<40} {first_comment}")
                # 后续注释行
                remaining_comment = ' '.join(comment_lines[10:])
                if remaining_comment:
                    lines.append(f"{'':<12} {'':<30} {'':<40} {remaining_comment}")
            else:
                lines.append(f"{scope:<12} {name:<30} {param_type:<40} {comment}")
    
    return "\n".join(lines)


def format_function_info_json(info: dict, url: str = "") -> str:
    """
    将解析的Function信息格式化为JSON格式
    
    参数:
        info: 解析的Function信息字典
        url: 函数页面的URL
    
    返回:
        JSON格式的字符串
    """
    json_data = {
        "name": info.get("name", ""),
        "type": info.get("type", "Function"),
        "signature": info.get("signature", ""),
        "return_type": info.get("return_type", ""),
        "description": info.get("description", ""),
        "url": url,
        "parameters": []
    }
    
    # 按Scope分组参数
    for param in info.get("parameters", []):
        json_data["parameters"].append({
            "scope": param.get("scope", ""),
            "name": param.get("name", ""),
            "type": param.get("type", ""),
            "comment": param.get("comment", "")
        })
    
    # 返回格式化的JSON字符串
    return json.dumps(json_data, ensure_ascii=False, indent=2)


def scrape_function_page(function_url: str, extract_sub_links_flag: bool = False) -> tuple:
    """
    爬取函数页面的详细信息
    
    参数:
        function_url: 页面URL
        extract_sub_links_flag: 是否提取子链接
    
    返回:
        (格式化后的内容, 子链接列表)
    """
    try:
        response = session.get(function_url, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取主要内容
        main_content = soup.find('main') or soup.find('div', class_=re.compile(r'content', re.I))
        
        content_text = ""
        if main_content:
            content_text = main_content.get_text(separator='\n', strip=True)
        else:
            body = soup.find('body')
            if body:
                content_text = body.get_text(separator='\n', strip=True)
        
        # 尝试解析Function信息
        parsed_info = parse_function_info(content_text)
        
        # 如果成功解析出函数信息，使用格式化后的内容
        if parsed_info.get("name") and parsed_info.get("signature"):
            # 同时生成文本和JSON格式
            formatted_content = format_function_info(parsed_info)
            json_content = format_function_info_json(parsed_info, function_url)
            parsed_info["_formatted_text"] = formatted_content
            parsed_info["_json"] = json_content
        else:
            # 如果解析失败，使用原始内容（但清理一些无关信息）
            # 移除导航路径等无关信息
            lines = content_text.split('\n')
            cleaned_lines = []
            skip_patterns = ['Docs', '»', '¶', 'CODESYS', 'Menu', 'Search']
            
            for line in lines:
                line_stripped = line.strip()
                # 跳过只包含导航符号的行
                if line_stripped and not all(c in skip_patterns or c.isspace() for c in line_stripped.split()):
                    cleaned_lines.append(line)
            
            formatted_content = '\n'.join(cleaned_lines)
        
        # 提取子链接
        sub_links = []
        if extract_sub_links_flag:
            sub_links = extract_sub_links(soup, function_url)
        
        # 返回格式化的内容和子链接，以及解析的信息（如果成功）
        return formatted_content, sub_links, parsed_info if parsed_info.get("name") else None
        
    except Exception as e:
        print(f"    爬取页面失败: {e}")
        return "", [], None


def scrape_single_library(lib_index_url: str, lib_name: Optional[str] = None):
    """
    爬取指定库的文档
    
    参数:
        lib_index_url: 库的版本页面URL
        lib_name: 库名称（可选，如果不提供则从URL提取）
    """
    print("=" * 60)
    print("爬取指定库的文档")
    print("=" * 60)
    print(f"库URL: {lib_index_url}")
    
    # 从URL提取库名（如果未提供）
    if not lib_name:
        match = re.search(r'/libs/([^/]+)/index\.html', lib_index_url)
        if match:
            lib_name = unquote(match.group(1))
        else:
            lib_name = "Unknown"
    
    print(f"库名: {lib_name}")
    
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
        description = extract_description(soup)
        print(f"描述长度: {len(description)} 字符")
        
        # 提取Contents链接
        contents = extract_contents_links(soup, current_url)
        print(f"找到 {len(contents)} 个函数/内容")
        
        # 保存库信息
        lib_dir_name = sanitize_filename(lib_name)
        lib_dir = Path(OUTPUT_DIR) / lib_dir_name
        lib_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存库描述
        description_file = lib_dir / "description.txt"
        with open(description_file, 'w', encoding='utf-8') as f:
            f.write(description)
        print(f"\n已保存库描述: {description_file}")
        
        # 用于跟踪已处理的URL，避免重复爬取
        processed_urls = set()
        
        def process_content(content_item: dict, parent_name: str = "", depth: int = 0):
            """
            递归处理内容项及其子链接
            
            参数:
                content_item: 内容项字典 {"name": ..., "url": ..., "type": ...}
                parent_name: 父级名称（用于文件命名）
                depth: 递归深度（防止无限递归）
            """
            if depth > 3:  # 限制递归深度
                return
            
            func_name = content_item["name"]
            func_url = content_item["url"]
            
            # 跳过已处理的URL
            if func_url in processed_urls:
                return
            processed_urls.add(func_url)
            
             indent = "  " * (depth + 1)
             print(f"{indent}[深度{depth}] 处理: {func_name}")
             
             # 爬取页面内容，并提取子链接
             func_content, sub_links, parsed_info = scrape_function_page(func_url, extract_sub_links_flag=True)
             
             if not func_content:
                 func_content = f"URL: {func_url}\n\n详细信息爬取失败，请手动访问上述URL查看。"
             
             # 构建文件名
             if parent_name:
                 base_file_name = sanitize_filename(f"{parent_name}_{func_name}")
             else:
                 base_file_name = sanitize_filename(func_name)
             
             txt_file = lib_dir / (base_file_name + ".txt")
             json_file = lib_dir / (base_file_name + ".json")
             
             # 保存文本格式
             with open(txt_file, 'w', encoding='utf-8') as f:
                 # 检查内容是否已经包含格式化信息（包含"名称:"和"函数签名:"）
                 if "名称:" in func_content and "函数签名:" in func_content:
                     # 已经格式化，直接写入，但添加URL信息
                     f.write(f"URL: {func_url}\n")
                     f.write("\n")
                     f.write(func_content)
                 else:
                     # 未格式化，使用原始格式
                     f.write(f"名称: {func_name}\n")
                     if "type" in content_item:
                         f.write(f"类型: {content_item['type']}\n")
                     f.write(f"URL: {func_url}\n")
                     f.write(f"\n{'='*60}\n\n")
                     f.write(func_content)
             
             print(f"{indent}  已保存文本: {txt_file.name}")
             
             # 如果成功解析，保存JSON格式
             if parsed_info and parsed_info.get("name"):
                 json_content = format_function_info_json(parsed_info, func_url)
                 with open(json_file, 'w', encoding='utf-8') as f:
                     f.write(json_content)
                 print(f"{indent}  已保存JSON: {json_file.name}")
            
            # 如果有子链接，递归处理
            if sub_links:
                print(f"{indent}  找到 {len(sub_links)} 个子链接")
                for sub_link in sub_links:
                    # 添加延迟
                    time.sleep(0.3)
                    process_content(sub_link, func_name, depth + 1)
            
            # 添加延迟
            time.sleep(0.3)
        
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
        print("用法: python scrape_single_library.py <库的版本页面URL> [库名]")
        print("示例: python scrape_single_library.py \"https://content.helpme-codesys.com/en/libs/CAA%20Segmented%20Buffer%20Manager%20Extern/index.html\"")
        sys.exit(1)
    
    lib_url = sys.argv[1]
    lib_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    scrape_single_library(lib_url, lib_name)

