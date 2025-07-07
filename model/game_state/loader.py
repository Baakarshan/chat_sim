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
        with open(STATE_PATH, 'r', encoding='utf-8-sig') as f:  # ✅ 修改这里
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


def save_state(state_obj):
    """保存状态到文件"""
    try:
        with open(STATE_PATH, 'w', encoding='utf-8-sig') as f:
            json.dump(state_obj.to_dict(), f, ensure_ascii=False, indent=2)
        debug_print("状态保存成功")
    except Exception as e:
        debug_print("保存状态失败：", e)

def reset_state_file():
    """清空状态文件"""
    try:
        with open(STATE_PATH, 'w', encoding='utf-8') as f:
            f.write("")
        debug_print("状态文件已重置为空")
    except Exception as e:
        debug_print("重置状态文件失败：", e)
