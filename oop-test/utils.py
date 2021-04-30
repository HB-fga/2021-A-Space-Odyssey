import random
from typing import Callable
from abc import ABC, abstractmethod
import enum
import pyxel
from easymunk import Vec2d, Arbiter, CircleBody, Space
from easymunk import pyxel as phys

WIDTH, HEIGHT = 256, 196

class ColType(enum.IntEnum):
    PLAYER = 1
    PLANET = 2

class GameState(enum.IntEnum):
    RUNNING = 1
    MENU = 2
    GAME_OVER = 3
    HAS_WON = 4

class GameObject(ABC):
    @abstractmethod
    def update(self):
        ...
    
    @abstractmethod
    def draw(self):
        ...

    @abstractmethod
    def register(self, space: Space, message: Callable[[str, "GameObject"], None]):
        ...