import pygame

from View.Scene import GenerateScene

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 700))
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        GenerateScene(screen)
        pygame.display.update()
        clock.tick(30)
    pygame.quit()