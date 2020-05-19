from multi import startMultiMode
from single import startSingleMode
from ai import startAiMode
import pygame


pygame.init()
win = pygame.display.set_mode((800, 600))


def getText(text, font):
    txt = font.render(text, True, (255, 255, 255))
    return txt, txt.get_rect()


def button(msg, xi, xa, y, width, height, inactive, active, mode = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)

    if xa + width > mouse[0] > xa and y + height > mouse[1] > y:
        pygame.draw.rect(win, active, (xa, y, width, height))
        if click[0] == 1 and mode != None:
            if mode == 'multi':
                startMultiMode(True)
            if mode == 'single':
                startSingleMode(True)
            if mode == 'ai':
                startAiMode(True)

    else:
        pygame.draw.rect(win, inactive, (xi, y, width, height))

    smallText = pygame.font.SysFont(None, 40)
    txt, txtDirection = getText(msg, smallText)
    txtDirection.center = (xa + (width / 2), y + (height / 2))
    win.blit(txt, txtDirection)

# (204, 153, 255) a
# (255, 153, 204) ia
def menu():
    run=True
    while run:
        win.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        mainMenu = pygame.font.SysFont(None, 55)
        txt, txtDirection = getText('MENU', mainMenu)
        txtDirection.center = (400, 100)
        win.blit(txt, txtDirection)

        button('Multi Mode', 400, 300, 250, 200, 50, (255, 153, 204), (204, 153, 255), 'multi')
        button('Single Mode', 400, 300, 320, 200, 50, (255, 153, 204), (204, 153, 255), 'single')
        button('Ai mode', 400, 300, 390, 200, 50, (255, 153, 204), (204, 153, 255), 'ai')


        # mouse = pygame.mouse.get_pos()
        #
        # if 300+200 > mouse[0] > 350 and 250+50 > mouse[1] > 250:
        #     pygame.draw.rect(win, (204, 153, 255), (305, 250, 200, 50))
        # else:
        #     pygame.draw.rect(win, (255, 153, 204), (350, 250, 200, 50))
        #
        # smallText = pygame.font.SysFont(None, 40)
        # txt, txtDirection = getText('Multi Mode', smallText)
        # txtDirection.center = (305+(200/2), 250+(50/2))
        # win.blit(txt, txtDirection)


        pygame.display.flip()

menu()
