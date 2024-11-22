import random
from Models.Square import Square

class Platform:
    def __init__(self, map_height, size, x, y, width):
        self.width = width
        self.map_height = map_height
        self.size = size
        self.y = y
        self.x = x

    def draw(self, map_surface, map_data):
        for i in range(self.width):
            print(self.x)
            obstacle = Square(self.x + (i * self.size), self.y, self.size, (0, 255, 0))
            obstacle.draw(map_surface)
            map_data.append(obstacle)
