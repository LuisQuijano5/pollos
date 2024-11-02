import pygame
import random
from Models.Square import Square


class Map:
    map_data = []

    def __init__(self, screen, camera_x, camera_y, map_width, map_height, scroll_speed, size):
        self.screen = screen
        self.camera_x = camera_x
        self.camera_y = camera_y
        self.scroll_speed = scroll_speed
        self.map_width = (map_width // size) * size
        self.map_height = (map_height // size) * size
        self.size = size

        # Cargar las capas de nubes para el fondo
        self.cloud_layers = [pygame.image.load(f"assets/Clouds/{i + 1}.png").convert_alpha()
            for i in range(4)]

        # Ajustar el tamaño de las imágenes al tamaño de la pantalla
        self.cloud_layers = [pygame.transform.scale(img, (screen.get_width(), screen.get_height()))
            for img in self.cloud_layers]

        self.cloud_positions = [0] * len(self.cloud_layers)

        self.map_surface = pygame.Surface((self.map_width * 2, self.map_height), pygame.SRCALPHA)
        self.screen_rect = pygame.Rect(self.camera_x, self.camera_y, self.screen.get_width(), self.screen.get_height())
        self.map_data = []

    def generate_blocks(self, x):
        x = (x // self.size) * self.size

        floor_square = Square(x, self.map_height - self.size, self.size, (139, 69, 19))
        ceiling_square = Square(x, 0, self.size, (255, 255, 255))
        floor_square.draw(self.map_surface)
        ceiling_square.draw(self.map_surface)
        self.map_data.append(floor_square)
        self.map_data.append(ceiling_square)

        if random.random() < 0.4:  # 40% de probabilidad
            obstacle_height = random.randint(1, self.map_height // self.size - 2) * self.size
            obstacle = Square(x, self.map_height - self.size - obstacle_height, self.size, (0, 255, 0))
            obstacle.draw(self.map_surface)
            self.map_data.append(obstacle)

    def set_map_surface(self):
        for x in range(0, self.map_width * 2, self.size):
            self.generate_blocks(x)

    def draw_background(self):
        # Dibujar cada capa de nubes con parallax
        for i, cloud in enumerate(self.cloud_layers):
            # Las capas más profundas se mueven más lento
            parallax_speed = self.scroll_speed * (i + 1) * 0.2

            # Actualizar posición
            self.cloud_positions[i] -= parallax_speed

            # Reiniciar posición si la imagen sale de la pantalla
            if self.cloud_positions[i] <= -cloud.get_width():
                self.cloud_positions[i] = 0

            # Dibujar la capa actual y su repetición
            self.screen.blit(cloud, (self.cloud_positions[i], 0))
            self.screen.blit(cloud, (self.cloud_positions[i] + cloud.get_width(), 0))

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
                    if (not animal.gravity_is_inverted and animal.hitbox.bottom == sq.hitbox.top) or \
                            (animal.gravity_is_inverted and animal.hitbox.top == sq.hitbox.bottom):
                        animal.collision()
                        vertical_collision_detected = True

                    # horizontal collision
                    elif animal.hitbox.right > sq.hitbox.left > animal.hitbox.left:
                        animal.collision()
                        horizontal_collision_detected = True

        return vertical_collision_detected, horizontal_collision_detected

    def scroll(self):
        # Dibujar fondo
        self.draw_background()

        self.screen.blit(self.map_surface, (-self.camera_x, -self.camera_y))
        self.camera_x += self.scroll_speed
        self.screen_rect = pygame.Rect(self.camera_x, self.camera_y, self.screen.get_width(), self.screen.get_height())

        # Verificar si necesitamos extender el mapa
        if self.camera_x + self.screen.get_width() >= self.map_surface.get_width() - self.map_width:
            # Extender la superficie del mapa agregando más terreno
            new_width = self.map_surface.get_width() + self.map_width
            new_surface = pygame.Surface((new_width, self.map_height), pygame.SRCALPHA)

            new_surface.blit(self.map_surface, (0, 0))
            self.map_surface = new_surface

            # Calcular la posición inicial correcta para los nuevos bloques
            start_x = (new_width - self.map_width) // self.size * self.size

            # Generar nuevos bloques para el terreno extendido
            for x in range(start_x, new_width, self.size):
                self.generate_blocks(x)

    def setChicken(self, animal):
        animal.update()
        animal.draw(self.screen, self.camera_x)

    def setPerry(self, animal):
        animal.update()
        animal.draw(self.screen, self.camera_x)

    def setSquare(self, sq):
        sq.draw(self.screen)