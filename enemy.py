import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((20, 20))
        self.image.fill(pygame.Color("#ffffff"))

        pygame.draw.rect(self.image, pygame.Color("#ff00ff"), (0, 0, 20, 20))
