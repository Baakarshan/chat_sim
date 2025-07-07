# controller/helpers.py
# coding: utf-8
"""
辅助函数模块。
遵循 Google Python 风格指南，增加详细中文注释。
"""

def is_sentence_end(text: str) -> bool:
    """
    判断一段文字是否已构成完整回复（用于气泡分段）。

    满足以下任一条件即可判定为“结束”：
    - 末尾有句号、叹号、问号（。！？）或换行符
    - 或长度超过 30 字
    - 或以 '）' 结尾（常见动作括号）

    Args:
        text: 输入的文本字符串。
    Returns:
        bool: 是否为完整回复。
    """
    # 检查是否包含句号、叹号、问号或换行符
    if any(p in text for p in "。！？\n"):
        return True
    # 检查长度是否超过 30 字
    if len(text) > 30:
        return True
    # 检查是否以 '）' 结尾
    if text.endswith("）"):
        return True
    return False
