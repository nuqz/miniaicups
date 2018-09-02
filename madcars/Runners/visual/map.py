import math
from object import Object

# map_id: [points]
maps = {}

class Map(Object):
    def __init__(self, proto_map, layer=1):
        Object.__init__(self, layer)
        global maps
        if proto_map["external_id"] in maps:
            self.points = maps[proto_map["external_id"]]
            return
        points = []
        for (start, end, width) in proto_map["segments"]:
            bigdx = end[0] - start[0]
            bigdy = end[1] - start[1]
            segment_len = math.sqrt((bigdx) ** 2 + (bigdy) ** 2)
            gamma = math.acos(bigdx / segment_len)
            dy = math.cos(gamma) * width
            dx = math.sin(gamma) * width
            points.append([
                    [start[0] - dx, start[1] - dy],
                    [end[0] - dx, end[1] - dy]
                ])
            points.append([
                    [start[0] + dx, start[1] + dy],
                    [end[0] + dx, end[1] + dy]
                ])
        maps[proto_map["external_id"]] = points
        self.points = points

    def draw(self, rewind):
        for (start, end) in self.points:
            rewind.line(start[0], start[1], end[0], end[1], 0x0000FF, self.layer)