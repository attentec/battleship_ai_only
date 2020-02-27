import colors
import pygame
from constants import RECT_MARGIN, RECT_SIZE, SCREEN_PADDING, FONT_SIZE, SHIP_PADDING
from collections import defaultdict
from tile import Tile
import random

#random.seed(a=1, version=2)


class Battleship:
  """Game mechanics class."""

  def __init__(self, display, font, width, height, ships, ais, ai_names):
    self.display = display
    self.font = font
    self.width = width
    self.height = height

    self.ai_turn = random.randint(0,1)
    self.ais = ais
    self.ai_boards = [
      [[Tile(True) for _ in range(self.width)] for _ in range(self.height)],
      [[Tile(True) for _ in range(self.width)] for _ in range(self.height)]
    ]
    self.ai_names = ai_names
    self.last_result = [None, None]

    self.next_ship_id = 1
    self.place_ai_ships(ships)

    self.game_ended = False
    self.message = ""


  def place_ai_ships(self, ships):
    for ship_len in ships:
      x, y, rotation = self.ais[self.ai_turn].place_ship(ship_len, self.valid_ship_pos)
      if not self.valid_ship_pos(x, y, rotation, ship_len):
        print(self.ai_names[self.ai_turn] + " tried to place a invalid ship!")
        exit(1)
      self.place_ship(x, y, ship_len, rotation)

    self.ai_turn = (self.ai_turn + 1) % 2

    for ship_len in ships:
      x, y, rotation = self.ais[self.ai_turn].place_ship(ship_len, self.valid_ship_pos)
      if not self.valid_ship_pos(x, y, rotation, ship_len):
        print(self.ai_names[self.ai_turn] + " tried to place a invalid ship!")
        exit()
      self.place_ship(x, y, ship_len, rotation)

    self.ai_turn = (self.ai_turn + 1) % 2

  def next_turn(self):
    if self.game_ended:
      return

    x, y = self.ais[self.ai_turn].get_move(self.last_result[self.ai_turn])
    self.ai_turn = (self.ai_turn + 1) % 2

    result = 0
    tile = self.ai_boards[self.ai_turn][y][x]
    if tile.is_ship:
      tile.hit = True
      if self.ship_sunk(tile.ship_id):
        result = 2
      else:
        result = 1
      if self.all_ships_sunk():
        self.game_ended = True
    else:
      self.ai_boards[self.ai_turn][y][x].miss = True

    self.ai_turn = (self.ai_turn + 1) % 2

    if self.game_ended:
        self.message = "Winner: " + self.ai_names[self.ai_turn]

    self.last_result[self.ai_turn] = result
    self.ai_turn = (self.ai_turn + 1) % 2



  def draw_board(self, board, offset):
    """Draw board with ships"""
    w = RECT_SIZE * self.width + (self.width + 1) * RECT_MARGIN
    h = RECT_SIZE * self.height + (self.height + 1) * RECT_MARGIN
    pygame.draw.rect(self.display, colors.GRID, (SCREEN_PADDING + offset, SCREEN_PADDING, w, h))

    for x in range(self.width):
      for y in range(self.height):
        color = board[y][x].get_background_color()
        x_pos = self.calc_x(x, offset)
        y_pos = self.calc_y(y)
        pygame.draw.rect(self.display, color, (x_pos, y_pos, RECT_SIZE, RECT_SIZE))

        if board[y][x].is_ship:
          color = board[y][x].get_ship_color()
          piece = board[y][x].ship_piece
          if piece == '^':
            self.draw_top_ship(x, y, offset, color)
          elif piece == '|':
            self.draw_vertical_ship(x, y, offset, color)
          elif piece == 'v':
            self.draw_btm_ship(x, y, offset, color)
          elif piece == '<':
            self.draw_left_ship(x, y, offset, color)
          elif piece == '-':
            self.draw_horizontal_ship(x, y, offset, color)
          elif piece == '>':
            self.draw_right_ship(x, y, offset, color)

  def all_ships_sunk(self):
    for x in range(self.width):
      for y in range(self.height):
        if self.ai_boards[self.ai_turn][y][x].is_ship and not self.ai_boards[self.ai_turn][y][x].hit:
          return False
    return True

  def ship_sunk(self, id):
    for x in range(self.width):
      for y in range(self.height):
        if self.ai_boards[self.ai_turn][y][x].ship_id == id and not self.ai_boards[self.ai_turn][y][x].hit:
          return False
    return True

  def draw_ai1_board(self):
    self.draw_board(self.ai_boards[0], 0)

  def draw_ai2_board(self):
    offset = RECT_SIZE * self.width + (self.width + 1) * RECT_MARGIN + SCREEN_PADDING * 4
    self.draw_board(self.ai_boards[1], offset)

  def draw_boards(self):
    self.draw_ai1_board()
    self.draw_ai2_board()

  def draw(self):
    self.display.fill(colors.BACKGROUND)
    self.draw_boards()
    self.draw_text(self.ai_names[0] + " board", SCREEN_PADDING, (SCREEN_PADDING - FONT_SIZE) / 2)
    offset = RECT_SIZE * self.width + (self.width + 1) * RECT_MARGIN + SCREEN_PADDING * 4
    self.draw_text(self.ai_names[1] + " board", SCREEN_PADDING + offset, (SCREEN_PADDING - FONT_SIZE) / 2)

    middle_y = ((RECT_SIZE * self.height + (self.height + 1) * RECT_MARGIN) + SCREEN_PADDING * 2) / 2 - FONT_SIZE
    self.draw_center_text('vs', middle_y)

    btm_text_y = (RECT_SIZE * self.height + (self.height + 1) * RECT_MARGIN) + SCREEN_PADDING * 2
    self.draw_center_text(self.message, btm_text_y)

  def draw_text(self, text, x, y):
    textsurface = self.font.render(text, True, colors.TEXT)
    self.display.blit(textsurface, (x, y))

  def draw_center_text(self, text, y):
    text = self.font.render(text, True, colors.TEXT)
    width = (RECT_SIZE * self.width + (self.width + 1) * RECT_MARGIN) * 2 + SCREEN_PADDING * 6
    text_rect = text.get_rect(center=(width/2, y))
    self.display.blit(text, text_rect)


  def calc_x(self, x, offset):
    return x * RECT_SIZE + (x + 1) * RECT_MARGIN + SCREEN_PADDING + offset

  def calc_y(self, y):
    return y * RECT_SIZE + (y + 1) * RECT_MARGIN + SCREEN_PADDING


  def valid_ship_pos(self, x, y, rotation, ship_len):
    board = self.ai_boards[self.ai_turn]
    if self.x_out_of_bounds(x) or self.y_out_of_bounds(y) or rotation not in [0, 90]:
      return False
    if rotation == 0:
      for i in range(ship_len):
        if self.x_out_of_bounds(x + i) or board[y][x + i].is_ship:
          return False
    elif rotation == 90:
      for i in range(ship_len):
        if self.y_out_of_bounds(y + i) or board[y + i][x].is_ship:
          return False
    return True

  def place_ship(self, x, y, ship_len, rotation):
    board = self.ai_boards[self.ai_turn]
    id = self.next_ship_id
    if rotation == 0:
      for i in range(ship_len):
        piece = "<" if i == 0 else ">" if i == ship_len - 1 else '-'
        board[y][x + i] = Tile(False, id, piece)
    elif rotation == 90:
      for i in range(ship_len):
        piece = "^" if i == 0 else "v" if i == ship_len - 1 else '|'
        board[y + i][x] = Tile(False, id, piece)
    self.next_ship_id += 1

  def x_out_of_bounds(self, x):
    return x < 0 or x > self.width - 1

  def y_out_of_bounds(self, y):
    return y < 0 or y > self.height - 1

  def draw_top_ship(self, x, y, offset, color):
    x_pos = self.calc_x(x, offset)
    y_pos = self.calc_y(y)
    offsets = [
      [RECT_SIZE / 2, SHIP_PADDING],
      [SHIP_PADDING, RECT_SIZE - SHIP_PADDING * 2],
      [SHIP_PADDING, RECT_SIZE - 1],
      [RECT_SIZE - 1 - SHIP_PADDING, RECT_SIZE - 1],
      [RECT_SIZE - 1 - SHIP_PADDING, RECT_SIZE - SHIP_PADDING * 2]
    ]
    pygame.draw.polygon(self.display, color, list([x_pos + off_x, y_pos + off_y] for [off_x, off_y] in offsets))

  def draw_vertical_ship(self, x, y, offset, color):
    x_pos = self.calc_x(x, offset)
    y_pos = self.calc_y(y)
    pygame.draw.rect(self.display, color, (x_pos + SHIP_PADDING, y_pos, RECT_SIZE - SHIP_PADDING * 2, RECT_SIZE))

  def draw_btm_ship(self, x, y, offset, color):
    x_pos = self.calc_x(x, offset)
    y_pos = self.calc_y(y)
    offsets = [
      [SHIP_PADDING, 0],
      [RECT_SIZE - 1 - SHIP_PADDING, 0],
      [RECT_SIZE - 1 - SHIP_PADDING, SHIP_PADDING * 2],
      [RECT_SIZE / 2, RECT_SIZE - SHIP_PADDING],
      [SHIP_PADDING, SHIP_PADDING * 2]]
    pygame.draw.polygon(self.display, color, list([x_pos + off_x, y_pos + off_y] for [off_x, off_y] in offsets))

  def draw_right_ship(self, x, y, offset, color):
    x_pos = self.calc_x(x, offset)
    y_pos = self.calc_y(y)
    offsets = [
      [0, SHIP_PADDING],
      [SHIP_PADDING * 2, SHIP_PADDING],
      [RECT_SIZE - 1 - SHIP_PADDING, RECT_SIZE / 2],
      [SHIP_PADDING * 2, RECT_SIZE - 1 - SHIP_PADDING],
      [0, RECT_SIZE - 1 - SHIP_PADDING]
    ]
    pygame.draw.polygon(self.display, color, list([x_pos + off_x, y_pos + off_y] for [off_x, off_y] in offsets))

  def draw_horizontal_ship(self, x, y, offset, color):
    x_pos = self.calc_x(x, offset)
    y_pos = self.calc_y(y)
    pygame.draw.rect(self.display, color, (x_pos, y_pos + SHIP_PADDING, RECT_SIZE, RECT_SIZE - SHIP_PADDING * 2))

  def draw_left_ship(self, x, y, offset, color):
    x_pos = self.calc_x(x, offset)
    y_pos = self.calc_y(y)
    offsets = [
      [RECT_SIZE - SHIP_PADDING * 2, SHIP_PADDING],
      [RECT_SIZE - 1, SHIP_PADDING],
      [RECT_SIZE - 1, RECT_SIZE - SHIP_PADDING - 1],
      [RECT_SIZE - SHIP_PADDING * 2, RECT_SIZE - SHIP_PADDING - 1],
      [SHIP_PADDING, RECT_SIZE / 2]
    ]
    pygame.draw.polygon(self.display, color, list([x_pos + off_x, y_pos + off_y] for [off_x, off_y] in offsets))
