import pygame
import os


class Lives:
    def __init__(self, game_surface, screen_width, screen_height, font_size, lives):
        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_size = font_size
        self.lives = lives
        self.font = self.font = pygame.font.Font(os.path.join("fonts", "SevenSegment.ttf"), self.font_size)

    def __eq__(self, value):
        return self.lives == value

    def decrement(self):
        self.lives -= 1 if self.lives > 0 else 0

    def update(self):
        text_surface = self.font.render(
            f"Lives: {self.lives}", True, pygame.Color("#ffffff")
        )
        text_rect = text_surface.get_rect()
        text_rect.topleft = (2, 2)
        self.game_surface.blit(text_surface, text_rect)
