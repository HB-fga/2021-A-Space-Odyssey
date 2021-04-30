import utils
import player
import planet

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

        self.state = utils.GameState.RUNNING

        self.player = player.Player(30, 30)
        self.player.register(self.space, self.message)

        self.planet1 = planet.Planet(100, 100)
        self.planet1.register(self.space, self.message)

        self.planet2 = planet.Planet(180, 110)
        self.planet2.register(self.space, self.message)

        L = 48
        phys.margin(-L, -L, pyxel.width + 2 * L, pyxel.width + 2 * L, radius = 5)

    def message(self, msg, sender):
        fn = getattr(self, f'handle_{msg}', None)
        if fn is None:
            print(f'Mensagem desconhecida: "{msg} ({sender})')
        else:
            fn(sender)

    def update(self):
        self.space.step(1 / 30, 2)
        if self.state is not utils.GameState.GAME_OVER:
            self.player.update(self.camera)
            self.planet1.update()
            self.planet2.update()
        self.camera.follow(self.player.player_body.position)


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

pyxel.init(utils.WIDTH, utils.HEIGHT)
pyxel.mouse(True)
game = Game()
pyxel.run(game.update, game.draw)