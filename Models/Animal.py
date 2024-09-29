import pygame

class Animal:
    def __init__(self, x, y, speed, size, color, max_y, min_y, gravity):
        self.x = x
        self.y = y
        self.scroll_speed = speed
        self.size = size
        self.color = color
        self.hitbox = pygame.Rect(x, y, size, size)
        # Se descomentaron max_y y min_y para usarlos en la lógica de colisiones
        self.max_y = max_y
        self.min_y = min_y
        self.gravity = gravity
        # Se añadió velocity_y para manejar la velocidad vertical
        self.velocity_y = 0
        self.gravity_is_inverted = False
        self.can_invert = True

    def draw(self, surface, camera_x):
        draw_x = self.hitbox.x - camera_x
        pygame.draw.rect(surface, self.color, (draw_x, self.hitbox.y, self.size, self.size))

    def move(self):
        self.hitbox.x += self.scroll_speed

    def invert_gravity(self):
        if self.can_invert:
            self.gravity_is_inverted = not self.gravity_is_inverted
            # Se simplificó la inversión de la gravedad
            self.gravity = -self.gravity
            # Se reinicia la velocidad vertical al invertir la gravedad
            self.velocity_y = 0
            self.can_invert = False
        # if not self.is_falling:
        #     self.is_falling = True
        #     self.can_invert = False
        #     self.gravity = -1 * self.gravity
        #     threading.Thread(target=self._fall_thread).start()

    def collision(self):
        #Se reinicia la velocidad vertical en colisiones
        self.velocity_y = 0
        self.can_invert = True

    def fall(self):
        # Se implementó una física más realista
        self.velocity_y += self.gravity
        self.hitbox.y += self.velocity_y

        # Se añadió lógica para manejar colisiones con los límites superior e inferior
        if self.hitbox.top < self.min_y:
            self.hitbox.top = self.min_y
            self.collision()
        elif self.hitbox.bottom > self.max_y:
            self.hitbox.bottom = self.max_y
            self.collision()
        # while self.is_falling:
        #     self.hitbox.y += self.gravity
        #     if self.hitbox.y <= self.max_y:
        #         self.hitbox.y = self.max_y
        #         self.is_falling = False
        #         break
        #     elif self.hitbox.y >= self.min_y:
        #         self.hitbox.y = self.min_y
        #         self.is_falling = False
        #         break
        #     pygame.time.delay(20)

    # Se añadió un metodo update para manejar toda la lógica de actualización
    def update(self, map_surface):
        self.move()
        self.fall()
        if map_surface.check_for_collisions(self):
            self.collision()