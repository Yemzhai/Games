import pygame, random, math

pygame.init()

win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")

bg = pygame.image.load('img/bg.jpg')
##PLAYER
spaceship = pygame.image.load('img/space-invaders.png')
playerX = 370
playerY = 480
move_x = 0
###ENEMY
enemyIMG = []
enemyX = []
enemyY = []
enemy_move_x = []
enemy_move_y = []
numberOfEnemies = 10
for i in range(numberOfEnemies):
    enemyIMG.append(pygame.image.load('img/enemy1.png'))
    enemyIMG.append(pygame.image.load('img/enemy2.png'))
    enemyIMG.append(pygame.image.load('img/enemy3.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(50)
    enemy_move_x.append(4)
    enemy_move_y.append(40)
##BULLET
bulletIMG = pygame.image.load('img/bullet.png')
bulletX = 0
bulletY = 480
bullet_move_x = 0
bullet_move_y = 10
bullet_state = "ready"
#score
cnt = 0



def player(x, y):
    win.blit(spaceship, (x, y))

def enemy(x, y, i):
    win.blit(enemyIMG[i], (x, y))

def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    win.blit(bulletIMG, (x+16, y+10))

def isDead(bulletX, bulletY, enemyX, enemyY):
    distance =math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY-bulletY, 2))
    if distance < 30:
        return True
    else:
        return False
run = True
while(run):
    win.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        playerX -= 5
    if pressed[pygame.K_RIGHT]:
        playerX += 5
    if pressed[pygame.K_SPACE]:
        bulletX = playerX
        bullet(playerX, bulletY)

    #player movemen
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    #enemy movement
    for i in range(numberOfEnemies):
        enemyX[i] += enemy_move_x[i]
        if enemyX[i] <= 0:
            enemy_move_x[i] = 4
            enemyY[i] += enemy_move_y[i]
        if enemyX[i] >= 736:
            enemy_move_x[i] = -4
            enemyY[i] += enemy_move_y[i]
        # DEAD
        dead = isDead(bulletX, bulletY, enemyX[i], enemyY[i])
        if dead:
            bulletY = 480
            bullet_state = "ready"
            cnt += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = 50
        enemy(enemyX[i], enemyY[i], i)
    ## bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        bullet(playerX, bulletY)
        bulletY -= bullet_move_y

    player(playerX, playerY)
    pygame.display.update()

pygame.quit()