# model/scene.py

from config import SCENES
from model.chatbot_api import generate_scene_description
from utils.debug_tools import debug_print

def get_prompt(scene_name):
    """获取该场景的旁白文本，如未缓存则通过AI生成"""
    scene = SCENES.get(scene_name)
    if not scene:
        debug_print(f"未找到场景定义：{scene_name} → 返回默认旁白")
        return "（你正站在一个不知名的校园角落。）"

    if scene.get("autogen"):
        debug_print(f"场景 {scene_name} 设置为自动生成旁白，调用 AI")
        return generate_scene_description(scene_name)

    debug_print(f"场景 {scene_name} 使用预设旁白")
    return scene.get("preset", f"（你来到了 {scene_name}。）")
