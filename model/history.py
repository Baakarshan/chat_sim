# model/history.py

import json
import os
from config import HISTORY_PATH
from utils.debug_tools import debug_print

def load_history():
    if not os.path.exists(HISTORY_PATH):
        return []
    try:
        with open(HISTORY_PATH, 'r') as f:
            content = f.read().strip()
            if not content:
                debug_print("历史记录文件为空")
                return []
            history = json.loads(content)
            debug_print("成功加载历史记录")
            return history
    except Exception as e:
        debug_print("加载历史记录失败：", repr(e))
        return []

def save_history(history):
    try:
        with open(HISTORY_PATH, 'w') as f:
            json.dump(history, f, indent=2)
        debug_print("成功保存历史记录")
    except Exception as e:
        debug_print("保存历史记录失败：", repr(e))

def clear_history():
    """清空历史聊天记录文件"""
    if os.path.exists(HISTORY_PATH):
        try:
            os.remove(HISTORY_PATH)
            debug_print("历史记录已清除")
        except Exception as e:
            debug_print("清除历史记录失败：", repr(e))
