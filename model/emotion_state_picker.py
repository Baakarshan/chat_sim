# model/emotion_state_picker.py

from utils.debug_tools import debug_print

# （已废弃）候选列表已移至 config.py 管理
# EMOTION_CANDIDATES = [...]
# STATE_CANDIDATES = [...]

def pick_emotion_state(history, reply_text, scene):
    """
    （已废弃）旧逻辑：调用模型判断情绪 + 状态
    ✅ 当前所有结构化结果应从主 chat_stream 中一次性返回。
    保留此函数仅做兼容占位用。
    """
    debug_print("跳过 pick_emotion_state，已由主接口统一决定")
    return "平静", "放空"
