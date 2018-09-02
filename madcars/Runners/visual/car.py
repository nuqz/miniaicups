import math
from object import Object

def rotate_point(point, angle):
	ln = math.sqrt(point[0] ** 2 + point[1] ** 2)
	ang = math.acos(point[0] / ln)
	return [
		ln * math.cos(ang + angle),
		ln * math.sin(ang + angle)
	]


class Wheel(Object):
	def __init__(self, pos, radius, layer=2):
		Object.__init__(self, layer)
		self.type = "round"
		self.radius = radius
		self.angle = 0
		self.x, self.y = pos[0], pos[1]

	def update(self, data):
		self.x, self.y, self.angle = data

	def draw(self, rewind):
		rewind.circle(self.x, self.y, self.radius, 0xFF0000, self.layer)
		rewind.line(
			self.x, self.y,
			self.x + math.cos(self.angle)*self.radius,
			self.y + math.sin(self.angle)*self.radius,
			0x000000, self.layer)

class Body(Object):
	def __init__(self, points, layer=2, spawn=1):
		Object.__init__(self, layer)
		self.spawn = spawn
		self.lines = []
		self.angle = 0
		for i in range(len(points)):
			self.lines.append([points[i-1], points[i]])

	def update(self, x, y, angle, spawn):
		self.x = x
		self.y = y
		self.angle = angle
		self.spawn = spawn

	def draw(self, rewind):
		for (start, end) in self.lines:
			start = rotate_point(start, self.angle*self.spawn)
			end = rotate_point(end, self.angle*self.spawn)
			rewind.line(
				self.x + start[0] * self.spawn,
				self.y + start[1],
				self.x + end[0] * self.spawn,
				self.y + end[1],
				0x0eFF0e, self.layer)

class Car(Object):
	def __init__(self, proto_car, spawn=1):
		Object.__init__(self)
		self.proto_car = proto_car
		self.angle = 0
		self.spawn = spawn
		self.body = Body(proto_car["car_body_poly"], spawn=self.spawn)
		self.button = Body(proto_car["button_poly"], layer=3, spawn=self.spawn)
		self.front_wheel = Wheel(proto_car["front_wheel_position"],
			proto_car["front_wheel_radius"])
		self.rear_wheel = Wheel(proto_car["rear_wheel_position"],
			proto_car["rear_wheel_radius"])

	def update(self, data):
		self.x, self.y = data[0]
		self.angle = data[1]
		self.spawn = data[2]
		self.body.update(self.x, self.y, self.angle, self.spawn)
		self.button.update(self.x, self.y, self.angle, self.spawn)
		self.front_wheel.update(data[3])
		self.rear_wheel.update(data[4])

	def draw(self, rewind):
		self.reset()
		self.objects = [self.body, self.button, self.front_wheel, self.rear_wheel]
		Object.draw(self, rewind)
