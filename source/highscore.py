import pygame
import os
import typing

from . import utils
from . import db_utils

FONT_SIZE = 24
PADDING_TOP = 5


class HighscoreRow:
	def __init__(self, name: str, score: int):
		self.name = name
		self.score = score
		self.font = utils.load_font("source.fonts", "fixedsys.ttf", FONT_SIZE)
		self.string_to_render = f"{self.name} - {self.score}"
		self.rendered_row = self.font.render(self.string_to_render, True, pygame.Color("#FFFFFF"))


class HighscoreTable:
	def __init__(self, game_surface: pygame.Surface, screen_width: int, screen_height: int):
		db_utils.create_database_and_table_if_not_exists()
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.game_surface = game_surface
		self.font = utils.load_font("source.fonts", "fixedsys.ttf", FONT_SIZE)
		self.title = "High Scores"
		self.rows = self.generate_rows()
		self.num_rows = len(self.rows)
		self.visible = False
		self.surface_to_draw = self.render()

	def add_new_score(self, name: str, score: int):
		db_utils.insert_score(name, score)
		self.update_highscore_surface()

	def generate_rows(self):
		raw_rows = db_utils.get_high_scores()
		parsed_rows = []
		for row in raw_rows:
			parsed_rows.append(HighscoreRow(row[0], row[1]))
		return parsed_rows

	def render(self):
		title_surface = self.font.render(self.title, True, pygame.Color("#FFFFFF"))
		title_surface_rect = title_surface.get_rect()
		title_surface_rect.midtop = (self.screen_width // 2, PADDING_TOP)

		highscore_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
		highscore_surface.blit(title_surface, title_surface_rect)

		next_row_midtop = [self.screen_width // 2, PADDING_TOP + FONT_SIZE]
		for row in self.rows:
			row_rect = row.rendered_row.get_rect()
			row_rect.midtop = next_row_midtop
			highscore_surface.blit(row.rendered_row, row_rect)
			next_row_midtop[1] += FONT_SIZE

		return highscore_surface

	def update_highscore_surface(self):
		self.rows = self.generate_rows()
		self.surface_to_draw = self.render()

	def update(self):
		self.game_surface.blit(self.surface_to_draw, (0, 0))
