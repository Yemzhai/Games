import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Welcome to Game")
walkRight = [
    pygame.image.load('img/pygame_right_1.png'),
    pygame.image.load('img/pygame_right_2.png'),
    pygame.image.load('img/pygame_right_3.png'),
    pygame.image.load('img/pygame_right_4.png'),
    pygame.image.load('img/pygame_right_5.png'),
    pygame.image.load('img/pygame_right_6.png'),
]
walkLeft = [
    pygame.image.load('img/pygame_left_1.png'),
    pygame.image.load('img/pygame_left_2.png'),
    pygame.image.load('img/pygame_left_3.png'),
    pygame.image.load('img/pygame_left_4.png'),
    pygame.image.load('img/pygame_left_5.png'),
    pygame.image.load('img/pygame_left_6.png'),
]

stay = pygame.image.load('img/pygame_idle.png')
bg = pygame.image.load('img/flag.jpg')
clock = pygame.time.Clock()

x = 50
y = 425
width = 60
height = 71
speed = 5

left = False
right = False
animationCount = 0

jump = 10
isJump = False
win.fill((255, 255, 255))
bullets = []
lastMove = "right"

class shoot():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8*facing
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

def drowWindow():
    global animationCount
    win.blit(bg, (0,0))

    if animationCount+1 >= 30:
        animationCount = 0
    if(left):
        win.blit(walkLeft[int(animationCount/5)], (x, y))
        animationCount += 1
    elif(right):
        win.blit(walkRight[int(animationCount/5)], (x, y))
        animationCount += 1
    else:
        win.blit(stay, (x, y))

    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()



run = True
while(run):
    # pygame.time.delay(10)
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    key = pygame.key.get_pressed()

    if key[pygame.K_f]:
        if(lastMove == "right"):
            facing = 1
        else:
            facing = -1
        if len(bullets) < 5:
            bullets.append(shoot(int(x + width // 2), int(y + height//2), 6, (0, 0, 128), facing))
    if key[pygame.K_LEFT] and x > 5:
        x -= speed
        left = True
        right = False
        lastMove = "left"
    elif key[pygame.K_RIGHT] and x < 500 - width - 5:
        x += speed
        left = False
        right = True
        lastMove = "right"
    else:
        left = False
        right = False
        animationCount = 0
    if(not(isJump)):
        if key[pygame.K_SPACE]  :
            isJump = True
    else:
        if jump >= -10:
            if jump < 0:
                y += (jump**2)/2
            else:
                y -= (jump**2)/2
            jump -= 1
        else:
            jump = 10
            isJump = False
    drowWindow()
pygame.quit()