import pygame
import os


class GameOver:
    def __init__(self, game_surface, screen_width, screen_height, font_size):
        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_size = font_size
        self.font = self.font = pygame.font.Font(
            os.path.join("fonts", "SevenSegment.ttf"), self.font_size
        )

    def update(self):
        game_over_surface = self.font.render("GAME OVER", True, pygame.Color("#ff0000"))
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.center = self.game_surface.get_rect().center
        self.game_surface.blit(game_over_surface, game_over_rect)
        restart_msg_surface = self.font.render(
            "Press [Y] to restart or [N] to quit", True, pygame.Color("#ff0000")
        )
        restart_msg_rect = restart_msg_surface.get_rect()
        restart_msg_rect.center = (
            game_over_rect.center[0],
            game_over_rect.center[1] + self.font_size,
        )
        self.game_surface.blit(restart_msg_surface, restart_msg_rect)
