import pygame
import math

SPRITE_WIDTH = 10
SPRITE_HEIGHT = 10
MISSILE_VELOCITY = 5


class Missile(pygame.sprite.Sprite):
    
    def __init__(self, game_surface, screen_width, screen_height, reticle_x, reticle_y):
        super().__init__()

        self.game_surface = game_surface
        self.visible = True
        self.moving = True
        self.x, self.y = screen_width // 2, screen_height
        self.end_x, self.end_y = reticle_x, reticle_y
        self.velocity_x, self.velocity_y = self.vector_from_positions()

        self.image = pygame.Surface((SPRITE_WIDTH, SPRITE_HEIGHT))
        self.image.fill(pygame.Color("#000000"))

        pygame.draw.rect(self.image, pygame.Color("#ff0000"), (0, 0, SPRITE_WIDTH, SPRITE_HEIGHT))

    def vector_from_positions(self):
        velocity_x = MISSILE_VELOCITY * (self.end_x - self.x) / math.sqrt(((self.end_y - self.y)**2) + ((self.end_x - self.x)**2))
        velocity_y = MISSILE_VELOCITY * (self.end_y - self.y) / math.sqrt(((self.end_y - self.y)**2) + ((self.end_x - self.x)**2))
        return (velocity_x, velocity_y)

    def explode(self):
        raise NotImplementedError

    def update(self):
        if self.moving:
            self.x += self.velocity_x
            self.y += self.velocity_y
            
        if self.visible:
            self.game_surface.blit(self.image, (self.x, self.y))
