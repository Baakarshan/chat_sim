# model/game_state/emotion_logic.py

import random

def update_emotion(state):
    """
    根据 tone_history 和 affection 决定当前情绪（供本地情绪候选使用）

    - 最近连续 3 次 neutral / compliment / flirt，可从 angry/cold 恢复
    - affection 阶段性决定情绪区间，但有轻度随机
    """
    recent = state.tone_history[-3:]
    positive = {"neutral", "compliment", "flirt"}

    if state.emotion in ["angry", "cold"] and all(t in positive for t in recent):
        state.emotion = "happy" if state.affection >= 60 else "neutral"
        return

    aff = state.affection
    roll = random.random()

    if aff >= 80:
        state.emotion = "happy" if roll > 0.2 else "neutral"
    elif aff >= 50:
        state.emotion = "neutral" if roll > 0.2 else "shy"
    elif aff >= 30:
        state.emotion = random.choice(["neutral", "shy"])
    else:
        state.emotion = random.choice(["cold", "angry"])
