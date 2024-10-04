import pygame

from Models.Chick import Chick
from Models.Platypus import Platypus
from View.Map import Map

def game_over(screen):
    pygame.mixer.music.stop()
    font = pygame.font.SysFont('Impact', 60)
    text = font.render('GAME OVER', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    screen.blit(text, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                return True
            if event.type == pygame.KEYDOWN:
                waiting = False
    return False

def you_win(screen):
    pygame.mixer.music.stop()
    font = pygame.font.SysFont('Impact', 60)
    text = font.render('YOU WIN!', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    screen.blit(text, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                return True
            if event.type == pygame.KEYDOWN:
                waiting = False
    return False

def show_start_message(screen):
    font = pygame.font.SysFont('Impact', 40)
    text = font.render('Chicken Surfers Press K to start', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    screen.blit(text, text_rect)
    pygame.display.flip()


if __name__ == '__main__':
    #param definition
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1000, 600))
    clock = pygame.time.Clock()
    square_size = 40
    scroll_speed = 4
    camera_x = 0
    camera_y = 0
    map_width = 2000
    map_height = 600
    gravity = 5

    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.play(-1)  # -1 para reproducir en bucle

    #Objects creation
    map_surface = Map(screen, camera_x, camera_y, map_width, map_height, scroll_speed, square_size)

    animations = []
    animations2 = []

    for i in range (10):
        img = pygame.image.load(f"models/images/{i}.png")
        image= pygame.transform.scale(img, (40,40))
        animations.append(image)
    for c in range(18):
        img = pygame.image.load(f"models/images/{c}p.png")
        image = pygame.transform.scale(img, (80, 40))
        iamge = pygame.transform.flip(img, False, True)
        animations2.append(image)
    chick = Chick(200, 300, scroll_speed, square_size, square_size, animations, 40, 40, gravity)
    perry = Platypus(100, 300, scroll_speed, square_size * 2, square_size, animations2,  40, 40, gravity)


    map_surface.set_map_surface()

    i = 0 #debugging
    #Game cycle
    run = True
    game_active = False  # Cambiado a False para iniciar en la pantalla de inicio
    game_over_state = False  # Variable para controlar si el juego ha terminado
    show_start = True  # Variable para controlar la visualización del mensaje de inicio

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if show_start:
                    if event.key == pygame.K_k:
                        show_start = False
                        game_active = True
                else:
                    if event.key == pygame.K_UP:
                        chick.invert_gravity()
                        if chick.gravity > 0:
                            chick.flip = False
                        else:
                            chick.flip = True

                    if event.key == pygame.K_w:
                        perry.invert_gravity()
                        if perry.gravity > 0:
                            perry.flip = False
                        else:
                            perry.flip = True

        if game_active:
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

            if chick.hitbox.right - map_surface.camera_x < 0:
                game_active = False
                game_over_state = game_over(screen)

            if perry.hitbox.right - map_surface.camera_x < 0:
                game_active = False
                game_over_state = you_win(screen)

        if show_start:
            show_start_message(screen)  # Mostrar el mensaje de inicio

        if game_active:
            map_surface.scroll()
            map_surface.setChicken(chick)
            map_surface.setPerry(perry)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()