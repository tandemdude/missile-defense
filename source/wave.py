import pygame
import random
import typing

from .enemy import Enemy
from . import utils


class Wave:
    """
    Class to represent a 'wave' of enemies. Controls how enemies are spawned over a specific time frame
    using a :class:`pygame.sprite.Group` to contain all enemies for any specific wave.

    :param number_of_enemies: Int amount of enemies to be spawned during the wave
    :param time_limit: Length of the enemy spawn period in frames
    :param game_surface: The :class:`pygame.Surface` to draw wave number and blit enemies
    :param screen_width: :class:`int` width of the window in pixels
    :param screen_height: :class:`int` height of the window in pixels
    :param hit_ground_func: Procedure called when any :class:`source.enemy.Enemy` reaches the bottom of the screen
    :param wave_num: :class:`int` number of the the current wave
    :param font_size: :class:`int` height of the font in pixels
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
        self.font = utils.load_font("source.fonts", "fixedsys.ttf", font_size)
        self.enemy_spawn_times = [
            round(random.random() * self.time_limit_in_frames)
            for _ in range(number_of_enemies)
        ]

    def register_enemies(self) -> None:
        """
        Adds a specific amount of enemies to the :attr:`Wave.enemies` :class:`pygame.sprite.Group`, all are spawned at the same time.

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
        Adds a single :class:`source.enemy.Enemy` to the :attr:`Wave.enemies` :class:`pygame.sprite.Group`. Enemies spawn as soon as they are registered.

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
        Checks whether sufficient time has passed to spawn a new :class:`source.enemy.Enemy`.
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

    def get_all_enemies(self) -> typing.Optional[typing.List]:
        """
        Function to get all enemies for the wave

        :return: Optional[:class:`list`] of all wave enemies
        """
        return self.enemies.sprites()

    def update(self) -> None:
        """
        Calls the update method on the :attr:`Wave.enemies` :class:`pygame.sprite.Group` and increments the frames since start counter.
        Draws the wave counter onto the surface.

        :return: None
        """
        self.draw_wave_number()
        self.register_new_enemy_if_required()

        current_enemies = self.enemies.sprites()
        if 0 < len(current_enemies) <= self.number_of_enemies:
            self.finished = True
            self.enemies.update()

        if len(current_enemies) != self.number_of_enemies:
            self.finished = False

        self.frames_since_start += 1
