import pygame
import os


class Lives:
    def __init__(
        self,
        game_surface: pygame.Surface,
        screen_width: int,
        screen_height: int,
        font_size: int,
        lives: int,
    ) -> None:
        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lives = lives
        self.font = pygame.font.Font(os.path.join("fonts", "fixedsys.ttf"), font_size)

    def __eq__(self, value: int) -> bool:
        return self.lives == value

    def decrement(self) -> None:
        self.lives -= 1 if self.lives > 0 else 0

    def update(self) -> None:
        white, red = pygame.Color("#ffffff"), pygame.Color("#ff0000")
        colour = red if self.lives <= 1 else white
        lives_text_surface = self.font.render("LIVES", True, white)
        lives_text_rect = lives_text_surface.get_rect()
        lives_text_rect.topleft = (2, 2)
        lives_num_surface = self.font.render(f"      {self.lives}", True, colour)
        lives_num_rect = lives_num_surface.get_rect()
        lives_num_rect.topleft = (2, 2)
        self.game_surface.blit(lives_text_surface, lives_text_rect)
        self.game_surface.blit(lives_num_surface, lives_num_rect)
