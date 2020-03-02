from constants import BOARD_HEIGHT, BOARD_WIDTH
from pathlib import Path

class AiContainer:
  def __init__(self, path):
    self.module = __import__(path.replace('.py', '').replace('.\\', ''))
    self.name = Path(self.module.__file__).stem
    self.ai = None
    self.reset_ai()
    self.last_result = None
    self.wins = 0

  def reset_ai(self):
    self.ai = self.module.Ai(BOARD_WIDTH, BOARD_HEIGHT)

  def place_ship(self, ship_len, valid_pos_fn):
    return self.ai.place_ship(ship_len, valid_pos_fn)

  def get_move(self):
    return self.ai.get_move(self.last_result)
