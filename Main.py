import pygame

from Models.Chick import Chick
from Models.Square import Square
from View.Map import Map

if __name__ == '__main__':
    #param definition
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    clock = pygame.time.Clock()
    square_size = 40
    scroll_speed = 4
    camera_x = 0
    camera_y = 0
    map_width = 2000
    map_height = 600
    gravity = 0.5

    #Objects creation
    map_surface = Map(screen, camera_x, camera_y, map_width, map_height, scroll_speed, square_size)
    chick = Chick(400, 300, scroll_speed, square_size, (0, 0, 0),  map_height - square_size, square_size, gravity)
    map_surface.set_map_surface()

    #Game cycle
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    chick.invert_gravity()

        # Handling functionality
        #vcol, hcol = map_surface.check_for_collisions(chick)
        #if not hcol:
        #    chick.move()
        #if not vcol:
        #    chick.fall()

        map_surface.scroll()
        chick.update(map_surface)
        map_surface.setChick(chick)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()