import pygame

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
    screen.fill((100,150,255))

    pygame.display.update()
    clock.tick(30)
pygame.quit()