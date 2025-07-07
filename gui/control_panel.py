# gui/control_panel.py
# coding: utf-8
"""
控制面板构建模块。
遵循 Google Python 风格指南，增加详细中文注释。
"""

import tkinter as tk  # 导入 Tkinter 库

def build_control_panel(window):
    """
    创建控制面板：状态标签 + 按钮。
    Args:
        window: 主窗口对象，需实现 on_restart 和 quit 方法。
    Returns:
        dict: 控件字典 {frame, aff, emo, stat}。
    """
    frame = tk.Frame(window, bg="#f0f0f0", pady=4)  # 外部面板
    frame.pack(fill=tk.X)

    aff_label = tk.Label(frame, text="好感度: 0", width=12, anchor="w")  # 好感度标签
    emo_label = tk.Label(frame, text="情绪: 平静", width=14, anchor="w")  # 情绪标签
    stat_label = tk.Label(frame, text="状态: 放空", width=14, anchor="w")  # 状态标签

    restart_btn = tk.Button(frame, text="重新开始", command=window.on_restart)  # 重新开始按钮
    quit_btn = tk.Button(frame, text="关闭游戏", command=window.quit)  # 关闭游戏按钮

    aff_label.pack(side=tk.LEFT, padx=5)
    emo_label.pack(side=tk.LEFT, padx=5)
    stat_label.pack(side=tk.LEFT, padx=5)
    restart_btn.pack(side=tk.RIGHT, padx=5)
    quit_btn.pack(side=tk.RIGHT, padx=5)

    return {
        "frame": frame,  # 面板框架
        "aff": aff_label,  # 好感度标签
        "emo": emo_label,  # 情绪标签
        "stat": stat_label  # 状态标签
    }
