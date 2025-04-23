from gym import Env

class Game(Env):
  def __init__(self):
    super().__init__()

  @property
  def _possible_actions(self):
    return []