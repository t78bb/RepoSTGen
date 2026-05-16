"""
批量爬取所有CODESYS库的文档
从库索引页面获取所有库链接，然后对每个库执行爬取操作
"""

import os
import re
import json
import time
import requests
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup

# 导入单个库爬取函数
import sys
import importlib.util

# 动态导入scrape_with_llm模块
spec = importlib.util.spec_from_file_location(
    "scrape_with_llm", 
    os.path.join(os.path.dirname(__file__), "scrape_with_llm.py")
)
scrape_with_llm_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scrape_with_llm_module)

# 导入需要的函数和变量
scrape_library_with_llm = scrape_with_llm_module.scrape_library_with_llm
BASE_URL = scrape_with_llm_module.BASE_URL
OUTPUT_DIR = scrape_with_llm_module.OUTPUT_DIR
session = scrape_with_llm_module.session
sanitize_filename = scrape_with_llm_module.sanitize_filename

# 配置
LIBS_INDEX_URL = f"{BASE_URL}/en/libs/index.html"
PROGRESS_FILE = os.path.join(OUTPUT_DIR, ".batch_scrape_progress.json")


def get_all_library_links(index_url: str) -> List[Dict[str, str]]:
    """
    从库索引页面获取所有库的链接
    
    返回: [{"name": "库名", "url": "库URL"}, ...]
    """
    print(f"正在获取所有库列表: {index_url}")
    
    try:
        response = session.get(index_url, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        libraries = []
        seen_urls = set()
        
        # 查找所有链接
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            if not text or not href:
                continue
            
            # 处理相对路径和绝对路径
            if not href.startswith('http'):
                href = urljoin(index_url, href)
            
            # 过滤出库链接（指向 /en/libs/库名/index.html）
            if '/libs/' in href and '/index.html' in href:
                # 提取库名
                match = re.search(r'/libs/([^/]+)/index\.html', href)
                if match:
                    lib_path = match.group(1)
                    lib_path = unquote(lib_path)
                    
                    # 去重
                    if href not in seen_urls:
                        seen_urls.add(href)
                        libraries.append({
                            "name": text.strip() or lib_path,
                            "url": href,
                            "lib_path": lib_path
                        })
        
        print(f"找到 {len(libraries)} 个库")
        if libraries:
            print(f"示例库: {libraries[0]['name']} -> {libraries[0]['url']}")
        
        return libraries
        
    except Exception as e:
        print(f"获取库列表失败: {e}")
        import traceback
        traceback.print_exc()
        return []


def load_progress() -> set:
    """加载已处理的库列表（用于断点续传）"""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return set(data.get("processed_libs", []))
        except:
            return set()
    return set()


def save_progress(processed_libs: set):
    """保存已处理的库列表"""
    try:
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump({"processed_libs": list(processed_libs)}, f, indent=2)
    except Exception as e:
        print(f"保存进度失败: {e}")


def is_library_processed(lib_name: str) -> bool:
    """检查库是否已经处理过（通过检查目录是否存在且包含description.json）"""
    lib_dir_name = sanitize_filename(lib_name)
    lib_dir = Path(OUTPUT_DIR) / lib_dir_name
    description_file = lib_dir / "description.json"
    return description_file.exists()


def batch_scrape_all_libraries():
    """
    批量爬取所有库的文档
    """
    print("=" * 60)
    print("批量爬取所有CODESYS库文档")
    print("=" * 60)
    
    # 检查API配置
    from scrape_with_llm import LLM_API_KEY
    if not LLM_API_KEY:
        print("错误: 未配置LLM API密钥！")
        print("请设置环境变量: ZHIZENGZENG_API_KEY 或 OPENAI_API_KEY")
        return
    
    # 加载进度
    processed_libs = load_progress()
    print(f"已处理的库数量: {len(processed_libs)}")
    
    # 获取所有库链接
    libraries = get_all_library_links(LIBS_INDEX_URL)
    
    if not libraries:
        print("未找到任何库，退出")
        return
    
    # 过滤掉已处理的库
    libraries_to_process = [
        lib for lib in libraries 
        if lib["url"] not in processed_libs and not is_library_processed(lib["name"])
    ]
    
    print(f"\n总共 {len(libraries)} 个库，待处理 {len(libraries_to_process)} 个库")
    print("=" * 60)
    
    if not libraries_to_process:
        print("所有库都已处理完成！")
        return
    
    # 处理每个库
    for i, lib in enumerate(libraries_to_process, 1):
        lib_name = lib["name"]
        lib_url = lib["url"]
        
        print(f"\n{'='*60}")
        print(f"[{i}/{len(libraries_to_process)}] 处理库: {lib_name}")
        print(f"{'='*60}")
        print(f"库URL: {lib_url}")
        
        try:
            # 爬取库文档
            scrape_library_with_llm(lib_url, lib_name)
            
            # 标记为已处理
            processed_libs.add(lib_url)
            save_progress(processed_libs)
            
            print(f"\n✓ 完成库: {lib_name}")
            
            # 添加延迟，避免请求过快
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\n\n用户中断，已保存进度")
            save_progress(processed_libs)
            return
        except Exception as e:
            print(f"\n✗ 处理库时出错: {e}")
            import traceback
            traceback.print_exc()
            # 即使出错也标记为已处理，避免重复尝试
            processed_libs.add(lib_url)
            save_progress(processed_libs)
            continue
    
    print("\n" + "=" * 60)
    print("所有库处理完成！")
    print("=" * 60)
    
    # 清理进度文件
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        print("已清理进度文件")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h"]:
        print("用法: python batch_scrape_all_libraries.py [库名或URL]")
        print("\n功能: 批量爬取所有CODESYS库的文档，或爬取指定的库")
        print("\n参数:")
        print("  无参数: 爬取所有库")
        print("  库名: 只爬取指定的库（如: Standard）")
        print("  库URL: 只爬取指定的库URL")
        print("\n示例:")
        print("  python batch_scrape_all_libraries.py")
        print("  python batch_scrape_all_libraries.py Standard")
        print("  python batch_scrape_all_libraries.py \"https://content.helpme-codesys.com/en/libs/Standard/index.html\"")
        print("\n注意: 需要设置环境变量:")
        print("  ZHIZENGZENG_API_KEY 或 OPENAI_API_KEY")
        print("  ZHIZENGZENG_BASE_URL (可选，默认: https://api.zhizengzeng.com/v1)")
        print("  LLM_MODEL (可选，默认: gpt-4o)")
        print("\n支持断点续传，如果中断可以重新运行继续处理")
        sys.exit(0)
    
    # 如果提供了参数，只处理指定的库
    if len(sys.argv) > 1:
        lib_arg = sys.argv[1]
        
        # 判断是URL还是库名
        if lib_arg.startswith('http'):
            # 是URL
            lib_url = lib_arg
            # 从URL提取库名
            match = re.search(r'/libs/([^/]+)/index\.html', lib_url)
            if match:
                lib_name = unquote(match.group(1))
            else:
                lib_name = None
        else:
            # 是库名，需要构建URL
            lib_name = lib_arg
            # URL编码库名
            from urllib.parse import quote
            lib_path = quote(lib_name)
            lib_url = f"{BASE_URL}/en/libs/{lib_path}/index.html"
        
        print(f"只处理指定的库: {lib_name}")
        print(f"库URL: {lib_url}")
        
        # 直接调用单个库的爬取函数
        scrape_library_with_llm(lib_url, lib_name)
    else:
        # 批量处理所有库
        batch_scrape_all_libraries()

