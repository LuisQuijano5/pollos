import random
from Models.Square import Square


class Column:
    def __init__(self, map_height, size, x, y, height):
        self.height = height
        self.map_height = map_height
        self.size = size
        self.y = y
        self.x = x

    def draw(self, map_surface, map_data):
        for i in range(self.height):
            if self.y - (i * self.size) == 0:
                continue
            obstacle = Square(self.x, self.y - (i * self.size), self.size, (0, 255, 0))
            obstacle.draw(map_surface)
            map_data.append(obstacle)