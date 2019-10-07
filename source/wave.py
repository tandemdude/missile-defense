import pygame
import random
import os
import typing
from source.enemy import Enemy


class Wave:
    """
    Class to represent a 'wave' of enemies. Controls how enemies are spawned over a specific time frame
    using a sprite group to contain all enemies for any specific wave.
    """
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
        """
        Adds a specific amount of enemies to the sprite group, all are spawned at the same time.

        .. note::
            This method is no longer used.

        :return: None
        """
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
        """
        Adds a single enemy to the sprite group. Enemies spawn as soon as they are registered.

        :return: None
        """
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
        """
        Checks whether sufficient time has passed to spawn a new enemy.
        If it has, a new enemy is registered.

        :return: None
        """
        if self.frames_since_start in self.enemy_spawn_times:
            for _ in range(self.enemy_spawn_times.count(self.frames_since_start)):
                self.register_enemy()

    def draw_wave_number(self) -> None:
        """
        Renders and draws the current wave number onto the game surface.
        Acts as an indicator to the user as to when the wave ends/a new wave begins.

        :return: None
        """
        text_surface = self.font.render(
            f"Wave {self.num}", True, pygame.Color("#ffffff")
        )
        text_rect = text_surface.get_rect()
        text_rect.midtop = self.game_surface.get_rect().midtop
        self.game_surface.blit(text_surface, text_rect)

    def mark_incomplete(self) -> None:
        """
        Marks the wave as unfinished.

        :return: None
        """
        self.finished = False

    def update(self) -> None:
        """
        Calls the update method on the enemies sprite group and increments the frames since start counter.
        Draws the wave counter onto the surface.

        :return: None
        """
        self.draw_wave_number()
        self.register_new_enemy_if_required()

        current_enemies = self.enemies.sprites()
        if len(current_enemies) > 0 and len(current_enemies) <= self.number_of_enemies:
            self.finished = True
            self.enemies.update()

        if len(current_enemies) != self.number_of_enemies:
            self.finished = False

        self.frames_since_start += 1