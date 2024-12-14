# Example file showing a basic pg "game loop"
import pygame as pg
import random, datetime
from collections.abc import Iterable

resolution = (1280,720)

resizeScale = resolution[1]/720

# pygame setup
pg.init()
screen:pg.Surface = pg.display.set_mode(resolution, pg.SHOWN)
pg.display.set_caption("Tetris")
clock = pg.time.Clock()
running = True
dt = 0

class Pos:
	def __init__(self, x, y) -> None:
		self.x = x
		self.y = y

	def getTuple(self) -> tuple:
		return (self.x, self.y)

	def reverse(self):
		self.y, self.x = self.getTuple()
  
	def __eq__(self, other) -> bool:
		return self.getTuple() == other.getTuple()

	def add(self, other) -> object:
		return Pos(self.x + other.x, self.y + other.y)

	def multiply(self, other) -> object:
		return Pos(self.x * other.x, self.y * other.y)

	def extremeValues(positions:Iterable):
		xValues, yValues = Pos.uniqueValues(positions)
		return (Pos(max(xValues), max(yValues)), Pos(min(xValues), min(yValues)))

	def uniqueValues(positions:Iterable):
		xValues =  set(map(lambda pos : pos.x, positions))
		yValues =  set(map(lambda pos : pos.y, positions))
		return (xValues, yValues)

class Constants:
	def __init__(self) -> None:
		self.font = pg.font.Font("RetroFont.ttf", 32)
		self.gridSize = 36 * resizeScale
		self.updateInvervalVerti = .5 # Tetromino movement interval vertical (- in seconds)
		self.updateInvervalHori = .1 # Tetromino movement interval horizontaly (- in seconds)

		self.possibleTetrominos = [
			[Pos(0,0),Pos(0,-1),Pos(0,-2),Pos(0,1), "cyan"], # 4x1
			[Pos(0,0),Pos(0,-1),Pos(0,1),Pos(-1,-1), "blue"], # L-left
			[Pos(0,0),Pos(0,-1),Pos(0,1),Pos(1,1), "orange"], # L-right
			[Pos(0,0),Pos(0,1),Pos(1,0),Pos(1,1), "yellow"], # 2x2
			[Pos(0,0),Pos(1,0),Pos(0,1),Pos(-1,1), "green"], # Z-left
			[Pos(0,0),Pos(-1,0),Pos(0,1),Pos(1,1), "magenta"], # Z-right
			[Pos(0,0),Pos(0,-1),Pos(-1,-1),Pos(1,-1), "red"] # T
		]

		self.rotations = [Pos(1,1),Pos(1,-1),Pos(-1,-1),Pos(-1,1)]

constants = Constants()

class Tile():
	def __init__(self):
		self.id = 0 # 0: empty, 1: tetromino block
		self.color = "gray5"

class Game():
	def __init__(self):
		self.gameOver = False
		w, h = (10*constants.gridSize, 20*constants.gridSize)
		self.rect = pg.Rect(resolution[0]/2 - w/2, resolution[1]/2 - h/2, w, h)
		self.grid = [[Tile() for i in range(10)] for j in range(20)]
  
		self.tetrominos = []
	
	def update(self):
		# Reset game board
		self.grid = [[Tile() for i in range(10)] for j in range(20)]

		# Update tetrominos positions
		for tetromino in self.tetrominos:
			tetromino.update()
		self.tetrominos[0].move()		

		# Check for full rows
			# If so, remove row and update tetrominos positions again
		# Draw tetrominos
  
		self.draw()

	def draw(self):
		pg.draw.rect(screen, pg.Color("gray2"), self.rect)
		gs = constants.gridSize
		for i, row in enumerate(self.grid):
			for j, tile in enumerate(row):
				rect = pg.Rect(self.rect[0] + gs * j + 1, self.rect[1] + gs * i + 1, gs - 2, gs - 2)
				pg.draw.rect(screen, pg.Color(tile.color), rect)

		# Line surrounding the gameboard
		x, y, w, h, = self.rect
		pg.draw.line(screen, pg.Color("white"), (x - 1, y), (x - 1, h))
		pg.draw.line(screen, pg.Color("white"), (x + w + 1, y), (x + w + 1, h))

class Tetromino():
	def __init__(self, shape):
		self.originalShape = list(shape[:-1])
		self.shape = list(shape)
		self.color = self.shape.pop()
		self.pos = Pos(4, 5)

		self.rotationIndex = 0
		self.lastUpdateVert = 0
		self.lastUpdateHori = 0

	def update(self):
		self.draw()
  
	def draw(self):
		for pos in self.shape:
			x, y = self.pos.add(pos).getTuple()
			try:
				game.grid[y][x].id = 1
				game.grid[y][x].color = self.color
			except: pass
	
	def rotate(self) -> None:
		if self.color == "yellow": return None
		self.rotationIndex += 1
		if self.rotationIndex > 3: self.rotationIndex = 0
  
		for index, pos in enumerate(self.originalShape):
			if index == 0: continue
			self.shape[index] = pos.multiply(constants.rotations[self.rotationIndex])
			if self.rotationIndex == 1 or self.rotationIndex == 3: self.shape[index].reverse()

	def move(self) -> None:
		now = datetime.datetime.now().timestamp()
		interval = .05 if keys[pg.K_s] else constants.updateInvervalVerti
		if now - self.lastUpdateVert >= interval:
			self.lastUpdateVert = now
			self.pos.y += 1
			if self.pos.y >= len(game.grid):
				game.tetrominos.insert(0, Tetromino.random())

		if keys[pg.K_a] or keys[pg.K_d]:
			if now - self.lastUpdateHori >= constants.updateInvervalHori:
				self.lastUpdateHori = now
				if keys[pg.K_a]: self.pos.x -= 1
				else: self.pos.x += 1

	def random() -> object:
		return Tetromino(random.choice(constants.possibleTetrominos))

game = Game()
game.tetrominos.insert(0, Tetromino(constants.possibleTetrominos[1]))

while running:
	# poll for events
	# pg.QUIT event means the user clicked X to close your window
	for event in pg.event.get():
		keys = pg.key.get_pressed()
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if keys[pg.K_ESCAPE]:
				pg.quit()
			if keys[pg.K_w]:
				game.tetrominos[0].rotate()
	
	# fill the screen with a color to wipe away anything from last frame
	screen.fill("black")
 
	# RENDER YOUR GAME HERE
	game.update()

	# flip() the display to put your work on screen
	pg.display.flip()

	dt = clock.tick(60) / 1000  # limits FPS to 60

pg.quit()
