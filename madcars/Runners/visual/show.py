#!/usr/bin/env python3
import gzip
import sys
import json
import math

from rewind import RewindClient
from object import Object
from deadline import Deadline
from car import Car
from map import Map

class Visualizer(Object):
	def __init__(self):
		self.map = None
		self.player1 = None
		self.player2 = None
		self.deadline = None

	def set_map(self, map):
		self.map = map

	def set_cars(self, car_left, car_right):
		self.player1 = car_left
		self.player2 = car_right

	def set_deadline(self, deadline):
		self.deadline = deadline

	def draw(self, rewind):
		for obj in [self.map, self.player1, self.player2, self.deadline]:
			if obj != None:
				self.objects.append(obj)

		Object.draw(self, rewind)
		rewind.end_frame()
		return

if __name__ == '__main__':
	rewind = RewindClient()
	visualizer = Visualizer()

	with gzip.open(sys.argv[1], 'r') as f:
		log = json.loads(f.read().decode('utf-8'))
		m = None
		for msg in log["visio_info"]:
			visualizer.reset()

			if msg["type"] == "new_match":
				m = Map(msg["params"]["proto_map"], layer=1)
				car_left = Car(msg["params"]["proto_car"])
				car_right = Car(msg["params"]["proto_car"], spawn=-1)
				visualizer.set_map(m)
				visualizer.set_cars(car_left, car_right)
			elif msg["type"] == "end_game":
				print("END")
			else:
				visualizer.set_deadline(Deadline(msg["params"]["deadline_position"]))
				visualizer.player1.update(msg["params"]["cars"]["1"])
				visualizer.player2.update(msg["params"]["cars"]["2"])

			visualizer.draw(rewind)

	rewind.close()

