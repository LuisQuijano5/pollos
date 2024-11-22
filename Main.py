import pygame

from Models.Chick import Chick
from Models.Platypus import Platypus
from View.Map import Map


def game_over(screen, message):
    pygame.mixer.music.stop()

    font = pygame.font.SysFont('Impact', 60)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 20)  # Adjust position slightly

    font2 = pygame.font.SysFont('Impact', 30)  # Create a separate font object
    text2 = font2.render('Press any key to continue', True, (255, 255, 255))
    text_rect2 = text2.get_rect()
    text_rect2.center = (screen.get_width() // 2, screen.get_height() // 2 + 40)  # Adjust position

    screen.blit(text, text_rect)  # Blit the first text surface
    screen.blit(text2, text_rect2)  # Blit the second text surface
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                return True
            if event.type == pygame.KEYDOWN:
                waiting = False
                pygame.mixer.music.play(-1)
    return False


def show_start_message(screen):
    font = pygame.font.SysFont('Impact', 40)
    text = font.render('Chicken Surfers Press K to start', True, (255, 255, 255))
    screen.fill((0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    screen.blit(text, text_rect)
    pygame.display.flip()


def game_cycle(screen):
    # Objects creation
    map_surface = Map(screen, camera_x, camera_y, map_width, map_height, scroll_speed, square_size)
    chick = Chick(init_chick_pos, init_y_pos, scroll_speed, square_size, square_size, animations, square_size,
                  square_size, gravity)
    chick_fell = False
    perry = Platypus(init_perry_pos, init_y_pos, scroll_speed, square_size * 2, square_size, animations2, square_size,
                     square_size, gravity)
    map_surface.set_map_surface()
    perry_fell = False

    # Game cycle
    run = True
    game_active = False  # Cambiado a False para iniciar en la pantalla de inicio
    game_over_state = False  # Variable para controlar si el juego ha terminado
    show_start = True  # Variable para controlar la visualización del mensaje de inicio

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
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
                chick_fell = chick.fall(map_height)

            vcol, hcol = map_surface.check_for_collisions(perry)
            if not hcol:
                perry.move()
            if not vcol:
                perry_fell = perry.fall(map_height)

            if chick.hitbox.right - map_surface.camera_x < 0 or perry.eat(chick) or chick_fell:
                game_active = False
                game_over_state = game_over(screen, 'GAME OVER')
                break

            if perry.hitbox.right - map_surface.camera_x < 0 or perry_fell:
                game_active = False
                game_over_state = game_over(screen, 'YOU WIN')
                break

        if show_start:
            show_start_message(screen)  # Mostrar el mensaje de inicio

        if game_active:
            map_surface.scroll()
            map_surface.setAnimal(chick)
            map_surface.setAnimal(perry)

        pygame.display.flip()
        clock.tick(60)

    return True


if __name__ == '__main__':
    # param definition
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1000, 600))
    clock = pygame.time.Clock()
    square_size = 50
    scroll_speed = 5
    camera_x = 0
    camera_y = 0
    map_width = 200
    map_height = 600
    init_chick_pos = 500
    init_perry_pos = 300
    init_y_pos = 300
    gravity = 5

    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.play(-1)  # -1 para reproducir en bucle

    animations = []
    animations2 = []

    for i in range(10):
        img = pygame.image.load(f"models/images/{i}.png")
        image = pygame.transform.scale(img, (square_size, square_size))
        animations.append(image)
    for c in range(18):
        img = pygame.image.load(f"models/images/{c}p.png")
        image = pygame.transform.scale(img, (square_size * 2, square_size))
        iamge = pygame.transform.flip(img, False, True)
        animations2.append(image)

    go = True
    while go:
        go = game_cycle(screen)

    pygame.quit()
