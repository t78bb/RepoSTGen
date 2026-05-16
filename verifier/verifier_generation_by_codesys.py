import json
import os
import time
from codesys_debug import CodesysCompiler, ResponseData, ErrorMessage

# CODESYS API 配置 - 优先使用环境变量，否则使用默认值
# 可以通过环境变量 CODESYS_API_URL 来设置，例如：
# export CODESYS_API_URL="http://localhost:9000/api/v1/pou/workflow"
CODESYS_API_URL = os.getenv("CODESYS_API_URL", "http://192.168.103.117:9000/api/v1/pou/workflow")


def check_st_code(block_name: str, st_code: str, ip_port: str = None):
    """
    检查ST代码语法（基于 verifier_agent.py 的实现）
    
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
    
    # 初始化编译器实例（参考 verifier_agent.py 第70行）
    compiler = CodesysCompiler()
    start_time = time.time()
    
    # 调用语法检查（参考 verifier_agent.py 第96行）
    check_result = compiler.syntax_check(block_name, st_code, ip_port)
    no_error = check_result.success
    
    elapsed_time = time.time() - start_time
    print(f"编译耗时: {elapsed_time:.2f} 秒")
    
    if no_error:
        print(f"{block_name} SUCCESS!")
        return check_result
    else:
        error_list = []
        
        # 首选 Declaration Section 的错误，因为会引发级联错误（参考 verifier_agent.py 第105-109行）
        for error in check_result.errors:
            if error.error_type == "Declaration Section Error":
                print(f"Declaration Error >>> {str(error)}")
                error_list.append(error.to_dict())
        
        # 如果没有 Declaration Section 的错误，则检查 Implementation Section 的错误（参考 verifier_agent.py 第112-116行）
        if not error_list:
            for error in check_result.errors:
                if error.error_type == "Implementation Section Error":
                    print(f'Implementation Error >>>> {str(error)}')
                    error_list.append(error.to_dict())
        
        # 记录所有错误信息（参考 verifier_agent.py 第122行）
        all_errors = [error.to_dict() for error in check_result.errors]
        
        return check_result


if __name__ == "__main__":
    # 测试代码 - 直接用三引号字符串指定要编译检测的代码
    test_code = """
FUNCTION_BLOCK TestFB
VAR_INPUT
    x: BOOL;
END_VAR
VAR_OUTPUT
    y: BOOL;
END_VAR
BEGIN
    y := x1;
END_FUNCTION_BLOCK
"""
    
    # 执行编译检查
    print("=" * 60)
    print("开始编译检查...")
    print("=" * 60)
    
    check_result = check_st_code("TestFB", test_code)
    
    # 打印详细结果
    print("\n" + "=" * 60)
    print("编译结果详情:")
    print("=" * 60)
    print(f"编译成功: {check_result.success}")
    print(f"编译结果: {check_result.result}")
    
    if check_result.errors:
        print(f"\n错误总数: {len(check_result.errors)}")
        
        # 优先显示 Declaration Section 错误
        declaration_errors = [e for e in check_result.errors if e.error_type == "Declaration Section Error"]
        if declaration_errors:
            print(f"\n声明区错误 ({len(declaration_errors)} 个):")
            for i, error in enumerate(declaration_errors, 1):
                print(f"\n  [{i}] {error.error_type}")
                print(f"  描述: {error.error_desc}")
                if error.code_window:
                    print(f"  代码窗口:\n{error.code_window}")
        
        # 然后显示 Implementation Section 错误
        implementation_errors = [e for e in check_result.errors if e.error_type == "Implementation Section Error"]
        if implementation_errors:
            print(f"\n实现区错误 ({len(implementation_errors)} 个):")
            for i, error in enumerate(implementation_errors, 1):
                print(f"\n  [{i}] {error.error_type}")
                print(f"  描述: {error.error_desc}")
                if error.code_window:
                    print(f"  代码窗口:\n{error.code_window}")
    else:
        print("\n✓ 没有错误！编译成功！")
    
    # 输出完整JSON结果
    print("\n" + "=" * 60)
    print("完整JSON结果:")
    print("=" * 60)
    print(check_result.to_json())

