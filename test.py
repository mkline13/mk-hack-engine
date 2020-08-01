import blessed, time
from types import SimpleNamespace

chars = SimpleNamespace()
chars.DR = chr(9484)
chars.DL = chr(9488)
chars.UR = chr(9492)
chars.UL = chr(9496)
chars.HL = chr(9472)
chars.VL = chr(9474)


term = blessed.Terminal()



class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __add__(self, other):
		if isinstance(other, int):
			return Vector(self.x+other, self.y+other)
		elif isinstance(other, Vector):
			return Vector(self.x+other.x, self.y+other.y)
		elif isinstance(other, tuple) and len(other) == 2:
			return Vector(self.x+other[0], self.y+other[1])

	def __sub__(self, other):
		if isinstance(other, int):
			return Vector(self.x-other, self.y-other)
		elif isinstance(other, Vector):
			return Vector(self.x-other.x, self.y-other.y)
		elif isinstance(other, tuple) and len(other) == 2:
			return Vector(self.x-other[0], self.y-other[1])

	def __repr__(self):
		return self.x, self.y

	def __str__(self):
		return str((self.x, self.y))



class LineTool:
	directions = {
		"up"     : Vector(0,-1),
		"down"   : Vector(0,1),
		"left"   : Vector(0,-1),
		"right"  : Vector(0,1),
	}

	def __init__(self, x, y, d, l, cap=False):
		self._prev = d
		self._draw(x, y, d, l, cap)

	def _draw(self, x, y, d, l, cap):
		xdir, ydir = self.directions[d]
		for i in range(l):
			print(term.move_xy())


a = Vector(0,0)
b = Vector(4,5)

c = a - 5

print(c)
