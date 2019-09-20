import pygame
import typing
import math
import os

SPRITE_WIDTH = 15
SPRITE_HEIGHT = 25
MISSILE_VELOCITY = 7


class Missile(pygame.sprite.Sprite):
    def __init__(
        self,
        game_surface: pygame.Surface,
        screen_width: int,
        screen_height: int,
        reticle_x: typing.Union[int, float],
        reticle_y: typing.Union[int, float],
    ) -> None:
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
        self.image = pygame.transform.scale(self.image, (SPRITE_WIDTH, SPRITE_HEIGHT))

        self.image = pygame.transform.rotate(self.image, self.get_angle_positions())

    def get_angle_positions(self) -> float:
        radius, angle = pygame.math.Vector2(
            self.end_x - self.x, self.end_y - self.y
        ).as_polar()
        return -angle - 90

    def vector_from_positions(self) -> tuple:
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

    def update(self) -> None:
        if self.moving:
            self.x += self.velocity_x
            self.y += self.velocity_y

        if self.visible:
            self.game_surface.blit(self.image, (self.x, self.y))
