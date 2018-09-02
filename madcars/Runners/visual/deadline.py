from object import Object

class Deadline(Object):
	def __init__(self, level, layer=4):
		Object.__init__(self, layer)
		self.level = level

	def draw(self, rewind):
		rewind.line(0, self.level,
			1200, self.level,
			0x000000, self.layer)
