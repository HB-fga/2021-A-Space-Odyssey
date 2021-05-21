import utils
import player
import planet

import random
from math import sqrt
from collections import deque
from easymunk import pyxel as phys, Vec2d
from easymunk import Constraint, Arbiter
import pyxel

class Game:
    def __init__(self):
        self.camera = phys.Camera(flip_y=False)
        self.space = phys.space(
            camera = self.camera,
            elasticity = 1.0,
        )

        self.transition = 0

        # Inicializa objetos
        self.state = utils.GameState.MENU

        self.player = player.Player(utils.WIDTH/2, utils.HEIGHT/2-26)
        self.player.register(self.space)

        self.planets = []

        planet1 = planet.Planet(utils.WIDTH/2-60, utils.HEIGHT/2+40, 18)
        planet1.register(self.space)
        planet2 = planet.Planet(utils.WIDTH/2, utils.HEIGHT/2, 20)
        planet2.register(self.space)
        planet3 = planet.Planet(utils.WIDTH/2+60, utils.HEIGHT/2+40, 16)
        planet3.register(self.space)

        self.planets.append(planet1)
        self.planets.append(planet2)
        self.planets.append(planet3)

        self.particles = utils.Particles(self.space)

        # Cria margem
        L = 48
        self.margin = phys.margin(-L, -L, pyxel.width + 2 * L, pyxel.height + 2 * L)

    # Administra colisões
        self.space.collision_handler(
            utils.ColType.PLAYER, utils.ColType.PLANET, post_solve=self.on_planet
        )

        # self.space.collision_handler(
        #     utils.ColType.PLAYER, utils.ColType.MOON, post_solve=self.on_death
        # )

    def on_planet(self, arb: Arbiter):

        shape_a, shape_b = arb.bodies
        if shape_a.collision_type == utils.ColType.PLAYER:
            player, planet = shape_a, shape_b
        else:
            player, planet = shape_b, shape_a

        if self.player.planet_joint is not None:
            self.player.planet_joint.max_force = 0
            self.space.remove(self.player.planet_joint)
            self.player.planet_joint = None

        self.player.planet_joint = player.junction(planet).pivot()
        self.player.landed_on = planet

        self.player.planet_joint.max_force = float("inf")

        for _ in range(2):
            self.particles.emmit(
                position=self.player.player_body.local_to_world((random.uniform(-2, 2), -3)),
                velocity=(0, 0) #-random.uniform(50, 90) * self.player.player_body.rotation_vector.rotated(90),
            )

    def update(self):
        self.space.step(1 / 30, 2)

        if self.state is not utils.GameState.PAUSED and self.state is not utils.GameState.CREDITS and self.state is not utils.GameState.GAME_OVER:
            self.planets[0].planet_body.position -= (self.transition, 0)       
            self.planets[2].planet_body.position += (self.transition, 0) 

            # print(self.state)    
        
            self.player.update(self.camera)

            # for p in self.planets:
            #     p.update()

            # Camera segue o Player
            self.camera.follow(self.player.player_body.position)            
            
            # atualiza particulas
            self.particles.update()

        # Atualiza lógica caso o jogo esteja rodando
        if self.state == utils.GameState.MENU:
            if self.player.landed_on is not None and pyxel.btnp(pyxel.KEY_SPACE):
                if self.player.landed_on.radius == 18:
                    self.state = utils.GameState.OPTIONS
                elif self.player.landed_on.radius == 20:
                    self.transition = 0
                    self.state = utils.GameState.TRANSITION
                elif self.player.landed_on.radius == 16:
                    self.state = utils.GameState.CREDITS
        elif self.state == utils.GameState.TRANSITION :
            if self.transition < 50:
                self.transition += 2 
            elif self.transition >= 50:
                self.transition = 0
                self.state = utils.GameState.RUNNING
                self.space.remove(self.margin)
                self.margin = phys.margin(-200, -950, utils.WIDTH + (2 * 200), 1200)
                i = 0
                while i < 10 :
                    new_planet = planet.Planet(random.randint(30, utils.WIDTH - 30),  10+(-90*(i)), random.randint(8, 35))
                    # new_planet.register(self.space)
                    self.planets.append(new_planet)

                    # self.planets.append(planet.Planet(random.randint(30, utils.WIDTH - 30),  10+(-90*(i)), random.randint(8, 35)))
                    print(10+(-90*(i)))
                    i += 1
        elif self.state == utils.GameState.RUNNING :
            # print(self.player.player_body.position)
            if self.player.player_body.position.x < -190 or self.player.player_body.position.x > utils.WIDTH + 190 or self.player.player_body.position.y < -940 or self.player.player_body.position.y > 230:
                self.state = utils.GameState.GAME_OVER
        elif self.state == utils.GameState.GAME_OVER :
            if pyxel.btnp(pyxel.KEY_SPACE):
                while len(self.planets) > 3:
                    print(len(self.planets))
                    self.space.remove(self.planets[-1].planet_body)
                    self.planets.pop()

                self.planets[0].planet_body.position = (utils.WIDTH/2-60, utils.HEIGHT/2+40)
                self.planets[2].planet_body.position = (utils.WIDTH/2+60, utils.HEIGHT/2+40)

                self.player.player_body.velocity = (0, 10)
                self.player.player_body.position = (utils.WIDTH/2, utils.HEIGHT/2-26)

                self.state = utils.GameState.MENU
        elif self.state == utils.GameState.CREDITS :
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.state = utils.GameState.MENU
        elif self.state == utils.GameState.OPTIONS :
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.state = utils.GameState.MENU
    
    def draw(self):
        pyxel.cls(0)

        for p in self.planets:
            p.draw(self.camera)

        self.camera.draw(self.player.player_body)
        self.player.draw(self.camera)
        
        self.particles.draw(self.camera)

        # UI
        self.camera.draw(self.margin)

        if(self.state == utils.GameState.MENU or self.state == utils.GameState.TRANSITION):
            utils.centralized_text(self.camera, utils.WIDTH/2, utils.HEIGHT/2-40 - self.transition*2, "Space Escapers!", pyxel.COLOR_WHITE, 0)
            utils.centralized_text(self.camera, utils.WIDTH/2, utils.HEIGHT/2+80 + self.transition*2, "Click and drag to fly   |   Press Space to Confirm", pyxel.COLOR_WHITE, 0)
            utils.centralized_text(self.camera, self.planets[0].planet_body.position.x - self.transition, self.planets[0].planet_body.position.y, "Options", pyxel.COLOR_WHITE, 2)
            utils.centralized_text(self.camera, self.planets[2].planet_body.position.x + self.transition, self.planets[2].planet_body.position.y, "Credits", pyxel.COLOR_WHITE, 2)
            if self.state == utils.GameState.MENU:
                utils.centralized_text(self.camera, *self.planets[1].planet_body.position, "Start", pyxel.COLOR_WHITE, 2)
        elif self.state == utils.GameState.CREDITS:
            pyxel.cls(0)
            pyxel.text(20, utils.HEIGHT/2-10, "Everything done by: Hugo Bezerra :D", pyxel.frame_count % 15+1)
            pyxel.text(20, utils.HEIGHT/2+10, "Press Space to return", pyxel.COLOR_WHITE)
        elif self.state == utils.GameState.GAME_OVER:
            utils.centralized_text(self.camera, *self.player.player_body.position, "Press Space to try again", pyxel.COLOR_WHITE, 2)

pyxel.init(utils.WIDTH, utils.HEIGHT)
pyxel.mouse(True)
game = Game()
pyxel.run(game.update, game.draw)