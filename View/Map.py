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
        self.screen_rect = pygame.Rect(self.camera_x, self.camera_y, self.screen.get_width(), self.screen.get_height())

    def set_map_surface(self):
        for x in range(0, self.map_width, self.size):
            floor_square = Square(x, 560, self.size, (0, 255, 0))
            ceiling_square = Square(x, 0, self.size, (255, 255, 255))
            floor_square.draw(self.map_surface)
            ceiling_square.draw(self.map_surface)
            self.map_data.append(floor_square)
            self.map_data.append(ceiling_square)
        floor_square = Square(800, 520, self.size, (0, 255, 0))
        floor_square.draw(self.map_surface)
        self.map_data.append(floor_square)
        floor_square = Square(1200, 520, self.size, (0, 255, 0))
        floor_square.draw(self.map_surface)
        self.map_data.append(floor_square)

    def check_for_collisions(self, animal):
        vertical_collision_detected, horizontal_collision_detected = False, False
        for sq in self.map_data:
            if self.screen_rect.colliderect(sq.hitbox):
                # Predictive check for vertical collision
                future_y = animal.hitbox.y
                future_y += animal.gravity

                # build a future hitbox for the chick
                future_chick_hitbox = pygame.Rect(animal.hitbox.x, future_y, animal.hitbox.width, animal.hitbox.height)

                if future_chick_hitbox.colliderect(sq.hitbox):
                    # print(sq.hitbox.bottom, animal.hitbox.top) #debgginh
                    if (not animal.gravity_is_inverted and animal.hitbox.bottom == sq.hitbox.top) or \
                            (animal.gravity_is_inverted and animal.hitbox.top == sq.hitbox.bottom):

                        sq.change_color((0, 0, 0), self.map_surface)
                        animal.collision()
                        vertical_collision_detected = True

                    #  horizontal collision
                    elif animal.hitbox.right > sq.hitbox.left > animal.hitbox.left:
                        sq.change_color((0, 0, 0), self.map_surface)
                        animal.collision()
                        horizontal_collision_detected = True
        return vertical_collision_detected, horizontal_collision_detected

    def scroll(self):
        self.screen.blit(self.map_surface, (-self.camera_x, -self.camera_y))
        self.camera_x += self.scroll_speed
        self.screen_rect = pygame.Rect(self.camera_x, self.camera_y, self.screen.get_width(), self.screen.get_height())

    def setChick(self, chick):
        chick.draw(self.screen, self.camera_x)

    def setSquare(self, sq):
        sq.draw(self.screen)
