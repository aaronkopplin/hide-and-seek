import pygame
import neural_network as nn

class hider():
	def __init__(self, x, y, w, h, color):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.color = color
		self.surface = pygame.Surface((self.width, self.height))
		self.surface.fill(self.color)
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.speed = 5
		self.network = nn.neural_network(4,8,4)

	def get_center(self):
		return (self.x + (self.width / 2), self.y + (self.height / 2))

	def update_rect(self):
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

	def move_left(self, value, screen_width):
		self.x -= self.speed * value
		if self.x < 0:
			self.x = 0
		self.update_rect()

	def move_right(self, value, screen_width):
		self.x += self.speed * value 
		if self.x + self.width > screen_width:
			self.x = screen_width - self.width
		self.update_rect()

	def move_up(self, value, screen_height):
		self.y -= self.speed * value
		if self.y < 0:
			self.y = 0
		self.update_rect()

	def move_down(self, value, screen_height):
		self.y += self.speed * value
		if self.y + self.height > screen_height:
			self.y = screen_height - self.height
		self.update_rect()