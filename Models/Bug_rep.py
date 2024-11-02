from Models.Square import Square


class Bug_rep():
    def __init__(self, map_height, size, x, y):
        self.width = 0
        self.map_height = map_height
        self.size = size
        self.y = y
        self.x = x

    def draw(self, map_surface, map_data):
        obstacle = Square(self.x, self.map_height - 150, 50, (255, 255, 255))
        obstacle.draw(map_surface)
        map_data.append(obstacle)
        obstacle = Square(self.x + 150, self.map_height - 100, 50, (255, 255, 255))
        obstacle.draw(map_surface)
        map_data.append(obstacle)