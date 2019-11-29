import pygame
import math
import typing

from .reticle import Reticle
from .missile import Missile
from .wave import Wave
from .score import Score
from .balance import Balance
from .lives import Lives
from .game_over import GameOver
from .tower import Tower
from .highscore import HighscoreTable
from .textinput import TextInput

# Constants
MAX_MISSILES = 5
INITIAL_ENEMIES = 5
ENEMY_CONSTANTS = {"EASY": 0.5, "NORMAL": 0.8, "HARD": 1.3}
TIME_BETWEEN_WAVES = 1
FRAME_RATE = 60
LIVES = 3
FONT_SIZE = 24
PLAYER_MISSILE_VELOCITY = 7
TOWER_MISSILE_VELOCITY = 5
POSSIBLE_TOWER_POSITIONS = [(100, 550), (200, 550), (565, 550), (665, 550)]


def calculate_enemies_for_wave(
    initial_enemies: int, wave_number: int, constant: float
) -> int:
    """
    Equation to calculate the number of enemies for any given wave.
    Exponential equation ensures the difficulty progression is non-linear
    meaning the number of enemies does not increase at a constant rate.

    :param initial_enemies: The :class:`int` starting number of enemies for the zeroth wave
    :param wave_number: The :class:`int` current wave number
    :param constant: The enemy constant, usually a :class:`float` between 0 and 1
    :return: :class:`int` amount of enemies for the given wave
    """
    return round(initial_enemies + (wave_number ** 2 * constant))


def calculate_wave_spawn_period(wave_number: int) -> float:
    """
    Equation to calculate the amount of time enemies have to spawn for any given wave.
    Equates to :math:`5√(4x) + 5` where :math:`x` is the wave number.
    This gives a surd curve meaning that for the first 5 waves, the amount of time increases
    at a faster rate than for later waves, hence increasing the late-game difficulty.

    :param wave_number: The :class:`int` current wave number
    :return: :class:`float` amount of seconds that enemies will spawn over
    """
    return 5 * math.sqrt(4 * wave_number) + 5


def get_rect_of_instance(instance) -> pygame.Rect:
    """
    Gets the pygame.Rect of a given instance's image attribute
    Returns a pygame.Rect in the correct position.

    :param instance: An object that has an image attribute
    :return: :class:`pygame.Rect` in the correct position
    """
    rect = instance.image.get_rect()
    rect.x = instance.x
    rect.y = instance.y
    return rect


