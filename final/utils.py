import random
from typing import Callable
from abc import ABC, abstractmethod
import enum
import pyxel
from easymunk import Vec2d, Arbiter, CircleBody, Space, ShapeFilter
from easymunk import pyxel as phys

WIDTH, HEIGHT = 256, 196

class Particles:
    def __init__(self, space):
        self.particles = []
        self.space = space

    def draw(self, camera=pyxel):
        for p in self.particles:
            x, y = p.position
            if random.random() < 0.15:
                camera.rect(x, y, 2, 2, self.get_color(p.duration))
            else:
                camera.pset(x, y, self.get_color(p.duration))

    def update(self):
        for p in self.particles.copy():
            p.velocity = p.velocity.rotated(random.uniform(-5, 5)) 
            p.duration -= 1
            if p.duration <= 0:
                self.particles.remove(p)

    def emmit(self, position, velocity):
        p = self.space.create_circle(
            radius=1,
            mass=0.1,
            moment=float("inf"),
            position=position,
            velocity=velocity,
            filter=ShapeFilter(group=1),
            color=pyxel.COLOR_BLACK
        )
        p.duration = 70 - random.expovariate(1 / 10)
        self.particles.append(p)

    def get_color(self, t):
        if t > 40:
            return 7
        elif t > 25:
            return 13
        else:
            return 1

def centralized_text(camera, x, y, text, col, flag):
    n = len(text)
    x_fix = (x - (n * pyxel.FONT_WIDTH) / 2)

    if flag == 0:
        camera.text(x_fix, y, text, col)
    elif flag == 1:
        camera.text(x_fix+1, y+1, text, 0)
        camera.text(x_fix, y, text, col)
    elif flag == 2:
        camera.text(x_fix-1, y-1, text, 0)
        camera.text(x_fix+1, y+1, text, 0)
        camera.text(x_fix-1, y+1, text, 0)
        camera.text(x_fix+1, y-1, text, 0)
        camera.text(x_fix, y-1, text, 0)
        camera.text(x_fix, y+1, text, 0)
        camera.text(x_fix-1, y, text, 0)
        camera.text(x_fix+1, y, text, 0)
        camera.text(x_fix, y, text, col)

class ColType(enum.IntEnum):
    PLAYER = 1
    PLANET = 2
    MOON = 3
    SHIP = 4

class GameState(enum.IntEnum):
    RUNNING = 1
    MENU = 2
    GAME_OVER = 3
    HAS_WON = 4
    OPTIONS = 5
    CREDITS = 6
    TRANSITION = 7
    PAUSED = 8

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