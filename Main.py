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

    animations = []

    for i in range (10):
        img = pygame.image.load(f"models/images/{i}.png")
        image= pygame.transform.scale(img, (100,40))
        animations.append(image)
    chick = Chick(100, 40, scroll_speed, 40, animations, 40, 40, gravity)
    #chick2= Chick(200,100, scroll_speed, 100, "models/images/perry.png", 40, 520, gravity)
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

        # Handling functionality
        vcol, hcol = map_surface.check_for_collisions(chick)
        if not hcol:
            chick.move()
        if not vcol:
            chick.fall()

        #Refreshing screen
        map_surface.scroll()
        map_surface.setChick(chick)
        #map_surface.setSquare(chick2)
        pygame.display.update()
        clock.tick(30)
    pygame.quit()