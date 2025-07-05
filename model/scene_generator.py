# model/scene_generator.py

from model.chatbot_api import chat_once
from utils.debug_tools import debug_print

def generate_scene_intro(current_scene, emotion, status, history):
    """
    调用大模型生成一条新的场景提示语（除首次外）
    :param current_scene: 当前场景名，如 "intro"
    :param emotion: 当前情绪，如 "冷漠"
    :param status: 当前状态，如 "学习"
    :param history: 历史对话列表
    :return: 场景提示语（建议 10~25 字）
    """
    system_prompt = f"""
你是校园恋爱模拟器中的旁白生成器。
请根据以下要素生成一条简洁的场景描写（10~25字）：

- 当前场景：“{current_scene}”
- 女主情绪：“{emotion}”
- 女主状态：“{status}”
- 玩家刚刚说的话：“{get_last_user_input(history)}”

请直接返回一句中文短句，不加注释。
    """.strip()

    messages = [{"role": "system", "content": system_prompt}]
    result = chat_once(messages)
    debug_print("AI生成场景提示：", result)
    return result.strip()

def get_last_user_input(history):
    """
    返回最近一条用户输入
    """
    for msg in reversed(history):
        if msg["role"] == "user":
            return msg["content"]
    return "（无）"
