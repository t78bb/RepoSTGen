#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time, json, os, re, sys
import argparse
from datetime import datetime
import random

extract_libraries = ["3S Storage", "3SLicense", "AC_DataLog", "AC_Alarming", "AC_ModuleBase", "AlarmManager", "Asynchronous Job Manager", "BACnet", "BACnet2", "Base Interfaces", "Building Automation", "CAA File", "CAA Real Time Clock Extern", "CAA Storage", "CANbus", "CANbusDevice", "CODESYS Safe Control", "CmpBACnet", "CmpCharDevice", "CmpCrypto", "CmpCrypto Interfaces", "CmpDNP3", "CmpDNP3 Interfaces" , "CmpDNP3 Implementation", "CmpCrypto Implementation", "CmpLog", "CmpWebServer", "CmpWebServer Implementation", "CmpWebServer_Itfs", "CommFB", "Common Behaviour Model", "Collections Interfaces", "Component Manager", "DHCP Client", "DNP3", "Data Server Interfaces", "Datasources", "Element Collections", "Empty", "ExtensionAPI", "FloatingPointUtils", "Generic String Base", "IoDriver Bus Control Interfaces", "IoDriver CIPService Interfaces", "IoDriver EIPAcyclicService Interfaces", "IoDriver Hilscher Interfaces", "IoDriver Parameter2 Interfaces", "IoDriver ProfiNet2 Interfaces", "IoDriver Profibus2 Interfaces", "IoDriver2 Interfaces", "IoDrvCIFXEthernetIP", "IoDrvCIFXProfibus", "IoDrvEtherCAT", "IoDrvEtherNetIP", "IoDrvEthernet", "IoDrvEthernet Interfaces", "IoDrvJ1939", "IoDrvKnxStack Interfaces", "IoDrvModbus", "IoDrvModbusBase", "IoDrvModbusSerial", "IoDrvModbusSerialServer", "IoDrvModbusSerialSlave", "IoDrvModbusTCP", "IoDrvModbusTCPServer", "IoDrvModbusTCPSlave", "IoDrvProfinet", "IoDrvProfinetBase", "IoDrvProfinetDevice", "IoStandard", "J1939 Safety", "J1939 Safety Interfaces", "J1939 Safety Standard", "MQTT Client SL", "Mail Service SL", "Matrix", "Memory Block Manager", "MemoryBarrier", "MemoryUtils", "ModbusFB", "ModbusFB non standard extensions", "ModbusTCP Server", "ModbusTCP Slave", "Net Base Services", "NotImplementedByDevice", "PLCopen Safety FBs", "Plc Services", "Profinet", "ProfinetCommon", "ProfinetDevice", "ProfinetDeviceConfig", "Recipe Management", "Redundancy Interfaces", "Redundancy Implementation", "RedundancyDataTransfer", "Remote Procedure Calls", "Rts Service Handler", "SDO Server", "SM3_Basic", "SM3_Basic_Visu", "SM3_CNC", "SM3_CNC_Visu", "SM3_CamBuilder"
"SM3_CommonPublic",
"SM3_Drive_CAN_Bonfiglioli_iBMD",
"SM3_Drive_CAN_CMZ_BD",
"SM3_Drive_CAN_CMZ_LBD",
"SM3_Drive_CAN_CMZ_SBD",
"SM3_Drive_CAN_CMZ_SD",
"SM3_Drive_CAN_Festo_CMMP",
"SM3_Drive_CAN_Festo_EMCA",
"SM3_Drive_CAN_INFRANOR",
"SM3_Drive_CAN_INFRANOR_CD1K",
"SM3_Drive_CAN_JAT",
"SM3_Drive_CAN_KEB",
"SM3_Drive_CAN_KEB_ITMotorB",
"SM3_Drive_CAN_KEB_SD",
"SM3_Drive_CAN_METRONIX",
"SM3_Drive_CAN_Maxon_EPOS4",
"SM3_Drive_CAN_Nanotec_PD4_C59",
"SM3_Drive_CAN_Schneider_Lexium05",
"SM3_Drive_CAN_Schneider_Lexium23",
"SM3_Drive_CAN_Schneider_Lexium28",
"SM3_Drive_CAN_Schneider_Lexium32",
"SM3_Drive_ETC",
"SM3_Drive_ETC_BRC_CtrlXDrive_CoE",
"SM3_Drive_ETC_BRC_CtrlXDrive_SoE",
"SM3_Dynamics",
"SM3_Error",
"SM3_Robotics",
"SM3_Robotics_Visu",
"SM3_Transformation",
"SML_Basic", "SMS Service SL", "SNCM Manager", "SNMP Service SL", "SNTP Service SL", "Standard", "Standard64", "Standard Monitoring Data Server Driver", "String Builder", "String Builder Base", "String Functions", "String Segments", "String Util Intern", "StringUtils", "SysDir", "SysFile", "SysEthernet", "SysFileAsync", "SysPipe Interfaces", "SysPipeWindows", "SysSem", "SysSem23", "SysSocket", "SysTime", "TCP", "Test Manager IEC Unit Test", "TextListUtils", "UDP", "UTF-16 Encoding Support", "Unicode Data", "Util", "Visu Interfaces", "Visu Utils", "VisuElemBase", "VisuGlobalClientManager", "VisuRedundancy", "VisuShared", "VisuUserMgmt", "Web Client SL", "iParServer"]


