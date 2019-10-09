import pygame
import random
import os
import typing

from source import utils

# Constants
SPRITE_WIDTH = 25
SPRITE_HEIGHT = 30
ENEMY_VELOCITY = 2
ANGLE_OFFSET = 270
NUMBER_OF_FRAMES = 14
FRAME_SIZE = (210, 387)


class Enemy(pygame.sprite.Sprite):
    """
    Represents a game enemy, what the player is trying to prevent
    from reaching the bottom of the screen.

    :param sprite_group: The :class:`pygame.sprite.Group` that the enemy is a part of
    :param game_surface: The :class:`pygame.Surface` to blit the sprite onto
    :param screen_width: Int width of the screen in pixels
    :param screen_height: Int height of the screen in pixels
    :param hit_ground_func: Method called when the enemy reaches the bottom of the screen
    :param mark_wave_incomplete_func: Method called to mark the wave incomplete while the enemy is still visible
    """

    spritesheet = None

    def __init__(
        self,
        sprite_group: pygame.sprite.Group,
        game_surface: pygame.Surface,
        screen_width: int,
        screen_height: int,
        hit_ground_func: typing.Callable,
        mark_wave_incomplete_func: typing.Callable,
    ) -> None:
        super().__init__(sprite_group)

        if Enemy.spritesheet is None:
            Enemy.spritesheet = pygame.image.load(
                os.path.join("images", "enemy_spritesheet.png")
            ).convert_alpha()
        self.asset = Enemy.spritesheet

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_surface = game_surface
        self.hit_ground_func = hit_ground_func
        self.mark_wave_incomplete_func = mark_wave_incomplete_func
        self.generate_positions_and_velocities()
        self.visible = True
        self.respawn = False
        self.hit_ground = False
        self.current_frame = 0
        self.value = 150

        self.frames = []
        self.create_animation_frames()
        self.rotate_all_frames()

        self.image: pygame.Surface

    def create_animation_frames(self) -> None:
        """
        Takes the spritesheet and splits it into a list of animation frames.

        :return: None
        """
        for x in range(NUMBER_OF_FRAMES):
            self.frames.append(self.asset.subsurface(((5 + x * 220, 5), FRAME_SIZE)))

    def random_start_position(self) -> tuple:
        """
        Defines a random x coordinate at the top of the screen where the enemy spawns.

        :return: Tuple x, y coordinate
        """
        return random.randint(0, self.screen_width - SPRITE_WIDTH), 0

    def random_aim_position(self) -> tuple:
        """
        Defines a random x coordinate at the bottom of the screen where the enemy
        is aimed towards.

        :return: Tuple x, y coordinate
        """
        return (
            random.randint(0, self.screen_width - SPRITE_WIDTH),
            self.screen_height - SPRITE_HEIGHT,
        )

    def generate_positions_and_velocities(self) -> None:
        """
        Defines the start and end coordinates, calculates the velocity vector required to
        move between them.

        :return: None
        """
        self.x, self.y = self.random_start_position()
        self.end_x, self.end_y = self.random_aim_position()
        self.velocity_x, self.velocity_y = utils.vector_from_positions(
            self.x, self.y, self.end_x, self.end_y, ENEMY_VELOCITY
        )

    def move(self) -> None:
        """
        Moves the enemy by the amount defined by its velocity.

        :return: None
        """
        self.x += self.velocity_x
        self.y += self.velocity_y

    def rotate_all_frames(self) -> None:
        """
        Rotates all frames of the enemy animation to point towards the enemy's aim position.

        :return: None
        """
        fixed_frames = []
        for frame in self.frames:
            frame = pygame.transform.scale(frame, (SPRITE_WIDTH, SPRITE_HEIGHT))
            frame = pygame.transform.rotate(
                frame,
                utils.get_angle_positions(
                    self.x, self.y, self.end_x, self.end_y, ANGLE_OFFSET
                ),
            )
            fixed_frames.append(frame)
        self.frames = fixed_frames

    def next_frame(self) -> None:
        """
        Defines the index of the current frame, looping back to 0 once all frames have been shown.

        :return:
        """
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0

    def draw_frame(self) -> None:
        """
        Draws the current frame of the animation onto the game surface

        :return: None
        """
        current_frame_image = self.frames[self.current_frame]
        self.image = current_frame_image
        self.game_surface.blit(current_frame_image, (self.x, self.y))
        self.next_frame()

    def update(self) -> None:
        """
        Updates the enemy's position on the screen, also checks
        whether or not it has reached the bottom of the screen.

        :return:
        """
        if self.y >= self.screen_height - SPRITE_HEIGHT:
            self.velocity_y = 0
            self.hit_ground = True

        if self.visible:
            self.move()
            self.draw_frame()
        elif self.respawn:
            self.generate_positions_and_velocities()
            self.visible = True

        if self.hit_ground and self.visible:
            self.hit_ground_func()
            self.visible = False
        if self.visible:
            self.mark_wave_incomplete_func()
