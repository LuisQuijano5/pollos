import pygame
import random

from Models.Square import Square

class Map:

    def __init__(self, screen, camera_x, camera_y, map_width, map_height, scroll_speed, size):
        self.screen = screen
        self.camera_x = camera_x
        self.camera_y = camera_y
        self.scroll_speed = scroll_speed
        self.map_width = map_width
        self.map_height = map_height
        self.size = size
        # Se duplicó el ancho de la superficie del mapa para permitir un scrolling continuo
        self.map_surface = pygame.Surface((self.map_width * 2, self.map_height))
        # Se movió map_data a ser un atributo de instancia
        self.map_data = []
        # Se añadió last_generated_x para rastrear la generación del mapa
        self.last_generated_x = 0
        self.set_map_surface()
        self.visible_distance = screen.get_width() + size * 10  # Distancia visible más un margen

    def set_map_surface(self):
        self.map_surface.fill((100, 150, 255))
        # Llamar a generate_surface en lugar de generar directamente
        self.generate_surface(0, self.map_width * 2)

    # Metodo para generar la superficie del mapa
    def generate_surface(self, start_x, end_x):
        new_objects = []
        for x in range(start_x, end_x, self.size):
            floor_square = Square(x, self.map_height - self.size, self.size, (139, 69, 19))
            ceiling_square = Square(x, 0, self.size, (255, 255, 255))
            floor_square.draw(self.map_surface)
            ceiling_square.draw(self.map_surface)
            new_objects.extend([floor_square, ceiling_square])

            # Generar obstáculos aleatorios
            if random.random() < 0.02:  # 5% de probabilidad
                obstacle_height = 1 * self.size
                obstacle = Square(x, self.map_height - self.size - obstacle_height, self.size, (0, 255, 0))
                obstacle.draw(self.map_surface)
                new_objects.append(obstacle)

        self.map_data.extend(new_objects)
        self.last_generated_x = end_x

    # Se actualizó la lógica de detección de colisiones
    def check_for_collisions(self, animal):
        animal_rect = animal.hitbox.copy()
        animal_rect.x -= self.camera_x
        vcol, hcol = False, False

        for sq in self.map_data:
            if animal_rect.colliderect(sq.hitbox):
                if animal.gravity > 0:  # Caer hacia abajo
                    if animal_rect.bottom > sq.hitbox.top and animal_rect.top < sq.hitbox.top:
                        vcol = True
                else:  # Caer hacia arriba
                    if animal_rect.top < sq.hitbox.bottom and animal_rect.bottom > sq.hitbox.bottom:
                        vcol = True

                # Colisión horizontal
                if animal_rect.right > sq.hitbox.left and animal_rect.left < sq.hitbox.left:
                    hcol = True
                sq.change_color((255, 0, 0), self.map_surface)
        return vcol, hcol

    # Se actualizó scroll para manejar el scrolling continuo
    def scroll(self):
        # Calcular la posición de dibujo
        draw_x = -(self.camera_x % self.map_width)

        # Dibujar el mapa
        self.screen.blit(self.map_surface, (draw_x, -self.camera_y))
        if draw_x > -self.screen.get_width():
            self.screen.blit(self.map_surface, (draw_x + self.map_width, -self.camera_y))

        # Generación continua del mapa
        if self.camera_x + self.screen.get_width() > self.last_generated_x - self.size:
            new_start = self.last_generated_x % self.map_width
            self.generate_surface(new_start, new_start + self.map_width)

        # Dibujar solo los elementos visibles
        for sq in self.map_data:
            if self.camera_x - self.size < sq.x < self.camera_x + self.visible_distance:
                sq.draw(self.screen, self.camera_x)

        self.camera_x += self.scroll_speed

    def setChick(self, chick):
        chick.draw(self.screen, self.camera_x)

    #def setSquare(self, sq):
    #    sq.draw(self.screen)