# model/game_state/transition.py
# coding: utf-8
"""
场景跳转逻辑模块。
遵循 Google Python 风格指南，增加详细中文注释。
"""

from model.scene import get_trigger_threshold, get_next_scene, is_autogen  # 导入场景相关方法
from model.scene_generator import generate_scene_intro  # 导入场景 intro 生成
from utils.debug_tools import debug_print  # 导入��试打印

def check_scene_transition(state) -> None:
    """
    判断当前好感度是否满足场景跳转条件，如满足则切换场景并添加旁白。
    Args:
        state: 游戏状态对象。
    Returns:
        None
    """
    current = state.current_scene
    trigger = get_trigger_threshold(current)

    if state.favor >= trigger and current not in state.triggered:
        debug_print(f"好感度已达阈值（{state.favor} >= {trigger}），触发场景跳转")
        state.triggered.add(current)

        next_scene = get_next_scene(current)
        if not next_scene:
            debug_print("无下一个场景")
            return

        state.current_scene = next_scene

        if is_autogen(next_scene):
            debug_print("新场景支持自动旁白，等待异步生成")
        else:
            debug_print("新场景使用 preset 旁白")
