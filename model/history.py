# model/history.py

import json
import os
from config import HISTORY_PATH
from utils.debug_tools import debug_print

def load_history():
    """从文件加载历史记录"""
    if not os.path.exists(HISTORY_PATH):
        return []
    try:
        with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception as e:
        debug_print("加载历史记录失败：", e)
        return []

def save_history(history):
    """保存当前历史记录"""
    try:
        with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        debug_print("历史记录保存成功")
    except Exception as e:
        debug_print("保存历史记录失败：", e)

def reset_history():
    """清空历史记录文件"""
    try:
        with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
            f.write("[]")
        debug_print("历史记录已清空")
    except Exception as e:
        debug_print("重置历史记录失败：", e)
