import numpy as np
from gym.spaces import Discrete, MultiDiscrete
from math import floor

from environments.game import Game

class TicTacToe(Game):
  def __init__(self):
    super().__init__()
    self.action_space = Discrete(n = 9)
    self.observation_space = MultiDiscrete(np.array([[3,3,3],[3,3,3],[3,3,3]]))
    
    self._player_turn = 0
    self._grid = np.zeros((3,3), dtype = np.int64)

  def step(self, action):
    if action not in self._possible_actions(self):
      return self.game_state, -1, True, False, {}

    self._grid[self._action_to_row(action)][self._action_to_column(action)] = self._player_turn

    return super().step(action)
  
  @property
  def game_state(self):
    observation = np.zeros((3,3), dtype = np.int64)
    for i in range(3):
      for j in range(3):
        if self._grid[i][j] == self._player_turn:
          observation[i][j] = 1
        elif self._grid[i][j] != 0:
          observation[i][j] = 2

  @property
  def terminal(self):
    if len(self._possible_actions) == 0 or self.winner != 0:
      return True
    return False
  
  @property
  def winner(self):
    for i in range(3):
      #Check rows
      if self._grid[i][0] == self._grid[i][1] == self._grid[i][2] != 0:
        return self._grid[i][0]

      #Check columns
      if self._grid[0][i] == self._grid[1][i] == self._grid[2][i] != 0:
        return self._grid[0][i]

    #Check diagonals
    if self._grid[0][0] == self._grid[1][1] == self._grid[2][2] != 0:
      return self._grid[0][0]

    return 0

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
  