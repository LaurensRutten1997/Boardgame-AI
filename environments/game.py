from gym import Env
from random import randint, sample

class Game(Env):
  def __init__(self):
    super().__init__()
    self.num_players = 0
    self.player_turn = 0

  @property
  def game_state(self):
    return []
  
  @property
  def game_state_code(self):
    return ""
  
  @property
  def possible_actions(self):
    return []
  
  @property
  def reward(self):
    return 0
  
  @property
  def terminal(self):
    return False

class PlayRoom(Env):
  def __init__(self, game: Game, opponent: str = 'random'):
    super().__init__()
    self.game = game
    self.opponent = opponent
    self.action_space = self.game.action_space
    self.observation_space = self.game.observation_space
    self.player_turn = 0
  
  def reset(self):
    self.player_turn = randint(1, self.game.num_players)
    obs = self.game.reset()
    while self.player_turn != self.game.player_turn:
      obs, _, _, _, _ = self._take_opponent_turn()
    return obs, {}
  
  def step(self, action):
    obs, reward, terminated, truncated, info = self.game.step(action)
    
    #Check if game is finished
    if terminated or truncated:
      return obs, reward, terminated, truncated, info
    
    #Check if the player turn
    while self.player_turn != self.game.player_turn:
      obs, reward, terminated, truncated, info = self._take_opponent_turn()
      #Check if game is finished
      if terminated or truncated:
        self.game.player_turn = self.player_turn
        return self.game.game_state, self.game.reward, self.game.terminal, False, {}
    
    return obs, reward, terminated, truncated, info

  def _take_opponent_turn(self):
    if self.opponent == 'random':
      action = sample(self.game.possible_actions)
    return self.game.step(action)