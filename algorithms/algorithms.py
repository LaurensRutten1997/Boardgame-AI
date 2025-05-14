from os.path import dirname, join, realpath

HYPER_PARAMETERS_FOLDER = join(dirname(realpath(__file__)), 'hyper_parameters')
SAVED_MODELS_FOLDER = join(dirname(realpath(__file__)), 'saved_models')

class Algo():
  def __init__(self):
    pass

  def determine_action(self, deterministic: bool):
    pass

  def load(self):
    pass

  def reset(self):
    pass

  def save(self):
    pass

class Transition():
  def __init__(self, state_code: str, action: int, reward: int, next_state_code: str):
    self.state_code = state_code
    self.action = action
    self.next_state_code = next_state_code
    self.reward = reward