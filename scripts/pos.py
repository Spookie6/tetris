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

	def extreme_values(positions):
		xValues, yValues = Pos.unique_values(positions)
		return (Pos(min(xValues), min(yValues)), Pos(max(xValues), max(yValues)))

	def unique_values(positions):
		xValues =  set(map(lambda pos : pos.x, positions))
		yValues =  set(map(lambda pos : pos.y, positions))
		return (xValues, yValues)