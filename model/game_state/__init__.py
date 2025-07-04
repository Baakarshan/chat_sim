# model/game_state/__init__.py

from .loader import load_state, save_state, reset_state_file
from .emotion_logic import update_emotion
from .transition import check_scene_transition
import random

class GameState:
    def __init__(self):
        self.current_scene = "intro"
        self.affection = 0
        self.triggered = set()
        self.is_finished = False
        self.emotion = "neutral"
        self.status = "放空"
        self.tone_history = []

    def to_dict(self):
        return {
            "current_scene": self.current_scene,
            "affection": self.affection,
            "triggered": list(self.triggered),  # set 不可 JSON 序列化
            "is_finished": self.is_finished,
            "emotion": self.emotion,
            "status": self.status,
            "tone_history": self.tone_history
        }

    def save(self):
        save_state(self)

    def reset(self):
        reset_state_file()
        self.__init__()

    @classmethod
    def load(cls):
        return load_state(cls)

    def increase_affection(self, base_delta):
        """好感度提升速度根据阶段递减"""
        if self.affection < 30:
            delta = base_delta
        elif self.affection < 70:
            delta = int(base_delta * 0.5)
        else:
            delta = int(base_delta * 0.2)
        self.affection = min(100, self.affection + delta)

    def add_tone_tag(self, tag):
        """情绪记忆，用于上下文判断"""
        self.tone_history.append(tag)
        if len(self.tone_history) > 5:
            self.tone_history.pop(0)
        update_emotion(self)

    def check_scene_transition(self):
        check_scene_transition(self)
