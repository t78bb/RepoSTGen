#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LITL 单用例测试脚本
用于测试API连接和评估功能
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from litl_evaluator import LITLEvaluator
import config

def test_single_case():
    """测试单个用例评估"""
    
    # 示例数据
    requirement = """
This code is intended to implement dual-axis power control and readiness 
monitoring for two axes with error handling.
    """
    
    ground_truth = """
FUNCTION_BLOCK FB_DualAxisPower
VAR_INPUT
    Axis1       : AXIS_REF;     // 轴1引用
    Axis2       : AXIS_REF;     // 轴2引用
    bEnable     : BOOL := TRUE; // 使能信号
END_VAR
VAR_OUTPUT
    bAxis1Ready : BOOL;         // 轴1准备就绪
    bAxis2Ready : BOOL;         // 轴2准备就绪
    bBothReady  : BOOL;         // 两轴都准备就绪
    bError      : BOOL;         // 错误标志
END_VAR
VAR
    fbPower1    : MC_Power;
    fbPower2    : MC_Power;
END_VAR

// 控制轴1电源
fbPower1(
    Axis := Axis1,
    Enable := bEnable,
    Enable_Positive := TRUE,
    Enable_Negative := TRUE
);

// 控制轴2电源
fbPower2(
    Axis := Axis2,
    Enable := bEnable,
    Enable_Positive := TRUE,
    Enable_Negative := TRUE
);

// 更新状态
bAxis1Ready := fbPower1.Status;
bAxis2Ready := fbPower2.Status;
bBothReady := bAxis1Ready AND bAxis2Ready;
bError := fbPower1.Error OR fbPower2.Error;

END_FUNCTION_BLOCK
    """
    
    generated_code = """
FUNCTION_BLOCK FB_DualAxisPower
VAR_INPUT
    Axis1       : AXIS_REF;
    Axis2       : AXIS_REF;
    bEnable     : BOOL := TRUE;
END_VAR
VAR_OUTPUT
    bAxis1Ready : BOOL;
    bAxis2Ready : BOOL;
    bBothReady  : BOOL;
    bError      : BOOL;
END_VAR
VAR
    power1      : MC_Power;
    power2      : MC_Power;
END_VAR

power1(
    Axis := Axis1,
    Enable := bEnable,
    Enable_Positive := TRUE,
    Enable_Negative := TRUE
);

power2(
    Axis := Axis2,
    Enable := bEnable,
    Enable_Positive := TRUE,
    Enable_Negative := TRUE
);

bAxis1Ready := power1.Status;
bAxis2Ready := power2.Status;
bBothReady := bAxis1Ready AND bAxis2Ready;
bError := power1.Error OR power2.Error;

END_FUNCTION_BLOCK
    """
    
    print("=" * 80)
    print("LITL 单用例测试")
    print("=" * 80)
    print(f"使用模型: {config.MODEL_NAME}")
    print(f"API端点: {config.API_BASE}")
    print()
    
    try:
        # 创建评估器
        evaluator = LITLEvaluator()
        
        # 执行评估
        print("正在评估测试用例...")
        result = evaluator.evaluate_code(
            requirement=requirement,
            ground_truth=ground_truth,
            generated_code=generated_code,
            case_name="TEST_CASE",
            project_name="test_project"
        )
        
        # 打印结果
        print("\n评估结果:")
        print("-" * 80)
        if result["status"] == "success":
            print(f"✅ 评估成功")
            print(f"\n各维度评分:")
            for dim, score in result["scores"].items():
                dim_name = config.EVALUATION_DIMENSIONS[dim]["name"]
                print(f"  - {dim_name}: {score}/100")
            print(f"\n综合得分: {result['overall_score']:.2f}/100")
            print(f"评估结果: {'通过 ✅' if result['passed'] else '未通过 ❌'}")
            print(f"\n主要发现:")
            print(f"  {result['key_findings']}")
            print(f"\n详细理由:")
            for dim, justification in result["justifications"].items():
                dim_name = config.EVALUATION_DIMENSIONS[dim]["name"]
                print(f"  [{dim_name}] {justification}")
        else:
            print(f"❌ 评估失败")
            print(f"错误: {result['error']}")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_single_case()
    sys.exit(0 if success else 1)

