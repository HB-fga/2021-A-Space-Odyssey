import utils
import enemies

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

# Gravitational constants
S_mass = 100
G = 1e2
a = 16 # "a" is here to make things smoother 
alpha = 1

class Planet(utils.GameObject):

    def __init__(self, x, y, r, flag):

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
        self.planet_body.angular_velocity = 1500/r

        self.moon = None
        self.ufo = None

        if flag == 1 and self.planet_body.radius < 23:
            if random.random() < 0.75:
                self.moon = phys.circ(self.planet_body.position.x + 2*self.planet_body.radius, self.planet_body.position.y + 2*self.planet_body.radius, random.randint(2, 4), col1+1)
                self.moon.elasticity=1.0
                self.moon.collision_type = utils.ColType.ENEMY
                # self.moon.mass = ...
        
                dist = self.moon.position - self.planet_body.position
                r = dist.length
                self.moon.velocity = dist.normalized().perpendicular() * sqrt(G * S_mass * r / (r + a)**alpha) * 0.5

                self.trajectory = deque([self.moon.position], 16)
            else :
                self.ufo = enemies.Ufo(self.planet_body.position.x + 2*self.planet_body.radius, self.planet_body.position.y + 2*self.planet_body.radius)
                self.ufo.over = self.planet_body

                dist = self.ufo.ufo_body.position - self.planet_body.position
                r = dist.length
                self.ufo.ufo_body.velocity = dist.normalized().perpendicular() * sqrt(G * S_mass * r / (r + a)**alpha) * 0.5
                self.ufo.ufo_body.velocity *= -1

        self.crater_r1 = random.uniform(1, self.planet_body.radius/2-2)
        self.crater_pos1 = random.uniform(2+self.crater_r1, self.planet_body.radius-self.crater_r1-2)

        self.crater_r2 = random.uniform(1, self.planet_body.radius/2-2)
        self.crater_pos2 = random.uniform(2+self.crater_r2, self.planet_body.radius-self.crater_r2-2)

        self.crater_r3 = random.uniform(1, self.planet_body.radius/2-2)
        self.crater_pos3 = random.uniform(2+self.crater_r3, self.planet_body.radius-self.crater_r3-2)



    def update(self, player):
        self.planet_body.angular_velocity = 1500/self.planet_body.radius

        if self.moon is not None:
            dist = self.moon.position - self.planet_body.position
            direction = dist.normalized()
            r = dist.length
            F = G * S_mass * self.moon.mass / (r + a)**alpha

            self.moon.force += -F * direction
            # print("moon mass = ", self.moon.mass)

        if self.ufo is not None:
            x1, y1 = player.position
            x2, y2 = self.ufo.ufo_body.position

            dist = sqrt( (x2 - x1)**2 + (y2 - y1)**2 )

            # print("ufo/player dist", dist)

            if dist < 70:
                self.ufo.hatch_col = 8
                coords = self.ufo.ufo_body.position - player.position
                direction = coords.normalized()

                self.ufo.ufo_body.force += -20000 * direction

                p_angle = Vec2d(*(self.ufo.ufo_body.position - player.position))
                self.ufo.ufo_body.angle = p_angle.rotated(90).angle
            else:
                self.ufo.hatch_col = 10
                dist = self.ufo.ufo_body.position - self.planet_body.position
                direction = dist.normalized()
                r = dist.length
                F = G * S_mass * self.ufo.ufo_body.mass / (r + a)**alpha

                # print("ufo applied force", F)

                self.ufo.ufo_body.force += -F * direction

                p_angle = Vec2d(*(self.ufo.ufo_body.position - self.planet_body.position))
                self.ufo.ufo_body.angle = p_angle.rotated(90).angle
                # print("ufo mass = ", self.ufo.ufo_body.mass)
    
    def draw(self, camera): 

        if self.ufo is not None:
            self.ufo.draw(camera)

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

        if self.moon is not None:
            camera.circ(*self.moon.position, self.moon.radius, self.moon.color)

            if pyxel.frame_count % 3 == 0:
                self.trajectory.append(self.moon.position)
            for (x, y) in self.trajectory:
                camera.pset(x, y, self.moon.color)

        

    def register(self, space):
        space.add(self.planet_body)
