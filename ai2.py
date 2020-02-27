import random

# Class name must be Ai
class Ai():
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.moves = self.__get_all_possible_moves()

  def get_move(self, last_result):
    """
    Needed for the AI.
    Called when it's time to make the next move

    :param last_result: The result of the last move, will be None the first round.
                        0 = Miss
                        1 = Hit
                        2 = Hit + ship sunken

    :return: The coordinates to fire at as a list [x, y], upper left is [0, 0]
    """

    return self.moves.pop(0)

  def place_ship(self, ship_len, valid_pos_fn):
    """
    Needed for the AI.
    Called once for each ship.

    :param ship_len: The length of the next ship to place
    :param valid_pos_fn: A function to validate that the position is valid
                         valid_pos_fn(x: int, y: int, ship_len: int, rotation: 0|90)

    :return: Placement of ship as list [x: int, y: int, rotation: 0|90]
    """
    while(True):
      x, y, rotation = self.__get_random_ship_placement(ship_len)
      if valid_pos_fn(x, y, rotation, ship_len):
        return [x, y, rotation]


  def __get_random_ship_placement(self, ship_len):
    rotation = random.choice([0, 90])
    if rotation == 0:
      x = random.randint(0, self.width - ship_len)
      y = random.randint(0, self.height - 1)
    else:
      x = random.randint(0, self.width - 1)
      y = random.randint(0, self.height - ship_len)
    return [x, y, rotation]


  def __get_all_possible_moves(self):
    moves = []
    for y in range(self.height):
      for x in range(self.width):
        moves.append([x, y])
    return moves
