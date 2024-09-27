import pygame
import threading

class Animal:
    def __init__(self, x, y, speed, size, color, max_y, min_y):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.color = color
        self.hitbox = pygame.Rect(x, y, size, size)
        self.max_y = max_y
        self.min_y = min_y
        self.gravity = 10
        self.is_falling = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.hitbox)

    def move(self):
        self.hitbox.x += self.speed

    def invert_gravity(self):
        if not self.is_falling:
            self.is_falling = True
            self.gravity = -1 * self.gravity
            threading.Thread(target=self._fall_thread).start()

    def _fall_thread(self):
        while self.is_falling:
            self.hitbox.y += self.gravity
            if self.hitbox.y <= self.max_y:
                self.hitbox.y = self.max_y
                self.is_falling = False
                break
            elif self.hitbox.y >= self.min_y:
                self.hitbox.y = self.min_y
                self.is_falling = False
                break
            pygame.time.delay(abs(self.speed * 15))
