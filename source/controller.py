import pygame
import os
import math

from source.reticle import Reticle
from source.missile import Missile
from source.wave import Wave
from source.score import Score
from source.lives import Lives
from source.game_over import GameOver

# Constants
MAX_MISSILES = 5
INITIAL_ENEMIES = 5
ENEMY_CONSTANT = 0.5
TIME_BETWEEN_WAVES = 1
FRAME_RATE = 60
LIVES = 3
FONT_SIZE = 24


def calculate_enemies_for_wave(
    initial_enemies: int, wave_number: int, constant: float
) -> int:
    """
    Equation to calculate the number of enemies for any given wave.
    Exponential equation ensures the difficulty progression is non-linear
    meaning the number of enemies does not increase at a constant rate.

    :param initial_enemies: The starting number of enemies for the zeroth wave
    :param wave_number: The current wave number
    :param constant: The enemy constant, usually a float between 0 and 1
    :return: Integer number of enemies for the given wave
    """
    return round(initial_enemies + (wave_number ** 2 * constant))


def calculate_wave_spawn_period(wave_number: int) -> float:
    """
    Equation to calculate the amount of time enemies have to spawn for any given wave.
    Equates to :math:`5√(4x) + 5` where :math:`x` is the wave number.
    This gives a surd curve meaning that for the first 5 waves, the amount of time increases
    at a faster rate than for later waves, hence increasing the late-game difficulty.

    :param wave_number: The current wave number
    :return: Float amount of seconds that enemies will spawn over
    """
    return 5 * math.sqrt(4 * wave_number) + 5


def get_rect_of_instance(instance) -> pygame.Rect:
    """
    Gets the pygame.Rect of a given instance's image attribute
    Returns a pygame.Rect in the correct position.

    :param instance: An object that has an image attribute
    :return: pygame.Rect in the correct position
    """
    rect = instance.image.get_rect()
    rect.x, rect.y = instance.x, instance.y
    return rect


