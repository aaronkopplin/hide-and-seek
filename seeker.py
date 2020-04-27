import pygame
import math

class seeker():
	def __init__(self, x, y, w, h, color):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.color = color
		self.surface = pygame.Surface((self.width, self.height))
		self.surface.fill(self.color)
		self.easing = .05

	def get_center(self):
		return (self.x + (self.width / 2), self.y + (self.height / 2))

	def update(self, rectangle):
		target_center = (rectangle[0] + (rectangle[2] / 2), rectangle[1] + (rectangle[3]/2))
		self_center = (self.x + self.width / 2, self.y + self.height / 2)
		if rectangle.colliderect(pygame.Rect(self.x, self.y, self.width, self.height)):
			return True
		else:
			self.x += (target_center[0] - self_center[0]) * self.easing
			self.y += (target_center[1] - self_center[1]) * self.easing
			return False