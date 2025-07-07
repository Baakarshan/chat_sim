# controller/stream_handler.py
# coding: utf-8
"""
流式响应处理模块。
遵循 Google Python 风格指南，增加详细中文注释。
"""

import time  # 导入时间模块，用于延时
import threading  # 导入线程模块（如需异步）
from model.chatbot_api import chat_stream  # 导入 AI 聊天流接口
from model.scene import get_prompt  # 导入场景提示获取方法
from controller.helpers import is_sentence_end  # 导入句子结束判断
from model.history import save_history  # 导入历史保存方法
from utils.debug_tools import debug_print  # 导入调试打印
from controller.stream_utils import split_reply_into_blocks, safe_append_text  # 导入分段与安全追加

def handle_stream_response(chat_frame, state, history, update_status_callback=None):
    """
    处理 AI 的流式回复，并更新 UI、历史和状态。
    Args:
        chat_frame: 聊天界面框架。
        state: 游戏状态对象。
        history: 聊天历史列表。
        update_status_callback: 状态更新回调函数，可选。
    """
    # 构建上下文消息（含系统提示）
    emotion_prompt = {"role": "system", "content": f"当前情绪：{state.emotion}，状态：{state.status}"}
    messages = [emotion_prompt] + history  # 合成消息上下文

    # 获取 AI 回复（结构化返回）
    ai_response = chat_stream(messages)  # 请求 AI 聊天接口
    reply_text = ai_response.get("reply", "")  # 获取回复文本
    new_emotion = ai_response.get("emotion", state.emotion)  # 获取新情绪
    new_status = ai_response.get("status", state.status)  # 获取新状态
    favor_delta = ai_response.get("favor", 0)  # 获取好感度变化

    debug_print("最终回复：", reply_text)  # 输出 AI 回复
    debug_print("AI判断情绪：", new_emotion)
    debug_print("AI判断状态：", new_status)
    debug_print("AI判定好感度变化：", favor_delta)

    # 分段显示回复内容（逐字流式输出）
    reply_blocks = split_reply_into_blocks(reply_text)  # 分段
    for block in reply_blocks:
        if not block.strip():
            continue  # 跳过空段
        debug_print("流式生成一段气泡：", block)
        chat_frame.after(0, lambda: chat_frame.start_stream_reply("npc"))  # 启动 NPC 气泡

        sentence = ""  # 当前句子缓存
        for char in block:
            sentence += char  # 累加字符
            if is_sentence_end(sentence) or len(sentence) >= 30:
                temp = sentence.strip()
                if temp:
                    chat_frame.after(0, lambda s=temp: safe_append_text(chat_frame, s))  # 安全追加文本
                    time.sleep(len(temp) / 10)  # 按长度延时
                sentence = ""

        if sentence.strip():
            temp = sentence.strip()
            chat_frame.after(0, lambda s=temp: safe_append_text(chat_frame, s))

        chat_frame.after(0, chat_frame.finalize_stream_reply)  # 结束气泡

    # 更新本地状态
    history.append({"role": "assistant", "content": reply_text})  # 记录 AI 回复
    state.emotion = new_emotion  # 更新情绪
    state.status = new_status  # 更新状态
    state.favor += favor_delta  # 更新好感度

    # 检查是否进入终场景
    state.check_scene_transition()  # 检查场景切换
    if state.current_scene == "wedding":
        chat_frame.after(0, lambda: chat_frame.add_message("system", get_prompt("wedding")))  # 终场景旁白
        state.is_finished = True  # 标记结束

    # 保存历史与状态
    save_history(history)  # 保��历史
    state.save()  # 保存状态

    # ✅ 显式调用 UI 更新函数
    if update_status_callback:
        chat_frame.after(0, update_status_callback)  # UI 线程安全调用
