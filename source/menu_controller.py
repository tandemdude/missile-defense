import pygame
import typing
import webbrowser
import copy

from . import utils

COLOURS = {
    "EASY": pygame.Color("#77DD77"),
    "NORMAL": pygame.Color("#FFB347"),
    "HARD": pygame.Color("#FF6961"),
}


class Button:
    def __init__(
        self,
        game_surface,
        text,
        font_size,
        position_x,
        position_y,
        pressed_funcs,
        size=None,
    ):
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

    def on_press(self):
        for func in self.pressed_funcs:
            func()

    def check_if_pressed(self, mouse_position):
        button_rect = self.image.get_rect()
        button_rect.topleft = (self.x, self.y)
        if button_rect.collidepoint(mouse_position):
            self.on_press()

    def update(self):
        self.game_surface.blit(self.image, (self.x, self.y))


class MenuController:
    def __init__(
        self, game_surface, screen_width, screen_height, settings, advance_state_func
    ):
        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.settings = settings
        self.advance_state_func = advance_state_func

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

        self.state = "MENU"

        self.menu_buttons = [
            Button(
                self.game_surface,
                "START GAME",
                24,
                self.screen_width // 2,
                self.screen_height // 2,
                [self.advance_state_func],
            ),
            Button(
                self.game_surface,
                "SETTINGS",
                24,
                self.screen_width // 2,
                self.screen_height // 2 + 50,
                [self.settings_state],
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

    def open_docs_in_browser(self):
        webbrowser.open("https://tandemdude.gitlab.io/a-level-project")

    def open_source_code_in_browser(self):
        webbrowser.open("https://gitlab.com/tandemdude/a-level-project")

    def settings_state(self):
        self.state = "SETTINGS"

    def menu_state(self):
        self.state = "MENU"

    def listen_up(self):
        self.listening_up = True

    def listen_down(self):
        self.listening_down = True

    def listen_left(self):
        self.listening_left = True

    def listen_right(self):
        self.listening_right = True

    def listen_fire(self):
        self.listening_fire = True

    def centre_rect(self, surface, position):
        surface_rect = surface.get_rect()
        surface_rect.center = position
        return surface_rect

    def render_menu_background(self):
        welcome_text = self.title_font.render(
            "Missile Defence", True, pygame.Color("#FFFFFF")
        )
        self.menu_background.blit(
            welcome_text,
            self.centre_rect(
                welcome_text, (self.screen_width // 2, self.screen_height // 2 - 250)
            ),
        )

    def render_settings_background(self):
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

    def render_current_difficulty(self, target):
        current_difficulty = self.text_font.render(
            self.settings.difficulty, True, COLOURS[self.settings.difficulty]
        )
        target.blit(
            current_difficulty, self.centre_rect(current_difficulty, (150, 380))
        )

    def render_current_controls(self, target):
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

    def check_if_any_button_pressed(self, mouse_position):
        if self.state == "MENU":
            for button in self.menu_buttons:
                button.check_if_pressed(mouse_position)
        elif self.state == "SETTINGS":
            for button in self.settings_buttons:
                button.check_if_pressed(mouse_position)

    def submit_key(self, key):
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

    def process_event(self, event):
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

    def get_what_needs_to_be_updated(self):
        if self.state == "MENU":
            return self.menu_buttons
        elif self.state == "SETTINGS":
            return self.settings_buttons

    def update_all(self):
        if self.state == "MENU":
            self.game_surface.blit(self.menu_background, (0, 0))
        elif self.state == "SETTINGS":
            background_to_blit = copy.copy(self.settings_background)
            self.render_current_difficulty(background_to_blit)
            self.render_current_controls(background_to_blit)
            self.game_surface.blit(background_to_blit, (0, 0))

        to_be_updated = self.get_what_needs_to_be_updated()
        for instance in to_be_updated:
            instance.update()

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
