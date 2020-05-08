import pygame
import GlobalVariables
import NeuralNetwork
import math


def distance(x1, x2, y1, y2):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


class Hider:
    def __init__(self, network):
        self.x = GlobalVariables.hider_spawn_x
        self.y = GlobalVariables.hider_spawn_y
        self.width = GlobalVariables.hider_width
        self.height = GlobalVariables.hider_height
        self.color = GlobalVariables.hider_color
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)
        self.surface.set_alpha(GlobalVariables.hider_alpha)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = GlobalVariables.hider_speed
        self.acceleration = GlobalVariables.hider_acceleration
        self.network = network
        self.fitness = 1
        # self.distances_from_seeker = []
        self.alive = True

    def reset(self, new_genes):
        self.alive = True
        self.x = GlobalVariables.hider_spawn_x
        self.y = GlobalVariables.hider_spawn_y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.load_genes(new_genes)

    def reproduce(self, b_genes: list, mutation_rate: int):
        new_network = GlobalVariables.new_neural_network()
        new_network.load_genes(self.get_genes())
        new_network.mate(b_genes, mutation_rate)
        return Hider(new_network)

    def load_genes(self, new_genes):
        self.network.load_genes(new_genes)

    def get_genes(self):
        return self.network.get_genes()

    def get_fitness(self):
        return self.fitness

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def get_rect(self):
        self.update_rect()
        return self.rect

    def update_fitness(self, seeker):
        self.fitness += math.pow(distance(self.x, seeker.x, self.y, seeker.y), 2)

    def hide(self, seeker, background_rect):
        x_value = self.x / (GlobalVariables.screen_width * 1.0)
        y_value = self.y / (GlobalVariables.screen_height * 1.0)
        seeker_x_value = seeker.x / (GlobalVariables.screen_width * 1.0)
        seeker_y_value = seeker.y / (GlobalVariables.screen_height * 1.0)
        d_to_top_wall = (self.y - background_rect.y) / (GlobalVariables.screen_height * 1.0)
        d_to_bottom_wall = (background_rect.height - self.y) / (GlobalVariables.screen_height * 1.0)
        d_to_left_wall = (self.x - background_rect.x) / (GlobalVariables.screen_width * 1.0)
        d_to_right_wall = (background_rect.width - self.x) / (GlobalVariables.screen_width * 1.0)
        movement = self.network.fire([x_value,
                                      y_value,
                                      seeker_x_value,
                                      seeker_y_value,
                                      d_to_top_wall,
                                      d_to_bottom_wall,
                                      d_to_left_wall,
                                      d_to_right_wall])

        # update fitness
        self.update_fitness(seeker)
        # self.distances_from_seeker.append(distance(self.x, seeker.x, self.y, seeker.y))

        self.speed = movement[4]
        self.acceleration = movement[5]

        # move left
        self.x -= self.calculate_movement_distance(movement[0])
        if self.x < 0:
            self.x = 0

        # move right
        self.x += self.calculate_movement_distance(movement[1])
        if self.x + self.width > background_rect.width:
            self.x = background_rect.width - self.width

        # move up
        self.y -= self.calculate_movement_distance(movement[2])
        if self.y < 0:
            self.y = 0

        # move down
        self.y += self.calculate_movement_distance(movement[3])
        if self.y + self.height > background_rect.height:
            self.y = background_rect.height - self.height

        # update the rect
        self.update_rect()

    def calculate_movement_distance(self, input):
        self.speed = self.speed * self.acceleration
        return self.speed * input

    def is_alive(self):
        return self.alive

    def kill(self):
        self.alive = False

    def __str__(self):
        return "(" + str(self.x)[:5] + ", " + str(self.y)[:5] + \
               "), width: " + str(self.width) + ", height: " + str(self.height) + ", fitness: "\
               + str(self.get_fitness())
