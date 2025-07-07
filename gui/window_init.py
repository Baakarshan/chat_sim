# gui/window_init.py
# coding: utf-8
"""
窗口初始化相关逻辑。
遵循 Google Python 风格指南，增加详细中文注释。
"""

from model.history import load_history  # 导入历史加载
from model.scene import get_prompt  # 导入场景提示
from model.scene_generator import generate_scene_intro  # 导入场景 intro 生成
from utils.debug_tools import debug_print  # 导入调试打印
import threading  # 导入线程库

def load_history_if_any(ctrl, chat_frame):
    """
    加载历史记录到聊天界面。
    Args:
        ctrl: 聊天控制器。
        chat_frame: 聊天界面。
    Returns:
        list: 历史消息列表。
    """
    history = load_history()  # 加载历史
    if not history:
        return []

    debug_print("成功加载历史记录")
    debug_print("加载历史记录条数：", len(history))
    for msg in history:
        role = msg["role"]
        if role == "assistant":
            role = "npc"  # assistant 统一为 npc
        chat_frame.add_message(role, msg["content"])

    # ✅ 添加历史记录标线
    chat_frame.add_message("system", "———— 以上为历史记录 ————")
    return history

def start_intro_if_needed(ctrl, chat_frame, history):
    """
    启动时判断是否需要补充旁白。
    - 无历史：插入默认 preset
    - 有历史：异步生成 AI 场景提示，避免卡顿
    Args:
        ctrl: 聊天控制器。
        chat_frame: 聊天界面。
        history: 历史消息列表。
    """
    if not history:
        debug_print("首次启动，注入初始旁白")
        preset = get_prompt(ctrl.state.current_scene)  # 获取当前场景 preset
        ctrl.push_system(preset)
        return

    debug_print("历史存在，异步生成 intro 场景提示")
    def generate():
        intro = generate_scene_intro(
            current_scene=ctrl.state.current_scene,
            emotion=ctrl.state.emotion,
            status=ctrl.state.status,
            history=history
        )
        ctrl.push_system(intro)

    threading.Thread(target=generate, daemon=True).start()  # 异步生成 intro