main_extract_libraries = ["BACnet","CommFB","DNP3","Empty","IoDrvEtherCAT", "IoStandard", "MQTT Client SL", "MemoryBarrier", "MemoryUtils", "ModbusFB", "PLCopen Safety FBs", "SM3_Basic", "SM3_Basic_Visu", "SM3_CNC", "SM3_CNC_Visu", "SM3_CommonPublic", "SM3_Drive_ETC", "SM3_Dynamics", "SM3_Error", "SM3_Robotics", "SM3_Robotics_Visu", "SML_Basic", "Standard", "Standard64", "String Builder", "String Builder Base", "String Functions", "String Segments", "StringUtils", "SysDir", "SysFile", "SysSem", "SysSocket", "SysTime", "Util", "Visu Utils"]



BASE = "https://content.helpme-codesys.com/en/libs/index.html"
ROOT_OUTPUT = "SCRIPT_LIBRARY"

HEADERS = {"User-Agent": "codesys-crawler/1.0 (+https://github.com)"}
session = requests.Session()
session.headers.update(HEADERS)

# 匹配包含括号的链接文本，如 "GetLibVersion (Function)", "AsyncProperty (FunctionBlock)" 等
# 简化：直接检查是否包含括号对
def is_target_link(txt):
    """检查链接文本是否包含括号（表示是一个可提取的目标）
    例如: "GetLibVersion (Function)", "AsyncProperty (FunctionBlock)", "ERROR (Enum)" 等
    """
    if not txt:
        return False
    # 检查是否包含括号对，且括号内有内容
    if '(' in txt and ')' in txt:
        # 确保括号是成对的，且括号内有内容
        return bool(re.search(r'\([^)]+\)', txt))
    return False
MAX_DEPTH = 8
# 延迟设置：基础延迟 + 随机延迟，避免被检测为爬虫
SLEEP_MIN = 1.5  # 最小延迟（秒）
SLEEP_MAX = 3.0  # 最大延迟（秒）
MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = 5  # 重试延迟（秒）


def safe_filename(s: str):
    return re.sub(r'[\\\\/:*?"<>|]', "_", s).strip()


