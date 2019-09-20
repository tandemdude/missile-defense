import pygame
import random
import os
import typing
from enemy import Enemy


class Wave:
    def __init__(
        self,
        number_of_enemies: int,
        time_limit: typing.Union[int, float],
        game_surface: pygame.Surface,
        screen_width: int,
        screen_height: int,
        hit_ground_func: typing.Callable,
        wave_num: int,
        font_size: int,
    ) -> None:
        self.number_of_enemies = number_of_enemies
        self.time_limit_in_frames = time_limit
        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.hit_ground_func = hit_ground_func
        self.enemies = []
        self.finished = False
        self.frames_since_start = 0
        self.num = wave_num + 1
        self.font = pygame.font.Font(
            os.path.join("fonts", "SevenSegment.ttf"), font_size
        )
        self.enemy_spawn_times = [
            round(random.random() * self.time_limit_in_frames)
            for i in range(number_of_enemies)
        ]

    def register_enemies(self) -> None:
        for _ in range(self.number_of_enemies):
            self.enemies.append(
                Enemy(self.game_surface, self.screen_width, self.screen_height)
            )

    def register_enemy(self) -> None:
        self.enemies.append(
            Enemy(self.game_surface, self.screen_width, self.screen_height)
        )

    def register_new_enemy_if_required(self) -> None:
        if self.frames_since_start in self.enemy_spawn_times:
            for i in range(self.enemy_spawn_times.count(self.frames_since_start)):
                self.register_enemy()

    def draw_wave_number(self) -> None:
        text_surface = self.font.render(
            f"Wave {self.num}", True, pygame.Color("#ffffff")
        )
        text_rect = text_surface.get_rect()
        text_rect.midtop = self.game_surface.get_rect().midtop
        self.game_surface.blit(text_surface, text_rect)

    def update(self) -> None:
        self.draw_wave_number()
        self.register_new_enemy_if_required()

        if len(self.enemies) > 0 and len(self.enemies) <= self.number_of_enemies:
            self.finished = True
            for enemy in self.enemies:
                enemy.update()
                if enemy.hit_ground and enemy.visible:
                    self.hit_ground_func()
                    enemy.visible = False
                if enemy.visible:
                    self.finished = False

        if len(self.enemies) != self.number_of_enemies:
            self.finished = False

        self.frames_since_start += 1
