# Example file showing a basic pg "game loop"
import pygame as pg
import random, datetime
from copy import deepcopy

resolution = (1280,720)

resizeScale = resolution[1]/720

# pygame setup
pg.init()
screen = pg.display.set_mode(resolution, pg.NOFRAME)
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
		x = self.x
		self.x = self.y
		self.y = x

class Constants:
	def __init__(self) -> None:
		self.font = pg.font.SysFont("default", 36, bold=False, italic=False)
		self.gridSize = 36 * resizeScale

		self.possibleTetrominos = [
			[Pos(0,0),Pos(0,-1),Pos(0,-2),Pos(0,1), "cyan"], # 4x1
			[Pos(0,0),Pos(0,-1),Pos(0,1),Pos(-1,-1), "blue"], # L-left
			[Pos(0,0),Pos(0,-1),Pos(0,1),Pos(1,1), "orange"], # L-right
			[Pos(0,0),Pos(0,-1),Pos(-1,0),Pos(-1,-1), "yellow"], # 2x2
			[Pos(0,0),Pos(1,0),Pos(0,1),Pos(-1,1), "green"], # Z-left
			[Pos(0,0),Pos(-1,0),Pos(0,1),Pos(1,1), "magenta"], # Z-right
			[Pos(0,0),Pos(0,-1),Pos(-1,-1),Pos(1,-1), "red"] # T
		]
		self.blockSpeed = self.gridSize # pixels/second

		self.rotations = [Pos(1,1),Pos(-1,1),Pos(-1,-1),Pos(-1,1)]

constants = Constants()

class Game:
	def __init__(self,) -> None:
		self.playField = [constants.gridSize*10, constants.gridSize*20]
		w, h = self.playField
		self.rect = pg.Rect(resolution[0]/2 - w/2, 0, w, h)
		self.player = None
		self.hasStarted = False
		self.gameOver = False

		self.upcoming = []

		self.tetrominos = []
		self.activeTetromino = None
  
	def draw(self, screen) -> None:
		pg.draw.rect(screen, "black", self.rect)

class Block:
		def __init__(self, pos) -> None:
			self.rect = pg.Rect(pos.x,pos.y,constants.gridSize, constants.gridSize)
		def draw(self, screen, color) -> None:
			pg.draw.rect(screen, color, self.rect)
   
class Tetromino:
	def __init__(self, shape) -> None:
		self.shape = list(shape)
		self.shapeIndex = constants.possibleTetrominos.index(shape)
		self.color = self.shape.pop()
  
		xValues = list(map(lambda el : el.x, list(self.shape)))
		self.minX = min(xValues)
		self.maxX = max(xValues)
  
		yValues = list(map(lambda el : el.y, list(self.shape)))
		self.minY = min(yValues)
		self.maxY = max(yValues)
  
		self.pos = Pos(game.rect[0] + constants.gridSize*5, -1*(self.maxY + 1)*constants.gridSize)
		# self.pos = Pos(game.rect[0] + constants.gridSize*5, constants.gridSize*2)
  
		self.last_move_y = datetime.datetime.now().timestamp()
		self.last_move_x = datetime.datetime.now().timestamp()
		self.rotationIndex = 0

	def draw(self, screen):
		for pos in self.shape:
			blockPos = Pos(pos.x * constants.gridSize + self.pos.x, pos.y * constants.gridSize + self.pos.y)
			block = Block(blockPos)
			block.draw(screen, self.color)
   
	def rotate(self, direction) -> None:
		if self.shapeIndex == 3: return

		self.rotationIndex += 1
		if self.rotationIndex == 4: self.rotationIndex = 0
	
		if direction == 0:
			for pos in self.shape:
				x, y = pos.getTuple()
				pos.x = y
				pos.y = -1 * x
		if direction == 1:
			for pos in self.shape:
				x, y = pos.getTuple()
				pos.x = -1 * y
				pos.y = x
   
		xValues = list(map(lambda el : el.x, list(self.shape)))
		self.minX = min(xValues)
		self.maxX = max(xValues)
  
		if self.pos.x + self.minX * constants.gridSize < game.rect[0]:
			self.pos.x = game.rect[0] + abs(self.minX * 36)
			print("WALL KICK")
   
		if self.pos.x + self.maxX * constants.gridSize + 36 > game.rect[0] + game.rect[2]:
			self.pos.x = game.rect[0] + game.rect[2] + (abs(self.maxX * 36) * -1) - 36
			print("WALL KICK")
   
	def move(self, keys):
		now_y = datetime.datetime.now().timestamp()
		now_x = datetime.datetime.now().timestamp()
  
		interval = .05 if keys[pg.K_s] else 1
  
		yValues = list(map(lambda el : el.y, list(self.shape)))
		self.minY = min(yValues)
		self.maxY = max(yValues)
  
		# lowest_y = []
		# if len(game.tetrominos) == 0:
		# 	lowest_y = game.rect[3]
		# else:
		# 	for tetros in game.tetrominos:
		# 		pass
			# tetros = filter(lambda x: x.pos.x , game.tetrominos)
  
		# Vertical movement
		if now_y - self.last_move_y >= interval:
			self.pos.y += constants.blockSpeed
			if self.pos.y + constants.gridSize + self.maxY * constants.gridSize >= game.rect[3]:
				game.tetrominos.append(deepcopy(game.activeTetromino))
				game.activeTetromino = Tetromino.random()
			self.last_move_y = now_y

		# Horizontal movement
		if now_x - self.last_move_x >= .05:
			if keys[pg.K_a] or keys[pg.K_LEFT]:
				if not (self.pos.x + self.minX * constants.gridSize <= game.rect[0]):
					self.pos.x -= constants.gridSize
					self.last_move_x = now_x
			if keys[pg.K_d] or keys[pg.K_RIGHT]:
				if not (self.pos.x + (self.maxX + 1) * constants.gridSize >= game.rect[0] + game.rect[2]):
					self.pos.x += constants.gridSize
					self.last_move_x = now_x

	def random(): return Tetromino(random.choice(constants.possibleTetrominos))

game = Game()
tetro = Tetromino.random()
game.activeTetromino = tetro
game.upcoming = [3*(Tetromino.random())]
print(game.upcoming)
# game.tetrominos.append(tetro)

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
				if game.activeTetromino is not None:
					game.activeTetromino.rotate(0)		
			if keys[pg.K_SPACE]:
				pass
    
	# fill the screen with a color to wipe away anything from last frame
	screen.fill("black")
 
	# RENDER YOUR GAME HERE
	game.draw(screen)
 
	for tetro in game.tetrominos:
		tetro.draw(screen)
 
	game.activeTetromino.move(keys)
	game.activeTetromino.draw(screen)
  

	for i in range(0,20):
		pg.draw.line(screen, "black", (0,constants.gridSize*i), (resolution[0], constants.gridSize*i))
	for i in range(0,10):
		pg.draw.line(screen, "black", (game.rect[0] + constants.gridSize*i, 0), (game.rect[0] + constants.gridSize*i, resolution[1]))
 
	pg.draw.line(screen, "White", (game.rect[0], 0), (game.rect[0], resolution[1]))
	pg.draw.line(screen, "White", (game.rect[0] + game.rect[2], 0), (game.rect[0] + game.rect[2], resolution[1]))
	# flip() the display to put your work on screen
	pg.display.flip()

	dt = clock.tick(60) / 1000  # limits FPS to 60

pg.quit()
