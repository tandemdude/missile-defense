import pygame
import os
import typing

# Constants
RETICLE_SPEED = 6.5


def clamp(n: typing.Union[int, float], maxn: int, minn: int = 0) -> int:
    return max(min(maxn, n), minn)


class Reticle:
    def __init__(
        self, game_surface: pygame.Surface, screen_width: int, screen_height: int
    ) -> None:
        self.asset = pygame.image.load(
            os.path.join("images", "reticle.png")
        ).convert_alpha()
        self.asset_width, self.asset_height = (
            self.asset.get_width(),
            self.asset.get_height(),
        )
        self.game_surface = game_surface
        self.screen_width, self.screen_height = screen_width, screen_height
        self.x, self.y = game_surface.get_rect().center

        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

        self.speed = RETICLE_SPEED

        self.image = pygame.Surface(
            (self.asset_width, self.asset_height), pygame.SRCALPHA
        )
        self.image.blit(self.asset, (0, 0))
        self.image = pygame.transform.scale(self.image, (50, 50))

    def current_position(self) -> tuple:
        return (self.x, self.y)

    def up(self, enable: bool = True) -> None:
        self.moving_up = enable

    def down(self, enable: bool = True) -> None:
        self.moving_down = enable

    def left(self, enable: bool = True) -> None:
        self.moving_left = enable

    def right(self, enable: bool = True) -> None:
        self.moving_right = enable

    def update(self) -> None:
        if self.moving_up:
            self.y -= self.speed
        if self.moving_down:
            self.y += self.speed
        if self.moving_left:
            self.x -= self.speed
        if self.moving_right:
            self.x += self.speed

        self.x = clamp(self.x, self.screen_width)
        self.y = clamp(self.y, self.screen_height - self.speed)

        self.game_surface.blit(
            self.image,
            (
                self.x - self.image.get_width() // 2,
                self.y - self.image.get_height() // 2,
            ),
        )
