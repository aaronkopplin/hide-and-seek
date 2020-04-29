import pygame
import GlobalVariables
import itertools
import Hider
import Seeker
import time


class HideAndSeek:
    def __init__(self, hiders: list):
        pygame.init()
        # the background will be a surface at (0,0)
        self.x = 0
        self.y = 0
        # for infinite game loop
        self.running = True

        # get the width of the screen
        self.width = GlobalVariables.screen_width

        # get the height of the screen
        self.height = GlobalVariables.screen_height

        # set the background color for the window
        self.background_color = (100, 100, 100)

        # background surface for the hiders and seekers as input
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(self.background_color)
        self.background_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # pygame window
        self.screen = pygame.display.set_mode((self.width, self.height))

        # for frame rate
        self.clock = time.time()

        # list of entities controlled by neural networks
        self.hiders = hiders

        # controlled by an algorithm
        self.seekers = [GlobalVariables.new_seeker() for x in self.hiders]

        # error checking to see that there were an equal amount of hiders and seekers passed in
        self.check_entities()

        # for checking when the trial is over
        self.initial_population_size = len(hiders)
        self.kill_count = 0

        # final
        self.run()

    def check_entities(self):
        # each hider should have a seeker
        if len(self.seekers) != len(self.hiders):
            raise ValueError('length of hiders and seekers must be the same.')

    def tick(self):
        self.check_entities()
        if self.kill_count == self.initial_population_size:
            self.running = False

        # fill background before drawing objects
        self.screen.blit(self.background, (self.x, self.y))

        # draw objects on the background
        for h, s in zip(self.hiders, self.seekers):
            if h.is_alive():
                self.screen.blit(h.surface, (h.x, h.y))
            if s.is_alive():
                self.screen.blit(s.surface, (s.x, s.y))

        # after drawing the objects, update their position for next frame
        for h, s in zip(self.hiders, self.seekers):
            if h.is_alive() and s.is_alive():
                h.hide(s, self.background_rect)
                collision = s.seek(h)
                if collision:
                    h.kill()
                    s.kill()
                    self.kill_count += 1

        # advance frame in pygame
        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current_time = time.time()
            if current_time - self.clock > GlobalVariables.frame_rate:
                self.clock = time.time()
                self.tick()

        pygame.quit()