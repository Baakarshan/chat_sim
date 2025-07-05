# model/scene.py

from config import SCENES
from model.scene_generator import generate_scene_intro

def get_prompt(scene_id: str) -> str:
    """
    获取指定场景的固定 preset 旁白（若存在）
    """
    scene = SCENES.get(scene_id)
    if scene and scene.get("preset"):
        return scene["preset"]
    return ""

def is_autogen(scene_id: str) -> bool:
    """
    判断该场景是否允许自动生成旁白
    """
    scene = SCENES.get(scene_id)
    return scene.get("autogen", False)

def get_trigger_threshold(scene_id: str) -> int:
    """
    获取该场景的好感触发阈值
    """
    scene = SCENES.get(scene_id)
    return scene.get("trigger", 0)

def get_next_scene(scene_id: str) -> str:
    """
    获取该场景的下一步（默认取第一个）
    """
    scene = SCENES.get(scene_id)
    next_list = scene.get("next", [])
    return next_list[0] if next_list else ""

def should_enter_scene(current_scene, favor) -> bool:
    """
    判断是否触发进入下一个场景
    """
    threshold = get_trigger_threshold(current_scene)
    return favor >= threshold
