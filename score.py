import pygame
import os

PADDING = 2
SCORE_LENGTH = 10


class Score:
    def __init__(self, game_surface, screen_width, screen_height, font_size):
        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(os.path.join("fonts", "SevenSegment.ttf"), font_size)
        self.value = 0

    def reset(self):
        self.value = 0

    def increment(self, amt: int):
        self.value += amt

    def score_to_text(self):
        str_score = str(self.value)
        zero_padding = "0" * (SCORE_LENGTH - len(str_score))
        return "score " + zero_padding + str_score

    def update(self):
        text_surface = self.font.render(
            self.score_to_text(), True, pygame.Color("#ffffff")
        )
        text_rect = text_surface.get_rect()
        text_rect.topright = (self.screen_width - PADDING, PADDING)
        self.game_surface.blit(text_surface, text_rect)
