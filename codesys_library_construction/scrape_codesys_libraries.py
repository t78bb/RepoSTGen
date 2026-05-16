"""
CODESYS官方库文档爬虫
从 https://content.helpme-codesys.com/en/libs/index.html 爬取所有库的文档信息
"""

import os
import re
import time
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse, unquote
from bs4 import BeautifulSoup


# 配置
BASE_URL = "https://content.helpme-codesys.com"
LIBS_INDEX_URL = f"{BASE_URL}/en/libs/index.html"

# 获取脚本所在目录的父目录（项目根目录）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "CODESYS_LIBRARIES")
PROGRESS_FILE = os.path.join(OUTPUT_DIR, ".scrape_progress.json")

# 请求头，模拟浏览器
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

# 创建会话
session = requests.Session()
session.headers.update(HEADERS)


def sanitize_filename(name: str) -> str:
    """
    清理文件名，移除或替换不合法字符
    """
    # 移除或替换Windows文件名不合法字符
    invalid_chars = r'[<>:"/\\|?*]'
    name = re.sub(invalid_chars, '_', name)
    # 移除前后空格
    name = name.strip()
    # 如果为空，使用默认名称
    if not name:
        name = "unnamed"
    return name


def get_library_links(index_url: str) -> List[Dict[str, str]]:
    """
    从库索引页面获取所有库的链接
    
    返回: [{"name": "库名", "url": "库URL"}, ...]
    """
    print(f"正在获取库列表: {index_url}")
    
    try:
        response = session.get(index_url, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        libraries = []
        
        # 方法1: 查找所有链接
        links = soup.find_all('a', href=True)
        print(f"  找到 {len(links)} 个链接")
        
        seen_libs = set()  # 用于去重
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            if not href:
                continue
            
            # 处理相对路径和绝对路径
            if not href.startswith('http'):
                href = urljoin(index_url, href)
            
            # 过滤出库链接（指向 /en/libs/库名/ 或 /libs/库名/）
            # 支持多种格式：
            # /en/libs/库名/index.html
            # /en/libs/库名/
            # libs/库名/index.html
            # ../libs/库名/index.html
            if '/libs/' in href:
                # 提取库名
                match = re.search(r'/libs/([^/?]+)', href)
                if match:
                    lib_path = match.group(1)
                    # URL解码（处理%20等）
                    lib_path = unquote(lib_path)
                    
                    # 确保URL以/index.html结尾
                    if not href.endswith('/index.html'):
                        if href.endswith('/'):
                            lib_url = href + 'index.html'
                        else:
                            lib_url = href + '/index.html'
                    else:
                        lib_url = href
                    
                    # 使用lib_path作为唯一标识去重
                    if lib_path not in seen_libs:
                        seen_libs.add(lib_path)
                        # 使用链接文本作为库名，如果没有则使用路径
                        lib_name = text.strip() if text.strip() else lib_path
                        libraries.append({
                            "name": lib_name,
                            "url": lib_url,
                            "lib_path": lib_path
                        })
        
        # 方法2: 如果方法1没找到，尝试查找列表项中的文本链接
        if not libraries:
            # 查找所有列表项
            list_items = soup.find_all(['li', 'div', 'p'])
            for item in list_items:
                # 查找其中的链接
                link = item.find('a', href=True)
                if link:
                    href = link.get('href', '')
                    text = link.get_text(strip=True)
                    
                    if href and '/libs/' in href:
                        if not href.startswith('http'):
                            href = urljoin(index_url, href)
                        
                        match = re.search(r'/libs/([^/]+)', href)
                        if match:
                            lib_name = match.group(1)
                            if not href.endswith('/index.html'):
                                if href.endswith('/'):
                                    lib_url = href + 'index.html'
                                else:
                                    lib_url = href + '/index.html'
                            else:
                                lib_url = href
                            
                            if not any(lib['lib_path'] == lib_name for lib in libraries):
                                libraries.append({
                                    "name": text or lib_name,
                                    "url": lib_url,
                                    "lib_path": lib_name
                                })
        
        # 方法3: 如果还是没找到，尝试从列表项中提取（可能是纯文本）
        if not libraries:
            # 查找所有列表项
            list_items = soup.find_all('li')
            for li in list_items:
                # 检查是否有链接
                link = li.find('a', href=True)
                if link:
                    continue  # 已经有链接，跳过
                
                # 获取文本内容
                text = li.get_text(strip=True)
                if text and len(text) > 2:  # 过滤太短的文本
                    # 尝试构建URL（库名可能需要URL编码）
                    # 例如 "3S CANopenSafety" -> "3S_CANopenSafety" 或保持原样
                    lib_path = text.replace(' ', '_')
                    lib_url = f"{BASE_URL}/en/libs/{lib_path}/index.html"
                    
                    # 检查这个URL是否有效（可选，会增加请求时间）
                    # 暂时先添加到列表
                    if not any(lib['lib_path'] == lib_path for lib in libraries):
                        libraries.append({
                            "name": text,
                            "url": lib_url,
                            "lib_path": lib_path
                        })
        
        print(f"找到 {len(libraries)} 个库")
        if len(libraries) > 0:
            print(f"  示例库: {libraries[0]['name']} -> {libraries[0]['url']}")
        
        return libraries
        
    except Exception as e:
        print(f"获取库列表失败: {e}")
        import traceback
        traceback.print_exc()
        return []


def get_latest_version_url(lib_url: str) -> Optional[str]:
    """
    获取库的最新版本URL
    优先选择Current，否则选择最新版本号
    
    返回: 最新版本的URL，如 https://content.helpme-codesys.com/en/libs/SysFile/Current/index.html
    """
    try:
        response = session.get(lib_url, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找版本链接
        # 通常Current链接会包含"Current"文本
        version_links = soup.find_all('a', href=True)
        
        current_url = None
        version_urls = []
        
        for link in version_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # 优先查找Current
            if text.strip().lower() == 'current':
                current_url = urljoin(lib_url, href)
                break
            
            # 收集版本号链接（格式如 3.5.17.0）
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', text.strip()):
                version_urls.append((text.strip(), urljoin(lib_url, href)))
        
        # 优先返回Current
        if current_url:
            return current_url
        
        # 如果没有Current，选择最新版本（按版本号排序）
        if version_urls:
            # 按版本号排序（降序）
            version_urls.sort(key=lambda x: tuple(map(int, x[0].split('.'))), reverse=True)
            return version_urls[0][1]
        
        # 如果都没有，返回原URL（可能该库没有版本页面）
        return lib_url
        
    except Exception as e:
        print(f"  获取版本URL失败: {e}")
        return None


def extract_description(soup: BeautifulSoup) -> str:
    """
    从页面中提取Description部分的内容
    """
    description = ""
    
    # 方法1: 查找Description标题（h1-h4）
    desc_heading = soup.find(['h1', 'h2', 'h3', 'h4'], string=re.compile(r'Description', re.I))
    
    if desc_heading:
        # 查找Description后面的所有兄弟元素，直到遇到下一个标题
        current = desc_heading.find_next_sibling()
        while current:
            # 如果遇到下一个标题，停止
            if current.name in ['h1', 'h2', 'h3', 'h4']:
                break
            
            # 提取文本内容
            if current.name in ['p', 'div', 'span']:
                text = current.get_text(separator=' ', strip=True)
                if text:
                    description += text + "\n"
            elif isinstance(current, str):
                text = current.strip()
                if text:
                    description += text + "\n"
            
            current = current.find_next_sibling()
        
        # 如果还是没找到，尝试查找父容器内的下一个元素
        if not description.strip():
            parent = desc_heading.parent
            if parent:
                # 找到Description标题后的所有段落
                found_desc = False
                for elem in parent.find_all(['p', 'div']):
                    if found_desc:
                        # 如果遇到下一个标题，停止
                        if elem.find(['h1', 'h2', 'h3', 'h4']):
                            break
                        text = elem.get_text(separator=' ', strip=True)
                        if text:
                            description += text + "\n"
                    elif desc_heading in elem.find_all(['h1', 'h2', 'h3', 'h4']):
                        found_desc = True
    
    # 方法2: 如果还没找到，尝试查找包含"Description"文本的元素
    if not description.strip():
        # 查找所有包含"Description"的元素
        for elem in soup.find_all(['div', 'section', 'article']):
            if elem.find(string=re.compile(r'Description', re.I)):
                # 获取该元素下的所有段落文本
                paragraphs = elem.find_all(['p', 'div'])
                for p in paragraphs:
                    text = p.get_text(separator=' ', strip=True)
                    if text and 'Description' not in text:  # 避免重复包含标题
                        description += text + "\n"
                if description.strip():
                    break
    
    # 方法3: 如果还是没找到，尝试查找id或class包含"description"的元素
    if not description.strip():
        desc_elem = soup.find(id=re.compile(r'description', re.I)) or \
                    soup.find(class_=re.compile(r'description', re.I))
        if desc_elem:
            description = desc_elem.get_text(separator='\n', strip=True)
    
    return description.strip()


def extract_contents_links(soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
    """
    从页面中提取Contents部分的链接列表
    
    返回: [{"name": "函数名", "url": "函数URL"}, ...]
    """
    contents = []
    
    # 方法1: 查找Contents标题
    contents_heading = soup.find(['h1', 'h2', 'h3', 'h4'], string=re.compile(r'Contents', re.I))
    
    if contents_heading:
        # 查找Contents后面的列表元素（ul, ol）或包含链接的div
        list_elem = contents_heading.find_next(['ul', 'ol', 'div'])
        
        if not list_elem:
            # 如果没找到，查找父元素的下一个兄弟元素
            parent = contents_heading.parent
            if parent:
                list_elem = parent.find_next(['ul', 'ol', 'div'])
        
        if list_elem:
            # 查找所有链接
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
    
    # 方法2: 如果没找到，尝试查找id或class包含"contents"的元素
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
    
    # 方法3: 如果还是没找到，尝试查找所有指向库内函数的链接
    # （通常库内链接的格式是相对路径，如 "FunctionName.html"）
    if not contents:
        # 查找所有链接，过滤出可能是函数/功能块的链接
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            href = link.get('href', '')
            name = link.get_text(strip=True)
            # 如果链接是相对路径且不是指向index.html，可能是函数链接
            if name and href and not href.startswith('http') and \
               'index.html' not in href and '.' in href:
                full_url = urljoin(base_url, href)
                contents.append({
                    "name": name,
                    "url": full_url
                })
    
    return contents


def scrape_library_page(version_url: str) -> Dict[str, any]:
    """
    爬取库版本页面的信息
    
    返回: {
        "description": "库描述",
        "contents": [{"name": "函数名", "url": "函数URL"}, ...]
    }
    """
    try:
        print(f"  正在爬取: {version_url}")
        response = session.get(version_url, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取Description
        description = extract_description(soup)
        
        # 提取Contents链接
        contents = extract_contents_links(soup, version_url)
        
        return {
            "description": description,
            "contents": contents
        }
        
    except Exception as e:
        print(f"  爬取失败: {e}")
        return {
            "description": "",
            "contents": []
        }


def scrape_function_page(function_url: str) -> str:
    """
    爬取函数页面的详细信息
    
    返回: 函数详细信息的文本
    """
    try:
        response = session.get(function_url, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取主要内容（通常在<main>或<div class="content">中）
        main_content = soup.find('main') or soup.find('div', class_=re.compile(r'content', re.I))
        
        if main_content:
            # 获取所有文本，保留基本格式
            text = main_content.get_text(separator='\n', strip=True)
            return text
        else:
            # 如果没有找到main，返回body的文本
            body = soup.find('body')
            if body:
                return body.get_text(separator='\n', strip=True)
        
        return ""
        
    except Exception as e:
        print(f"    爬取函数页面失败: {e}")
        return ""


def save_library_info(lib_name: str, description: str, contents: List[Dict[str, str]]):
    """
    保存库信息到文件系统
    """
    # 清理库名作为目录名
    lib_dir_name = sanitize_filename(lib_name)
    lib_dir = Path(OUTPUT_DIR) / lib_dir_name
    lib_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存库描述
    description_file = lib_dir / "description.txt"
    with open(description_file, 'w', encoding='utf-8') as f:
        f.write(description)
    print(f"  已保存库描述: {description_file}")
    
    # 保存每个函数/内容
    for content in contents:
        func_name = content["name"]
        func_url = content["url"]
        
        # 清理函数名作为文件名
        func_file_name = sanitize_filename(func_name) + ".txt"
        func_file = lib_dir / func_file_name
        
        # 爬取函数详细信息
        func_content = scrape_function_page(func_url)
        
        # 如果爬取失败，至少保存URL
        if not func_content:
            func_content = f"URL: {func_url}\n\n详细信息爬取失败，请手动访问上述URL查看。"
        
        with open(func_file, 'w', encoding='utf-8') as f:
            f.write(f"名称: {func_name}\n")
            f.write(f"URL: {func_url}\n")
            f.write(f"\n{'='*60}\n\n")
            f.write(func_content)
        
        print(f"    已保存: {func_file_name}")
        
        # 添加延迟，避免请求过快
        time.sleep(0.5)


def load_progress() -> set:
    """
    加载已处理的库列表（用于断点续传）
    """
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return set(data.get("processed_libs", []))
        except:
            return set()
    return set()


def save_progress(processed_libs: set):
    """
    保存已处理的库列表
    """
    try:
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump({"processed_libs": list(processed_libs)}, f, indent=2)
    except Exception as e:
        print(f"保存进度失败: {e}")


def is_library_processed(lib_name: str) -> bool:
    """
    检查库是否已经处理过（通过检查目录是否存在且包含description.txt）
    """
    lib_dir_name = sanitize_filename(lib_name)
    lib_dir = Path(OUTPUT_DIR) / lib_dir_name
    description_file = lib_dir / "description.txt"
    return description_file.exists()


def main():
    """
    主函数
    """
    print("=" * 60)
    print("CODESYS官方库文档爬虫")
    print("=" * 60)
    
    # 创建输出目录
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # 加载进度（用于断点续传）
    processed_libs = load_progress()
    print(f"已处理的库数量: {len(processed_libs)}")
    
    # 获取所有库链接
    libraries = get_library_links(LIBS_INDEX_URL)
    
    if not libraries:
        print("未找到任何库，退出")
        return
    
    # 过滤掉已处理的库
    libraries_to_process = [
        lib for lib in libraries 
        if lib["name"] not in processed_libs and not is_library_processed(lib["name"])
    ]
    
    print(f"\n总共 {len(libraries)} 个库，待处理 {len(libraries_to_process)} 个库")
    print("=" * 60)
    
    if not libraries_to_process:
        print("所有库都已处理完成！")
        return
    
    # 遍历每个库
    for i, lib in enumerate(libraries_to_process, 1):
        lib_name = lib["name"]
        lib_url = lib["url"]
        lib_path = lib["lib_path"]
        
        print(f"\n[{i}/{len(libraries_to_process)}] 处理库: {lib_name}")
        print(f"  库URL: {lib_url}")
        
        try:
            # 获取最新版本URL
            version_url = get_latest_version_url(lib_url)
            
            if not version_url:
                print(f"  警告: 无法获取版本URL，跳过")
                processed_libs.add(lib_name)
                save_progress(processed_libs)
                continue
            
            print(f"  版本URL: {version_url}")
            
            # 爬取库页面
            lib_info = scrape_library_page(version_url)
            
            description = lib_info["description"]
            contents = lib_info["contents"]
            
            print(f"  描述长度: {len(description)} 字符")
            print(f"  找到 {len(contents)} 个函数/内容")
            
            # 保存库信息
            save_library_info(lib_name, description, contents)
            
            # 标记为已处理
            processed_libs.add(lib_name)
            save_progress(processed_libs)
            
            # 添加延迟，避免请求过快
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n\n用户中断，已保存进度")
            save_progress(processed_libs)
            return
        except Exception as e:
            print(f"  处理库时出错: {e}")
            import traceback
            traceback.print_exc()
            # 即使出错也标记为已处理，避免重复尝试
            processed_libs.add(lib_name)
            save_progress(processed_libs)
            continue
    
    print("\n" + "=" * 60)
    print("爬取完成！")
    print("=" * 60)
    
    # 清理进度文件
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        print("已清理进度文件")


if __name__ == "__main__":
    main()

