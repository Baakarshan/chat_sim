# model/emotion_analyzer.py

from utils.debug_tools import debug_print

def analyze_user_input(text: str) -> tuple[int, str]:
    """根据用户输入内容分析情绪，返回：(好感增量, 情绪标签)"""
    lowered = text.lower()
    debug_print("开始分析用户输入情绪内容：", lowered)

    # 冒犯类
    if any(bad in lowered for bad in ["滚", "烦", "闭嘴", "傻", "脑子", "废", "没用"]):
        debug_print("检测到冒犯词汇 → insult")
        return (-5, "insult")

    # 冷漠类
    if any(bored in lowered for bored in ["随便", "无聊", "不管", "懒得", "走开"]):
        debug_print("检测到轻度冷漠词汇 → disrespect")
        return (-2, "disrespect")

    # 赞美类
    if any(praise in lowered for praise in ["好看", "漂亮", "喜欢你", "你真棒", "可爱", "温柔"]):
        debug_print("检测到赞美词汇 → compliment")
        return (3, "compliment")

    # 调情类
    if any(flirt in lowered for flirt in ["亲一下", "想你", "抱抱", "约会", "想见你", "你真迷人"]):
        debug_print("检测到调情词汇 → flirt")
        return (2, "flirt")

    # 极限舔狗（不一定得分）
    if any(extreme in lowered for extreme in ["你最美", "我非你不娶", "为你去死"]):
        debug_print("检测到夸张言语 → too_much")
        return (0, "too_much")

    debug_print("无特殊关键词 → neutral")
    return (1, "neutral")
