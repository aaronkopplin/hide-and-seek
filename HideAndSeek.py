import statistics
import pygame
import GlobalVariables
import time
import random
import Hider


def reproduce(parent_a: Hider, parent_b: Hider, rate: int):
    return parent_a.reproduce(parent_b.get_genes(), rate)


# def print_results(gen_, scores_, final_fitness_):
#     print("generations: " + str(gen_))
#     print("starting fitness: " + str(scores_[0])[:5])
#     print("final fitness: " + str(final_fitness_)[:5])
#     print("percent improvement: " + str(((final_fitness_ / scores_[0]) - 1) * 100)[:5] + "%")
#
#
# def print_diagnostics(gen_, avg_fit_):
#     print("gen " + str(gen_) + "\taverage fitness: " + str(int(avg_fit_)) + " ", end='')
#     for i in range(int(avg_fit_ / 2)):
#         print("|", end='')
#     print("")


class HideAndSeek:
    def __init__(self, population_size: int, mutation_rate: int, num_generations: int):
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

        self.population_size = population_size

        # list of entities controlled by neural networks
        self.hiders = [GlobalVariables.new_hider() for i in range(self.population_size)]

        # controlled by an algorithm
        self.seekers = [GlobalVariables.new_seeker() for x in self.hiders]

        # for checking when the trial is over
        self.kill_count = 0

        self.mutation_rate = mutation_rate
        self.num_generations = num_generations
        self.current_generation = 0

        self.scores = []

        # final
        self.run()

    def evolve(self):
        # reset the seekers so they spawn at the default spawn point
        self.seekers = [GlobalVariables.new_seeker() for x in self.hiders]

        # calculate fitness of population
        fitness = [x.get_fitness() for x in self.hiders]

        # append to scores for printing diagnostics
        self.scores.append(statistics.median(fitness))

        # select parents
        self.hiders.sort(key=lambda x: x.get_fitness(), reverse=True)
        reproducers = self.hiders[0:int(len(self.hiders)/2)]

        # mate reproducers
        population = []
        for parent in reproducers:
            # get the genes from a random reproducer and reproduce
            x = random.randint(0, len(reproducers) - 1)
            population.append(reproduce(parent, reproducers[x], self.mutation_rate))
            population.append(reproduce(parent, reproducers[x], self.mutation_rate))

        self.hiders = population
        self.current_generation += 1
        self.kill_count = 0
        print("generation " + str(self.current_generation) + "\timprovement: " +
              str(self.scores[-1] / self.scores[0] - 1)[:5] + "%")

    def tick(self):
        if self.kill_count == self.population_size:
            self.evolve()

        if self.current_generation == self.num_generations:
            self.running = False

        # fill background before drawing objects
        self.screen.blit(self.background, (self.x, self.y))

        # draw objects on the background
        for h, s in zip(self.hiders, self.seekers):
            if h.is_alive() and s.is_alive():
                self.screen.blit(h.surface, (h.x, h.y))
                self.screen.blit(s.surface, (s.x, s.y))
                h.hide(s, self.background_rect)
                if s.seek(h):
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
