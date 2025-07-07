# config.py
# coding: utf-8
"""
全局配置文件。
遵循 Google Python 风格指南，增加详细中文注释。
"""

import os  # 导入操作系统接口模块

# ========== OPENAI 接口配置 ==========
API_KEY: str = os.getenv("ARK_API_KEY", "0696b289-62f9-46dc-812c-1c5e2d3bfbef")  # API 密钥，优先从环境变量读取
ENDPOINT_ID: str = os.getenv("ENDPOINT_ID", "doubao-seed-1-6-250615")  # 接口端点 ID
BASE_URL: str = "https://ark.cn-beijing.volces.com/api/v3/"  # API 基础 URL

# ========== 路径配置 ==========
HISTORY_PATH: str = "data/history.json"  # 聊天历史文件路径
STATE_PATH: str = "data/state.json"  # 游戏状态文件路径

# ========== 游戏场景配置 ==========
SCENES: dict = {
    "intro": {
        "trigger": 10,  # 触发分数
        "next": ["library"],  # 下一个场景
        "preset": "旁白：你在校园里第一次遇到她...",  # 预设旁白
        "autogen": False  # 是否自动生成
    },
    "library": {
        "trigger": 30,
        "next": ["wedding"],
        "autogen": True
    },
    "wedding": {
        "trigger": 80,
        "next": [],
        "preset": "旁白：多年后，你们在樱花树下举行了婚礼。",
        "autogen": False
    }
}

# ========== 候选情绪（固定两个字） ==========
EMOTIONS: list = [
    "开心", "冷漠", "害羞", "生气", "难过", "惊讶", "平静"
]

# ========== 候选状态（固定两个字） ==========
STATUSES: list = [
    "放空", "紧张", "期待", "学习", "烦恼", "思考", "回忆"
]

# ========== 控制项 ==========
DEBUG_MODE: bool = True  # 是否开启调试模式
