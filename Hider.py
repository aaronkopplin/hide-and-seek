import pygame
import GlobalVariables
import NeuralNetwork


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
        self.network = network
        self.alive = True

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
        return self.network.get_fitness()

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def get_rect(self):
        self.update_rect()
        return self.rect

    def hide(self, seeker, background_rect):
        x_value = self.x / GlobalVariables.screen_width
        y_value = self.y / GlobalVariables.screen_height
        seeker_x_value = seeker.x / GlobalVariables.screen_width
        seeker_y_value = seeker.y / GlobalVariables.screen_height
        d_to_top_wall = (self.y - background_rect.y) / GlobalVariables.screen_height
        d_to_bottom_wall = (background_rect.height - self.y) / GlobalVariables.screen_height
        d_to_left_wall = (self.x - background_rect.x) / GlobalVariables.screen_width
        d_to_right_wall =(background_rect.width - self.x) / GlobalVariables.screen_width
        movement = self.network.fire([x_value,
                                      y_value,
                                      seeker_x_value,
                                      seeker_y_value,
                                      d_to_top_wall,
                                      d_to_bottom_wall,
                                      d_to_left_wall,
                                      d_to_right_wall])

        # move left
        self.x -= self.speed * movement[0]
        if self.x < 0:
            self.x = 0

        # move right
        self.x += self.speed * movement[1]
        if self.x + self.width > background_rect.width:
            self.x = background_rect.width - self.width

        # move up
        self.y -= self.speed * movement[2]
        if self.y < 0:
            self.y = 0

        # move down
        self.y += self.speed * movement[3]
        if self.y + self.height > background_rect.height:
            self.y = background_rect.height - self.height

        # update the rect
        self.update_rect()

    def is_alive(self):
        return self.alive

    def kill(self):
        self.alive = False

    def __str__(self):
        return "(" + str(self.x)[:5] + ", " + str(self.y)[:5] + \
               "), width: " + str(self.width) + ", height: " + str(self.height) + ", fitness: "\
               + str(self.get_fitness())
