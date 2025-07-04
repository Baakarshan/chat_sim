# model/game_state/transition.py

from config import SCENES
from utils.debug_tools import debug_print

def check_scene_transition(state):
    """
    判断当前场景是否已满足切换条件（affection ≥ trigger）
    若满足则切换到下一个场景（默认只切一次）
    """
    scene = SCENES.get(state.current_scene)
    if not scene:
        debug_print(f"无法获取场景 {state.current_scene} 配置")
        return

    if state.current_scene in state.triggered:
        return

    trigger = scene.get("trigger", 999)
    if state.affection >= trigger:
        state.triggered.add(state.current_scene)
        next_scenes = scene.get("next", [])
        if next_scenes:
            next_scene = next_scenes[0]
            debug_print(f"好感度达到 {state.affection}，切换场景 → {next_scene}")
            state.current_scene = next_scene
