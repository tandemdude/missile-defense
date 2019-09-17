import pygame
from enemy import Enemy
import os


class Wave:
    def __init__(
        self,
        number_of_enemies,
        time_limit,
        game_surface,
        screen_width,
        screen_height,
        hit_ground_func,
        wave_num,
        font_size
    ):
        self.number_of_enemies = number_of_enemies
        self.time_limit = None
        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.hit_ground_func = hit_ground_func
        self.enemies = []
        self.finished = False
        self.register_enemies()
        self.num = wave_num + 1
        self.font = pygame.font.Font(os.path.join("fonts", "SevenSegment.ttf"), font_size)

    def register_enemies(self):
        for _ in range(self.number_of_enemies):
            self.enemies.append(
                Enemy(self.game_surface, self.screen_width, self.screen_height)
            )

    def register_enemy(self):
        self.enemies.append(
            Enemy(self.game_surface, self.screen_width, self.screen_height)
        )

    def draw_wave_number(self):
        text_surface = self.font.render(
            f"Wave {self.num}", True, pygame.Color("#ffffff")
        )
        text_rect = text_surface.get_rect()
        text_rect.midtop = self.game_surface.get_rect().midtop
        self.game_surface.blit(text_surface, text_rect)

    def update(self):
        self.draw_wave_number()

        self.finished = True
        for enemy in self.enemies:
            enemy.update()
            if enemy.hit_ground:
                self.hit_ground_func()
            if enemy.visible:
                self.finished = False
