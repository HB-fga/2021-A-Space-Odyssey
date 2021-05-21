from easymunk.pyxel.draw_options import Color
import utils

from math import sqrt
from collections import deque
from easymunk import pyxel as phys, Vec2d
from easymunk import Constraint, Arbiter
import pyxel

class Ufo(utils.GameObject):

    def __init__(self, x, y):
        self.ufo_body = phys.poly([(0, 0), (0, 3), (-7, 0), (-4, 4), (4, 4), (7, 0)], color=pyxel.COLOR_GRAY)
        # self.beam = 
        self.ufo_body.position=(x, y)
        self.ufo_body.elasticity=1.0
        self.ufo_body.collision_type = utils.ColType.ENEMY
        self.hatch_col = 10
        self.over = None
        # self.planet_body.mass = ...
        
    def update(self, player):
        ...


        
    
    def draw(self, camera):
        r = self.ufo_body.rotation_vector.rotated(-90) * 3
        x2, y2 = self.ufo_body.position + r

        camera.draw(self.ufo_body)
        camera.circ(x2, y2, 2, self.hatch_col)
        # camera.line(*self.ufo_body.position, *self.over.position, 8)

    def register(self, space):
        space.add(self.ufo_body)
