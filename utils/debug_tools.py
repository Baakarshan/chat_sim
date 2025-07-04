# utils/debug_tools.py

from config import DEBUG_MODE

def debug_print(*args, **kwargs):
    """仅在开启调试模式时输出调试信息"""
    if DEBUG_MODE:
        print("[DEBUG]", *args, **kwargs)
