# model/chat_fallback.py
# coding: utf-8
"""
模型兜底与旁白引导模块。
遵循 Google Python 风格指南，增加详细中文注释。
"""

def get_default_reply() -> str:
    """
    当模型长时间不响应时，返回默认文本。
    Returns:
        str: 默认回复文本。
    """
    return "……（她没回应你，好像有点冷淡）"

def build_scene_prompt(scene_name: str) -> str:
    """
    构造旁白生成引导词，用于 AI 输出一句简洁的场景提示语。
    示例输出：
        “午后，图书馆一角，阳光透过玻璃。”
        “黄昏，操场边，她独自坐在长椅。”
    Args:
        scene_name: 场景名称。
    Returns:
        str: 旁白引导词。
    """
    return (
        f"你是游戏旁白系统，请基于当前场景“{scene_name}”生成简洁场景描述，包含时间、地点、天气，"
        "如：“傍晚，教学楼门口，天空飘着细雨。”。请模仿这种口吻，每次只返回一句话。"
    )