def fetch(url, retry_count=0):
    """获取网页内容，带重试机制和随机延迟"""
    try:
        res = session.get(url, timeout=20)
        
        # 检查HTTP状态码
        if res.status_code == 429:  # Too Many Requests
            wait_time = RETRY_DELAY * (retry_count + 1)
            print(f"[WARN] 请求过于频繁 (429)，等待 {wait_time} 秒后重试...", file=sys.stderr)
            time.sleep(wait_time)
            if retry_count < MAX_RETRIES:
                return fetch(url, retry_count + 1)
            else:
                print(f"[ERROR] 重试次数已达上限: {url}", file=sys.stderr)
                return None
        
        res.raise_for_status()
        
        # 随机延迟，模拟人类行为
        sleep_time = random.uniform(SLEEP_MIN, SLEEP_MAX)
        time.sleep(sleep_time)
        
        return res.text
    
    except requests.exceptions.Timeout:
        if retry_count < MAX_RETRIES:
            print(f"[WARN] 请求超时，{RETRY_DELAY}秒后重试 ({retry_count + 1}/{MAX_RETRIES}): {url}", file=sys.stderr)
            time.sleep(RETRY_DELAY)
            return fetch(url, retry_count + 1)
        else:
            print(f"[ERROR] 请求超时，重试次数已达上限: {url}", file=sys.stderr)
            return None
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429 and retry_count < MAX_RETRIES:
            wait_time = RETRY_DELAY * (retry_count + 1)
            print(f"[WARN] HTTP错误 {e.response.status_code}，等待 {wait_time} 秒后重试...", file=sys.stderr)
            time.sleep(wait_time)
            return fetch(url, retry_count + 1)
        else:
            print(f"[WARN] HTTP错误: {url} ({e})", file=sys.stderr)
            return None
    
    except Exception as e:
        if retry_count < MAX_RETRIES:
            print(f"[WARN] 请求失败，{RETRY_DELAY}秒后重试 ({retry_count + 1}/{MAX_RETRIES}): {url} ({e})", file=sys.stderr)
            time.sleep(RETRY_DELAY)
            return fetch(url, retry_count + 1)
        else:
            print(f"[ERROR] 请求失败，重试次数已达上限: {url} ({e})", file=sys.stderr)
            return None


def soupify(html):
    return BeautifulSoup(html, "html.parser")


def normalize(href, base):
    return urljoin(base, href) if href else None


def extract_tables(soup):
    tables_data = []
    for table in soup.find_all("table"):
        headers = []
        first_row = table.find("tr")
        if first_row:
            headers = [c.get_text(strip=True) for c in first_row.find_all(["th", "td"])]
        rows = []
        for tr in table.find_all("tr")[1:]:
            cells = [c.get_text(strip=True) for c in tr.find_all(["td", "th"])]
            if headers and len(cells) == len(headers):
                rows.append({h: v for h, v in zip(headers, cells)})
            else:
                rows.append(cells)
        tables_data.append({"headers": headers, "rows": rows})
    return tables_data


def extract_main_text(soup):
    for sel in ["main", "#content", ".content", ".article", ".page"]:
        found = soup.select_one(sel)
        if found and found.get_text(strip=True):
            return found.get_text("\n", strip=True)
    body = soup.body
    return body.get_text("\n", strip=True) if body else ""


def find_current_link(soup, base):
    for a in soup.find_all("a", href=True):
        txt = a.get_text(strip=True).lower()
        href = a["href"]
        if txt == "current" or "/current/" in href or "#current" in href:
            return normalize(href, base)
    return None


def find_library_links(index_soup):
    libs = []
    for a in index_soup.find_all("a", href=True):
        full = normalize(a["href"], BASE)
        if full and "/en/libs/" in full:
            libs.append((a.get_text(strip=True), full))
    seen, final = set(), []
    for title, url in libs:
        if url not in seen:
            seen.add(url)
            final.append((title, url))
    return final


