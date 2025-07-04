# gui/control_panel.py

import tkinter as tk

def build_control_panel(window):
    """
    创建控制面板：状态标签 + 按钮
    返回控件字典 {aff, emo, stat}
    """
    frame = tk.Frame(window, bg="#f0f0f0", pady=4)
    frame.pack(fill=tk.X)

    aff_label = tk.Label(frame, text="好感度: 0", width=12, anchor="w")
    emo_label = tk.Label(frame, text="情绪: neutral", width=14, anchor="w")
    stat_label = tk.Label(frame, text="状态: 放空", width=14, anchor="w")

    restart_btn = tk.Button(frame, text="重新开始", command=window.on_restart)
    quit_btn = tk.Button(frame, text="关闭游戏", command=window.quit)

    aff_label.pack(side=tk.LEFT, padx=5)
    emo_label.pack(side=tk.LEFT, padx=5)
    stat_label.pack(side=tk.LEFT, padx=5)
    restart_btn.pack(side=tk.RIGHT, padx=5)
    quit_btn.pack(side=tk.RIGHT, padx=5)

    return {
        "frame": frame,
        "aff": aff_label,
        "emo": emo_label,
        "stat": stat_label
    }
