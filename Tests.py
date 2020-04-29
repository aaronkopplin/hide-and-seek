import NeuralNetwork
import math
import HideAndSeek
import Hider
import Seeker
import GlobalVariables

num_pairs = 50

hiders = [GlobalVariables.new_hider() for i in range(num_pairs)]
seekers = [GlobalVariables.new_seeker() for i in range(num_pairs)]
trial = HideAndSeek.HideAndSeek(hiders, seekers)



