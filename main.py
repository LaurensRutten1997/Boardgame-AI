from gym import spaces

from environments.tic_tac_toe.tic_tac_toe import TicTacToe

space = spaces.Discrete(n = 9, seed = 23)
space.sample()