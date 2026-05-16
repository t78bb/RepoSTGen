"""
CodeBLEU 简单测试脚本
测试 CodeBLEU 核心功能（不依赖 editdistance）
"""

import sys
from pathlib import Path

# 添加 codebleu 模块到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from codebleu import calc_codebleu, AVAILABLE_LANGS


def print_divider(title=""):
    """打印分隔线"""
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}")
    else:
        print("="*80)


def print_result(result):
    """打印评估结果"""
    print("\n【评估结果】")
    print(f"  ✅ CodeBLEU 总分:        {result['codebleu']:.4f}")
    print(f"  📊 N-gram 匹配分数:      {result['ngram_match_score']:.4f}")
    print(f"  📊 加权 N-gram 分数:     {result['weighted_ngram_match_score']:.4f}")
    print(f"  🌳 语法树匹配分数:       {result['syntax_match_score']:.4f}")
    print(f"  🔄 数据流匹配分数:       {result['dataflow_match_score']:.4f}")


def test_1_basic_python():
    """测试 1: 基础 Python 代码评估"""
    print_divider("测试 1: 基础 Python 代码评估")
    
    reference = "def add(a, b):\n    return a + b"
    prediction = "def sum(first, second):\n    return second + first"
    
    print("\n【参考代码】")
    print(reference)
    print("\n【生成代码】")
    print(prediction)
    
    result = calc_codebleu([reference], [prediction], lang="python")
    print_result(result)


def test_2_identical_code():
    """测试 2: 完全相同的代码"""
    print_divider("测试 2: 完全相同的代码（预期得分 1.0）")
    
    code = "def foo(x):\n    return x"
    
    print("\n【代码】（参考和生成完全相同）")
    print(code)
    
    result = calc_codebleu([code], [code], lang="python")
    print_result(result)


def test_3_similarity_comparison():
    """测试 3: 不同相似度的代码对比"""
    print_divider("测试 3: 不同相似度的代码对比")
    
    reference = "def foo(x):\n    return x"
    
    test_cases = [
        ("完全相同", "def foo(x):\n    return x"),
        ("变量名不同", "def bar(x):\n    return x"),
        ("逻辑略微不同", "def foo(x):\n    return x * x"),
        ("逻辑完全不同", "def bar(y, x):\n    a = x * x\n    return a"),
    ]
    
    print(f"\n【参考代码】\n{reference}\n")
    print(f"{'场景':<15} {'CodeBLEU':>12} {'N-gram':>12} {'语法树':>12} {'数据流':>12}")
    print("-" * 80)
    
    for name, pred in test_cases:
        result = calc_codebleu([reference], [pred], lang="python")
        print(f"{name:<15} {result['codebleu']:>12.4f} "
              f"{result['ngram_match_score']:>12.4f} "
              f"{result['syntax_match_score']:>12.4f} "
              f"{result['dataflow_match_score']:>12.4f}")



def test_5_batch_evaluation():
    """测试 5: 批量评估"""
    print_divider("测试 5: 批量评估多个样本")
    
    references = [
        "def add(x, y): return x + y",
        "def sub(x, y): return x - y",
        "def mul(x, y): return x * y",
    ]
    
    predictions = [
        "def sum(a, b): return a + b",
        "def subtract(x, y): return x - y",
        "def multiply(m, n): return m * n",
    ]
    
    print(f"\n评估 {len(references)} 个样本...")
    
    # 逐个显示每个样本
    for i, (ref, pred) in enumerate(zip(references, predictions), 1):
        print(f"\n  样本 {i}:")
        print(f"    参考: {ref}")
        print(f"    生成: {pred}")
    
    result = calc_codebleu(references, predictions, lang="python")
    print_result(result)


