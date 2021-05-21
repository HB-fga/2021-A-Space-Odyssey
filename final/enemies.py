# import utils

# from math import sqrt
# from collections import deque
# from easymunk import pyxel as phys, Vec2d
# from easymunk import Constraint, Arbiter
# import pyxel

# class Ufo(utils.GameObject):

#     def __init__(self, x, y):
#         self.planet_body = phys.circ(pyxel.width / 2, pyxel.height / 2, 15, pyxel.COLOR_YELLOW)
#         self.planet_body.position=(x, y)
#         self.planet_body.elasticity=1.0
#         self.planet_body.collision_type = utils.ColType.PLANET
#         self.planet_body.mass = 1e10
#         self.planet_body.angular_velocity = 100
        
#     def update(self):
#         # self.planet_body.angular_velocity = 100
#         ...
    
#     def draw(self, camera):
#         r = self.planet_body.rotation_vector * self.planet_body.radius
#         x1, y1 = self.planet_body.position
#         x2, y2 = self.planet_body.position + r

#         camera.line(x1, y1, x2, y2, pyxel.COLOR_PURPLE)

#     def register(self, space, message):
#         space.add(self.planet_body)


# class Mole(utils.GameObject):

#     def __init__(self, x, y):
#         self.planet_body = phys.circ(pyxel.width / 2, pyxel.height / 2, 15, pyxel.COLOR_YELLOW)
#         self.planet_body.position=(x, y)
#         self.planet_body.elasticity=1.0
#         self.planet_body.collision_type = utils.ColType.PLANET
#         self.planet_body.mass = 1e10
#         self.planet_body.angular_velocity = 100
        
#     def update(self):
#         # self.planet_body.angular_velocity = 100
#         ...
    
#     def draw(self, camera):
#         r = self.planet_body.rotation_vector * self.planet_body.radius
#         x1, y1 = self.planet_body.position
#         x2, y2 = self.planet_body.position + r

#         camera.line(x1, y1, x2, y2, pyxel.COLOR_PURPLE)

#     def register(self, space, message):
#         space.add(self.planet_body)
