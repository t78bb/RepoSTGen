#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LITL 评估提示模板
"""

def get_evaluation_prompt(requirement: str, ground_truth: str, generated_code: str, 
                          requirement_path: str = None, ground_truth_path: str = None, 
                          generated_code_path: str = None) -> str:
    """
    生成LITL评估提示
    
    参数:
        requirement: 任务规范描述
        ground_truth: 参考解决方案（正确代码）
        generated_code: 待评估的生成代码
        requirement_path: 任务规范文件路径（可选）
        ground_truth_path: 参考代码文件路径（可选）
        generated_code_path: 生成代码文件路径（可选）
    
    返回:
        完整的评估提示文本
    """
    # 构建文件路径信息
    path_info = []
    if requirement_path:
        path_info.append(f"任务规范文件路径: {requirement_path}")
    if ground_truth_path:
        path_info.append(f"参考代码文件路径: {ground_truth_path}")
    if generated_code_path:
        path_info.append(f"生成代码文件路径: {generated_code_path}")
    
    path_section = ""
    if path_info:
        path_section = "\n# 文件路径信息\n" + "\n".join(path_info) + "\n"
    
    prompt = f"""你是一位IEC 61131-3结构化文本（ST）代码评估专家。你的任务是客观评估一个生成的PLC程序的质量，通过将其与参考解决方案和原始需求进行比较。

# 评估数据

## 任务规范
代码应满足以下功能和安全要求：
```
{requirement}
```

## 参考解决方案（Ground Truth）
这是经过验证的正确实现，作为黄金标准：
```st
{ground_truth}
```

## 生成代码（待评估）
这是由LLM生成的、需要评估的代码：
```st
{generated_code}
```
{path_section}
# 评估说明
你必须从四个关键维度评估生成的代码。对于每个维度，请提供：
1. 0到100之间的数值分数（0 = 完全失败，100 = 完美）
2. 评分理由（最多2-3句话）

## 维度1：功能正确性
- 生成的代码是否正确实现了任务中指定的主要要求？
- 它是否支持参考代码中的大部分功能逻辑？
- 注意：评估目标不是判断逻辑是否完美匹配参考实现，而是判断它是否能够支持大部分逻辑。
- 非必要或冗余的代码元素是可接受的，应视为通过。
- 只要核心功能得到支持，实现方法的差异是可接受的。

## 维度2：可读性和风格
- 变量名是否有意义并遵循约定？
- 代码结构是否清晰易懂？
- 注释是否适当且有用（如需要）？
- 是否遵循IEC 61131-3 ST编码风格约定？

## 维度3：安全合规性
- 代码是否符合IEC 61131-3标准？
- 安全关键方面（如错误处理、状态管理）是否得到适当处理？
- 是否避免了可能导致未定义行为的不安全做法？

## 维度4：模块化
- 代码结构是否良好且可维护？
- 是否展示了适当的关注点分离？
- 是否易于扩展或修改？

# 输出格式
你必须按照以下JSON格式响应（且仅此格式）：

```json
{{
  "scores": {{
    "functional_correctness": <0-100>,
    "readability_and_style": <0-100>,
    "safety_compliance": <0-100>,
    "modularity": <0-100>
  }},
  "justifications": {{
    "functional_correctness": "<评分理由>",
    "readability_and_style": "<评分理由>",
    "safety_compliance": "<评分理由>",
    "modularity": "<评分理由>"
  }},
  "overall_assessment": "<PASS 或 FAIL>",
  "key_findings": "<1-2句话总结最重要的观察结果，必须使用中文>"
}}
```

# 总体评估指导原则
在确定 "overall_assessment"（PASS 或 FAIL）时，请遵循以下指导原则：
- **如果通过（PASS）**：代码支持参考代码中的大部分功能逻辑，即使存在微小差异、非必要添加或冗余代码元素。
- **如果通过（PASS）**：实现方法不同但达到相似的功能结果。
- **仅在失败（FAIL）时**：代码无法支持大部分所需功能，或存在阻止其工作的严重缺陷。
- **记住**：目标是评估代码是否能够支持大部分逻辑，而不是是否完美匹配参考实现。

# 关键规则
- 不要重写或修改代码
- 不要提供建议或推荐
- 仅基于提交的代码进行评估
- 在所有评估中保持客观和一致
- 确保所有分数都是0到100之间的整数
- 你的响应必须是有效的JSON格式，不要添加额外文本
- key_findings 字段必须使用中文

现在，请评估生成的代码，并以指定的JSON格式提供你的评估结果。
"""
    return prompt


def get_system_prompt() -> str:
    """
    获取系统提示（用于设置LLM的角色）
    """
    return """你是一位客观、专业的IEC 61131-3结构化文本（ST）PLC代码评估专家。
你具备以下专业知识：
- IEC 61131-3标准和最佳实践
- PLC编程模式和安全要求
- 多维度代码质量评估

你的评估特点：
- 严格客观，基于技术标准
- 在不同代码样本间保持一致
- 不受主观偏好影响
- 专注于提交的代码，不提供建议

你始终按照提示中指定的格式，以有效的JSON格式响应。"""