def test_6_st_like_code():
    """测试 6: ST 风格代码 - 不同相似度对比"""
    print_divider("测试 6: ST (Structured Text) 代码 - 不同相似度对比")
    
    # 参考 ST 代码
    reference_st = """FUNCTION_BLOCK FB_Counter
VAR_INPUT
    bEnable : BOOL;
    bReset : BOOL;
END_VAR
VAR_OUTPUT
    nCount : INT;
END_VAR

IF bReset THEN
    nCount := 0;
ELSIF bEnable THEN
    nCount := nCount + 1;
END_IF"""
    
    # 不同相似度的 ST 代码示例
    test_cases = [
        ("完全相同", """FUNCTION_BLOCK FB_Counter
VAR_INPUT
    bEnable : BOOL;
    bReset : BOOL;
END_VAR
VAR_OUTPUT
    nCount : INT;
END_VAR

IF bReset THEN
    nCount := 0;
ELSIF bEnable THEN
    nCount := nCount + 1;
END_IF"""),
        
        ("变量名略微不同", """FUNCTION_BLOCK FB_Counter
VAR_INPUT
    bEnable : BOOL;
    bReset : BOOL;
END_VAR
VAR_OUTPUT
    nCounter : INT;
END_VAR

IF bReset THEN
    nCounter := 0;
ELSIF bEnable THEN
    nCounter := nCounter + 1;
END_IF"""),
        
        ("逻辑结构不同", """FUNCTION_BLOCK FB_Counter
VAR_INPUT
    bEnable : BOOL;
    bReset : BOOL;
END_VAR
VAR_OUTPUT
    nCount : INT;
END_VAR

IF bReset THEN
    nCount := 0;
END_IF;

IF bEnable AND NOT bReset THEN
    nCount := nCount + 1;
END_IF"""),
        
        ("增加临时变量", """FUNCTION_BLOCK FB_Counter
VAR_INPUT
    bEnable : BOOL;
    bReset : BOOL;
END_VAR
VAR_OUTPUT
    nCount : INT;
END_VAR
VAR
    nTemp : INT;
END_VAR

IF bReset THEN
    nCount := 0;
ELSIF bEnable THEN
    nTemp := nCount + 1;
    nCount := nTemp;
END_IF"""),
        
        ("功能完全不同", """FUNCTION_BLOCK FB_Timer
VAR_INPUT
    bStart : BOOL;
    tDelay : TIME;
END_VAR
VAR_OUTPUT
    bDone : BOOL;
END_VAR
VAR
    tElapsed : TIME;
END_VAR

IF bStart THEN
    tElapsed := tElapsed + T#100MS;
    IF tElapsed >= tDelay THEN
        bDone := TRUE;
    END_IF;
ELSE
    tElapsed := T#0S;
    bDone := FALSE;
END_IF"""),
    ]
    
    print(f"\n【参考 ST 代码】")
    print(reference_st)
    
    print("\n⚠️  注意：ST 语言不被原生支持，使用 Python 解析器作为近似\n")
    print(f"{'场景':<20} {'CodeBLEU':>12} {'N-gram':>12} {'语法树':>12} {'数据流':>12}")
    print("-" * 80)
    
    for name, pred in test_cases:
        result = calc_codebleu([reference_st], [pred], lang="python")
        print(f"{name:<20} {result['codebleu']:>12.4f} "
              f"{result['ngram_match_score']:>12.4f} "
              f"{result['syntax_match_score']:>12.4f} "
              f"{result['dataflow_match_score']:>12.4f}")


def test_7_available_languages():
    """测试 7: 显示支持的语言"""
    print_divider("测试 7: CodeBLEU 支持的语言")
    
    print("\n【支持的编程语言】")
    for i, lang in enumerate(AVAILABLE_LANGS, 1):
        print(f"  {i:2d}. {lang}")


def main():
    """主函数：运行所有测试"""
    print("\n" + "🎯" * 40)
    print(" " * 30 + "CodeBLEU 测试演示 (Python & ST)")
    print("🎯" * 40)
    
    try:
        # 只运行 Python 和 ST 相关测试
        test_1_basic_python()
        test_2_identical_code()
        test_3_similarity_comparison()
        test_6_st_like_code()
        
        print_divider("")
        print("✅ 所有测试完成！")
        print_divider("")
        
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

