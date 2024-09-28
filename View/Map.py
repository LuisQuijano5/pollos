import pygame

from Models.Square import Square


class Map:
    map_data = []

    def __init__(self, screen, camera_x, camera_y, map_width, map_height, scroll_speed, size):
        self.screen = screen
        self.camera_x = camera_x
        self.camera_y = camera_y
        self.scroll_speed = scroll_speed
        self.map_width = map_width
        self.map_height = map_height
        self.size = size
        self.map_surface = pygame.Surface((self.map_width, self.map_height))
        self.map_surface.fill((100, 150, 255))

    def set_map_surface(self):
        for x in range(0, self.map_width, self.size):
            floor_square = Square(x, 560, self.size, (0, 255, 0))
            ceiling_square = Square(x, 0, self.size, (255, 255, 255))
            floor_square.draw(self.map_surface)
            ceiling_square.draw(self.map_surface)
            self.map_data.append(floor_square)
            self.map_data.append(ceiling_square)

    def check_for_collisions(self, chick):
        screen_rect = pygame.Rect(self.camera_x, self.camera_y, self.screen.get_width(), self.screen.get_height())
        collision_detected = False
        for sq in self.map_data:
            if screen_rect.colliderect(sq.hitbox):
                if chick.hitbox.colliderect(sq.hitbox):
                    if (not chick.gravity_is_inverted and sq.hitbox.top <= chick.hitbox.bottom < sq.hitbox.bottom) or \
                            (chick.gravity_is_inverted and sq.hitbox.bottom >= chick.hitbox.top > sq.hitbox.top):
                        sq.change_color((0, 0, 0), self.map_surface)
                        chick.vertical_collision()
                        collision_detected = True
                        break
        return collision_detected

    def refreshForeground(self):
        self.screen.blit(self.map_surface, (-self.camera_x, -self.camera_y))
        self.camera_x += self.scroll_speed

    def setChick(self, chick):
        chick.draw(self.screen, self.camera_x)

    def setSquare(self, sq):
        sq.draw(self.screen)
