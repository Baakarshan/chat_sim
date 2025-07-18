# model/emotion_analyzer.py
# coding: utf-8
"""
情绪分析模块（兼容占位，已废弃）。
遵循 Google Python 风格指南，增加详细中文注释。
"""

from utils.debug_tools import debug_print  # 导入调试打印

def analyze_user_input(text: str) -> tuple[int, str]:
    """
    （已废弃）根据用户输入内容分析情绪（旧版关键词判断）。
    当前逻辑交由大模型决定，本函数仅保留为兼容占位。
    Args:
        text: 用户输入文本。
    Returns:
        tuple[int, str]: (好感增量, 情绪标签)，均为默认值。
    """
    debug_print("（已废弃）本地情绪分析已禁用，由大模型接管")
    return (0, "")
