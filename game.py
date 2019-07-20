import pygame


class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((800, 600))
		self.running = True
		self.clock = pygame.time.Clock()
		self.background = pygame.Surface((800, 600))
		self.background.fill(pygame.Color("#000000"))

	def run(self):
		while self.running:
			self.screen.blit(self.background, (0, 0))
			self.clock.tick(60)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

			pygame.display.flip()

		pygame.quit()


def main():
	game = Game()
	game.run()

if __name__ == "__main__":
	main()
