import random
import pygame
import time
from enum import Enum
import glob
pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
#------------ ground ---------------
grassImg = "images/bkgnd_green_3_brt.jpg"
background = pygame.image.load(grassImg)
#------------ tanks ----------------
me = "images/tank_red.png"
myTank = pygame.image.load(me)
angle = 0
someone = "images/tank_blue.png"
enemyTank = pygame.image.load(someone)
#------------- bullet --------------
bullet1 = ("images/bullet.png")
myBullet =  pygame.image.load(bullet1)
bullet2 = ("images/enemy-bullet.jpg")
enemyBullet =  pygame.image.load(bullet2)


font = pygame.font.SysFont(None, 20)


clock = pygame.time.Clock()
pressed = pygame.key.get_pressed()


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Tank:
    def __init__(self, x, y,  d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP,  d_down=pygame.K_DOWN):
        self.x = x
        self.y = y
        self.bulcnt = 0
        self.speed = 2
        self.life = 3
        self.direction = Direction.RIGHT

        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT, d_up: Direction.UP, d_down: Direction.DOWN}

    def draw(self,justTank, angle):
        if self.direction == Direction.RIGHT:
            angle -= 90
            if angle < 0:
                angle += 360
            tank = pygame.transform.rotate(justTank, angle)

        if self.direction == Direction.LEFT:
            angle += 90
            if angle >= 360:
                angle -= 360
            tank = pygame.transform.rotate(justTank, angle)

        if self.direction == Direction.UP:
            tank = justTank

        if self.direction == Direction.DOWN:
            tank = pygame.transform.rotate(justTank, 180)

        screen.blit(tank, (self.x, self.y))

    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed


    def borders(self):
        if self.x > width or self.x < -30:
            self.x = (self.x + width) % width
        if self.y > height or self.y < -30:
            self.y = (self.y + height) % height

    def game_over(self):
        global run
        if self.life == 0:
            screen.fill((255, 153, 204))
            gameOver = font.render('G a m e   O v e r', True, (0, 90, 255))
            screen.blit(gameOver, (120, 150))
            pygame.display.flip()
            time.sleep(5)
            self.life = 3
            self.x = random.randint(100, 700)
            self.y = random.randint(100, 500)


# ------------------------------------B U L L E T---------------------------------

class Bullet:
    def __init__(self, x, y, dy, dx, d_space=pygame.K_SPACE):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.bul = False
        self.speed = 12

    def draw(self):
        screen.blit(myBullet, (self.x, self.y))

    def move(self):
        if self.bul:
            self.x += self.dx
            self.y += self.dy
        self.draw()

    def borders(self):
        if self.x < -30 or self.x > width or self.y < -30 or self.y > height:
            self.bul = False

    def shoot(self, Tank):
        if Tank.direction == Direction.RIGHT:
            self.x = Tank.x + 50
            self.y = Tank.y + 18
            self.dx = self.speed
            self.dy = 0

        if Tank.direction == Direction.LEFT:
            self.x = Tank.x - 15
            self.y = Tank.y + 15
            self.dx = -self.speed
            self.dy = 0

        if Tank.direction == Direction.UP:
            self.x = Tank.x + 15
            self.y = Tank.y - 20
            self.dx = 0
            self.dy = -self.speed

        if Tank.direction == Direction.DOWN:
            self.x = Tank.x + 15
            self.y = Tank.y + 50
            self.dx = 0
            self.dy = self.speed



def collision(tank, bullet):
    if bullet.x in range(tank.x, tank.x + 50) and bullet.y in range(tank.y, tank.y + 50):
        # sound2.play()
        bullet.bul = False
        bullet.x = -100
        bullet.y = -100
        return True
    return False


tank1 = Tank(300, 300)
tank2 = Tank(100, 100,  pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)
tanks = [tank1, tank2]

bullet1 = Bullet(-100, -100, 0, 0)
bullet2 = Bullet(-100, -100, 0, 0, pygame.K_RETURN)
bullets = [bullet1, bullet2]




map1 = """
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
w                               w
w                               w
w                               w
w                               w
wwwwwwwww                       w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w          wwwwwwwwwwwwwwwwwwwwww                     
w                               w
w                               w
w                               w
w                               w
w                               w
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
"""

# for line in map1:
#     print(line)

def init_display():
    global screen, tile
    screen = pygame.display.set_mode((800, 600))
    tile = pygame.image.load('images/wall.png')

def tiles(map1):
    global tile
    for y, line in enumerate(map1):
        for x, c in enumerate(line):
            if c == 'w':
                screen.blit(tile, (x*24, y*27))



def startSingleMode(will):
    if will:
        game()


map1 = map1.splitlines()
init_display()

def game():
    run = True
    while run:
        screen.blit(background, (0, 0))
        tiles(map1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key in tank1.KEY.keys():
                    tank1.change_direction(tank1.KEY[event.key])
                if event.key in tank2.KEY.keys():
                    tank2.change_direction(tank2.KEY[event.key])
                if event.key == pygame.K_SPACE and bullet1.bul == False:
                    bullet1.bul = True
                    bullet1.shoot(tank1)
                if event.key == pygame.K_RETURN and bullet2.bul == False:
                    bullet2.bul = True
                    bullet2.shoot(tank2)
                if event.key == pygame.K_ESCAPE:
                    run = False

        tank1.move()
        tank1.draw(myTank, 0)
        tank2.move()
        tank2.draw(enemyTank, 0)

        if collision(tank1, bullet2):
            tank1.life -= 1

        if collision(tank2, bullet1):
            tank2.life -= 1

        for tank in tanks:
            if tank.game_over():
                tank.life = 3
            tank.borders()

        bullet1.move()
        bullet2.move()

        bullet1.borders()
        bullet2.borders()

        pygame.display.flip()
    pygame.quit()

