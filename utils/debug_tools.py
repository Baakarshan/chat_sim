# utils/debug_tools.py
# coding: utf-8
"""
调试工具模块。
遵循 Google Python ��格指南，增加详细中文注释。
"""

from config import DEBUG_MODE  # 导入调试模式开关

def debug_print(*args, **kwargs) -> None:
    """
    仅在开启调试模式时输出调试信息。
    Args:
        *args: 位置参数，传递给 print。
        **kwargs: 关键字参数，传递给 print。
    """
    if DEBUG_MODE:
        print("[DEBUG]", *args, **kwargs)
