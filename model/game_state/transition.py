# model/game_state/transition.py

from model.scene import get_trigger_threshold, get_next_scene, is_autogen
from model.scene_generator import generate_scene_intro
from utils.debug_tools import debug_print

def check_scene_transition(state):
    """
    判断当前好感度是否满足场景跳转条件，如满足则切换场景并添加旁白
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
