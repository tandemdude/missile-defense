import pygame
import typing
import webbrowser
import copy
import random

from .missile import Missile
from . import utils

MISSILE_LIMIT = 10
COLOURS = {
    "EASY": pygame.Color("#77DD77"),
    "NORMAL": pygame.Color("#FFB347"),
    "HARD": pygame.Color("#FF6961"),
}


class Button:
    """
    Reusable class designed to act as a button which is clickable by the player.
    Takes a list of functions to be run when the button is clicked.

    :param game_surface: :class:`pygame.Surface` to draw button onto
    :param text: :class:`str` text to label the button with
    :param font_size: :class:`int` font size in pixels
    :param position_x: :class:`int` :math:`x` position of the button's centre
    :param position_y: :class:`int` :math:`y` position of the button's centre
    :param pressed_funcs: :class:`list`[Callable] functions to call in order on button press
    :param size: Optional[:class:`tuple`] of :class:`int` width and height of the button. If unspecified, size is calculated automatically
    """
    def __init__(
        self,
        game_surface: pygame.Surface,
        text: str,
        font_size: int,
        position_x: int,
        position_y: int,
        pressed_funcs: typing.List[typing.Callable],
        size: typing.Tuple[int] = None,
    ) -> None:
        self.game_surface = game_surface

        if size is None:
            self.size_x = len(text) * font_size
            self.size_y = font_size + 2
        else:
            self.size_x, self.size_y = size

        self.image = pygame.Surface((self.size_x, self.size_y))
        self.image.fill(pygame.Color("#737373"))
        self.title_font = utils.load_font("source.fonts", "fixedsys.ttf", font_size)
        self.text = self.title_font.render(text, True, pygame.Color("#FFFFFF"))
        text_rect = self.text.get_rect()
        text_rect.center = self.image.get_rect().center
        self.image.blit(self.text, text_rect)

        self.x = position_x - self.size_x // 2
        self.y = position_y - self.size_y // 2

        self.pressed_funcs = pressed_funcs

    def on_press(self) -> None:
        """
        Loops through each function to be executed on button press and calls them

        :return: `None`
        """
        for func in self.pressed_funcs:
            func()

    def check_if_pressed(self, mouse_position: typing.Tuple[typing.Union[int, float]]) -> None:
        """
        Checks if the mouse cursor is colliding with the button and calls :func:`source.menu_controller.Button.on_press` if
        a collision is found

        :param mouse_position: Tuple[Union[:class:`int`, :class:`float`]] current mouse cursor position
        :return: `None`
        """
        button_rect = self.image.get_rect()
        button_rect.topleft = (self.x, self.y)
        if button_rect.collidepoint(mouse_position):
            self.on_press()

    def update(self) -> None:
        """
        Draws the button onto the game :class:`pygame.Surface`

        :return: `None`
        """
        self.game_surface.blit(self.image, (self.x, self.y))


