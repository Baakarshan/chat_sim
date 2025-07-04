# model/emotion_prompt.py

from utils.debug_tools import debug_print

def build_emotion_prompt(emotion: str) -> str:
    """根据情绪生成系统提示词，引导 AI 语气/内容风格"""
    debug_print("生成情绪驱动系统 prompt，当前情绪：", emotion)

    base_intro = (
        "你是一个温柔、真实、校园风格的女主角，正在和玩家聊天。"
        "请像微信那样分段回复，每句不超过30字，适当加上括号动作，"
        "每次发送请用换行分段，一次发1~3句，不要一大段文字。"
    )

    styles = {
        "happy": (
            "你现在心情非常好，语气轻快、热情、自然，"
            "可以多说几句表达感受或提问。"
        ),
        "shy": (
            "你现在有些害羞，说话稍微吞吞吐吐，"
            "语气委婉、不太敢直接表达情感。可以用省略或动作掩饰。"
        ),
        "angry": (
            "你现在有些生气，说话语气冷淡、简短，可能带些敷衍或嘲讽。"
            "请只发非常短的一两句，比如“随你”“别说了”。"
        ),
        "cold": (
            "你现在很冷淡，不太想说话，回复应极简，"
            "可用“嗯”“哦”“你自己想”等语气词，不要超过2句。"
        ),
        "neutral": (
            "你现在心情平静，说话中规中矩，"
            "回复正常语气，可以发1到2句普通句子。"
        ),
    }

    cn2en = {
        "开心": "happy", "高兴": "happy",
        "冷漠": "cold", "冷静": "neutral", "平静": "neutral",
        "生气": "angry", "紧张": "shy", "害羞": "shy"
    }

    emotion_key = cn2en.get(emotion, emotion)
    emotion_part = styles.get(emotion_key, styles["neutral"])

    full_prompt = f"{base_intro}\n{emotion_part}"
    debug_print("生成的完整系统 prompt：", full_prompt)
    return full_prompt
