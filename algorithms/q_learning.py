
from algorithms.algorithms import Algo, HYPER_PARAMETERS_FOLDER, SAVED_MODELS_FOLDER, Transition
from environments.game import PlayRoom
from environments.tic_tac_toe.tic_tac_toe import TicTacToe
from json import load as jload
from matplotlib.pyplot import legend, plot, show, title, xlabel, ylabel
from os.path import dirname, join, realpath
from pickle import dump, load
from random import choice, random

with open(join(HYPER_PARAMETERS_FOLDER, 'q_learning.json')) as f:
  HYPER_PARAMETERS = jload(f)

class QLearning(Algo):
  def __init__(self, game: str, learning_rate: float = None, discount_factor: float = None, epsilon: float = None):
    super().__init__()
    self.Q_table = {}

    if learning_rate == None:
      self.learning_rate = HYPER_PARAMETERS[game]['learning_rate']
    else:
      self.learning_rate = learning_rate

    if discount_factor == None:
      self.discount_factor = HYPER_PARAMETERS[game]['discount_factor']
    else:
      self.discount_factor = discount_factor

    if epsilon == None:
      self.epsilon = HYPER_PARAMETERS[game]['epsilon']
    else:
      self.epsilon = epsilon

    self.game = game
    self._load_playroom(game = game)
  
  def determine_action(self, deterministic: bool):
    if random() < self.epsilon and not deterministic:
      return choice(self.playroom.possible_actions)
    
    state_code = self.playroom.game_state_code
    state_q_values = {k: v for k, v in self.Q_table.items() if state_code in k}

    if len(state_q_values) == 0:
      return choice(self.playroom.possible_actions)
    
    max_state_action = max(state_q_values, key = state_q_values.get)
    return int(max_state_action.split('-')[-1])
  
  def determine_discount_factor(self):
    df = 0.1
    while (df < 1.0):
      print(f'Discount factor: {df}')
      self.discount_factor = df
      self.reset()
      eval_x, eval_y = self.learn()
      plot(eval_x, eval_y, label = f'{df}')
      df += 0.1
    
    legend()
    title('Peformance during training for different discount factors')
    ylabel('Trained epochs')
    xlabel('Average evaluation reward')
    show()  
  
  def determine_epsilon(self):
    eps = 0.1
    while (eps < 1.0):
      print(f'Epsilon: {eps}')
      self.epsilon = eps
      self.reset()
      eval_x, eval_y = self.learn()
      plot(eval_x, eval_y, label = f'{eps}')
      eps += 0.1
    
    legend()
    title('Peformance during training for different epsilons')
    ylabel('Trained epochs')
    xlabel('Average evaluation reward')
    show()

  def determine_learning_rate(self):
    lr = 0.1
    while (lr < 1.0):
      print(f'Learning rate: {lr}')
      self.learning_rate = lr
      self.reset()
      eval_x, eval_y = self.learn()
      plot(eval_x, eval_y, label = f'{lr}')
      lr += 0.1
    
    legend()
    title('Peformance during training for different learning factors')
    ylabel('Trained epochs')
    xlabel('Average evaluation reward')
    show()

  def learn(self, n_epochs: int = 200_000, eval_freq: int = 1_000, num_eval_episodes: int = 500, early_stop: bool = True, early_stop_num: int = 10, verbose: bool = False):
    self.playroom.reset()
    done = False

    eval_y = []
    eval_x = []
    highest_eval = 0
    not_improved = 0

    for epoch in range(n_epochs):
      action = self.determine_action(deterministic = False)
      state_action_code = f'{self.playroom.game_state_code}-{action}'

      if state_action_code not in self.Q_table.keys():
        self.Q_table[state_action_code] = 0

      _, reward, done, _, _ = self.playroom.step(action = action)
      
      if done:
        self.playroom.reset()
        self.Q_table[state_action_code] = (1 - self.learning_rate) * self.Q_table[state_action_code] + self.learning_rate * (reward)
      
      else:
        next_optimal_state_action_code = f'{self.playroom.game_state_code}-{self.determine_action(deterministic = True)}'

        if next_optimal_state_action_code not in self.Q_table.keys():
          self.Q_table[next_optimal_state_action_code] = 0

        self.Q_table[state_action_code] = (1 - self.learning_rate) * self.Q_table[state_action_code] + self.learning_rate * (reward + self.discount_factor * self.Q_table[next_optimal_state_action_code])

      if (epoch + 1) % eval_freq == 0:
        eval_y.append(self._evaluate(num_eval_episodes = num_eval_episodes))
        eval_x.append(epoch + 1)

        if highest_eval < eval_y[-1]:
          highest_eval = eval_y[-1]
          not_improved = 0
        else:
          not_improved += 1

        if verbose:
          print(f'Evaluate {eval_x[-1]}/{n_epochs}: {eval_y[-1]}')
        self.playroom.reset()

        if early_stop and not_improved > early_stop_num:
          break
    
    if verbose:
      plot(eval_x, eval_y)
      title('Average reward during evalation')
      xlabel("Trained number of epochs")
      ylabel('Average reward')
      show()

    return eval_x, eval_y
  
  def load(self, file_name: str):
    with open(join(self._save_folder, file_name), 'rb') as f:
      self.Q_table = load(f)

  def reset(self):
    self.Q_table = {}

  def save(self, file_name: str):
    with open(join(self._save_folder, file_name), 'wb') as f:
      dump(self.Q_table, f)

  def _evaluate(self, num_eval_episodes: int):
    total_reward = 0
    for _ in range(num_eval_episodes):
      self.playroom.reset()
      done = False
      while not done:
        _, reward, done, _, _ = self.playroom.step(action = self.determine_action(deterministic = True))
      total_reward += reward
    return total_reward / num_eval_episodes

  def _load_playroom(self, game: str):
    if game == 'TicTacToe':
      self.playroom = PlayRoom(game = TicTacToe())
    else:
      raise ValueError(f'Game: {game} not known')

  @property
  def _save_folder(self):
    return join(SAVED_MODELS_FOLDER, 'q_learning', self.game)