def traverse_recursive(start_url):
    visited = set()
    targets = []
    seen_targets = set()  # 用于去重，避免重复添加相同的目标

    def _walk(url, depth):
        if depth > MAX_DEPTH or url in visited:
            return
        visited.add(url)
        # 🚨 新增：打印每一个访问到的链接
        print(url)

        html = fetch(url)
        if not html:
            return
        soup = soupify(html)
        for a in soup.find_all("a", href=True):
            txt = a.get_text(strip=True)
            full = normalize(a["href"], url)
            if not full:
                continue
            # 检查链接文本是否包含括号（如 "(Function)", "(FunctionBlock)", "(Enum)" 等）
            if is_target_link(txt):
                # 使用 URL 作为唯一标识进行去重
                if full not in seen_targets:
                    seen_targets.add(full)
                    print(f"  [MATCHED] {txt} -> {full}")
                    targets.append({"title": txt, "url": full})
            else:
                p = urlparse(full)
                if p.netloc == urlparse(BASE).netloc and "/en/libs/" in p.path:
                    _walk(full, depth + 1)

    _walk(start_url, 0)
    return targets


def extract_page(item, library_name):
    html = fetch(item["url"])
    if not html:
        return None
    soup = soupify(html)
    tables = extract_tables(soup)
    text = extract_main_text(soup)
    return {
        "library": library_name,
        "title": item["title"],
        "url": item["url"],
        "page_title": soup.title.get_text(strip=True) if soup.title else item["title"],
        "text": text,
        "tables": tables
    }


def library_exists(library_name):
    """检查库目录是否已存在（用于跳过已提取的库）"""
    folder = os.path.join(ROOT_OUTPUT, safe_filename(library_name))
    return os.path.exists(folder) and os.path.isdir(folder)


def get_saved_files(library):
    """获取已保存的文件集合（用于断点重续）"""
    folder = os.path.join(ROOT_OUTPUT, safe_filename(library))
    if not os.path.exists(folder):
        return set()
    saved = set()
    for fname in os.listdir(folder):
        if fname.endswith('.json'):
            # 移除 .json 后缀，恢复原始标题
            saved.add(fname[:-5])  # 保存文件名（不含扩展名）
    return saved


def save_json(obj, library):
    folder = os.path.join(ROOT_OUTPUT, safe_filename(library))
    os.makedirs(folder, exist_ok=True)
    fname = safe_filename(obj["title"]) + ".json"
    filepath = os.path.join(folder, fname)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        print(f"    [ITEM SAVED] {obj['title']} -> {filepath}")
        return True
    except Exception as e:
        print(f"    [ERROR] Failed to save {obj['title']}: {e}", file=sys.stderr)
        return False


