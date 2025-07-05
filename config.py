# config.py
import os

# ========== OPENAI 接口配置 ==========
API_KEY = os.getenv("ARK_API_KEY", "0696b289-62f9-46dc-812c-1c5e2d3bfbef")
ENDPOINT_ID = os.getenv("ENDPOINT_ID", "doubao-seed-1-6-250615")
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/"

# ========== 路径配置 ==========
HISTORY_PATH = "data/history.json"
STATE_PATH = "data/state.json"

# ========== 游戏场景配置 ==========
SCENES = {
    "intro": {
        "trigger": 10,
        "next": ["library"],
        "preset": "旁白：你在校园里第一次遇到她...",
        "autogen": False
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
EMOTIONS = [
    "开心", "冷漠", "害羞", "生气", "难过", "惊讶", "平静"
]

# ========== 候选状态（固定两个字） ==========
STATUSES = [
    "放空", "紧张", "期待", "学习", "烦恼", "思考", "回忆"
]

# ========== 控制项 ==========
DEBUG_MODE = True
