# model/chatbot_api.py

from openai import OpenAI
from config import API_KEY, ENDPOINT_ID, BASE_URL
from model.chat_fallback import get_default_reply
from utils.debug_tools import debug_print
import threading
import queue
import time
import json

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

def chat_stream(messages):
    """主对话流式生成函数：逐块返回模型输出；如超时自动 fallback"""
    result_queue = queue.Queue()
    finished = threading.Event()

    # 添加结构化提示 system prompt（确保总是开头）
    system_instruction = {
        "role": "system",
        "content": (
            "你是校园恋爱模拟器中的女主角，接下来你将扮演女主角，回复玩家说的话。"
            "请你以以下格式回复一个合法 JSON 对象，内容必须包含以下字段：\n"
            "- reply：你想说的话，1~3 句短句即可，建议加括号动作（如“（轻笑）真的吗？”）\n"
            "- emotion：当前情绪，必须是以下之一：开心、生气、冷漠、害羞、惊讶、难过、平静\n"
            "- status：当前状态，必须是以下之一：放空、思考、期待、紧张、学习\n"
            "- favor：整数，表示你对玩家的好感度变化（例如 2，-1）\n"
            "⚠️ 你必须只输出 JSON 对象，不加任何注释、解释或自然语言。"
        )
    }

    messages = [system_instruction] + messages[-20:]  # 限制长度

    def run_stream():
        try:
            debug_print("开始调用大模型（流式模式）...")
            for chunk in client.chat.completions.create(
                model=ENDPOINT_ID,
                messages=messages,
                stream=True,
            ):
                delta = chunk.choices[0].delta
                if hasattr(delta, "content") and delta.content:
                    result_queue.put(delta.content)
            finished.set()
        except Exception as e:
            debug_print("模型流异常：", e)
            finished.set()

    threading.Thread(target=run_stream, daemon=True).start()

    full_reply = ""
    start_time = time.time()

    while not finished.is_set() or not result_queue.empty():
        try:
            piece = result_queue.get(timeout=1)
            full_reply += piece
        except queue.Empty:
            if time.time() - start_time > 15:
                debug_print("等待模型超时，使用 fallback")
                break

    # 尝试解析结构化 JSON（reply/emotion/status/favor）
    try:
        response = json.loads(full_reply)
        if all(k in response for k in ("reply", "emotion", "status", "favor")):
            return response
    except Exception as e:
        debug_print("结构化解析失败，fallback 使用默认")

    return {
        "reply": full_reply.strip() or get_default_reply(),
        "emotion": "平静",
        "status": "放空",
        "favor": 0
    }

def chat_once(messages):
    """单轮调用，用于生成场景 intro 提示"""
    try:
        debug_print("调用 chat_once 获取单句文本")
        response = client.chat.completions.create(
            model=ENDPOINT_ID,
            messages=messages,
            stream=False,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        debug_print("chat_once 调用失败：", e)
        return get_default_reply()
