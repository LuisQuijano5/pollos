import pygame

class Square:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.hitbox = pygame.Rect(x, y, size, size)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.hitbox, 2)

    #Debugging purposes
    def change_color(self, new_color, surface):
        self.color = new_color
        pygame.draw.rect(surface, self.color, self.hitbox, 10)
