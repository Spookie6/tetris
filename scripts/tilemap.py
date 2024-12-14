import pygame as pg

from pos import Pos

class Tile():
	def __init__(self, pos):
		self.pos = pos
		self.type = 0 # 0: empty, 1: tetromino block
		self.color = "lightgray"

class Tilemap():
	def __init__(self, game, tile_size=54):
		self.game = game
		self.tile_size = tile_size
		self.tilemap = [[Tile(Pos(i, j)) for i in range(10)] for j in range(20)]
  
	def render(self, surf):
		for row in self.tilemap:
			for tile in row:
				pg.draw.rect(surf, tile.color, pg.Rect(tile.pos.x * self.tile_size + self.game.rect.left + 1, tile.pos.y * self.tile_size + self.game.rect.top + 1, self.tile_size - 2, self.tile_size - 2))
	
	def getVertical(self, y):
		all_tiles = {x for xs in self.tilemap for x in xs}
		return list(filter(lambda x : x.pos.y == y, all_tiles))

	def render_tetromino(self, surf):
		for pos in self.game.tetromino.shape:
			x, y = self.game.tetromino.pos.add(pos).getTuple()
			pg.draw.rect(surf, self.game.tetromino.color, pg.Rect(x * self.tile_size + self.game.rect.left + 1, y * self.tile_size + self.game.rect.top + 1, self.tile_size - 2, self.tile_size - 2))
   
	def full_row(self, row):
		del self.tilemap[row]
		self.tilemap.insert(0, [Tile(Pos(i, 0)) for i in range(10)])
  
	def add_tetromino(self, tetro):
		for pos in tetro.shape:
			self.tilemap[pos.y][pos.x].id = 1
			self.tilemap[pos.y][pos.x].color = tetro.color
  
if __name__ == "__main__":
	print(Tilemap(None).__dict__.get("tilemap")[0][2].pos.getTuple())