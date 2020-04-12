import pygame, math, random
pygame.init()
win = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def drawMeal(win, color, foodX, foodY, snakeSize):
    pygame.draw.rect(win, color, (foodX, foodY, snakeSize, snakeSize))

def isEaten(snakeX, snakeY, foodX, foodY):
    distance =math.sqrt(math.pow(snakeX - foodX, 2) + math.pow(snakeY-foodY, 2))
    if distance < 23:
        return True
    else:
        return False
def sceenTxt(text, color, x, y):
    screenTxt = font.render(text, True, color)
    win.blit(screenTxt, (x, y))
def getSnake(win, snakeList, snakeSize):
    for i in snakeList:
        pygame.draw.rect(win, (0, 0, 0), (i[0], i[1], snakeSize, snakeSize))


def play():
    # snake
    snakeX = 50
    snakeY = 50
    snakeSize = 25
    speed = 5
    snakeLength = 1
    snakeList = []
    # food
    foodX = random.randint(0, 850)
    foodY = random.randint(0, 550)
    score = 0
    # gaming
    gameOver = False
    run = True
    while(run):
        clock.tick(30)
        if(gameOver == True):
            win.fill((0,0,0))
            string = "Game Is Over"
            cont = "Press ENTER to continue"
            sceenTxt(string, (204, 0, 51), 900/2-len(string)-100, 600/2-50)
            sceenTxt(cont, (204, 0, 51), 900/2-len(string)-200, 600/2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        play()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            key = pygame.key.get_pressed()
            if key[pygame.K_RIGHT]:
                snakeX += speed
            if key[pygame.K_LEFT]:
                snakeX += -speed
            if key[pygame.K_UP]:
                snakeY += -speed
            if key[pygame.K_DOWN]:
                snakeY += speed
            if(snakeX >= 900):
                snakeX = -40
            elif(snakeX <= -50):
                snakeX = 890
            if(snakeY <= 0):
                snakeY = 600
            elif(snakeY >= 600):
                snakeY = -2
            if isEaten(snakeX, snakeY, foodX, foodY):
                score += 1
                speed += 0.5
                snakeLength += 5
                foodX = random.randint(0, 850)
                foodY = random.randint(0, 550)

            head = []
            head.append(snakeX)
            head.append(snakeY)
            snakeList.append(head)
            if len(snakeList) > snakeLength:
                del snakeList[0]

            if  head in snakeList[:-1]:
                gameOver = True
            win.fill((255,255,255))
            sceenTxt("Score: "+str(score), (128,128,128), 5, 5)
            drawMeal(win, (255,0,0), foodX, foodY, snakeSize)
            getSnake(win, snakeList, snakeSize)
        pygame.display.update()
    pygame.quit()
play()