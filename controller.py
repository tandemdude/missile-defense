import pygame
from enemy import Enemy
from reticle import Reticle
from missile import Missile


class ControlScheme:

    def __init__(self):
        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT
        self.fire = pygame.K_SPACE

        """
        self.events = {pygame.KEYDOWN: {self.up: ,
                                        self.down: ,
                                        self.left: ,
                                        self.right: ,
                                        self.fire: 
                                       }
                       pygame.KEYUP: {self.up: ,
                                      self.down: ,
                                      self.left: ,
                                      self.right: 
                                     }
                       }
        """


class Controller:
    
    def __init__(self, game_surface, screen_width, screen_height):
        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.control_scheme = ControlScheme()
        self.reticle = Reticle(self.game_surface, self.screen_width, self.screen_height)
        self.enemies = [Enemy(self.game_surface, self.screen_width, self.screen_height) for _ in range(6)]

        self.to_be_updated = self.enemies + [self.reticle]

    def trigger_fire_missile(self, aim_point):
        # Do something here to fire a missile
        print(f"Pew: fired towards {aim_point}")

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.control_scheme.left:
                self.reticle.left()
            elif event.key == self.control_scheme.right:
                self.reticle.right()
            elif event.key == self.control_scheme.up:
                self.reticle.up()
            elif event.key == self.control_scheme.down:
                self.reticle.down()
            elif event.key == self.control_scheme.fire:
                self.trigger_fire_missile(self.reticle.current_position())

        elif event.type == pygame.KEYUP:
            if event.key == self.control_scheme.left:
                self.reticle.left(False)
            elif event.key == self.control_scheme.right:
                self.reticle.right(False)
            elif event.key == self.control_scheme.up:
                self.reticle.up(False)
            elif event.key == self.control_scheme.down:
                self.reticle.down(False)

    def update_all(self):
        for instance in self.to_be_updated:
            instance.update()

