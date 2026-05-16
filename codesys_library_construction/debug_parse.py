"""
调试脚本：查看实际网页结构
"""
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://content.helpme-codesys.com"
LIBS_INDEX_URL = f"{BASE_URL}/en/libs/index.html"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

session = requests.Session()
session.headers.update(HEADERS)

print("正在获取网页...")
response = session.get(LIBS_INDEX_URL, timeout=30)
response.raise_for_status()
response.encoding = 'utf-8'

print(f"状态码: {response.status_code}")
print(f"内容长度: {len(response.text)} 字符")
print("\n" + "="*60)
print("前1000个字符:")
print("="*60)
print(response.text[:1000])

soup = BeautifulSoup(response.text, 'html.parser')

print("\n" + "="*60)
print("所有链接:")
print("="*60)
links = soup.find_all('a', href=True)
print(f"找到 {len(links)} 个链接")
for i, link in enumerate(links[:20]):  # 只显示前20个
    href = link.get('href', '')
    text = link.get_text(strip=True)
    print(f"{i+1}. {text[:50]:<50} -> {href[:80]}")

print("\n" + "="*60)
print("包含'libs'的链接:")
print("="*60)
lib_links = [link for link in links if 'libs' in link.get('href', '').lower()]
print(f"找到 {len(lib_links)} 个包含'libs'的链接")
for i, link in enumerate(lib_links[:20]):
    href = link.get('href', '')
    text = link.get_text(strip=True)
    print(f"{i+1}. {text[:50]:<50} -> {href[:80]}")

print("\n" + "="*60)
print("页面结构分析:")
print("="*60)
# 查找主要的容器
main = soup.find('main') or soup.find('body')
if main:
    print("找到main/body元素")
    # 查找列表
    lists = main.find_all(['ul', 'ol'])
    print(f"找到 {len(lists)} 个列表")
    for i, ul in enumerate(lists[:3]):
        items = ul.find_all('li')
        print(f"列表 {i+1}: {len(items)} 个项目")
        for j, li in enumerate(items[:5]):
            print(f"  - {li.get_text(strip=True)[:60]}")





