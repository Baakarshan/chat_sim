# gui/window_init.py

from model.history import load_history
from model.scene import get_prompt
from model.scene_generator import generate_scene_intro
from utils.debug_tools import debug_print
import threading

def load_history_if_any(ctrl, chat_frame):
    """
    加载历史记录到聊天界面，返回历史列表
    """
    history = load_history()
    if not history:
        return []

    debug_print("成功加载历史记录")
    debug_print("加载历史记录条数：", len(history))
    for msg in history:
        role = msg["role"]
        if role == "assistant":
            role = "npc"
        chat_frame.add_message(role, msg["content"])

    # ✅ 添加历史记录标线
    chat_frame.add_message("system", "———— 以上为历史记录 ————")
    return history

def start_intro_if_needed(ctrl, chat_frame, history):
    """
    启动时判断是否需要补充旁白：
    - 无历史：插入默认 preset
    - 有历史：异步生成 AI 场景提示，避免卡顿
    """
    if not history:
        debug_print("首次启动，注入初始旁白")
        preset = get_prompt(ctrl.state.current_scene)
        ctrl.push_system(preset)
        return

    debug_print("重新打开，有历史 → 异步注入 AI 场景提示")

    def generate_async():
        desc = generate_scene_intro(
            current_scene=ctrl.state.current_scene,
            emotion=ctrl.state.emotion,
            status=ctrl.state.status,
            history=history
        )
        chat_frame.after(0, lambda: ctrl.push_system(desc))

    threading.Thread(target=generate_async, daemon=True).start()
