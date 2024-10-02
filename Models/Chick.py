import pygame

from Models.Animal import Animal


class Chick(Animal):
    def __init__(self, x, y, speed, size, color, max_y, min_y, gravity):
        super().__init__(x, y, speed, size, color, max_y, min_y, gravity)
        self.hitbox = pygame.Rect(x, y, size, size)
