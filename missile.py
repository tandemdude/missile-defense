import pygame
import typing
import math
import os

import utils

SPRITE_WIDTH = 15
SPRITE_HEIGHT = 25
MISSILE_VELOCITY = 7
ANGLE_OFFSET = 90


class Missile(pygame.sprite.Sprite):
    asset = None

    def __init__(
        self,
        game_surface: pygame.Surface,
        screen_width: int,
        screen_height: int,
        reticle_x: typing.Union[int, float],
        reticle_y: typing.Union[int, float],
    ) -> None:
        super().__init__()

        if Missile.asset is None:
            Missile.asset = pygame.image.load(
                os.path.join("images", "missile.png")
            ).convert_alpha()
        self.asset = Missile.asset

        self.game_surface = game_surface
        self.visible = True
        self.moving = True
        self.x, self.y = screen_width // 2, screen_height
        self.end_x, self.end_y = reticle_x, reticle_y
        self.velocity_x, self.velocity_y = utils.vector_from_positions(
            self.x, self.y, self.end_x, self.end_y, MISSILE_VELOCITY
        )

        self.image = pygame.Surface(
            (self.asset.get_width(), self.asset.get_height()), pygame.SRCALPHA
        )
        self.image.blit(self.asset, (0, 0))
        self.image = pygame.transform.scale(self.image, (SPRITE_WIDTH, SPRITE_HEIGHT))

        self.image = pygame.transform.rotate(
            self.image,
            utils.get_angle_positions(
                self.x, self.y, self.end_x, self.end_y, ANGLE_OFFSET
            ),
        )

    def update(self) -> None:
        if self.moving:
            self.x += self.velocity_x
            self.y += self.velocity_y

        if self.visible:
            self.game_surface.blit(self.image, (self.x, self.y))
