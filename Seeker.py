import pygame
import Hider


class Seeker:
    def __init__(self, x, y, w, h, color, alpha):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = color
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)
        self.surface.set_alpha(alpha)
        self.rect = self.surface.get_rect()
        self.easing = .05
        self.alive = True

    def get_rect(self):
        return self.rect

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def seek(self, hider: Hider.Hider):
        hider_rect = hider.get_rect()

        # return true to tell game that you have collided
        if hider_rect.colliderect(self.rect):
            self.kill()
            hider.kill()
            return True
        else:
            # aim seeker at hider's center
            hider_center = (hider_rect.x + hider_rect.width / 2, hider_rect.y + hider_rect.height / 2)
            seeker_center = self.x + (self.width / 2), self.y + (self.height / 2)

            # move seeker based on easing
            self.x += (hider_center[0] - seeker_center[0]) * self.easing
            self.y += (hider_center[1] - seeker_center[1]) * self.easing
            self.update_rect()
            return False

    def is_alive(self):
        return self.alive

    def kill(self):
        self.alive = False

    def resuscitate(self):
        self.alive = True

    def __str__(self):
        return "(" + str(self.x)[:5] + ", " + str(self.y)[:5] + \
               ")\twidth: " + str(self.width) + "\theight:\t" + str(self.height)
