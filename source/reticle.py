import pygame
import typing

from . import utils

# Constants
RETICLE_SPEED = 6.5


def clamp(
    n: typing.Union[int, float],
    maxn: typing.Union[int, float],
    minn: typing.Union[int, float] = 0,
) -> typing.Union[int, float]:
    """
    Ensures that a given number, n, is between a set of upper and lower
    bounds.

    :param n: Union[:class:`int`, :class:`float`] number to clamp
    :param maxn: Union[:class:`int`, :class:`float`] upper bound
    :param minn: Union[:class:`int`, :class:`float`] lower bound
    :return: Union[:class:`int`, :class:`float`] clamped number
    """
    return max(min(maxn, n), minn)


class Reticle:
    """
    Class to represent the player's targeting reticle.

    :param game_surface: The :class:`pygame.Surface` to draw the reticle onto
    :param screen_width: :class:`int` width of the window in pixels
    :param screen_height: :class:`int` height of the window in pixels
    """

    def __init__(
        self, game_surface: pygame.Surface, screen_width: int, screen_height: int
    ) -> None:
        self.asset = utils.load_image("source.images", "reticle.png").convert_alpha()
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

    def current_position(self) -> typing.Tuple[int, int]:
        """
        Get the reticle's current x, y position on the game surface.

        :return: :class:`tuple`[:class:`int`] containing the x, y coordinates of the reticle.
        """
        return self.x, self.y

    def up(self, enable: bool = True) -> None:
        """
        Alter the moving_up flag to indicate whether the reticle is moving upwards.

        :param enable: Optional[:class:`bool`] representing whether or not the reticle should be moving up.
        :return: `None`
        """
        self.moving_up = enable

    def down(self, enable: bool = True) -> None:
        """
        Alter the moving_down flag to indicate whether the reticle is moving downwards.

        :param enable: Optional[:class:`bool`] representing whether or not the reticle should be moving down.
        :return: `None`
        """
        self.moving_down = enable

    def left(self, enable: bool = True) -> None:
        """
        Alter the moving_left flag to indicate whether the reticle is moving to the left.

        :param enable: Optional[:class:`bool`] representing whether or not the reticle should be moving left.
        :return: `None`
        """
        self.moving_left = enable

    def right(self, enable: bool = True) -> None:
        """
        Alter the moving_right flag to indicate whether the reticle is moving to the right.

        :param enable: Optional[:class:`bool`] representing whether or not the reticle should be moving right.
        :return: `None`
        """
        self.moving_right = enable

    def update(self) -> None:
        """
        Move the reticle in directions indicated by the flags and draw it onto the game surface.

        :return: `None`
        """
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
