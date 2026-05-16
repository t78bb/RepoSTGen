#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LITL 验证配置文件
"""

import os
from pathlib import Path

# ==================== 项目路径配置 ====================
# 项目根目录
REPO_ROOT = Path(__file__).parent.parent

# output目录
OUTPUT_BASE_DIR = REPO_ROOT / "output"

# dataset目录
DATASET_DIR = REPO_ROOT / "dataset"
PROJECT_CODE_DIR = DATASET_DIR / "project_code"
QUERY_DIR = DATASET_DIR / "query"

# ==================== LLM API 配置 ====================
# 支持的API类型: "openai", "azure", "deepseek", "custom"
API_TYPE = "openai"

# API密钥 (从环境变量读取，或在此处设置)
# 当前使用智增增中转站（https://api.zhizengzeng.com）
API_KEY = os.getenv("OPENAI_API_KEY", os.getenv("API_KEY"))

# API端点 - 智增增中转站
API_BASE = os.getenv("BASE_URL", os.getenv("OPENAI_API_BASE", "https://api.zhizengzeng.com/v1"))

# 模型名称
# 智增增支持多种模型，推荐使用 gpt-4、gpt-4-turbo、gpt-3.5-turbo 或 gpt-5.2
MODEL_NAME = os.getenv("LLM_MODEL", "gpt-5.2")

# API调用超时时间（秒）
API_TIMEOUT = 120

# API调用重试次数
MAX_RETRIES = 3

# ==================== 评估配置 ====================
# 评估维度及其权重
EVALUATION_DIMENSIONS = {
    "functional_correctness": {
        "name": "功能正确性",
        "weight": 0.4,
        "description": "代码是否正确实现了需求规范中定义的所有功能"
    },
    "readability_and_style": {
        "name": "可读性和风格",
        "weight": 0.2,
        "description": "代码的命名规范、注释质量、结构清晰度等"
    },
    "safety_compliance": {
        "name": "安全合规性",
        "weight": 0.25,
        "description": "代码是否符合IEC 61131-3标准和PLC安全规范"
    },
    "modularity": {
        "name": "模块化",
        "weight": 0.15,
        "description": "代码的模块化程度、可维护性和可扩展性"
    }
}

# 通过阈值（总分达到此分数视为通过）
PASS_THRESHOLD = 60.0

# ==================== 结果保存配置 ====================
# 结果文件名格式
RESULT_FILENAME_FORMAT = "litl_evaluation_{timestamp}.json"

# 是否保存详细日志
SAVE_DETAILED_LOG = True

# ==================== 其他配置 ====================
# 是否显示进度条
SHOW_PROGRESS = True

# 并发评估数量（设为1表示串行执行，避免API限流）
CONCURRENT_EVALUATIONS = 1

# 调试模式
DEBUG = False

