import numpy as np
from gym.spaces import Discrete, MultiDiscrete
from math import floor

from environments.game import Game

class TicTacToe(Game):
  def __init__(self):
    super().__init__()
    self.action_space = Discrete(n = 9)
    self.observation_space = MultiDiscrete(np.array([[3,3,3],[3,3,3],[3,3,3]]))
    self.grid = np.zeros((3,3), dtype = np.int64)

  def step(self, action):
    return super().step(action)
  
  @property
  def _possible_actions(self):
    return [action for action in range(self.action_space.n) if (self.grid[self._action_to_row(action)][self._action_to_column(action)] == 0)]
  
  @staticmethod
  def _action_to_column(action):
    #Convert the action to the corresponding column in the grid
    return action % 3

  @staticmethod
  def _action_to_row(action):
    #Conver the action to the corresponding column in the row
    return floor(action / 3)
  