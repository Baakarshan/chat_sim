# model/game_state/loader.py
# coding: utf-8
"""
游戏状态加载与保存模块。
遵循 Google Python 风格指南，增加详细中文注释。
"""

import json  # 导入 JSON 序列化模块
import os  # 导入操作系统模块
from config import STATE_PATH  # 导入状态��件路径
from utils.debug_tools import debug_print  # 导入调试打印

def load_state(GameStateClass):
    """
    从文件中加载状态，如果失败则返回初始状态。
    Args:
        GameStateClass: 游戏状态类。
    Returns:
        GameStateClass: 加载后的状态对象。
    """
    if not os.path.exists(STATE_PATH):
        debug_print("未找到状态文件，使用默认初始状态")
        return GameStateClass()

    try:
        with open(STATE_PATH, 'r', encoding='utf-8-sig') as f:
            content = f.read().strip()
            if not content:
                debug_print("状态文件为空，使用初始状态")
                return GameStateClass()

            data = json.loads(content)
            obj = GameStateClass()
            obj.current_scene = data.get("current_scene", "intro")
            obj.favor = data.get("favor", 0)
            obj.triggered = set(data.get("triggered", []))
            obj.is_finished = data.get("is_finished", False)
            obj.emotion = data.get("emotion", "平静")
            obj.status = data.get("status", "放空")
            return obj
    except Exception as e:
        debug_print("加载状态失败，错误信息：", e)
        return GameStateClass()

def save_state(state_obj) -> None:
    """
    保存状态到文件。
    Args:
        state_obj: 游戏状态对象。
    """
    try:
        with open(STATE_PATH, 'w', encoding='utf-8-sig') as f:
            json.dump(state_obj.to_dict(), f, ensure_ascii=False, indent=2)
        debug_print("状态保存成功")
    except Exception as e:
        debug_print("保存状态失败：", e)

def reset_state_file() -> None:
    """
    清空状态文件。
    """
    try:
        with open(STATE_PATH, 'w', encoding='utf-8') as f:
            f.write("")
        debug_print("状态文件已重置为空")
    except Exception as e:
        debug_print("重置状态文件失败：", e)
