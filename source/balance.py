import pygame

from . import utils

PADDING = 2
BALANCE_LENGTH = 8


class Balance:
    """
    Class to contain balance counter functionality.

    :param game_surface: The :class:`pygame.Surface` to draw the balance onto
    :param screen_width: :class:`int` width of the window in pixels
    :param screen_height: :class:`int` height of the window in pixels
    :param font_size: :class:`int` height of the font in pixels
    """

    def __init__(
        self,
        game_surface: pygame.Surface,
        screen_width: int,
        screen_height: int,
        font_size: int,
    ):

        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_size = font_size
        self.font = utils.load_font("source.fonts", "fixedsys.ttf", self.font_size)
        self.value = 0

    def increment(self, amount: int) -> None:
        """
        Increments the balance counter by a given amount.

        :param amount: :class:`int` to increase the balance by
        :return: `None`
        """
        self.value += amount

    def decrement(self, amount: int) -> None:
        """
        Decrements the balance counter by a given amount.

        :param amount: :class:`int` to decrease the balance by
        :return: `None`
        """
        self.value -= amount

    def balance_to_text(self) -> str:
        """
        Converts the balance value to a padded string to be rendered

        :return: :class:`str` formatted balance
        """
        str_balance = str(self.value)
        zero_padding = "0" * (BALANCE_LENGTH - len(str_balance))
        return "CREDITS " + zero_padding + str_balance

    def update(self) -> None:
        """
        Renders the balance onto the game surface.

        :return: `None`
        """
        text_surface = self.font.render(
            self.balance_to_text(), True, pygame.Color("#ffffff")
        )
        text_rect = text_surface.get_rect()
        text_rect.topright = (self.screen_width - PADDING, PADDING + self.font_size)
        self.game_surface.blit(text_surface, text_rect)
