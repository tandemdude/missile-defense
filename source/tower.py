import pygame
import math
import typing
import copy

from .missile import Missile
from . import enemy
from . import utils

SPRITE_WIDTH = 35
SPRITE_HEIGHT = 35
ANGLE_OFFSET = 90


class Tower(pygame.sprite.Sprite):
    """
    Class to represent a tower, intended to target and shoot at enemies automatically.
    Aims to decrease the difficulty of the game

    :param game_surface: The :class:`pygame.Surface` to draw the tower onto
    :param screen_width: :class:`int` width of the window in pixels
    :param screen_height: :class:`int` height of the window in pixels
    :param get_enemies_func: Function called to get all enemies currently on the screen
    """

    asset = None

    def __init__(
        self,
        game_surface: pygame.Surface,
        screen_width: int,
        screen_height: int,
        x_pos: int,
        y_pos: int,
        get_enemies_func: typing.Callable[[None], typing.Optional[typing.List]],
        missile_velocity: int
    ):
        super().__init__()

        if Tower.asset is None:
            Tower.asset = utils.load_image("source.images", "tower.png").convert_alpha()
        self.asset = Tower.asset

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
        self.missile_velocity = missile_velocity

        self.x = x_pos
        self.y = y_pos

        self.original_image = pygame.Surface(
            (self.asset.get_width(), self.asset.get_height()), pygame.SRCALPHA
        )
        self.original_image.blit(self.asset, (0, 0))
        self.original_image = pygame.transform.scale(
            self.original_image, (SPRITE_WIDTH, SPRITE_HEIGHT)
        )
        self.image = copy.copy(self.original_image)

    def calculate_distance(self, enemy: enemy.Enemy) -> typing.Union[int, float]:
        """
        Calculates the straight-line distance from the tower's location
        and a given enemy instance

        :param enemy: :class:`source.enemy.Enemy` to calculate the distance to
        :return: Union[:class:`int`, :class:`float`] distance between the tower and enemy
        """
        x_diff = self.x - enemy.x
        y_diff = self.y - enemy.y
        diagonal_distance = math.sqrt((x_diff ** 2) + (y_diff ** 2))
        return diagonal_distance

    def find_nearest_enemy_in_range(self) -> typing.Optional[enemy.Enemy]:
        """
        Checks if there is an enemy in range of the tower and returns the closest
        if multiple are found

        :return: Nearest Optional[:class:`source.enemy.Enemy`] in range
        """
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
        """
        Increments :attr:`source.tower.Tower.frames_since_last_fired` by one,
        wrapping back to 0 once the tower fires

        :return:
        """
        self.frames_since_last_fired += 1
        if self.frames_since_last_fired > self.fire_rate:
            self.frames_since_last_fired = 0

    def point_towards_enemy(self, enemy) -> None:
        """
        Rotates the tower to point towards the nearest enemy in its range

        :param enemy: :class:`source.enemy.Enemy` to point towards
        :return: None
        """
        self.image = pygame.transform.rotate(
            self.original_image,
            utils.get_angle_positions(self.x, self.y, enemy.x, enemy.y, ANGLE_OFFSET),
        )

    def fire_towards_nearest_in_range_enemy(self) -> None:
        """
        Fires a projectile towards the nearest enemy if
        the frames counter specifies

        :return: None
        """
        if self.frames_since_last_fired == 0:
            nearest_enemy = self.find_nearest_enemy_in_range()
            if nearest_enemy is None:
                return
            else:
                self.point_towards_enemy(nearest_enemy)
                image_rect = self.image.get_rect()
                image_rect.topleft = self.x, self.y
                self.missiles.append(
                    Missile(
                        self.game_surface,
                        self.screen_width,
                        self.screen_height,
                        self.x,
                        self.y,
                        nearest_enemy.x,
                        nearest_enemy.y,
                        self.missile_velocity,
                    )
                )

    def update(self) -> None:
        """
        Blits the tower's image onto the game surface
        and updates all missiles currently travelling fired by the tower

        :return: None
        """
        self.fire_towards_nearest_in_range_enemy()
        self.game_surface.blit(self.image, (self.x, self.y))
        for missile in self.missiles[:]:
            missile.update()
            if not missile.visible:
                self.missiles.remove(missile)

        self.increment_frames()
