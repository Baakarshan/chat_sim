# controller/stream_utils.py
# coding: utf-8
"""
流式输出工具模块。
遵循 Google Python 风格指南，增加详细中文注释。
"""

from controller.helpers import is_sentence_end  # 导入句子结束判断函数

def split_reply_into_blocks(text: str) -> list:
    """
    将完整回复按段落或语义拆分为多个小段，每段后续作为一个气泡独立显示。
    Args:
        text: 完整回复文本。
    Returns:
        list: 拆分后的小段列表。
    """
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]  # 按行去除空白
    blocks = []  # 存储分段结果
    current = ""  # 当前段落缓存
    for line in lines:
        current += line + " "  # 累加行内容
        # 若该行已构成完整语义或长度较长，则分段
        if is_sentence_end(line.strip()) or len(line.strip()) > 20:
            blocks.append(current.strip())
            current = ""
    if current.strip():
        blocks.append(current.strip())  # 处理最后一段
    return blocks

def safe_append_text(chat_frame, text: str) -> None:
    """
    用于 thread-safe 更新 Tkinter 气泡内容。
    注意：这个函数会在 lambda 中被调用。
    Args:
        chat_frame: 聊天界面框架。
        text: 追加的文本内容。
    """
    chat_frame.stream_append(text)  # 线程安全地追加文本
