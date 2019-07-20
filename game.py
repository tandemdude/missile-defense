import pygame
from enemy import Enemy

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.running = True
		self.clock = pygame.time.Clock()
		self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.background.fill(pygame.Color("#000000"))

	def run(self):
		bob = Enemy(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
		
		while self.running:
			self.screen.blit(self.background, (0, 0))
			self.clock.tick(60)

			bob.update()

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
