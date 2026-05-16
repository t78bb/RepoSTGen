import json
import os
import re
import time
from codesys_debug import CodesysCompiler, ResponseData, ErrorMessage

# CODESYS API 配置 - 优先使用环境变量，否则使用默认值
CODESYS_API_URL = os.getenv("CODESYS_API_URL", "http://192.168.103.117:9000/api/v1/pou/workflow")


def check_st_code(block_name: str, st_code: str, ip_port: str = None):
    """
    检查ST代码语法（基于 verifier_generation_by_codesys.py 的实现）
    
    参数:
    - block_name: 代码块名称
    - st_code: 要检查的ST代码（字符串）
    - ip_port: CODESYS API地址，如果为None则使用默认值
    
    返回:
    - check_result: ResponseData对象，包含编译结果
    """
    # 使用默认IP地址
    if ip_port is None:
        ip_port = CODESYS_API_URL
    
    # 初始化编译器实例
    compiler = CodesysCompiler()
    start_time = time.time()
    
    # 调用语法检查
    check_result = compiler.syntax_check(block_name, st_code, ip_port)
    no_error = check_result.success
    
    elapsed_time = time.time() - start_time
    print(f"编译耗时: {elapsed_time:.2f} 秒")
    
    if no_error:
        print(f"{block_name} SUCCESS!")
        return check_result
    else:
        error_list = []
        
        # 首选 Declaration Section 的错误，因为会引发级联错误
        for error in check_result.errors:
            if error.error_type == "Declaration Section Error":
                print(f"Declaration Error >>> {str(error)}")
                error_list.append(error.to_dict())
        
        # 如果没有 Declaration Section 的错误，则检查 Implementation Section 的错误
        if not error_list:
            for error in check_result.errors:
                if error.error_type == "Implementation Section Error":
                    print(f'Implementation Error >>>> {str(error)}')
                    error_list.append(error.to_dict())
        
        # 记录所有错误信息
        all_errors = [error.to_dict() for error in check_result.errors]
        
        return check_result


def extract_block_name(st_code: str) -> str:
    """
    从ST代码中提取代码块名称
    
    参数:
    - st_code: ST代码字符串
    
    返回:
    - block_name: 代码块名称
    """
    # 尝试提取FUNCTION_BLOCK或PROGRAM名称
    match = re.search(r'(?:FUNCTION_BLOCK|PROGRAM|FUNCTION)\s+(\w+)', st_code, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return "TestBlock"


def check_file(file_path: str, ip_port: str = None) -> ResponseData:
    """
    检查ST文件
    
    参数:
    - file_path: ST文件路径
    - ip_port: CODESYS API地址，如果为None则使用默认值
    
    返回:
    - check_result: ResponseData对象，包含编译结果
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        st_code = f.read()
    
    # 提取block名称
    block_name = extract_block_name(st_code)
    
    print(f"\n文件: {file_path}")
    print(f"代码块名称: {block_name}")
    print("-" * 60)
    
    # 执行编译检查
    check_result = check_st_code(block_name, st_code, ip_port)
    
    return check_result


if __name__ == "__main__":
    # 获取verifier目录路径
    verifier_dir = os.path.dirname(__file__)
    
    # 定义要检测的文件
    test_file = os.path.join(verifier_dir, "test.st")
    test_1_file = os.path.join(verifier_dir, "test_1.st")
    
    print("=" * 60)
    print("开始检测ST文件")
    print("=" * 60)
    
    results = {}
    
    # 检测test.st文件
    print("\n" + "=" * 60)
    print("检测文件 1: test.st")
    print("=" * 60)
    try:
        result_1 = check_file(test_file)
        results["test.st"] = result_1.to_dict()
        
        # 打印详细结果
        print("\n" + "-" * 60)
        print("test.st 编译结果详情:")
        print("-" * 60)
        print(f"编译成功: {result_1.success}")
        print(f"编译结果: {result_1.result}")
        
        if result_1.errors:
            print(f"\n错误总数: {len(result_1.errors)}")
            
            # 优先显示 Declaration Section 错误
            declaration_errors = [e for e in result_1.errors if e.error_type == "Declaration Section Error"]
            if declaration_errors:
                print(f"\n声明区错误 ({len(declaration_errors)} 个):")
                for i, error in enumerate(declaration_errors, 1):
                    print(f"\n  [{i}] {error.error_type}")
                    print(f"  描述: {error.error_desc}")
                    if error.code_window:
                        print(f"  代码窗口:\n{error.code_window}")
            
            # 然后显示 Implementation Section 错误
            implementation_errors = [e for e in result_1.errors if e.error_type == "Implementation Section Error"]
            if implementation_errors:
                print(f"\n实现区错误 ({len(implementation_errors)} 个):")
                for i, error in enumerate(implementation_errors, 1):
                    print(f"\n  [{i}] {error.error_type}")
                    print(f"  描述: {error.error_desc}")
                    if error.code_window:
                        print(f"  代码窗口:\n{error.code_window}")
        else:
            print("\n✓ 没有错误！编译成功！")
        
        # 输出JSON结果
        print("\n" + "-" * 60)
        print("test.st JSON结果:")
        print("-" * 60)
        print(result_1.to_json())
        
    except Exception as e:
        print(f"检测test.st文件时出错: {e}")
        results["test.st"] = {"error": str(e)}
    
    # 检测test_1.st文件
    print("\n\n" + "=" * 60)
    print("检测文件 2: test_1.st")
    print("=" * 60)
    try:
        result_2 = check_file(test_1_file)
        results["test_1.st"] = result_2.to_dict()
        
        # 打印详细结果
        print("\n" + "-" * 60)
        print("test_1.st 编译结果详情:")
        print("-" * 60)
        print(f"编译成功: {result_2.success}")
        print(f"编译结果: {result_2.result}")
        
        if result_2.errors:
            print(f"\n错误总数: {len(result_2.errors)}")
            
            # 优先显示 Declaration Section 错误
            declaration_errors = [e for e in result_2.errors if e.error_type == "Declaration Section Error"]
            if declaration_errors:
                print(f"\n声明区错误 ({len(declaration_errors)} 个):")
                for i, error in enumerate(declaration_errors, 1):
                    print(f"\n  [{i}] {error.error_type}")
                    print(f"  描述: {error.error_desc}")
                    if error.code_window:
                        print(f"  代码窗口:\n{error.code_window}")
            
            # 然后显示 Implementation Section 错误
            implementation_errors = [e for e in result_2.errors if e.error_type == "Implementation Section Error"]
            if implementation_errors:
                print(f"\n实现区错误 ({len(implementation_errors)} 个):")
                for i, error in enumerate(implementation_errors, 1):
                    print(f"\n  [{i}] {error.error_type}")
                    print(f"  描述: {error.error_desc}")
                    if error.code_window:
                        print(f"  代码窗口:\n{error.code_window}")
        else:
            print("\n✓ 没有错误！编译成功！")
        
        # 输出JSON结果
        print("\n" + "-" * 60)
        print("test_1.st JSON结果:")
        print("-" * 60)
        print(result_2.to_json())
        
    except Exception as e:
        print(f"检测test_1.st文件时出错: {e}")
        results["test_1.st"] = {"error": str(e)}
    
    # 输出所有结果的汇总
    print("\n\n" + "=" * 60)
    print("所有检测结果汇总 (JSON格式):")
    print("=" * 60)
    print(json.dumps(results, ensure_ascii=False, indent=2))





