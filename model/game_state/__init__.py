# model/game_state/__init__.py

from .loader import load_state, save_state, reset_state_file
from .transition import check_scene_transition

class GameState:
    def __init__(self):
        self.current_scene = "intro"
        self.favor = 0              # 好感度
        self.triggered = set()
        self.is_finished = False
        self.emotion = "平静"        # 当前情绪（固定两个字）
        self.status = "放空"         # 当前状态（固定两个字）

    def to_dict(self):
        return {
            "current_scene": self.current_scene,
            "favor": self.favor,
            "triggered": list(self.triggered),
            "is_finished": self.is_finished,
            "emotion": self.emotion,
            "status": self.status
        }

    def save(self):
        """保存当前状态到本地"""
        save_state(self)

    def reset(self):
        """重置状态并清除存档"""
        reset_state_file()
        self.__init__()

    def check_scene_transition(self):
        """判断是否达到跳转条件"""
        check_scene_transition(self)

    @classmethod
    def load(cls):
        """从本地加载游戏状态"""
        return load_state(cls)
