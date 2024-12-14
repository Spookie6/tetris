import pygame as pg
import random, datetime

from pos import Pos
from constants import Constants

class Tetromino():
	def __init__(self, game, shape):
		self.game = game

		self.original_shape = list(shape[:-1])
		self.shape = list(shape)
		self.color = self.shape.pop()
		self.pos = Pos(4, 5)

		self.rotation_index = 0
		self.last_update_vert = 0
		self.last_update_hori = 0
  
		self.update_extreme_values()
  
	def update(self, keys) -> None:
		now = datetime.datetime.now().timestamp()
  
		self.update_extreme_values()
  
		interval = .05 if keys[pg.K_s] else Constants.UPDATE_INTERVAL_VERTI

		if now - self.last_update_vert >= interval:
			self.last_update_vert = now
			self.pos.y += 1
			if self.extreme_values[1].y == len(self.game.tilemap.tilemap) - 1:
				self.game.tilemap.add_tetromino(self)
				self.game.new_tetromino()

		left = keys[pg.K_a]
		right = keys[pg.K_d]

		if left or right:
			if now - self.last_update_hori >= Constants.UPDATE_INTERVAL_HORI:
				if left and self.extreme_values[0].x <= 0 or right and self.extreme_values[1].x >= len(self.game.tilemap.tilemap[0]) - 1:
					return None
				self.last_update_hori = now
				if keys[pg.K_a]: self.pos.x -= 1
				else: self.pos.x += 1
	
	def rotate(self) -> None:
		if self.color == "yellow": return None
		self.rotation_index += 1
		if self.rotation_index > 3: self.rotation_index = 0
  
		for index, pos in enumerate(self.original_shape):
			if index == 0: continue
			self.shape[index] = pos.multiply(Constants.rotations[self.rotation_index])
			if self.rotation_index == 1 or self.rotation_index == 3: self.shape[index].reverse()
   
		self.update_extreme_values()
	
		if self.extreme_values[0].x < 0:
			self.pos.x += abs(self.extreme_values[0].x)

		if self.extreme_values[1].x > len(self.game.tilemap.tilemap[0]) - 1:
			self.pos.x -= (self.extreme_values[1].x - (len(self.game.tilemap.tilemap[0]) - 1))
   
	def update_extreme_values(self):
		in_tilemap_positions = list(map(lambda pos : pos.add(self.pos), self.shape))
		self.extreme_values = Pos.extreme_values(in_tilemap_positions)

	def random(game) -> object:
		return Tetromino(game, random.choice(Constants.POSSIBLE_TETROMINOS))