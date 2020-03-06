
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
from argparse import ArgumentParser, RawTextHelpFormatter
from battleship import Battleship
import colors
from constants import RECT_MARGIN, RECT_SIZE, SCREEN_PADDING, FONT_SIZE, BOARD_HEIGHT, BOARD_WIDTH, SHIPS, FPS, HINT_FONT_SIZE
from container import AiContainer


parser = ArgumentParser(description="Battleship, defaults can be found in constants.py and colors in colors.py")
parser.add_argument('--ai1', help="File name to the first ai.", dest='ai1', type=str, nargs='?', default=None)
parser.add_argument('--ai2', help="File name to the second ai.", dest='ai2', type=str, nargs='?', default=None)
parser.add_argument('--fps', help="How fast the game should update.", dest='fps', type=int, default=FPS)

args = parser.parse_args()

if not args.ai1 or not args.ai2:
  print("ERROR: You must provide two AIs!")
  exit(1)

ais = [
  AiContainer(args.ai1),
  AiContainer(args.ai2)
]

class Main:
  def __init__(self):
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Battleship')
    icon = pygame.Surface((1, 1))
    icon.fill(colors.MISS)
    pygame.display.set_icon(icon)

    self.width = BOARD_WIDTH
    self.height = BOARD_HEIGHT
    self.size = self.calc_size()
    self.running = True
    self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
    self.clock = pygame.time.Clock()
    self.font = pygame.font.Font('./Roboto-Regular.ttf', FONT_SIZE)
    self.small_font = pygame.font.Font('./Roboto-Regular.ttf', HINT_FONT_SIZE)
    self.game = Battleship(self.display, self.font, self.small_font, self.width, self.height, SHIPS, ais)

  def calc_size(self):
    height = (RECT_SIZE * self.height + (self.height + 1) * RECT_MARGIN) + SCREEN_PADDING * 4
    width = (RECT_SIZE * self.width + (self.width + 1) * RECT_MARGIN) * 2 + SCREEN_PADDING * 6
    return [width, height]

  def on_event(self, event):
    if event.type == pygame.QUIT:
      self.running = False
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
      self.running = False

    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.game.game_ended:
      for ai in ais:
        ai.reset_ai()
      self.game = Battleship(self.display, self.font, self.small_font, self.width, self.height, SHIPS, ais)

  def on_loop(self):
    self.game.run()

    # todo: remove
    if self.game.game_ended:
      for ai in ais:
        ai.reset_ai()
      self.game = Battleship(self.display, self.font, self.small_font, self.width, self.height, SHIPS, ais)

  def on_render(self):
    self.game.draw()
    pygame.display.update()
    self.clock.tick(args.fps)

  def on_cleanup(self):
    pygame.quit()

  def run(self):
    while(self.running):
      for event in pygame.event.get():
        self.on_event(event)
      self.on_loop()
      self.on_render()
    self.on_cleanup()

if __name__ == "__main__":
  main = Main()
  main.run()
