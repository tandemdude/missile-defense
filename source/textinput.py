import pygame

from . import utils

PACKAGE = "source.fonts"
ALLOWED_KEYS = {
    pygame.K_0: "0",
    pygame.K_1: "1",
    pygame.K_2: "2",
    pygame.K_3: "3",
    pygame.K_4: "4",
    pygame.K_5: "5",
    pygame.K_6: "6",
    pygame.K_7: "7",
    pygame.K_8: "8",
    pygame.K_9: "9",
    pygame.K_a: "A",
    pygame.K_b: "B",
    pygame.K_c: "C",
    pygame.K_d: "D",
    pygame.K_e: "E",
    pygame.K_f: "F",
    pygame.K_g: "G",
    pygame.K_h: "H",
    pygame.K_i: "I",
    pygame.K_j: "J",
    pygame.K_k: "K",
    pygame.K_l: "L",
    pygame.K_m: "M",
    pygame.K_n: "N",
    pygame.K_o: "O",
    pygame.K_p: "P",
    pygame.K_q: "Q",
    pygame.K_r: "R",
    pygame.K_s: "S",
    pygame.K_t: "T",
    pygame.K_u: "U",
    pygame.K_v: "V",
    pygame.K_w: "W",
    pygame.K_x: "X",
    pygame.K_y: "Y",
    pygame.K_z: "Z",
}


class TextInput:
    def __init__(
        self,
        game_surface: pygame.Surface,
        screen_width: int,
        screen_height: int,
        font_name: str,
        font_size: int,
        char_limit: int,
    ):
        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = utils.load_font(PACKAGE, font_name, font_size)
        self.font_size = font_size
        self.text = []
        self.char_limit = char_limit
        self.listening = True

    def __str__(self):
        return "".join(self.text)

    def process_event(self, event):
        if self.listening:
            if event.type == pygame.KEYDOWN:
                if event.key in ALLOWED_KEYS and len(self.text) < self.char_limit:
                    self.text.append(ALLOWED_KEYS[event.key])
                elif event.key == pygame.K_BACKSPACE and len(self.text) > 0:
                    self.text.pop(len(self.text) - 1)
                elif event.key == pygame.K_RETURN and len(self.text) == self.char_limit:
                    self.listening = False

    def draw(self):
        game_surface_center = self.game_surface.get_rect().center

        input_title = "Type your name, press Enter when finished."
        input_title_surface = self.font.render(
            input_title, True, pygame.Color("#FFFFFF")
        )
        input_title_rect = input_title_surface.get_rect()
        input_title_rect.center = (
            game_surface_center[0],
            game_surface_center[1] - self.font_size,
        )
        self.game_surface.blit(input_title_surface, input_title_rect)

        input_text = " ".join(self.text)
        input_text += " _" * (3 - len(self.text))
        input_surface = self.font.render(
            input_text.strip(), True, pygame.Color("#FFFFFF")
        )
        input_surface_rect = input_surface.get_rect()
        input_surface_rect.center = game_surface_center
        self.game_surface.blit(input_surface, input_surface_rect)

    def update(self):
        self.draw()
