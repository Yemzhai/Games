import pygame
pygame.init()
win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Circle Game")
x = 50
y = 50
width = 50
height = 50
rad = 30
speed = 5

win.fill((255,255,255))
run = True
while(run):
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and x > 35:
        x -= speed
    if key[pygame.K_RIGHT] and x < 465:
        x += speed
    if key[pygame.K_DOWN] and y < 465:
        y += speed
    if key[pygame.K_UP] and y > 35:
        y -= speed

    win.fill((255,255,255))
    pygame.draw.circle(win, (255, 153, 204), (x, y), rad)
    pygame.display.update()
pygame.quit()