class MenuController:
    """
    Class to control the menu state of the game, containing functionality
    including buttons for taking user choices and inputs for changing settings.

    :param game_surface: :class:`pygame.Surface` representing the game's window
    :param screen_width: :class:`int` width of the screen in pixels
    :param screen_height: :class:`int` height of the screen in pixels
    :param settings: Instance of :class:`source.settings.Settings`
    :param advance_state_func: Function which advances the game's state when called
    """
    def __init__(
        self, game_surface: pygame.Surface, screen_width: int, screen_height: int, settings, advance_state_func: typing.Callable
    ) -> None:
        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.settings = settings
        self.advance_state_func = advance_state_func

        self.decorative_missiles = []

        self.listening_up = False
        self.listening_down = False
        self.listening_left = False
        self.listening_right = False
        self.listening_fire = False

        self.title_font = utils.load_font("source.fonts", "fixedsys.ttf", 50)
        self.text_font = utils.load_font("source.fonts", "fixedsys.ttf", 24)

        self.menu_background = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )

        self.settings_background = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )

        self.instructions_background = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )

        self.listening_for_key_background = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )

        self.listening_for_key_background.fill((0, 0, 0, 200))
        key_prompt = self.title_font.render(
            "Press a key", True, pygame.Color("#FFFFFF")
        )
        self.listening_for_key_background.blit(
            key_prompt,
            self.centre_rect(
                key_prompt, (self.screen_width // 2, self.screen_height // 2)
            ),
        )

        self.render_menu_background()
        self.render_settings_background()
        self.render_instructions_background()

        self.state = "MENU"

        self.menu_buttons = [
            Button(
                self.game_surface,
                "START GAME",
                24,
                self.screen_width // 2,
                self.screen_height // 2 - 50,
                [self.advance_state_func],
                (200, 26),
            ),
            Button(
                self.game_surface,
                "SETTINGS",
                24,
                self.screen_width // 2,
                self.screen_height // 2,
                [self.settings_state],
                (200, 26),
            ),
            Button(
                self.game_surface,
                "INSTRUCTIONS",
                24,
                self.screen_width // 2,
                self.screen_height // 2 + 50,
                [self.instructions_state],
                (200, 26),
            ),
            Button(
                self.game_surface,
                "DOCS",
                24,
                self.screen_width - 55,
                self.screen_height - 20,
                [self.open_docs_in_browser],
            ),
            Button(
                self.game_surface,
                "CODE",
                24,
                self.screen_width - 55,
                self.screen_height - 50,
                [self.open_source_code_in_browser],
            ),
            Button(
                self.game_surface,
                "QUIT",
                24,
                55,
                self.screen_height - 20,
                [
                    self.advance_state_func,
                    self.advance_state_func,
                    self.advance_state_func,
                ],
            ),
        ]

        self.settings_buttons = [
            Button(
                self.game_surface,
                "EASY",
                24,
                150,
                200,
                [self.settings.set_difficulty_easy],
            ),
            Button(
                self.game_surface,
                "NORMAL",
                24,
                150,
                250,
                [self.settings.set_difficulty_normal],
            ),
            Button(
                self.game_surface,
                "HARD",
                24,
                150,
                300,
                [self.settings.set_difficulty_hard],
            ),
            Button(
                self.game_surface,
                "BACK",
                24,
                55,
                self.screen_height - 20,
                [self.menu_state],
            ),
            Button(
                self.game_surface,
                "UP",
                24,
                self.screen_width - 150,
                200,
                [self.listen_up],
            ),
            Button(
                self.game_surface,
                "DOWN",
                24,
                self.screen_width - 150,
                250,
                [self.listen_down],
            ),
            Button(
                self.game_surface,
                "LEFT",
                24,
                self.screen_width - 150,
                300,
                [self.listen_left],
            ),
            Button(
                self.game_surface,
                "RIGHT",
                24,
                self.screen_width - 150,
                350,
                [self.listen_right],
            ),
            Button(
                self.game_surface,
                "FIRE",
                24,
                self.screen_width - 150,
                400,
                [self.listen_fire],
            ),
        ]

        self.instructions_buttons = [
            Button(
                self.game_surface,
                "BACK",
                24,
                55,
                self.screen_height - 20,
                [self.menu_state],
            ),
        ]

    @staticmethod
    def open_docs_in_browser() -> None:
        """
        Opens the project docs page in a browser

        :return: `None`
        """
        webbrowser.open("https://tandemdude.gitlab.io/a-level-project")

    @staticmethod
    def open_source_code_in_browser() -> None:
        """
        Opens the git repo page in a browser

        :return:
        """
        webbrowser.open("https://gitlab.com/tandemdude/a-level-project")

    @staticmethod
    def centre_rect(surface: pygame.Surface, position: typing.Tuple[int]) -> pygame.Rect:
        """
        Centres the :class:`pygame.Rect` of a :class:`pygame.Surface` at a
        specified x,y coordinate.

        :param surface: :class:`pygame.Surface` to centre the rect of
        :param position: Tuple[:class:`int`] :math:`x, y` coordinate to centre at
        :return: :class:`pygame.Rect` centred in the correct position
        """
        surface_rect = surface.get_rect()
        surface_rect.center = position
        return surface_rect

    def settings_state(self) -> None:
        """
        Change the controller into the settings screen state

        :return: `None`
        """
        self.state = "SETTINGS"

    def instructions_state(self) -> None:
        """
        Change the controller into the instructions screen state
    
        :return: `None`
        """
        self.state = "INSTRUCTIONS"

    def menu_state(self) -> None:
        """
        Change the controller into the menu screen state
    
        :return: `None`
        """
        self.state = "MENU"

    def listen_up(self) -> None:
        """
        Mark the controller as listening for an input to bind to
        the reticle up key

        :return: `None`
        """
        self.listening_up = True

    def listen_down(self) -> None:
        """
        Mark the controller as listening for an input to bind to
        the reticle down key

        :return: `None`
        """
        self.listening_down = True

    def listen_left(self) -> None:
        """
        Mark the controller as listening for an input to bind to
        the reticle left key

        :return: `None`
        """
        self.listening_left = True

    def listen_right(self) -> None:
        """
        Mark the controller as listening for an input to bind to
        the reticle right key

        :return: `None`
        """
        self.listening_right = True

    def listen_fire(self) -> None:
        """
        Mark the controller as listening for an input to bind to
        the missile fire key

        :return: `None`
        """
        self.listening_fire = True

    def render_menu_background(self) -> None:
        """
        Render the menu screen with any text and images required

        :return: `None`
        """
        welcome_text = self.title_font.render(
            "Missile Defence", True, pygame.Color("#FFFFFF")
        )
        self.menu_background.blit(
            welcome_text,
            self.centre_rect(
                welcome_text, (self.screen_width // 2, self.screen_height // 2 - 250)
            ),
        )

    def render_instructions_background(self) -> None:
        """
        Render the menu screen with any text and images required

        :return: `None`
        """
        instructions_title = self.title_font.render(
            "Instructions", True, pygame.Color("#FFFFFF")
        )
        self.instructions_background.blit(
            instructions_title,
            self.centre_rect(
                instructions_title, (self.screen_width // 2, self.screen_height // 2 - 250)
            ),
        )
        instructions_text = self.text_font.render(
            "To Be Written...", True, pygame.Color("#FFFFFF")
        )
        self.instructions_background.blit(
            instructions_text,
            self.centre_rect(
                instructions_text, (self.screen_width // 2, self.screen_height // 2)
            ),
        )

    def render_settings_background(self) -> None:
        """
        Render the settings screen with any text and images required

        :return: `None`
        """
        settings_title = self.title_font.render(
            "Settings", True, pygame.Color("#FFFFFF")
        )
        self.settings_background.blit(
            settings_title,
            self.centre_rect(
                settings_title, (self.screen_width // 2, self.screen_height // 2 - 250)
            ),
        )

        difficulty_title = self.text_font.render(
            "Difficulty:", True, pygame.Color("#FFFFFF")
        )
        self.settings_background.blit(
            difficulty_title, self.centre_rect(difficulty_title, (150, 150))
        )

        difficulty_label = self.text_font.render(
            "Currently:", True, pygame.Color("#FFFFFF")
        )
        self.settings_background.blit(
            difficulty_label, self.centre_rect(difficulty_label, (150, 350))
        )

        controls_label = self.text_font.render(
            "Controls:", True, pygame.Color("#FFFFFF")
        )
        self.settings_background.blit(
            controls_label,
            self.centre_rect(controls_label, (self.screen_width // 2, 150)),
        )

        keybinds_label = self.text_font.render("Rebind:", True, pygame.Color("#FFFFFF"))
        self.settings_background.blit(
            keybinds_label,
            self.centre_rect(keybinds_label, (self.screen_width - 150, 150)),
        )

    def render_current_difficulty(self, target: pygame.Surface) -> None:
        """
        Render the current difficulty into a :class:`pygame.Surface` and blit it
        onto the target :class:`pygame.Surface`

        :param target: :class:`pygame.Surface` to draw difficulty onto
        :return: `None`
        """
        current_difficulty = self.text_font.render(
            self.settings.difficulty, True, COLOURS[self.settings.difficulty]
        )
        target.blit(
            current_difficulty, self.centre_rect(current_difficulty, (150, 380))
        )

    def render_current_controls(self, target: pygame.Surface) -> None:
        """
        Render the current control scheme into multiple :class:`pygame.Surface` and blit them
        onto the target :class:`pygame.Surface` accounting for a vertical offset between them

        :param target:
        :return:
        """
        up = self.text_font.render(
            f"UP - {pygame.key.name(self.settings.control_scheme.up)}",
            True,
            pygame.Color("#FFFFFF"),
        )
        down = self.text_font.render(
            f"DOWN - {pygame.key.name(self.settings.control_scheme.down)}",
            True,
            pygame.Color("#FFFFFF"),
        )
        left = self.text_font.render(
            f"LEFT - {pygame.key.name(self.settings.control_scheme.left)}",
            True,
            pygame.Color("#FFFFFF"),
        )
        right = self.text_font.render(
            f"RIGHT - {pygame.key.name(self.settings.control_scheme.right)}",
            True,
            pygame.Color("#FFFFFF"),
        )
        fire = self.text_font.render(
            f"FIRE - {pygame.key.name(self.settings.control_scheme.fire)}",
            True,
            pygame.Color("#FFFFFF"),
        )
        surfaces = [up, down, left, right, fire]
        vertical_offset = 200
        for surface in surfaces:
            target.blit(
                surface,
                self.centre_rect(surface, (self.screen_width // 2, vertical_offset)),
            )
            vertical_offset += 50

    def fire_decorative_missile(self):
        if len(self.decorative_missiles) < MISSILE_LIMIT:
            self.decorative_missiles.append(
                Missile(
                    self.game_surface,
                    self.screen_width,
                    self.screen_height,
                    random.randint(0, self.screen_width),
                    self.screen_height,
                    random.randint(0, self.screen_width),
                    random.randint(0, 3*(self.screen_height // 4)),
                    5,
                )
            )

    def check_if_any_button_pressed(self, mouse_position: typing.Tuple[typing.Union[int, float]]) -> None:
        """
        Loop through the list of :class:`source.menu_controller.Button` instances for the current
        game state and call :func:`source.menu_controller.Button.check_if_pressed` on each

        :param mouse_position: Tuple[Union[:class:`int`, :class:`float`]] position of the mouse cursor
        :return: `None`
        """
        if self.state == "MENU":
            for button in self.menu_buttons:
                button.check_if_pressed(mouse_position)
        elif self.state == "SETTINGS":
            for button in self.settings_buttons:
                button.check_if_pressed(mouse_position)
        elif self.state == "INSTRUCTIONS":
            for button in self.instructions_buttons:
                button.check_if_pressed(mouse_position)

    def submit_key(self, key: int) -> None:
        """
        Submit a new key for a direction's keybinding

        :param key: :class:`int` pygame key constant
        :return: `None`
        """
        if self.listening_up:
            self.settings.change_keybind("up", key)
            self.listening_up = False
        elif self.listening_down:
            self.settings.change_keybind("down", key)
            self.listening_down = False
        elif self.listening_left:
            self.settings.change_keybind("left", key)
            self.listening_left = False
        elif self.listening_right:
            self.settings.change_keybind("right", key)
            self.listening_right = False
        elif self.listening_fire:
            self.settings.change_keybind("fire", key)
            self.listening_fire = False

    def process_event(self, event: pygame.event.Event) -> None:
        """
        Check for a KEYDOWN event if the controller is listening for a new key
        input else check for a MOUSEBUTTONDOWN event and check if the player
        has clicked on a button.

        :param event: :class:`pygame.event.Event` to process
        :return: `None`
        """
        if any(
            [
                self.listening_up,
                self.listening_down,
                self.listening_left,
                self.listening_right,
                self.listening_fire,
            ]
        ):
            if event.type == pygame.KEYDOWN:
                self.submit_key(event.key)
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.check_if_any_button_pressed(event.pos)

    def get_what_needs_to_be_updated(self) -> typing.List[Button]:
        """
        Return the list of :class:`source.menu_controller.Button` which need
        to be updated in any given frame depending on the controller's state.

        :return: List[:class:`source.menu_controller.Button`]
        """
        to_be_updated = []

        if self.decorative_missiles:
            to_be_updated += self.decorative_missiles

        if self.state == "MENU":
            to_be_updated += self.menu_buttons
        elif self.state == "SETTINGS":
            to_be_updated += self.settings_buttons
        elif self.state == "INSTRUCTIONS":
            to_be_updated += self.instructions_buttons

        return to_be_updated

    def update_all(self) -> None:
        """
        Blit the menu or settings screen onto the game's :class:`pygame.Surface`, update
        all instances required in a given frame and blit a separate background if the controller
        is listening for a key input.

        :return: `None`
        """
        to_be_updated = self.get_what_needs_to_be_updated()
        for instance in to_be_updated:
            instance.update()

        if self.state == "MENU":
            self.game_surface.blit(self.menu_background, (0, 0))
        elif self.state == "SETTINGS":
            background_to_blit = copy.copy(self.settings_background)
            self.render_current_difficulty(background_to_blit)
            self.render_current_controls(background_to_blit)
            self.game_surface.blit(background_to_blit, (0, 0))
        elif self.state == "INSTRUCTIONS":
            self.game_surface.blit(self.instructions_background, (0, 0))

        self.fire_decorative_missile()
        for missile in self.decorative_missiles:
            if not missile.visible:
                self.decorative_missiles.remove(missile)

        if any(
            [
                self.listening_up,
                self.listening_down,
                self.listening_left,
                self.listening_right,
                self.listening_fire,
            ]
        ):
            self.game_surface.blit(self.listening_for_key_background, (0, 0))
