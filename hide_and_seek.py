import pygame
import global_vars as gv
import hider
import seeker
import time

pygame.init()

class window():
	def __init__(self, network):
		self.running = True
		self.width = gv.screen_width
		self.height = gv.screen_height
		self.background_color = (100, 100, 100)
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.screen.fill(self.background_color)
		self.hider = gv.spawn_hider()
		self.seeker = seeker.seeker(150, (self.height / 2) - 10, 20, 20, (255,0,0))
		self.clock = time.time()
		# inputs - seeker.x, seeker.y, hider.x, hider.y
		# outputs - move left, move right, move up, move down
		self.neural_network = network

		#final
		self.run()

	def draw_objects(self):
		self.screen.blit(self.hider.surface, (self.hider.x, self.hider.y))
		self.screen.blit(self.seeker.surface, (self.seeker.x, self.seeker.y))

	def update_objects(self):
		seeker_center = self.seeker.get_center()
		hider_center = self.hider.get_center()
		self.neural_network.input([(seeker_center[0] / self.width), 
			(seeker_center[1] / self.height), 
			(hider_center[0] / self.width), 
			(hider_center[1] / self.height)])
		self.update_hider(self.neural_network.get_output())

	def update_hider(self, moves):
		self.hider.move_left(moves[0], self.width)
		self.hider.move_right(moves[1], self.width)
		self.hider.move_up(moves[2], self.height)
		self.hider.move_down(moves[3], self.height)

	def update(self):
		self.update_objects()

		self.screen.fill(self.background_color)
		self.running = not self.seeker.update(self.hider.rect)
		self.draw_objects()
		pygame.display.update()

	def run(self):
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()

			current_time = time.time()
			if current_time - self.clock > 1.0/500.0:
				self.clock = time.time()
				self.update()
