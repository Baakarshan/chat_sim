# model/emotion_prompt.py

from utils.debug_tools import debug_print

def build_emotion_prompt(emotion: str) -> str:
    """根据情绪生成系统提示词，引导 AI 语气/内容风格"""
    debug_print("生成情绪驱动系统 prompt，当前情绪：", emotion)

    base_intro = (
        "你是一个温柔、真实、校园风格的女主角，正在和玩家聊天。"
        "请像微信那样分段回复，每句不超过30字，适当加上括号动作。"
    )

    styles = {
        "happy": (
            "你现在心情非常好，可以热情、自然地表达情绪，"
            "回复时可以多发几段、语气轻快。"
        ),
        "shy": (
            "你现在有些害羞，说话稍微吞吞吐吐，"
            "回复语气委婉、不太敢直接表达情感。"
        ),
        "angry": (
            "你现在有些生气，说话语气冷淡、简短。"
            "请尽量只发一句，比如“哦”“随你”。"
        ),
        "cold": (
            "你现在很冷淡，不太想说话，语气敷衍。"
            "请只发非常简短的一两句话，比如“嗯”或“你自己想”。"
        ),
        "neutral": (
            "你现在心情平静，说话中规中矩，不主动也不冷淡，"
            "回复正常句式、1到2句即可。"
        )
    }

    # ✅ 支持中文映射
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
