# Tetris, YAY!
import pygame as pg
import sys

from pos import Pos
from tilemap import Tilemap, Tile
from tetromino import Tetromino
from constants import Constants

class Game():
	def __init__(self):
		pg.init()

		Constants.FONT = pg.font.Font("RetroFont.ttf", 32)

		pg.display.set_caption("Tetris")
		self.screen = pg.display.set_mode((1280, 720), pg.SHOWN, display=0)
		self.display = pg.Surface(Constants.RESOLUTION)
  
		self.clock = pg.time.Clock()
  
		self.running = True
  
		self.assets = {}
  
		w, h = (10*Constants.TILE_SIZE, 20*Constants.TILE_SIZE)
		self.rect = pg.Rect(Constants.RESOLUTION[0]/2 - w/2, Constants.RESOLUTION[1]/2 - h/2, w, h)
  
		self.tilemap = Tilemap(self, Constants.TILE_SIZE)
		
		self.tetromino = Tetromino.random(self)
  
	def run(self):
		while self.running:
			keys = pg.key.get_pressed()

			if keys[pg.K_ESCAPE]:
				pg.quit()
				sys.exit()

			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.running = False
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_w:
						self.tetromino.rotate()
			
			self.display.fill("black")
		
			self.tetromino.update(keys)
			
			pg.draw.rect(self.display, pg.Color("gray2"), self.rect)
			self.tilemap.render(self.display)
	
			self.tilemap.render_tetromino(self.display)
 
			disp = pg.transform.scale(self.display, (1280, 720))
			self.screen.blit(disp, (0, 0))
 
			pg.display.flip()

			dt = self.clock.tick(60) / 1000  # limits FPS to 60

	def render(self):
		pg.draw.rect(self.display, pg.Color("gray2"), self.rect)
		self.tilemap.render(self.display)

		# Line surrounding the gameboard
		# x, y, w, h, = self.rect
		# pg.draw.line(self.display, pg.Color("gray6"), (x - 1, y), (x - 1, h), width=4)
		# pg.draw.line(self.display, pg.Color("gray6"), (x + w + 1, y), (x + w + 1, h), width=4)
  
	def new_tetromino(self):
		self.tetromino = Tetromino.random(self)

if __name__ == "__main__": 
	game = Game()
	game.run()