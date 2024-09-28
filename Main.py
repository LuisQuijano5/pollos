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
    gravity = 10

    #Objects creation
    map_surface = Map(screen, camera_x, camera_y, map_width, map_height, scroll_speed, square_size)
    chick = Chick(400, 300, scroll_speed, square_size, (0, 0, 0), 40, 520, gravity)
    map_surface.set_map_surface()

    i = 0 #debugging
    #Game cycle
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    chick.invert_gravity()

        #Setting foregorund
        map_surface.refreshForeground()
        chick.move()
        map_surface.setChick(chick)

        #Handling functionality
        if not map_surface.check_for_collisions(chick):
            chick.fall()

        pygame.display.update()
        clock.tick(30)
    pygame.quit()