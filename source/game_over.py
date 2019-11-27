import pygame

from . import utils


class GameOver:
    """
    Class to contain game_over screen functionality.

    :param game_surface: The :class:`pygame.Surface` to draw the text onto
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
    ) -> None:
        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_size = font_size
        self.font = utils.load_font("source.fonts", "fixedsys.ttf", self.font_size)

    def update(self) -> None:
        """
        Draws the game_over text onto the game surface each time this is called.

        :return: None
        """
        game_over_surface = self.font.render("GAME OVER", True, pygame.Color("#ff0000"))
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.center = self.game_surface.get_rect().center
        self.game_surface.blit(game_over_surface, game_over_rect)
        restart_msg_surface = self.font.render(
            "Press [Y] to return to menu or [N] to quit", True, pygame.Color("#ff0000")
        )
        restart_msg_rect = restart_msg_surface.get_rect()
        restart_msg_rect.center = (
            game_over_rect.center[0],
            game_over_rect.center[1] + self.font_size,
        )
        self.game_surface.blit(restart_msg_surface, restart_msg_rect)
