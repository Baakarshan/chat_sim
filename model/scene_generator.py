# model/scene_generator.py
# coding: utf-8
"""
场景提示语生成模块。
遵循 Google Python 风格指南，增加详细中文注释。
"""

from model.chatbot_api import chat_once  # 导入单轮对话接口
from utils.debug_tools import debug_print  # 导入调试打印

def generate_scene_intro(current_scene: str, emotion: str, status: str, history: list) -> str:
    """
    调用大模型生成一条新的场景提示语（除首次外）。
    Args:
        current_scene: 当前场景名，如 "intro"。
        emotion: 当前情绪，如 "冷漠"。
        status: 当前状态，如 "学习"。
        history: 历史对话列表。
    Returns:
        str: 场景提示语（建议 10~25 字）。
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

def get_last_user_input(history: list) -> str:
    """
    返回最近一条用户输入。
    Args:
        history: 聊天历史列表。
    Returns:
        str: 最近一条用户输入内容。
    """
    for msg in reversed(history):
        if msg["role"] == "user":
            return msg["content"]
    return "（无）"
