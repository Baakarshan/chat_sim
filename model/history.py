# model/history.py
# coding: utf-8
"""
历史记录管理模块。
遵循 Google Python 风格指南，增加详细中文注释。
"""

import json  # 导入 JSON 序列化模块
import os  # 导入操作系统模块
from config import HISTORY_PATH  # 导入历史文件路径
from utils.debug_tools import debug_print  # 导入调试打��

def load_history() -> list:
    """
    从文件加载历史记录。
    Returns:
        list: 聊天历史消息列表。
    """
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

def save_history(history: list) -> None:
    """
    保存当前历史记录。
    Args:
        history: 聊天历史消息列表。
    """
    try:
        with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        debug_print("历史记录保存成功")
    except Exception as e:
        debug_print("保存历史记录失败：", e)

def reset_history() -> None:
    """
    清空历史记录文件。
    """
    try:
        with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
            f.write("[]")  # 写入空列表，清空历史
        debug_print("历史记录已清空")
    except Exception as e:
        debug_print("重置历史记录失败：", e)
