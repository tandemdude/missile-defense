import pygame
import typing
import requests

from . import utils
from . import db_utils
from . import global_api_utils

FONT_SIZE = 24
PADDING_TOP = 5
PADDING_BOTTOM = 5


class HighscoreRow:
    """
    Class to represent a single row in the :class:`source.highscore.HighscoreTable`
    Contains the display name and score of a player

    :param name: The :class:`str` display name of the player
    :param score: The :class:`int` score of the player
    """

    font = None

    def __init__(self, name: str, score: int) -> None:
        if HighscoreRow.font is None:
            HighscoreRow.font = utils.load_font("source.fonts", "fixedsys.ttf", FONT_SIZE)
        self.font = HighscoreRow.font

        self.name = name
        self.score = score
        self.string_to_render = f"{self.name} - {self.score}"
        self.rendered_row = self.font.render(
            self.string_to_render, True, pygame.Color("#FFFFFF")
        )


class HighscoreTable:
    """
    Class to represent a table of global or local highscores
    There should only be one instance of this initialised at any time

    :param game_surface: The :class:`pygame.Surface` to draw the table onto
    :param screen_width: The :class:`int` width of the screen in pixels
    :param screen_height: The :class:`int` height of the screen in pixels
    """

    def __init__(
        self, game_surface: pygame.Surface, screen_width: int, screen_height: int
    ) -> None:
        db_utils.create_database_and_table_if_not_exists()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_surface = game_surface
        self.font = utils.load_font("source.fonts", "fixedsys.ttf", FONT_SIZE)
        self.rows = []
        self.num_rows = len(self.rows)
        self.visible = False
        self.surface_to_draw = None
        self.global_fetch_succeeded = False
        self.connected_to_internet = global_api_utils.is_connected()

    def add_new_score(self, name: str, score: int) -> None:
        """
        Save a score to both the local database and remote global
        database if the computer is connected to the internet

        :param name: :class:`str` name to store
        :param score: :class:`int` score to store
        :return: None
        """
        # Add a score to the local database and also POST it to the
        # api if the computer is connected to the internet
        db_utils.insert_score(name, score)
        if self.connected_to_internet:
            global_api_utils.post_new_score(name, score)
        self.update_highscore_surface()

    def generate_rows(self) -> typing.List[HighscoreRow]:
        """
        Gets highscore data from the appropriate source, be that local
        or global and parse the data into :class:`source.highscore.HighscoreRow` instances
        to be rendered by :func:`source.highscore.HighscoreTable.render`

        :return: :class:`list` of :class:`source.highscore.HighscoreRow` instances
        """
        # Get highscore data from the api if the computer is
        # connected to the internet
        if self.connected_to_internet:
            try:
                raw_rows = global_api_utils.get_high_scores()
                self.global_fetch_succeeded = True
            except (requests.exceptions.HTTPError, ConnectionError):
                self.global_fetch_succeeded = False
        # If global highscores could not be fetched then get the
        # local ones instead
        if not self.global_fetch_succeeded:
            raw_rows = db_utils.get_high_scores()

            # Loop through the raw response from the api or database and
            # reformat each to the format that self.render() is expecting
        parsed_rows = []
        for row in raw_rows:
            parsed_rows.append(HighscoreRow(row[0], row[1]))
        return parsed_rows

    def render(self) -> pygame.Surface:
        """
        Renders the highscores into a table creating a :class:`pygame.Surface` which is displayed
        to the user on game over

        :return: :class:`pygame.Surface` to blit to the game surface
        """
        # Render the highscore table header depending on if the scores are local or global
        title_text = (
            "Global High Scores" if self.global_fetch_succeeded else "Local High Scores"
        )
        title_surface = self.font.render(title_text, True, pygame.Color("#FFFFFF"))
        title_surface_rect = title_surface.get_rect()
        title_surface_rect.midtop = (self.screen_width // 2, PADDING_TOP)

        # Create a transparent surface the same dimentions as the game window
        highscore_surface = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        # Draw the table header onto the highscore surface
        highscore_surface.blit(title_surface, title_surface_rect)

        # Coordinate for the first row of the highscores table
        next_row_midtop = [self.screen_width // 2, PADDING_TOP + FONT_SIZE]
        # Loops through all HighscoreRow objects in self.rows and renders
        # each one, then draws them onto the highscore surface
        for row in self.rows:
            row_rect = row.rendered_row.get_rect()
            row_rect.midtop = next_row_midtop
            highscore_surface.blit(row.rendered_row, row_rect)
            # Move the coordinate for the next row downwards
            next_row_midtop[1] += FONT_SIZE

            # Displays a message to the user if the global high scores
            # couldn't be fetched from the api
        if not self.global_fetch_succeeded:
            footer_surface = self.font.render(
                "Global fetch failed: displaying local scores only.",
                True,
                pygame.Color("#FF0000"),
            )
            footer_surface_rect = footer_surface.get_rect()
            # Position the message in the bottom centre of the screen
            footer_surface_rect.midbottom = (
                self.screen_width // 2,
                self.screen_height - PADDING_BOTTOM,
            )
            # Draws the message onto the highscore surface
            highscore_surface.blit(footer_surface, footer_surface_rect)

        return highscore_surface

    def update_highscore_surface(self) -> None:
        """
        Regenerates the highscore surface when called, updating
        any values that are no longer accurate

        :return: None
        """
        # Check if the computer is connected to the internet
        self.connected_to_internet = global_api_utils.is_connected()
        # Generate rows and render the highscore surface
        self.rows = self.generate_rows()
        self.surface_to_draw = self.render()

    def update(self) -> None:
        """
        Draws the highscore table onto the game surface

        :return: None
        """
        self.game_surface.blit(self.surface_to_draw, (0, 0))
