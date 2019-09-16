import pygame
import math
import os

SPRITE_WIDTH = 10
SPRITE_HEIGHT = 10
MISSILE_VELOCITY = 7


class Missile(pygame.sprite.Sprite):
    def __init__(self, game_surface, screen_width, screen_height, reticle_x, reticle_y):
        super().__init__()

        self.asset = pygame.image.load(
            os.path.join("images", "missile.png")
        ).convert_alpha()
        self.asset_width, self.asset_height = (
            self.asset.get_width(),
            self.asset.get_height(),
        )

        self.game_surface = game_surface
        self.visible = True
        self.moving = True
        self.x, self.y = screen_width // 2, screen_height
        self.end_x, self.end_y = reticle_x, reticle_y
        self.velocity_x, self.velocity_y = self.vector_from_positions()

        self.image = pygame.Surface(
            (self.asset_width, self.asset_height), pygame.SRCALPHA
        )
        self.image.blit(self.asset, (0, 0))
        self.image = pygame.transform.scale(self.image, (25, 75))

        angle = self.get_angle_positions()
        print('angle:', angle * 180/math.pi)
        self.image = pygame.transform.rotate(self.image, angle * 180/math.pi)

        #self.image = pygame.Surface((SPRITE_WIDTH, SPRITE_HEIGHT))
        #self.image.fill(pygame.Color("#000000"))

        #pygame.draw.rect(
        #    self.image, pygame.Color("#ff0000"), (0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        #)

    def get_angle_positions(self):
        y_diff = (self.end_y - self.y)
        x_diff = (self.end_x - self.x)
        if x_diff == 0:
            angle = 0
        else:
            angle = math.pi/2 - math.atan(y_diff / x_diff)
        return angle

    def vector_from_positions(self):
        velocity_x = (
            MISSILE_VELOCITY
            * (self.end_x - self.x)
            / math.sqrt(((self.end_y - self.y) ** 2) + ((self.end_x - self.x) ** 2))
        )
        velocity_y = (
            MISSILE_VELOCITY
            * (self.end_y - self.y)
            / math.sqrt(((self.end_y - self.y) ** 2) + ((self.end_x - self.x) ** 2))
        )
        return (velocity_x, velocity_y)

    def explode(self):
        raise NotImplementedError

    def update(self):
        if self.moving:
            self.x += self.velocity_x
            self.y += self.velocity_y

        if self.visible:
            self.game_surface.blit(self.image, (self.x, self.y))
