import pygame
from pygame.examples.cursors import image


class Animal:
    def __init__(self, x, y, speed, width, height, animations, max_y, min_y, gravity):
        self.x = x
        self.y = y
        self.flip = False
        self.animations =  animations
        self.scroll_speed = speed
        self.width = width
        self.height = height
        self.frame_index = 0
        self.update_time= pygame.time.get_ticks()
        self.image = self.animations[self.frame_index]
        self.image= pygame.transform.scale(self.image, (width,height))
        self.hitbox = pygame.Rect(x, y, width, height)
        #self.max_y = max_y
        #self.min_y = min_y
        self.gravity = gravity
        self.gravity_is_inverted = False
        #self.is_falling = False
        self.can_invert = True

    def update(self):
        cooldown_animation= 100
        self.image = self.animations[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
            self.frame_index += 1
            self.update_time= pygame.time.get_ticks()
            if self.frame_index >= len(self.animations):
                self.frame_index = 0

    def draw(self, surface, camera_x):
        draw_x = self.hitbox.x - camera_x
        image_flip = pygame.transform.flip(self.image, False, self.flip)
        surface.blit(image_flip, (draw_x, self.hitbox.y))

    def move(self):
        self.hitbox.x += self.scroll_speed

    def invert_gravity(self):
        if self.can_invert:
            self.gravity_is_inverted = not self.gravity_is_inverted
            self.can_invert = False
            self.gravity = -1 * self.gravity

    def collision(self):
        self.can_invert = True

    def fall(self, map_height):
        self.hitbox.y += self.gravity
        return self.hitbox.y > map_height + self.height or self.hitbox.y < -1 * self.height
