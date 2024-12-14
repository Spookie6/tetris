from pos import Pos

class Constants:
	RESOLUTION = (1920,1080)
	FONT = None
	TILE_SIZE = 54
	UPDATE_INTERVAL_VERTI = .5 # Tetromino movement interval vertical (- in seconds)
	UPDATE_INTERVAL_HORI = .1 # Tetromino movement interval horizontaly (- in seconds)

	POSSIBLE_TETROMINOS = [
		[Pos(0,0),Pos(0,-1),Pos(0,-2),Pos(0,1), "cyan"], # 4x1
		[Pos(0,0),Pos(0,-1),Pos(0,1),Pos(-1,-1), "blue"], # L-left
		[Pos(0,0),Pos(0,-1),Pos(0,1),Pos(1,1), "orange"], # L-right
		[Pos(0,0),Pos(0,1),Pos(1,0),Pos(1,1), "yellow"], # 2x2
		[Pos(0,0),Pos(1,0),Pos(0,1),Pos(-1,1), "green"], # Z-left
		[Pos(0,0),Pos(-1,0),Pos(0,1),Pos(1,1), "magenta"], # Z-right
		[Pos(0,0),Pos(0,-1),Pos(-1,-1),Pos(1,-1), "red"] # T
	]

	rotations = [Pos(1,1),Pos(1,-1),Pos(-1,-1),Pos(-1,1)]