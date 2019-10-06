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
        self.enemies = pygame.sprite.Group()
        self.finished = False
        self.frames_since_start = 0
        self.num = wave_num + 1
        self.font = pygame.font.Font(os.path.join("fonts", "fixedsys.ttf"), font_size)
        self.enemy_spawn_times = [
            round(random.random() * self.time_limit_in_frames)
            for _ in range(number_of_enemies)
        ]

    def register_enemies(self) -> None:
        for _ in range(self.number_of_enemies):
            self.enemies.add(
                Enemy(
                    self.enemies,
                    self.game_surface,
                    self.screen_width,
                    self.screen_height,
                    self.hit_ground_func,
                    self.mark_incomplete,
                )
            )

    def register_enemy(self) -> None:
        self.enemies.add(
            Enemy(
                self.enemies,
                self.game_surface,
                self.screen_width,
                self.screen_height,
                self.hit_ground_func,
                self.mark_incomplete,
            )
        )

    def register_new_enemy_if_required(self) -> None:
        if self.frames_since_start in self.enemy_spawn_times:
            for _ in range(self.enemy_spawn_times.count(self.frames_since_start)):
                self.register_enemy()

    def draw_wave_number(self) -> None:
        text_surface = self.font.render(
            f"Wave {self.num}", True, pygame.Color("#ffffff")
        )
        text_rect = text_surface.get_rect()
        text_rect.midtop = self.game_surface.get_rect().midtop
        self.game_surface.blit(text_surface, text_rect)

    def mark_incomplete(self) -> None:
        self.finished = False

    def update(self) -> None:
        self.draw_wave_number()
        self.register_new_enemy_if_required()

        current_enemies = self.enemies.sprites()
        if len(current_enemies) > 0 and len(current_enemies) <= self.number_of_enemies:
            self.finished = True
            self.enemies.update()

        if len(current_enemies) != self.number_of_enemies:
            self.finished = False

        self.frames_since_start += 1
