from math import sqrt
from collections import deque
from easymunk import pyxel as phys, Vec2d
from easymunk import Constraint, Arbiter
import pyxel

pyxel.init(256, 196)
pyxel.mouse(True)

# create space
camera = phys.Camera(flip_y = False)
space = phys.space(elasticity = 1.0, camera = camera)

# define constants
PLAYER_COL_TYPE = 1
PLANET_COL_TYPE = 2

S_mass = 100
G = 1e2
a = 16 # "a" is here to make things smoother 
alpha = 1

flag = 0 # constraint handler flag

def on_collision(arb: Arbiter):
    global flag
    flag = 1

# create objects

player = phys.tri(0, 6, -3, -3, +3, -3, pyxel.COLOR_LIME)
player.collision_type = PLAYER_COL_TYPE

sun = phys.circ(pyxel.width / 2, pyxel.height / 2, 15, pyxel.COLOR_YELLOW)
sun.mass = 1e10
sun.angular_velocity = 100
sun.collision_type = PLANET_COL_TYPE
planet = phys.circ(64, 64, 3, pyxel.COLOR_DARKBLUE)

ectanus = phys.circ(pyxel.width / 2 + 100, pyxel.height / 2 + 100, 20, pyxel.COLOR_YELLOW)
ectanus.mass = 1e10
ectanus.angular_velocity = 100
ectanus.collision_type = PLANET_COL_TYPE

# setting landable planets constraints
player.position = (pyxel.width / 2 + 20, pyxel.height / 2)
p1 = player.junction(sun).pivot()
p1.max_force = 0

player.position = (pyxel.width / 2 + 125, pyxel.height / 2 + 100)
p2 = player.junction(ectanus).pivot()
p2.max_force = 0

player.position = (30, 30)

# adjusting orbiting planet starting velocity
dist = planet.position - sun.position
r = dist.length
planet.velocity = dist.normalized().perpendicular() * sqrt(G * S_mass * r / (r + a)**alpha) * 0.5

space.collision_handler(
    PLAYER_COL_TYPE, PLANET_COL_TYPE, post_solve=on_collision
)

# border with little bit of offset
L = 48
phys.margin(-L, -L, pyxel.width + 2 * L, pyxel.width + 2 * L, radius = 5)

# apply forces
@space.before_step(sub_steps=True)
def apply_forces():
    dist = planet.position - sun.position
    direction = dist.normalized()
    r = dist.length
    F = G * S_mass * planet.mass / (r + a)**alpha

    planet.force += -F * direction


pos_list = deque([planet.position], 128)
@space.after_step()
def paint_trajectory():

    counter = 0
    
    global flag
    camera.follow(player.position)

    # draws trajectory on screen
    if pyxel.frame_count % 2 == 0:
        pos_list.append(planet.position)

    for (x, y) in pos_list:
        # coi
        camera.pset(x, y, counter % 15)

        counter = counter + 1

    # calculate player slingshot vector
    slingshot = Vec2d(camera.mouse_x - pyxel.width / 2, camera.mouse_y - pyxel.height / 2).rotated(180)

    # manage planet landing
    if flag == 1:

        # find out which planet the player is landing
        d1 = abs(player.position.x - sun.position.x) + abs(player.position.y - sun.position.y)
        d2 = abs(player.position.x - ectanus.position.x) + abs(player.position.y - ectanus.position.y)
        
        df = d1 - d2

        if df < 0:
            p1.max_force = float("inf")
            p_angle = Vec2d(*(player.position - sun.position))

        else:
            p2.max_force = float("inf")
            p_angle = Vec2d(*(player.position - ectanus.position))

        player.angle = p_angle.rotated(-90).angle
    else:
        p1.max_force = 0
        p2.max_force = 0

    if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
        camera.line(*(slingshot + player.position), *player.position, pyxel.COLOR_LIME)
    elif pyxel.btnr(pyxel.MOUSE_LEFT_BUTTON):
        flag = 0
        p1.max_force = 0
        p2.max_force = 0
        player.velocity = slingshot
        player.angular_velocity = 0
        player.angle = player.velocity.rotated(-90).angle

    r = sun.rotation_vector * sun.radius
    x1, y1 = sun.position
    x2, y2 = sun.position + r

    camera.line(x1, y1, x2, y2, pyxel.COLOR_PURPLE)

    r = ectanus.rotation_vector * ectanus.radius
    x1, y1 = ectanus.position
    x2, y2 = ectanus.position + r

    camera.line(x1, y1, x2, y2, pyxel.COLOR_PURPLE)

space.run() 