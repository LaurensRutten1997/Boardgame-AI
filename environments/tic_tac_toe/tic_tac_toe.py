import numpy as np
from gym.spaces import Discrete, MultiDiscrete

from environments.game import Game

class TicTacToe(Game):
  def __init__(self):
    super().__init__()
    self.action_space = Discrete(n = 9)
    self.observation_space = MultiDiscrete(np.array([[3,3,3],[3,3,3],[3,3,3]]))