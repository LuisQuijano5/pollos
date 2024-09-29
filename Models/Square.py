import pygame

class Square:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.hitbox = pygame.Rect(x, y, size, size)

    def draw(self, surface, camera_x=0):
        # Ajustar la posición en función de la cámara
        draw_x = self.x - camera_x

        # Dibujar el cuadrado
        pygame.draw.rect(surface, self.color, (draw_x, self.y, self.size, self.size))

        # Dibujar la hitbox (un rectángulo rojo transparente)
        hitbox_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(hitbox_surface, (255, 0, 0, 128), (0, 0, self.size, self.size), 2)
        surface.blit(hitbox_surface, (draw_x, self.y))

        # Actualizar la posición del hitbox
        self.hitbox.x = draw_x
        self.hitbox.y = self.y

    def change_color(self, new_color, surface):
        self.color = new_color
        pygame.draw.rect(surface, self.color, self.hitbox)