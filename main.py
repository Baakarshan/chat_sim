# main.py
# coding: utf-8
"""
程序主入口。
遵循 Google Python 风格指南，增加详细中文注释。
"""

from gui.window import Window  # 导入主窗口类

def main() -> None:
    """
    主函数，启动应用程序。
    """
    app = Window()  # 创建窗口实例
    app.mainloop()  # 启动 Tkinter 主循环，进入消息处理

if __name__ == "__main__":
    main()  # 仅当直接运行本文件时才执行主函数
