import pygame
import os
from missile import Missile


class Reticle:
    
    def __init__(self, game_surface, screen_width, screen_height):

        self.asset = pygame.image.load(os.path.join("images", "reticle.png")).convert_alpha()
        self.asset_width, self.asset_height = self.asset.get_width(), self.asset.get_height()
        self.game_surface = game_surface
        self.screen_width, self.screen_height = screen_width, screen_height
        self.x, self.y = game_surface.get_rect().center

        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.update_missile = False

        self.image = pygame.Surface((self.asset_width, self.asset_height), pygame.SRCALPHA)
        self.image.blit(self.asset, (0, 0))
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.missile = None

    def update(self):
        if self.move_up:
            self.y -= 5
        if self.move_down:
            self.y += 5
        if self.move_left:
            self.x -= 5
        if self.move_right:
            self.x += 5

        self.game_surface.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2))

        if self.update_missile:
            self.missile.update()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_left = True
            elif event.key == pygame.K_RIGHT:
                self.move_right = True
            elif event.key == pygame.K_UP:
                self.move_up = True
            elif event.key == pygame.K_DOWN:
                self.move_down = True
            elif event.key == pygame.K_SPACE:
                self.missile = Missile(self.game_surface, self.screen_width, self.screen_height, self.x, self.y)
                self.update_missile = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.move_left = False
            elif event.key == pygame.K_RIGHT:
                self.move_right = False
            elif event.key == pygame.K_UP:
                self.move_up = False
            elif event.key == pygame.K_DOWN:
                self.move_down = False
