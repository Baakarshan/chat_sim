# model/scene.py
# coding: utf-8
"""
场景信息与逻辑模块。
遵循 Google Python 风格指南，增加详细中文注释。
"""

from config import SCENES  # 导入场景配置
from model.scene_generator import generate_scene_intro  # 导入场景 intro 生成

def get_prompt(scene_id: str) -> str:
    """
    获取指定场景的固定 preset 旁白（若存在）。
    Args:
        scene_id: 场景 ID。
    Returns:
        str: 旁白文本。
    """
    scene = SCENES.get(scene_id)
    if scene and scene.get("preset"):
        return scene["preset"]
    return ""

def is_autogen(scene_id: str) -> bool:
    """
    判断该场景是否允许自动生成旁白。
    Args:
        scene_id: 场景 ID。
    Returns:
        bool: 是否自动生成。
    """
    scene = SCENES.get(scene_id)
    return scene.get("autogen", False)

def get_trigger_threshold(scene_id: str) -> int:
    """
    获取该场景的好感触发阈值。
    Args:
        scene_id: 场景 ID。
    Returns:
        int: 好感度阈值。
    """
    scene = SCENES.get(scene_id)
    return scene.get("trigger", 0)

def get_next_scene(scene_id: str) -> str:
    """
    获取该场景的下一步（默认取第一个）。
    Args:
        scene_id: 场景 ID。
    Returns:
        str: 下一个场景 ID。
    """
    scene = SCENES.get(scene_id)
    next_list = scene.get("next", [])
    return next_list[0] if next_list else ""

def should_enter_scene(current_scene: str, favor: int) -> bool:
    """
    判断是否触发进入下一个场景。
    Args:
        current_scene: 当前场景 ID。
        favor: 当前好感度。
    Returns:
        bool: 是否满足进入条件。
    """
    threshold = get_trigger_threshold(current_scene)
    return favor >= threshold
