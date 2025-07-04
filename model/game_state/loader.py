# model/game_state/loader.py

import json
import os
from config import STATE_PATH
from utils.debug_tools import debug_print

def load_state(GameStateClass):
    """从文件中加载状态，如果失败则返回初始状态"""
    if not os.path.exists(STATE_PATH):
        debug_print("未找到状态文件，使用默认初始状态")
        return GameStateClass()

    try:
        with open(STATE_PATH, 'r') as f:
            content = f.read().strip()
            if not content:
                debug_print("状态文件为空，使用初始状态")
                return GameStateClass()

            data = json.loads(content)
            obj = GameStateClass()
            obj.current_scene = data.get("current_scene", "intro")
            obj.affection = data.get("affection", 0)
            obj.triggered = set(data.get("triggered", []))
            obj.is_finished = data.get("is_finished", False)
            obj.emotion = data.get("emotion", "neutral")
            obj.status = data.get("status", "放空")
            obj.tone_history = data.get("tone_history", [])
            debug_print("成功加载游戏状态")
            return obj
    except Exception as e:
        debug_print("加载游戏状态失败：", repr(e))
        return GameStateClass()

def save_state(game_state):
    try:
        with open(STATE_PATH, 'w') as f:
            json.dump(game_state.to_dict(), f, indent=2)
        debug_print("游戏状态已保存")
    except Exception as e:
        debug_print("保存状态失败：", repr(e))

def reset_state_file():
    if os.path.exists(STATE_PATH):
        try:
            os.remove(STATE_PATH)
            debug_print("游戏状态文件已清除")
        except Exception as e:
            debug_print("清除状态文件失败：", repr(e))
