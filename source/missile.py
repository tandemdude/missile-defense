import pygame
import typing

from . import utils

SPRITE_WIDTH = 15
SPRITE_HEIGHT = 25
ANGLE_OFFSET = 90


class Missile(pygame.sprite.Sprite):
    """
    Class to represent a fired missile :class:`pygame.sprite.Sprite`.

    :param game_surface: The :class:`pygame.Surface` to blit the missile onto
    :param screen_width: :class:`int` width of the window in pixels
    :param screen_height: :class:`int` height of the window in pixels
    :param start_x: :math:`x` position to fire from
    :param start_y: :math:`y` position to fire from
    :param end_x: :math:`x` position to fire towards
    :param end_y: :math:`y` position to fire towards
    :param fire_velocity: Magnitude of the missile's launch velocity
    """

    asset = None

    def __init__(
        self,
        game_surface: pygame.Surface,
        screen_width: int,
        screen_height: int,
        start_x: typing.Union[int, float],
        start_y: typing.Union[int, float],
        end_x: typing.Union[int, float],
        end_y: typing.Union[int, float],
        fire_velocity: typing.Union[int, float],
    ) -> None:
        super().__init__()

        if Missile.asset is None:
            Missile.asset = utils.load_image(
                "source.images", "missile.png"
            ).convert_alpha()
        self.asset = Missile.asset

        self.game_surface = game_surface
        self.visible = True
        self.moving = True
        self.screen_width, self.screen_height = screen_width, screen_height
        self.x, self.y = start_x, start_y
        self.end_x, self.end_y = end_x, end_y
        self.velocity_x, self.velocity_y = utils.vector_from_positions(
            self.x, self.y, self.end_x, self.end_y, fire_velocity
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
        """
        Moves the :class:`pygame.sprite.Sprite` on the game surface if required and draws it if the missile
        is currently visible.

        :return: None
        """
        if self.moving:
            self.x += self.velocity_x
            self.y += self.velocity_y

        if (
            0 > self.x
            or self.x > self.screen_width
            or self.y < 0
            or self.y > self.screen_height
        ):
            self.visible = False

        if self.visible:
            self.game_surface.blit(self.image, (self.x, self.y))
