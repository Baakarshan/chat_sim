# model/scene_generator.py

from model.chatbot_api import chat_once
from utils.debug_tools import debug_print

def generate_scene_intro(current_scene, emotion, status, history):
    """
    调用大模型生成一条新的场景提示语（除首次外）

    :param current_scene: 当前所在场景（如 intro / library）
    :param emotion: 当前角色情绪（如 开心）
    :param status: 当前角色状态（如 阅读）
    :param history: 当前历史对话（最近几轮）
    :return: 简短旁白文本（建议 10~20 字）
    """

    system_prompt = f"""
你是一个校园恋爱模拟器中的旁白生成器。
请基于以下要素，生成一条极短的场景提示（10~25 字）：

- 当前地点场景：“{current_scene}”
- 女主当前情绪是：“{emotion}”
- 女主当前状态是：“{status}”
- 玩家刚刚说的话是：“{get_last_user_input(history)}”

格式要求：
- 只返回一句“简短描写”，不要加任何多余注释
- 例如：“傍晚，图书馆，窗外微雨。”
- 或：“中午，操场边传来喧闹的笑声。”

现在请你生成提示。
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
    return "你好"
