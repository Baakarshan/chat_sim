# model/game_state/__init__.py
# coding: utf-8
"""
游戏状态主类与接口。
遵循 Google Python 风格指南，增加详细中文注释。
"""

from .loader import load_state, save_state, reset_state_file  # 导入状态加载与保存
from .transition import check_scene_transition  # 导入场景跳转逻辑

class GameState:
    """
    游戏状态类，管理当前场景、好感度、情绪等。
    """
    def __init__(self):
        self.current_scene = "intro"  # 当前场景
        self.favor = 0                # 好感度
        self.triggered = set()        # 已触发场景集合
        self.is_finished = False      # 是否已结束
        self.emotion = "平静"          # 当前情绪（固定两个字）
        self.status = "放空"           # 当前状态（固定两个字）

    def to_dict(self) -> dict:
        """
        转换为字典，便于序列化。
        Returns:
            dict: 状态字典。
        """
        return {
            "current_scene": self.current_scene,
            "favor": self.favor,
            "triggered": list(self.triggered),
            "is_finished": self.is_finished,
            "emotion": self.emotion,
            "status": self.status
        }

    def save(self) -> None:
        """
        保存当���状态到本地。
        """
        save_state(self)

    def reset(self) -> None:
        """
        重置状态并清除存档。
        """
        reset_state_file()
        self.__init__()

    def check_scene_transition(self) -> None:
        """
        判断是否达到跳转条件。
        """
        check_scene_transition(self)

    @classmethod
    def load(cls):
        """
        从本地加载游戏状态。
        Returns:
            GameState: 加载后的状态对象。
        """
        return load_state(cls)
