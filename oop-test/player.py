import utils

from math import sqrt
from collections import deque
from easymunk import pyxel as phys, Vec2d
from easymunk import Constraint, Arbiter
import pyxel

class Player(utils.GameObject):

    def __init__(self, x, y):
        self.slingshot = Vec2d(0, 0)
        self.landed_on = None
        self.planet_joint = None
        self.player_body = phys.tri(0, 6, -3, -3, +3, -3, pyxel.COLOR_LIME)
        self.player_body.position = (x, y)
        self.player_body.elasticity = 1.0
        self.player_body.collision_type = utils.ColType.PLAYER
        
    def update(self, camera):
        self.slingshot = Vec2d(camera.mouse_x - pyxel.width / 2, camera.mouse_y - pyxel.height / 2).rotated(180)

        # Atualiza o ângulo
        if self.landed_on is not None:
            p_angle = Vec2d(*(self.player_body.position - self.landed_on.planet_body.position))
            self.player_body.angle = p_angle.rotated(-90).angle

        # Movimentação
        if pyxel.btnr(pyxel.MOUSE_LEFT_BUTTON):
            self.player_body.velocity = self.slingshot
            self.player_body.angular_velocity = 0
            self.player_body.angle = self.player_body.velocity.rotated(-90).angle

            if self.landed_on is not None:
                self.planet_joint.max_force = 0
                self.planet_joint = None
                self.landed_on = None
            
    def draw(self, camera):
        self.slingshot = Vec2d(camera.mouse_x - pyxel.width / 2, camera.mouse_y - pyxel.height / 2).rotated(180)

        if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
            camera.line(*(self.slingshot + self.player_body.position), *self.player_body.position, pyxel.COLOR_LIME)

        # camera.circ(*self.player_body.position, 10, pyxel.COLOR_WHITE)

    def register(self, space, message):
        space.add(self.player_body)
