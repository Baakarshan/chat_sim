# model/chatbot_api.py

from openai import OpenAI
from config import API_KEY, ENDPOINT_ID, BASE_URL
from model.chat_fallback import get_default_reply, build_scene_prompt
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
    """主对话流式生成函数：逐块返回模型输出；如超时自动fallback"""
    result_queue = queue.Queue()
    finished = threading.Event()

    if len(messages) > 20:
        debug_print("历史消息过多，仅保留最近 20 条")
        messages = messages[:1] + messages[-19:]

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
    """
    单次调用模型（非流式），用于生成场景提示、摘要等
    返回纯文本（不结构化）
    """
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
