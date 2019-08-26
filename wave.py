import pygame
from enemy import Enemy


class Wave:
    def __init__(
        self,
        number_of_enemies,
        time_limit,
        game_surface,
        screen_width,
        screen_height,
        hit_ground_func,
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

    def register_enemies(self):
        for _ in range(self.number_of_enemies):
            self.enemies.append(
                Enemy(self.game_surface, self.screen_width, self.screen_height)
            )

    def register_enemy(self):
        self.enemies.append(
            Enemy(self.game_surface, self.screen_width, self.screen_height)
        )

    def update(self):
        # if len(self.enemies) == self.number_of_enemies:
        #    self.finished = True
        self.finished = True
        for enemy in self.enemies:
            enemy.update()
            if enemy.hit_ground:
                self.hit_ground_func()
            if enemy.visible:
                self.finished = False
