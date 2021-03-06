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

        # Inicializa objetos
        self.state = utils.GameState.RUNNING

        self.player = player.Player(30, 30)
        self.player.register(self.space, self.message)

        self.planet1 = planet.Planet(100, 100)
        self.planet1.register(self.space, self.message)

        self.planet2 = planet.Planet(180, 110)
        self.planet2.register(self.space, self.message)

        self.particles = utils.Particles(self.space)

        # Cria margem
        L = 48
        phys.margin(-L, -L, pyxel.width + 2 * L, pyxel.width + 2 * L, radius = 5)

    # Administra colisões
        self.space.collision_handler(
            utils.ColType.PLAYER, utils.ColType.PLANET, post_solve=self.on_collision
        )

    def on_collision(self, arb: Arbiter):
        d1 = abs(self.player.player_body.position.x - self.planet1.planet_body.position.x) + abs(self.player.player_body.position.y - self.planet1.planet_body.position.y)
        d2 = abs(self.player.player_body.position.x - self.planet2.planet_body.position.x) + abs(self.player.player_body.position.y - self.planet2.planet_body.position.y)

        if self.player.planet_joint is not None:
            self.player.planet_joint.max_force = 0

        if d1 < d2:
            self.player.planet_joint = self.player.player_body.junction(self.planet1.planet_body).pivot()
            self.player.landed_on = self.planet1
            print("hey")
        else:
            self.player.planet_joint = self.player.player_body.junction(self.planet2.planet_body).pivot()
            self.player.landed_on = self.planet2

        self.player.planet_joint.max_force = float("inf")

        for _ in range(2):
            self.particles.emmit(
                position=self.player.player_body.local_to_world((random.uniform(-2, 2), -3)),
                velocity=(0, 0) #-random.uniform(50, 90) * self.player.player_body.rotation_vector.rotated(90),
            )

    def message(self, msg, sender):
        fn = getattr(self, f'handle_{msg}', None)
        if fn is None:
            print(f'Mensagem desconhecida: "{msg} ({sender})')
        else:
            fn(sender)

    def update(self):
        self.space.step(1 / 30, 2)

        # Atualiza lógica caso o jogo esteja rodando
        if self.state is not utils.GameState.GAME_OVER:
            self.player.update(self.camera)
            self.planet1.update()
            self.planet2.update()

        # Camera segue o Player
        self.camera.follow(self.player.player_body.position)            
        
        # atualiza particulas
        self.particles.update()

    
    def draw(self):
        pyxel.cls(0)

        for body in self.space.bodies:
            if isinstance(body, (player.Player, planet.Planet)):
                body.draw(self.camera)
            else:
                self.camera.draw(body)

        self.player.draw(self.camera)
        self.planet1.draw(self.camera)
        self.planet2.draw(self.camera)
        self.particles.draw(self.camera)

pyxel.init(utils.WIDTH, utils.HEIGHT)
pyxel.mouse(True)
game = Game()
pyxel.run(game.update, game.draw)