def is_colliding(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """
    Takes two pygame.Rect instances and returns a bool indicating
    whether or not they are currently colliding.

    The pygame colliderect function already provides this functionality,
    this implementation simply makes it easier to read, more pythonic.

    :param rect1: :class:`pygame.Rect` instance
    :param rect2: :class:`pygame.Rect` instance
    :return: :class:`bool` to indicate whether or not the rects are colliding
    """
    return rect1.colliderect(rect2)


class GameController:
    """
    Link class which acts as a bridge between the main game
    and all other instances being used throughout the game.

    Prevents classes knowing about other classes which are
    unrelated, reducing code complexity.

    All classes communicate to each other through this class,
    unless other classes are directly related, such as the
    :class:`source.wave.Wave` and :class:`source.enemy.Enemy` class.

    :param game_surface: The game's window where sprites will be drawn
    :param screen_width: :class:`int` width of the window in pixels
    :param screen_height: :class:`int` height of the window in pixels
    :param settings: :class:`source.settings.Settings` instance
    :param advance_state_func: Procedure to advance the game state
    """

    def __init__(
        self,
        game_surface: pygame.Surface,
        screen_width: int,
        screen_height: int,
        settings,
        advance_state_func: typing.Callable,
    ) -> None:
        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.settings = settings
        self.advance_state_func = advance_state_func

        self.control_scheme = self.settings.control_scheme
        self.reticle = Reticle(self.game_surface, self.screen_width, self.screen_height)
        self.missiles = []

        self.wave_number = 0
        self.current_wave = None
        self.frames_to_next_wave = 0
        self.counting_down = False

        self.towers = self.create_towers()

        self.lives = Lives(
            self.game_surface, self.screen_width, self.screen_height, FONT_SIZE, LIVES
        )

        self.game_over_screen = GameOver(
            self.game_surface, self.screen_width, self.screen_height, FONT_SIZE
        )

        self.internal_game_over = False
        self.game_over = False

        self.score = Score(
            self.game_surface, self.screen_width, self.screen_height, FONT_SIZE
        )
        self.balance = Balance(
            self.game_surface, self.screen_width, self.screen_height, FONT_SIZE
        )
        self.highscores_table = HighscoreTable(
            self.game_surface, self.screen_width, self.screen_height
        )
        self.score_saved = False
        self.text_input = None

    def save_score(self, name: str) -> None:
        """
        Stores the name submitted by the player with their
        score into the databases.

        :param name: :class:`str` player name to be stored
        """
        if not self.score_saved:
            self.highscores_table.add_new_score(name, self.score.value)
            self.score_saved = True

    def enemy_hit_ground(self) -> None:
        """
        Callback function passed into Wave on instantiation. Provides a method for the enemies to
        tell the :class:`source.controller.Controller` class when to decrement the lives counter.

        :return: `None`
        """
        self.lives.decrement()

    def get_current_enemies(self) -> typing.Optional[typing.List]:
        """
        Function passed to :class:`source.tower.Tower` on init. When called, returns a list
        of all enemies in the current wave.

        :return: :class:`list` of all enemies in the current wave
        """
        return (
            None if self.current_wave is None else self.current_wave.get_all_enemies()
        )

    def create_towers(self):
        return [
            Tower(
                self.game_surface,
                self.screen_width,
                self.screen_height,
                x,
                y,
                self.get_current_enemies,
                TOWER_MISSILE_VELOCITY,
            )
            for x, y in POSSIBLE_TOWER_POSITIONS
        ]

    def create_new_wave(self) -> None:
        """
        Instantiate a new :class:`source.wave.Wave` object after calculating the correct number
        of enemies to be spawned in the wave.
        Increments the current wave number by 1.

        :return: `None`
        """
        number_of_enemies = calculate_enemies_for_wave(
            INITIAL_ENEMIES, self.wave_number, ENEMY_CONSTANTS[self.settings.difficulty]
        )
        # Instantiate a new :class:`source.wave.Wave` from given parameters
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

        :return: `None`
        """
        if len(self.missiles) < MAX_MISSILES:
            reticle_position = self.reticle.current_position()
            self.missiles.append(
                Missile(
                    self.game_surface,
                    self.screen_width,
                    self.screen_height,
                    self.screen_width // 2,
                    self.screen_height,
                    reticle_position[0],
                    reticle_position[1],
                    PLAYER_MISSILE_VELOCITY,
                )
            )

    def process_event(self, event: pygame.event.Event) -> None:
        """
        Process the passed in event, sending a signal to the reticle,
        or firing a missile if necessary.

        TODO: Reformat this to use switch/case type syntax to prevent large IF blocks?

        :param event: Any :class:`pygame.event.Event` instance
        :return: `None`
        """
        if self.internal_game_over and not self.text_input.listening:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.advance_state_func()
                elif event.key == pygame.K_ESCAPE:
                    self.advance_state_func()
                    self.advance_state_func()

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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.place_tower(event.pos)

        if self.text_input is not None:
            self.text_input.process_event(event)

    def check_collisions(self, missile_list) -> None:
        """
        Check if any sprites are colliding such that
        a missile or enemy needs to be removed from the display.

        :return: `None`
        """
        for missile in missile_list[:]:  # Loop through a copy of self.missiles
            # Check if a missile has flown out of bounds and remove it if necessary
            if not missile.visible:
                missile_list.remove(missile)
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
                    # Increment score and balance, toggle enemy visibility, mark the missile
                    # to be removed at the end of this iteration
                    self.score.increment(enemy.score_value)
                    self.balance.increment(enemy.balance_value)
                    enemy.visible = False
                    hit_enemy = True
            if hit_enemy:
                # Remove the missile from self.missiles if it hit an enemy
                missile.visible = False
                missile_list.remove(missile)

    def get_what_needs_to_be_updated(self) -> list:
        """
        Return a list of all the instances that need to be updated in any given frame.
        Only updates what needs to be updated,
        ie, does not update the game_over screen if the game_over conditions have not been met.

        :return: :class:`list` of all instances that need to be updated in a given frame
        """
        to_be_updated = []

        if self.internal_game_over:
            to_be_updated += [self.score, self.balance, self.lives]

            if self.text_input is None:
                self.text_input = TextInput(
                    self.game_surface,
                    self.screen_width,
                    self.screen_height,
                    "fixedsys.ttf",
                    FONT_SIZE,
                    3,
                )
            elif not self.text_input.listening:
                self.save_score(str(self.text_input))
                to_be_updated += [self.game_over_screen, self.highscores_table]
                # Marks text input complete allowing the Game to transfer into the
                # game over state to listen for the retry keys
                self.game_over = True

            if self.text_input is not None and self.text_input.listening:
                to_be_updated += [self.text_input]

        else:
            # Ensures that update_all does not attempt to update a NoneType
            if len(self.towers) > 0:
                to_be_updated += self.towers
            if self.current_wave is not None:
                to_be_updated += [self.current_wave]

            to_be_updated += self.missiles + [
                self.reticle,
                self.score,
                self.balance,
                self.lives,
            ]

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

    def place_tower(self, mouse_position: typing.Tuple[int]) -> None:
        """
        Place a tower in an empty position when the mouse is clicked.
        Checks where the mouse cursor is and if it is colliding with
        an empty tower position. If the tower is not already placed
        then place a tower at that position if the player has enough
        credits.

        :param mouse_position: :class:`tuple`[:class:`int`] containing cursor's x, y coordinate
        :return: None 
        """
        list_of_tower_rects = []
        for tower in self.towers:
            if not tower.placed:
                tower_rect = tower.unplaced_marker.get_rect()
                tower_rect.topleft = (tower.x, tower.y)
                list_of_tower_rects.append(tower_rect)
            else:
                tower_rect = get_rect_of_instance(tower)
                list_of_tower_rects.append(tower_rect)

        for index, tower_rect in enumerate(list_of_tower_rects, start=0):
            if tower_rect.collidepoint(mouse_position):
                tower_to_place = self.towers[index]
                break
            else:
                tower_to_place = None

        if tower_to_place is not None and not tower_to_place.placed:
            if self.balance.value >= tower_to_place.price:
                tower_to_place.placed = True
                self.balance.decrement(tower_to_place.price)

    def update_all(self) -> None:
        """
        Updates all instances fetched by get_what_needs_to_be_updated() and
        runs game_over logic.

        :return: None
        """
        # Transfers game into the game_over state if all lives have been lost, or runs wave logic
        if self.lives == 0:
            self.internal_game_over = True
        else:
            self.create_new_wave_if_required()
            self.check_collisions(self.missiles)
            tower_missiles = []
            for tower in self.towers:
                tower_missiles += tower.missiles
            self.check_collisions(tower_missiles)
            self.check_if_wave_finished()

        # Gets all instances that need to be updated in a given frame and calls update() on each in turn
        to_be_updated = self.get_what_needs_to_be_updated()
        for instance in to_be_updated:
            instance.update()
