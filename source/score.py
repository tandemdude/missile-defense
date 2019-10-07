import pygame
import os

PADDING = 2
SCORE_LENGTH = 10


class Score:
    """
    Class to contain score counter functionality.
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
        self.font = pygame.font.Font(os.path.join("fonts", "fixedsys.ttf"), font_size)
        self.value = 0

    def reset(self) -> None:
        """
        Resets the score counter to 0.

        :return: None
        """
        self.value = 0

    def increment(self, amt: int) -> None:
        """
        Increments the score counter by a given amount.

        :param amt: Int to increase the score by
        :return: None
        """
        self.value += amt

    def score_to_text(self) -> str:
        """
        Converts the score value to a padded string to be rendered

        :return: Str formatted score
        """
        str_score = str(self.value)
        zero_padding = "0" * (SCORE_LENGTH - len(str_score))
        return "SCORE " + zero_padding + str_score

    def update(self) -> None:
        """
        Renders the score onto the game surface.

        :return: None
        """
        text_surface = self.font.render(
            self.score_to_text(), True, pygame.Color("#ffffff")
        )
        text_rect = text_surface.get_rect()
        text_rect.topright = (self.screen_width - PADDING, PADDING)
        self.game_surface.blit(text_surface, text_rect)
