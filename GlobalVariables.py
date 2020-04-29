import Hider
import NeuralNetwork
import Seeker

frame_rate = 1/1000.0
screen_width = 200
screen_height = 200

square_length = 10
hider_spawn_x = 50
hider_spawn_y = (screen_height / 2) - 10
hider_width = square_length
hider_height = square_length
hider_inputs = 8
hider_hidden_layer = 12
hider_output = 4
hider_color = (0, 255, 0)
hider_alpha = 50
hider_speed = 5

seeker_spawn_x = 150
seeker_spawn_y = (screen_height / 2) - 10
seeker_width = square_length
seeker_height = square_length
seeker_color = (255, 0, 0)
seeker_alpha = 50


def new_neural_network():
    return NeuralNetwork.NeuralNetwork(hider_inputs, hider_hidden_layer, hider_output)


def new_hider():
    return Hider.Hider(new_neural_network())


def new_seeker():
    return Seeker.Seeker(seeker_spawn_x,
                         seeker_spawn_y,
                         seeker_width,
                         seeker_height,
                         seeker_color,
                         seeker_alpha)
