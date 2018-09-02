class Object:
	def __init__(self, layer=3):
		self.layer = layer
		self.objects = []
		self.x = 0
		self.y = 0
		pass

	def reset(self):
		self.objects = []

	def move(self, x, y):
		self.x, self.y = x, y

	def add_object(self, obj):
		self.objects.append(obj)

	def draw(self, rewind):
		for obj in self.objects:
			obj.draw(rewind)
		pass
