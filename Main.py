import pygame

from Models.Chick import Chick
from Models.Platypus import Platypus
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
    animations2 = []

    for i in range (10):
        img = pygame.image.load(f"models/images/{i}.png")
        image= pygame.transform.scale(img, (40,40))
        animations.append(image)
    for c in range(10):
        img = pygame.image.load(f"models/images/{c}p.png")
        image = pygame.transform.scale(img, (80, 40))
        animations2.append(image)
    chick = Chick(200, 300, scroll_speed, square_size, square_size, animations, 40, 40, gravity)
    perry = Platypus(100, 300, scroll_speed, square_size * 2, square_size, animations2,  40, 40, gravity)


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
                if event.key == pygame.K_d:
                    perry.invert_gravity()

        # Handling functionality
        vcol, hcol = map_surface.check_for_collisions(chick)
        if not hcol:
            chick.move()
        if not vcol:
            chick.fall()

        vcol, hcol = map_surface.check_for_collisions(perry)
        if not hcol:
            perry.move()
        if not vcol:
            perry.fall()

        if perry.eat(chick):
            print("Eat chicken")
        #Refreshing screen
        map_surface.scroll()
        map_surface.setChicken(chick)
        map_surface.setPerry(perry)
        pygame.display.update()
        clock.tick(30)
    pygame.quit()