# model/chatbot_api.py

from openai import OpenAI
from config import API_KEY, ENDPOINT_ID, BASE_URL
from model.chat_fallback import get_default_reply, build_scene_prompt
from utils.debug_tools import debug_print
import threading
import queue
import time

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
            debug_print("模型返回结束标志（finish_reason=stop）")
            finished.set()
        except Exception as e:
            debug_print("模型请求出错：", repr(e))
            finished.set()

    thread = threading.Thread(target=run_stream, daemon=True)
    thread.start()

    timeout = 12
    start_time = time.time()
    yielded = False

    while not finished.is_set() or not result_queue.empty():
        try:
            chunk = result_queue.get(timeout=0.1)
            yielded = True
            yield chunk
        except queue.Empty:
            if not yielded and time.time() - start_time > timeout:
                debug_print("模型响应超时，触发 fallback ...")
                yield get_default_reply()
                break

def chat_once(messages):
    """
    非流式对话：返回完整回复（用于情绪判断、状态识别、旁白生成）
    """
    try:
        if len(messages) > 15:
            messages = messages[:1] + messages[-14:]

        response = client.chat.completions.create(
            model=ENDPOINT_ID,
            messages=messages,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        debug_print("chat_once 请求出错，使用默认回复。错误：", repr(e))
        return get_default_reply()

def generate_scene_description(scene_name):
    """辅助调用：生成校园场景的时间、地点、天气旁白"""
    messages = [{"role": "user", "content": build_scene_prompt(scene_name)}]
    try:
        debug_print(f"请求生成场景旁白：{scene_name}")
        response = client.chat.completions.create(
            model=ENDPOINT_ID,
            messages=messages,
        )
        content = response.choices[0].message.content.strip()
        debug_print("旁白生成成功：", content)
        return content
    except Exception as e:
        debug_print("旁白生成失败，使用默认旁白。错误：", repr(e))
        return "（清晨，教学楼外，阳光微弱）"
