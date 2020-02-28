import colors
import pygame
from constants import RECT_MARGIN, RECT_SIZE, SCREEN_PADDING, FONT_SIZE, SHIP_PADDING
from collections import defaultdict
from tile import Tile
import random

class Battleship:
  """Game mechanics class."""

  def __init__(self, display, font, small_font, width, height, ships, ais):
    self.display = display
    self.font = font
    self.small_font = small_font
    self.width = width
    self.height = height

    self.current_turn = random.randint(0,1)
    self.next_turn = (self.current_turn + 1) % 2

    self.ais = ais
    self.ai_boards = [
      [[Tile() for _ in range(self.width)] for _ in range(self.height)],
      [[Tile() for _ in range(self.width)] for _ in range(self.height)]
    ]

    self.game_ended = False
    self.message = ""
    self.hint = ""

    self.next_ship_id = 1
    self.place_ai_ships(ships)


  def place_ai_ships(self, ships):
    for ship_len in ships:
      x, y, rotation = self.ais[self.current_turn].place_ship(ship_len, self.valid_ship_pos)
      if not self.valid_ship_pos(x, y, rotation, ship_len):
        self.message = f"Winner: {self.ais[self.next_turn].name}"
        self.hint = f"{self.ais[self.current_turn].name} placed an invalid ship: (x: {x}, y: {y}, r: {rotation})"
        self.ais[self.next_turn].wins += 1
        self.game_ended = True
        break
      self.place_ship(x, y, ship_len, rotation)

    self.current_turn = (self.current_turn + 1) % 2
    self.next_turn = (self.current_turn + 1) % 2

    for ship_len in ships:
      x, y, rotation = self.ais[self.current_turn].place_ship(ship_len, self.valid_ship_pos)
      if not self.valid_ship_pos(x, y, rotation, ship_len):
        self.message = f"Winner: {self.ais[self.next_turn].name}"
        self.hint = f"{self.ais[self.current_turn].name} placed an invalid ship: (x: {x}, y: {y}, r: {rotation})"
        self.ais[self.next_turn].wins += 1
        self.game_ended = True
        break
      self.place_ship(x, y, ship_len, rotation)

    self.current_turn = (self.current_turn + 1) % 2
    self.next_turn = (self.current_turn + 1) % 2

  def run(self):
    if self.game_ended:
      return

    x, y = self.ais[self.current_turn].get_move()

    if self.x_out_of_bounds(x) or self.y_out_of_bounds(y):
      self.message = f"Winner: {self.ais[self.next_turn].name}"
      self.hint =  f"{self.ais[self.current_turn].name} shot outside the board: (x: {x}, y: {y})"
      self.ais[self.next_turn].wins += 1
      self.game_ended = True
      return

    result = 0
    tile = self.ai_boards[self.next_turn][y][x]

    if tile.hit or tile.miss:
      self.game_ended = True
      self.message = f"Winner: {self.ais[self.next_turn].name}"
      self.hint = f"{self.ais[self.current_turn].name} shot twice on the same coordinate: (x: {x}, y: {y})"
      self.ais[self.next_turn].wins += 1
      return

    if tile.is_ship:
      tile.hit = True
      result = 2 if self.ship_sunk(tile.ship_id) else 1
      if self.all_ships_sunk():
        self.game_ended = True
        self.message = f"Winner: {self.ais[self.current_turn].name}"
        self.ais[self.current_turn].wins += 1
    else:
      self.ai_boards[self.next_turn][y][x].miss = True

    self.ais[self.current_turn].last_result = result

    self.current_turn = (self.current_turn + 1) % 2
    self.next_turn = (self.next_turn + 1) % 2



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
        if self.ai_boards[self.next_turn][y][x].is_ship and not self.ai_boards[self.next_turn][y][x].hit:
          return False
    return True

  def ship_sunk(self, id):
    for x in range(self.width):
      for y in range(self.height):
        if self.ai_boards[self.next_turn][y][x].ship_id == id and not self.ai_boards[self.next_turn][y][x].hit:
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
    self.draw_texts()


  def draw_texts(self):
    self.draw_text(f"Board for: {self.ais[0].name}", SCREEN_PADDING, (SCREEN_PADDING - FONT_SIZE) / 2)
    offset = RECT_SIZE * self.width + (self.width + 1) * RECT_MARGIN + SCREEN_PADDING * 4
    self.draw_text(f"Board for: {self.ais[1].name}", SCREEN_PADDING + offset, (SCREEN_PADDING - FONT_SIZE) / 2)

    middle_y = ((RECT_SIZE * self.height + (self.height + 1) * RECT_MARGIN) + SCREEN_PADDING * 2) / 2 - FONT_SIZE
    self.draw_center_text('vs', middle_y)

    message_y = (RECT_SIZE * self.height + (self.height + 1) * RECT_MARGIN) + SCREEN_PADDING * 3 - FONT_SIZE
    self.draw_center_text(self.message, message_y)

    hint_y = message_y + FONT_SIZE
    self.draw_center_text(self.hint, hint_y, self.small_font)

    wins_y = (RECT_SIZE * self.height + (self.height + 1) * RECT_MARGIN) + SCREEN_PADDING
    self.draw_text(f"Wins: {self.ais[0].wins}", SCREEN_PADDING, wins_y)
    self.draw_text(f"Wins: {self.ais[1].wins}", SCREEN_PADDING + offset, wins_y)


  def draw_text(self, text, x, y, font=None):
    font = self.font if font is None else font
    textsurface = font.render(text, True, colors.TEXT)
    self.display.blit(textsurface, (x, y))

  def draw_center_text(self, text, y, font=None):
    font = self.font if font is None else font
    text = font.render(text, True, colors.TEXT)
    width = (RECT_SIZE * self.width + (self.width + 1) * RECT_MARGIN) * 2 + SCREEN_PADDING * 6
    text_rect = text.get_rect(center=(width/2, y))
    self.display.blit(text, text_rect)


  def calc_x(self, x, offset):
    return x * RECT_SIZE + (x + 1) * RECT_MARGIN + SCREEN_PADDING + offset

  def calc_y(self, y):
    return y * RECT_SIZE + (y + 1) * RECT_MARGIN + SCREEN_PADDING


  def valid_ship_pos(self, x, y, rotation, ship_len):
    board = self.ai_boards[self.current_turn]
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
    board = self.ai_boards[self.current_turn]
    id = self.next_ship_id
    if rotation == 0:
      for i in range(ship_len):
        piece = "<" if i == 0 else ">" if i == ship_len - 1 else '-'
        board[y][x + i] = Tile(id, piece)
    elif rotation == 90:
      for i in range(ship_len):
        piece = "^" if i == 0 else "v" if i == ship_len - 1 else '|'
        board[y + i][x] = Tile(id, piece)
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
