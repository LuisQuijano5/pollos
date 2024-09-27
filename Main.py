import pygame

from Models.Chick import Chick
from View.Scene import setBackground, setChick

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 700))
    clock = pygame.time.Clock()

    chick = Chick(100, 500, 1,50, (255, 255, 255), 100, 500)

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

        #Handling functionality
        chick.move()

        #Setting background
        setBackground(screen)

        #Setting foregorund
        setChick(screen, chick)

        pygame.display.update()
        clock.tick(30)
    pygame.quit()