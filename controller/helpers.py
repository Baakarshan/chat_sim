# controller/helpers.py

def is_sentence_end(text: str) -> bool:
    """
    判断一段文字是否已构成完整回复（用于气泡分段）

    满足以下任一条件即可判定为“结束”：
    - 末尾有句号、叹号、问号（。！？）或换行符
    - 或长度超过 30 字
    - 或以 '）' 结尾（常见动作括号）
    """
    return (
        any(p in text for p in "。！？\n") or
        len(text) > 30 or
        text.endswith("）")
    )
