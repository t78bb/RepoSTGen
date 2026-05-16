#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速测试GPT-5.2模型是否可用
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from litl_evaluator import LITLEvaluator
import config

def test_gpt52():
    """测试GPT-5.2模型"""
    
    print("=" * 80)
    print("GPT-5.2 模型测试")
    print("=" * 80)
    print(f"API端点: {config.API_BASE}")
    print(f"测试模型: gpt-5.2")
    print()
    
    try:
        # 创建评估器（使用gpt-5.2）
        print("正在初始化评估器...")
        evaluator = LITLEvaluator(model="gpt-5.2")
        print(f"✅ 评估器初始化成功")
        print(f"   使用API版本: {'v1.0+' if evaluator.use_v1_api else 'v0.x'}")
        print()
        
        # 简单的测试提示
        test_prompt = "请回答：1+1等于几？只回答数字即可。"
        
        print("正在测试API调用...")
        response = evaluator._call_api(
            system_prompt="你是一个有用的助手。",
            user_prompt=test_prompt
        )
        
        print(f"✅ API调用成功！")
        print(f"   响应: {response}")
        print()
        print("=" * 80)
        print("✅ GPT-5.2 模型测试通过！可以正常使用。")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print()
        print("可能的原因：")
        print("1. 网络连接问题")
        print("2. API密钥无效")
        print("3. gpt-5.2模型在智增增中不可用")
        print("4. 账户余额不足")
        print()
        print("建议：")
        print("1. 检查网络连接")
        print("2. 确认智增增账户中gpt-5.2模型可用")
        print("3. 尝试使用其他模型: python test_single_case.py")
        print("4. 使用调试模式查看详细错误")
        print()
        import traceback
        if config.DEBUG:
            traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_gpt52()
    sys.exit(0 if success else 1)

