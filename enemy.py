import pygame
import random

SPRITE_WIDTH = 20
SPRITE_HEIGHT = 20


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game_surface, screen_width, screen_height):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_surface = game_surface
        self.x, self.y = self.random_start_position()
        self.image = pygame.Surface((SPRITE_WIDTH, SPRITE_HEIGHT))
        self.image.fill(pygame.Color("#ffffff"))

        pygame.draw.rect(self.image, pygame.Color("#ff00ff"), (0, 0, SPRITE_WIDTH, SPRITE_HEIGHT))

    def random_start_position(self):
        return (random.randint(0, self.screen_width - SPRITE_WIDTH), 0)

    def update(self):
        self.game_surface.blit(self.image, (self.x, self.y))
