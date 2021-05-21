import utils

from math import sqrt
from collections import deque
from easymunk import pyxel as phys, Vec2d
from easymunk import Constraint, Arbiter
import pyxel
import random

# Matching colors
# 6 12
# 12 5
# 10 9
# 11 3

class Planet(utils.GameObject):

    def __init__(self, x, y, r):

        choose_color = random.randint(0, 3)

        if choose_color == 0:
            col1 = 6
            col2 = 12
        elif choose_color == 1:
            col1 = 12
            col2 = 5
        elif choose_color == 2:
            col1 = 10
            col2 = 9
        elif choose_color == 3:
            col1 = 11
            col2 = 3

        self.planet_body = phys.circ(pyxel.width / 2, pyxel.height / 2, r, col1)
        self.crater_col = col2

        self.planet_body.position=(x, y)
        self.planet_body.elasticity=1.0
        self.planet_body.collision_type = utils.ColType.PLANET
        self.planet_body.mass = 1e10
        self.planet_body.angular_velocity = 1000/r

        self.crater_r1 = random.uniform(1, self.planet_body.radius/2-2)
        self.crater_pos1 = random.uniform(2+self.crater_r1, self.planet_body.radius-self.crater_r1-2)

        self.crater_r2 = random.uniform(1, self.planet_body.radius/2-2)
        self.crater_pos2 = random.uniform(2+self.crater_r2, self.planet_body.radius-self.crater_r2-2)

        self.crater_r3 = random.uniform(1, self.planet_body.radius/2-2)
        self.crater_pos3 = random.uniform(2+self.crater_r3, self.planet_body.radius-self.crater_r3-2)



    def update(self):
        # self.planet_body.angular_velocity = 100
        ...
    
    def draw(self, camera): 

        camera.circ(*self.planet_body.position, self.planet_body.radius+3, self.crater_col)      
        camera.circ(*self.planet_body.position, self.planet_body.radius, self.planet_body.color)      

        crater_vec = self.planet_body.rotation_vector * self.crater_pos1
        crater_x, crater_y = self.planet_body.position + crater_vec
        camera.circb(crater_x, crater_y, self.crater_r1, self.crater_col)
        camera.circ(crater_x, crater_y, self.crater_r1-2, self.crater_col)

        crater_vec = self.planet_body.rotation_vector.rotated(120) * self.crater_pos2
        crater_x, crater_y = self.planet_body.position + crater_vec
        camera.circb(crater_x, crater_y, self.crater_r2, self.crater_col)
        camera.circ(crater_x, crater_y, self.crater_r2-2, self.crater_col)

        crater_vec = self.planet_body.rotation_vector.rotated(240) * self.crater_pos3
        crater_x, crater_y = self.planet_body.position + crater_vec
        camera.circb(crater_x, crater_y, self.crater_r3, self.crater_col)
        camera.circ(crater_x, crater_y, self.crater_r3-2, self.crater_col)

    def register(self, space):
        space.add(self.planet_body)
