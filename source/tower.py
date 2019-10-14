import pygame
import math
import typing

from missile import Missile
import enemy
import utils

SPRITE_WIDTH = 20
SPRITE_HEIGHT = 20


class Tower(pygame.sprite.Sprite):
    """
    Class to represent a tower, intended to target and shoot at enemies automatically.
    Aims to decrease the difficulty of the game

    :param game_surface: The :class:`pygame.Surface` to draw the tower onto
    :param screen_width: Int width of the window in pixels
    :param screen_height: Int height of the window in pixels
    :param get_enemies_func: Function called to get all enemies currently on the screen
    """

    def __init__(self, game_surface, screen_width, screen_height, get_enemies_func):
        super().__init__()

        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.get_enemies_func = get_enemies_func

        self.range = 300
        self.fire_rate = 10
        self.projectile_speed = 5
        self.all_enemies = None
        self.frames_since_last_fired = 0

        self.missiles = []

        self.x = self.screen_width / 4
        self.y = self.screen_height - 50

        self.image = pygame.Surface(
            (SPRITE_WIDTH, SPRITE_HEIGHT), pygame.SRCALPHA
        )
        self.image.fill(pygame.Color("#FFFFFF"))

    def calculate_distance(self, enemy) -> typing.Union[int, float]:
        x_diff = self.x - enemy.x
        y_diff = self.y - enemy.y
        diagonal_distance = math.sqrt((x_diff ** 2) + (y_diff ** 2))
        return diagonal_distance

    def find_nearest_enemy_in_range(self) -> typing.Optional[enemy.Enemy]:
        closest = [None, 1000000]
        current_enemies = self.get_enemies_func()
        for enemy in [] if current_enemies is None else current_enemies:
            if enemy.visible:
                dist = self.calculate_distance(enemy)
                if dist < closest[1]:
                    closest = [enemy, dist]
        if closest[1] <= self.range:
            return closest[0]

    def increment_frames(self) -> None:
        self.frames_since_last_fired += 1
        if self.frames_since_last_fired > self.fire_rate:
            self.frames_since_last_fired = 0

    def fire_towards_nearest_in_range_enemy(self) -> None:
        if self.frames_since_last_fired == 0:
            nearest_enemy = self.find_nearest_enemy_in_range()
            if nearest_enemy is None:
                return
            else:
                self.missiles.append(
                    Missile(
                        self.game_surface, 
                        self.screen_width, 
                        self.screen_height, 
                        self.x, 
                        self.y, 
                        nearest_enemy.x, 
                        nearest_enemy.y
                    )
                )

    def update(self) -> None:
        self.game_surface.blit(
            self.image, (self.x, self.y)
        )
        self.fire_towards_nearest_in_range_enemy()
        for missile in self.missiles[:]:
            missile.update()
            if not missile.visible:
                self.missiles.remove(missile)

        self.increment_frames()
