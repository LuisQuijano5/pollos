import pygame


class Animal:
    def __init__(self, x, y, speed, size, color, max_y, min_y, gravity):
        self.x = x
        self.y = y
        self.scroll_speed = speed
        self.size = size
        self.color = color
        self.hitbox = pygame.Rect(x, y, size, size)
        # self.max_y = max_y
        # self.min_y = min_y
        self.gravity = gravity
        self.gravity_is_inverted = False
        # self.is_falling = False
        self.can_invert = True

    def draw(self, surface, camera_x):
        draw_x = self.hitbox.x - camera_x
        pygame.draw.rect(surface, self.color, (draw_x, self.hitbox.y, self.size, self.size))

    def move(self):
        self.hitbox.x += self.scroll_speed

    def invert_gravity(self):
        if self.can_invert:
            self.gravity_is_inverted = not self.gravity_is_inverted
            self.can_invert = False
            self.gravity = -1 * self.gravity

    def collision(self):
        self.can_invert = True

    def fall(self):
        self.hitbox.y += self.gravity
