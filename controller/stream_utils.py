# controller/stream_utils.py

from controller.helpers import is_sentence_end

def split_reply_into_blocks(text: str):
    """
    将完整回复按段落或语义拆分为多个小段，
    每段后续作为一个气泡独立显示。
    """
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    blocks = []
    current = ""
    for line in lines:
        current += line + " "
        if is_sentence_end(line.strip()) or len(line.strip()) > 20:
            blocks.append(current.strip())
            current = ""
    if current.strip():
        blocks.append(current.strip())
    return blocks

def safe_append_text(chat_frame, text):
    """
    用于 thread-safe 更新 Tkinter 气泡内容。
    注意：这个函数会在 lambda 中被调用。
    """
    chat_frame.stream_append(text)
