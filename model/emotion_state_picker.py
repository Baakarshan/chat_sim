# model/emotion_state_picker.py

from model.chatbot_api import chat_once
from utils.debug_tools import debug_print

EMOTION_CANDIDATES = ["开心", "高兴", "冷静", "生气", "冷漠", "紧张", "害羞", "沉思", "失落", "平静"]
STATE_CANDIDATES = ["阅读", "作业", "散步", "吃饭", "放空", "回忆", "等待", "想你", "观察", "避让"]

def pick_emotion_state(history, reply_text, scene):
    """
    调用大模型，判断当前角色的情绪与状态
    :param history: List[Dict] 聊天上下文
    :param reply_text: 最新 AI 回复文本
    :param scene: 当前场景名
    :return: (emotion, state)，中文两个字，来自候选项
    """
    system_prompt = f"""
你是校园恋爱模拟器中的女主角助手，负责根据上下文推断角色的情绪和状态。
你必须从以下固定选项中分别选择一个：

情绪选项：{"、".join(EMOTION_CANDIDATES)}
状态选项：{"、".join(STATE_CANDIDATES)}

当前场景是：“{scene}”
玩家刚才说了什么？你是如何回应的？请基于这些判断当前情绪和状态，并以以下格式返回：

情绪：XX
状态：XX

请直接回复，不要加多余说明。
""".strip()

    messages = [{"role": "system", "content": system_prompt}] + history[-10:]
    result = chat_once(messages)
    debug_print("AI判定情绪+状态原始返回：", result)

    emotion, state = extract_emotion_state(result)
    return emotion, state

def extract_emotion_state(text):
    """
    解析模型返回的格式，强制匹配本地候选词列表
    """
    emotion = "平静"
    state = "放空"

    for line in text.strip().splitlines():
        if line.startswith("情绪："):
            raw = line[3:].strip()
            if raw in EMOTION_CANDIDATES:
                emotion = raw
        elif line.startswith("状态："):
            raw = line[3:].strip()
            if raw in STATE_CANDIDATES:
                state = raw

    return emotion, state
