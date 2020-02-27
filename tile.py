import colors

class Tile:
  def __init__(self, is_water, ship_id=-1, ship_piece="^"):
    self.is_water = is_water
    self.ship_id = ship_id
    self.ship_piece = ship_piece # ^, v, <, >, |, -
    self.hit = False
    self.miss = False

  def get_background_color(self):
    if self.hit:
      return colors.HIT
    if self.miss:
      return colors.MISS
    return colors.WATER

  def get_ship_color(self):
    if self.hit:
      return colors.SHIP_HIT
    return colors.SHIP

  @property
  def is_ship(self):
      return not self.ship_id == -1