def main():
    start_time = time.time()
    
    parser = argparse.ArgumentParser(description="爬取 CODESYS 库文档")
    parser.add_argument(
        "--library", "-l",
        type=str,
        default=None,
        help="指定要提取的库名（支持部分匹配，不指定则提取所有库）"
    )
    parser.add_argument(
        "--use-list", "--list",
        action="store_true",
        help="使用 main_extract_libraries 列表中定义的库进行提取"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="启用断点重续功能，跳过已保存的文件"
    )
    args = parser.parse_args()

    os.makedirs(ROOT_OUTPUT, exist_ok=True)
    
    # 如果使用列表模式
    if args.use_list:
        print(f"📋 使用 main_extract_libraries 列表，共 {len(main_extract_libraries)} 个库")
        html = fetch(BASE)
        if not html:
            print("❌ Failed to fetch libs index page")
            return
        
        all_libs = find_library_links(soupify(html))
        # 从所有库中匹配 main_extract_libraries 中的库
        libs = []
        skipped_count = 0
        for lib_name in main_extract_libraries:
            if not lib_name.strip():  # 跳过空字符串
                continue
            
            # 检查库目录是否已存在，如果存在则跳过
            if library_exists(lib_name):
                print(f"⏭️  跳过已提取的库: '{lib_name}' (目录已存在)")
                skipped_count += 1
                continue
            
            matched = [(title, url) for title, url in all_libs if lib_name.lower() in title.lower() or title.lower() in lib_name.lower()]
            if matched:
                libs.extend(matched)
            else:
                print(f"⚠️  警告: 未找到库 '{lib_name}'")
        
        if skipped_count > 0:
            print(f"📊 已跳过 {skipped_count} 个已提取的库\n")
        
        if not libs:
            print("❌ 未找到任何匹配的库")
            return
        
        # 去重
        seen_urls = set()
        unique_libs = []
        for title, url in libs:
            if url not in seen_urls:
                seen_urls.add(url)
                unique_libs.append((title, url))
        libs = unique_libs
        
        print(f"📌 将处理 {len(libs)} 个库:\n")
        for title, _ in libs:
            print(f"  - {title}")
        print()
    
    # 如果指定了单个库名
    elif args.library:
        html = fetch(BASE)
        if not html:
            print("❌ Failed to fetch libs index page")
            return
        
        all_libs = find_library_links(soupify(html))
        print(f"🔍 Found {len(all_libs)} libraries\n")
        
        target_lib = args.library.lower()
        libs = [(title, url) for title, url in all_libs if target_lib in title.lower()]
        if not libs:
            print(f"❌ 未找到匹配的库: {args.library}")
            return
        print(f"📌 将处理 {len(libs)} 个匹配的库:\n")
        for title, _ in libs:
            print(f"  - {title}")
        print()
    
    # 否则提取所有库
    else:
        html = fetch(BASE)
        if not html:
            print("❌ Failed to fetch libs index page")
            return
        
        libs = find_library_links(soupify(html))
        print(f"🔍 Found {len(libs)} libraries\n")
        print("⚠️  未指定库，将提取所有库\n")

    total_saved = 0
    total_skipped = 0
    
    for idx, (lib_title, lib_url) in enumerate(libs, 1):
        lib_start_time = time.time()
        print(f"\n[{idx}/{len(libs)}] [LIB] {lib_title}")
        
        # 断点重续：检查已保存的文件
        saved_files = set()
        if args.resume:
            saved_files = get_saved_files(lib_title)
            if saved_files:
                print(f"  📂 发现 {len(saved_files)} 个已保存的文件，将跳过")
        
        html = fetch(lib_url)
        if not html:
            print(f"  ⚠️  跳过（无法获取页面）")
            continue
        
        soup = soupify(html)
        start = find_current_link(soup, lib_url) or lib_url
        print(f"  🔗 起始URL: {start}")
        
        targets = traverse_recursive(start)
        print(f"  ➤ 找到 {len(targets)} 个目标项")
        
        lib_saved = 0
        lib_skipped = 0
        
        for item in targets:
            # 断点重续：检查是否已保存
            item_filename = safe_filename(item["title"])
            if args.resume and item_filename in saved_files:
                lib_skipped += 1
                continue
            
            data = extract_page(item, lib_title)
            if data:
                if save_json(data, lib_title):
                    lib_saved += 1
                    total_saved += 1
                else:
                    lib_skipped += 1
                    total_skipped += 1
            else:
                lib_skipped += 1
                total_skipped += 1
        
        lib_elapsed = time.time() - lib_start_time
        print(f"  ✅ 完成: 保存 {lib_saved} 个，跳过 {lib_skipped} 个 (耗时 {lib_elapsed:.2f}秒)")
        print("  --- Done ---\n")

    total_elapsed = time.time() - start_time
    hours = int(total_elapsed // 3600)
    minutes = int((total_elapsed % 3600) // 60)
    seconds = int(total_elapsed % 60)
    
    print("\n" + "="*60)
    print("🎉 爬取完成!")
    print(f"📁 输出目录: {ROOT_OUTPUT}")
    print(f"📊 统计: 保存 {total_saved} 个文件，跳过 {total_skipped} 个文件")
    print(f"⏱️  总耗时: {hours}小时 {minutes}分钟 {seconds}秒 ({total_elapsed:.2f}秒)")
    print("="*60)


if __name__ == "__main__":
    main()