def is_colliding(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """
    Takes two pygame.Rect instances and returns a bool indicating
    whether or not they are currently colliding.

    The pygame colliderect function already provides this functionality,
    this implementation simply makes it easier to read, more pythonic.

    :param rect1: :class:`pygame.Rect` instance
    :param rect2: :class:`pygame.Rect` instance
    :return: Bool to indicate whether or not the rects are colliding
    """
    return rect1.colliderect(rect2)


class ControlScheme:
    """
    Class to contain the current keybindings for
    any actions that occur during gameplay.
    """

    def __init__(self) -> None:
        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT
        self.fire = pygame.K_SPACE


class Controller:
    """
    Link class which acts as a bridge between the main game
    and all other instances being used throughout the game.

    Prevents classes knowing about other classes which are
    unrelated, reducing code complexity.

    All classes communicate to each other through this class,
    unless other classes are directly related, such as the
    :class:`source.wave.Wave` and :class:`source.enemy.Enemy` class.

    :param game_surface: The game's window where sprites will be drawn
    :param screen_width: Int width of the window in pixels
    :param screen_height: Int height of the window in pixels
    """

    def __init__(
        self, game_surface: pygame.Surface, screen_width: int, screen_height: int
    ) -> None:
        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.running = False

        self.control_scheme = ControlScheme()
        self.reticle = Reticle(self.game_surface, self.screen_width, self.screen_height)
        self.missiles = []

        self.wave_number = 0
        self.current_wave = None
        self.frames_to_next_wave = 0
        self.counting_down = False

        self.lives = Lives(
            self.game_surface, self.screen_width, self.screen_height, FONT_SIZE, LIVES
        )

        self.game_over_screen = GameOver(
            self.game_surface, self.screen_width, self.screen_height, FONT_SIZE
        )

        self.game_over = False

        self.score = Score(
            self.game_surface, self.screen_width, self.screen_height, FONT_SIZE
        )
        self.font = pygame.font.Font(
            os.path.join("fonts", "SevenSegment.ttf"), FONT_SIZE
        )

    def enemy_hit_ground(self) -> None:
        """
        Callback function passed into Wave on instantiation. Provides a method for the enemies to
        tell the :class:`source.controller.Controller` class when to decrement the lives counter.

        :return: None
        """
        self.lives.decrement()

    def create_new_wave(self) -> None:
        """
        Instantiate a new :class:`source.wave.Wave` object after calculating the correct number
        of enemies to be spawned in the wave.
        Increments the current wave number by 1.

        :return: None
        """
        number_of_enemies = calculate_enemies_for_wave(
            INITIAL_ENEMIES, self.wave_number, ENEMY_CONSTANT
        )
        # Instantiate a new :class:`souce.wave.Wave` from given parameters
        self.current_wave = Wave(
            number_of_enemies,
            calculate_wave_spawn_period(self.wave_number) * FRAME_RATE,
            self.game_surface,
            self.screen_width,
            self.screen_height,
            self.enemy_hit_ground,
            self.wave_number,
            FONT_SIZE,
        )

        self.wave_number += 1

    def trigger_fire_missile(self) -> None:
        """
        Check if the maximum amount of missiles are already on the screen and
        instantiate a new one if the limit has not been reached.

        :return: None
        """
        if len(self.missiles) < MAX_MISSILES:
            self.missiles.append(
                Missile(
                    self.game_surface,
                    self.screen_width,
                    self.screen_height,
                    self.reticle.x,
                    self.reticle.y,
                )
            )

    def process_event(self, event: pygame.event.Event) -> None:
        """
        Process the passed in event, sending a signal to the reticle,
        or firing a missile if necessary.

        TODO: Reformat this to use switch/case type syntax to prevent large IF blocks?

        :param event: Any :class:`pygame.event.Event` instance
        :return: None
        """
        if not self.running:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == self.control_scheme.left:
                self.reticle.left()
            elif event.key == self.control_scheme.right:
                self.reticle.right()
            elif event.key == self.control_scheme.up:
                self.reticle.up()
            elif event.key == self.control_scheme.down:
                self.reticle.down()
            elif event.key == self.control_scheme.fire:
                self.trigger_fire_missile()

        elif event.type == pygame.KEYUP:
            if event.key == self.control_scheme.left:
                self.reticle.left(False)
            elif event.key == self.control_scheme.right:
                self.reticle.right(False)
            elif event.key == self.control_scheme.up:
                self.reticle.up(False)
            elif event.key == self.control_scheme.down:
                self.reticle.down(False)

    def check_collisions(self) -> None:
        """
        Check if any sprites are colliding such that
        a missile or enemy needs to be removed from the display.

        :return: None
        """
        for missile in self.missiles[:]:  # Loop through a copy of self.missiles
            # Check if a missile has flown out of bounds and remove it if necessary
            if 0 > missile.x or missile.x > self.screen_width or missile.y < 0:
                self.missiles.remove(missile)
                continue

            hit_enemy = False
            missile_rect = get_rect_of_instance(missile)
            # Loop through a list of enemies if there is currently a wave
            # else loop though an empty list meaning the loop does not occur
            for enemy in (
                [] if self.current_wave is None else self.current_wave.enemies.sprites()
            ):
                # Check if the enemy is colliding with the missile
                if enemy.visible and is_colliding(
                    missile_rect, get_rect_of_instance(enemy)
                ):
                    # Increment score and toggle enemy visibility, mark the missile
                    # to be removed at the end of this iteration
                    self.score.increment(enemy.value)
                    enemy.visible = False
                    hit_enemy = True
            if hit_enemy:
                # Remove the missile from self.missiles if it hit an enemy
                self.missiles.remove(missile)

    def get_what_needs_to_be_updated(self) -> list:
        """
        Return a list of all the instances that need to be updated in any given frame.
        Only updates what needs to be updated,
        ie, does not update the game_over screen if the game_over conditions have not been met.

        :return: List of all instances that need to be updated in a given frame
        """
        if self.game_over:
            to_be_updated = [self.score, self.lives, self.game_over_screen]
        else:
            to_be_updated = self.missiles + [self.reticle, self.score, self.lives]
            # Ensures that update_all does not attempt to update NoneType
            if self.current_wave is not None:
                to_be_updated += [self.current_wave]
        return to_be_updated

    def create_new_wave_if_required(self) -> None:
        """
        Checks if the conditions for the creation of a new wave have been met.
        Calls create_new_wave when required.

        :return: None
        """
        if self.frames_to_next_wave > 0:
            self.frames_to_next_wave -= 1
        else:
            self.counting_down = False

        # Creates new wave when the time gap between waves is finished
        if self.current_wave is None and self.frames_to_next_wave == 0:
            self.create_new_wave()

    def check_if_wave_finished(self) -> None:
        """
        Checks if the current wave is complete, ie, all the enemies have either hit the bottom
        of the screen or been hit by a missile.

        :return: None
        """
        if self.current_wave is None or self.current_wave.finished:
            self.current_wave = None
            # Begins the between wave timer if the wave has been completed
            if not self.counting_down:
                self.frames_to_next_wave = TIME_BETWEEN_WAVES * FRAME_RATE
                self.counting_down = True

    def update_all(self) -> None:
        """
        Updates all instances fetched by get_what_needs_to_be_updated() and
        runs game_over logic.

        :return: None
        """
        if not self.running:
            return

        # Transfers game into the game_over state if all lives have been lost, or runs wave logic
        if self.lives == 0:
            self.game_over = True
        else:
            self.create_new_wave_if_required()
            self.check_collisions()
            self.check_if_wave_finished()

        # Gets all instances that need to be updated in a given frame and calls update() on each in turn
        to_be_updated = self.get_what_needs_to_be_updated()
        for instance in to_be_updated:
            instance.update()
