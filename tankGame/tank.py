from game_function import * # Courtesy of Steve Paget
from math import sqrt
import random # Random not used yet
keydict["/"] = pygame.K_SLASH # This character is not in pygame_functions

# Author and Composer: Michael Szemborski

"""
This sets up a bkgnd scene with two tanks, labeled p1 p2. They are able to move
forward and backward, rotate left and right and fire. When one fires upon the
other he scores a hit. The first one to reach the winning score wins the game.
If they collide they both score a point.

A maze can be displayed which will limit movement. This is the enhancement in this version.
The maze can be displayed or hidden during gameplay by hitting "m"
"""

# variable setup
size = width, height = 1200, 695 # bkgnd size - best size for laptop screen
screenSize(width, height) # screenSize needed for setBackgroundImage

# player 1 & player 2
p1w = 50
p1h = 50
p1size = p1w, p1h
p1w_half = int(p1w / 2)
p1h_half = int(p1h / 2)
hyp1 = sqrt(p1w**2 + p1h**2)
p1hyp_half = int(hyp1 / 2)
p1hyp_half_half = int(p1hyp_half / 2)

p2w = 50
p2h = 50
p2size = p2w, p2h
p2w_half = int(p2w / 2)
p2h_half = int(p2h / 2)
hyp2 = sqrt(p2w**2 + p2h**2)
p2hyp_half = int(hyp2 / 2)
p2hyp_half_half = int(p2hyp_half / 2)

# Start position for p1
st_p1_x = 77 # 65 # 199
st_p1_y = 590 #605 # 409

# Start position for p2
st_p2_x = 1072 # 1084 # 660
st_p2_y = 58 # 65 # 115

spinSpeed = 100 # Pause time between spin displays
pixels2move = 1 # Speed: Recommend 1 - 10
fire2move = 5  # Speed: Number of pixels to move before redisplaying bullet
fireDelay = 500 # How long to display explosion

hits2win = 10

p1 = makeSprite("images/tank_red.png")
p2 = makeSprite("images/tank_blue.png")
burn1 = makeSprite("images/burn.png")
burn2 = makeSprite("images/burn.png")
bullet = makeSprite("images/bullet.png")
mazeSprite = makeSprite("images/maze01.png")
moveSprite(mazeSprite, 0, 0, False)

pygame.display.set_caption('Tank Battle')
setBackgroundImage("images/misty-lg.jpg") # size is 789 x 441
grassImg = "images/bkgnd_green_3_brt.jpg"
mazeImg = "images/maze01.png"

p1Display = makeLabel("Player 1:",30,10,10,"white")
p2Display = makeLabel("Player 2:",30,(width - 210),10,"white") # Works best on Raspberry Pi
start0 = makeLabel("Tank Battle",60,480,20,"black")
start1 = makeLabel("Player 1 (Red):",30,10,120,"black")
start1Color = makeLabel("Player 1 (Red):",30,10,120,"red")
start2 = makeLabel("Player 2 (Blue):",30, int(width/2),120,"black")
start2Color = makeLabel("Player 2 (Blue):",30, int(width/2),120,"blue")
start3 = makeLabel("W = forward, S = back, A = left, D = right",25,10,165,"black")
start4 = makeLabel("up = forward, down = back, left = left, right = right",25,int(width/2),165,"black")
start5 = makeLabel("Enter = fire",25,10,190,"black")
start6 = makeLabel("Space = fire",25,int(width/2),190,"black")
start7 = makeLabel("For START press 'Space' and choose number of round and press 'ENTER' ",32,100,235,"red", font='cambria')
M = makeLabel("press 'm' to change the map ",32,400,350,"blue", font='cambria')
start8 = makeLabel("to win? (esc to quit)",28,540,285,"black")
start9 = makeLabel("m = maze on/off",30,10,300,"black")
startA = makeLabel("by Islam Yemzhayev",20,110,670,"white")

endDisplay = makeLabel("y to play again or esc to quit",30,(width - 750),10,"white")

# Parms below are x, y, width, case, text, max chars, font
# case is set to 1 to convert to lowercase (2 is upper and 0 is no conversion)
# if max chars is set to 0 there is no limit
#inputBox = makeTextBox(450,400,300,1,"Enter text here",3,24)
##inputBox = makeTextBox(565,285,50,1,"10",3,24)
inputBox = makeTextBox(480,285,50,1,"10",3,24)

e1 = makeSound("sounds/movec2.wav") # engine sound playing a C note
e2 = makeSound("sounds/moved2.wav") # engine sound playing a D note
r1 = makeSound("sounds/rotd.wav") # rotating sound playing a D note
r2 = makeSound("sounds/rotc.wav") # rotating sound playing a C note
f1 = makeSound("sounds/fired.wav") # firing with a D note
f2 = makeSound("sounds/firec.wav") # firing with a C note
ex1 = makeSound("sounds/exploded.wav") # explode with a D note
ex2 = makeSound("sounds/explodec.wav") # explode with a C note

nut = makeSound("sounds/nuthin.wav") # 1 ms of nothing -  not used
ndm = makeSound("sounds/003_1.wav") # end music

muzik = True

"""
Beginning of Joystick Section
"""
joyCnt = pygame.joystick.get_count()
print('pygame.joystick.get_count() =', joyCnt)
joysticks = []
for x in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(x)
    # print('joystick.get_id() =', joystick.get_id(), flush=True)
    name = joystick.get_name()
    # print('joystick.get_name() = "', name, '"', flush=True)
    # print('Initializing joystick...', flush=True)
    joystick.init()
    joysticks.append(joystick)

# It is assumed that there are two joysticks
p1j = 0 # joystick id for player 1
p2j = 1 # joystick id for player 2

def gameSetup():
    # Initialize positions for both characters (centered on the character)
    global p1_x
    global p1_y
    global p2_x
    global p2_y
    global p1Angle
    global p2Angle
    global move_p1
    global move_p2
    global spin_p1
    global spin_p2
    global p1Score
    global p2Score
    global play
    global mazeShow
    
    p1_x = st_p1_x + p1w_half # \
    p1_y = st_p1_y + p1h_half #  \____ These provide the center positions for the sprites
    p2_x = st_p2_x + p2w_half #  /
    p2_y = st_p2_y + p2h_half # /
    p1Angle = 0
    p2Angle = 0

    move_p1 = False
    move_p2 = False
    spin_p1 = False
    spin_p2 = False

    p1Score = 0
    p2Score = 0
    play = True

    # Initial scene
    setBackgroundImage(grassImg) # size is 2048 x 1536
    # Maze is displayed or hidden by hitting "m"

    mazeShow = True # Using a sprite instead of background for the maze
    if mazeShow:
        showSprite(mazeSprite)
    else:
        hideSprite(mazeSprite)

    showLabel(p1Display) 
    showLabel(p2Display)

    transformSprite(p1,p1Angle,1) # Player 1 needs to point up
    p2Angle += 180
    transformSprite(p2,p2Angle,1) # Player 2 needs to point down
    moveSprite(p1, p1_x, p1_y, True) # True means assign position based upon the...
    moveSprite(p2, p2_x, p2_y, True) # ...center of the sprite.
    showSprite(p1)
    showSprite(p2)

# The next four functions could have been combined into one, providing a more elegant solution.
# But the complexity would have made it considerably less readable.
def player1MoveFwd():
    global p1_x
    global p1_y
    holdX = p1_x
    holdY = p1_y

    if p1Angle in (225, 270, 315):
        p1_x -= pixels2move
        if p1_x < 0:
            p1_x = width
            
    if p1Angle in (45, 90, 135):
        p1_x += pixels2move
        if p1_x > width:
            p1_x = 0
            
    if p1Angle in (0, 45, 315):
        p1_y -= pixels2move
        if p1_y < 0:
            p1_y = height
            
    if p1Angle in (135, 180, 225):
        p1_y += pixels2move
        if p1_y > height:
            p1_y = 0
            
    moveSprite(p1, p1_x, p1_y, True)
    
    if mazeShow and touching(p1, mazeSprite):
        p1_x = holdX
        p1_y = holdY
        moveSprite(p1, p1_x, p1_y, True)
        
    showSprite(p1)
    playSound(e1)

def player1MoveBak():
    global p1_x
    global p1_y
    holdX = p1_x
    holdY = p1_y
    
    if p1Angle in (225, 270, 315):
        p1_x += pixels2move
        if p1_x > width:
            p1_x = 0

    if p1Angle in (45, 90, 135):
        p1_x -= pixels2move
        if p1_x < 0:
            p1_x = width
            
    if p1Angle in (0, 45, 315):
        p1_y += pixels2move
        if p1_y > height:
            p1_y = 0
            
    if p1Angle in (135, 180, 225):
        p1_y -= pixels2move
        if p1_y < 0:
            p1_y = height
            
    moveSprite(p1, p1_x, p1_y, True)    
  
    if mazeShow and touching(p1, mazeSprite):
        p1_x = holdX
        p1_y = holdY        
        moveSprite(p1, p1_x, p1_y, True)
        
    showSprite(p1)
    playSound(e1)
            
def player2MoveFwd():
    global p2_x
    global p2_y
    holdX = p2_x
    holdY = p2_y
    
    if p2Angle in (225, 270, 315):
        p2_x -= pixels2move
        if p2_x < 0:
            p2_x = width
            
    if p2Angle in (45, 90, 135):
        p2_x += pixels2move
        if p2_x > width:
            p2_x = 0
            
    if p2Angle in (0, 45, 315):
        p2_y -= pixels2move
        if p2_y < 0:
            p2_y = height
            
    if p2Angle in (135, 180, 225):
        p2_y += pixels2move
        if p2_y > height:
            p2_y = 0
            
    moveSprite(p2, p2_x, p2_y, True)   
  
    if mazeShow and touching(p2, mazeSprite):
        p2_x = holdX
        p2_y = holdY
        moveSprite(p2, p2_x, p2_y, True)
        
    showSprite(p2)
    playSound(e2)

def player2MoveBak():
    global p2_x
    global p2_y
    holdX = p2_x
    holdY = p2_y
    
    if p2Angle in (225, 270, 315):
        p2_x += pixels2move
        if p2_x > width:
            p2_x = 0

    if p2Angle in (45, 90, 135):
        p2_x -= pixels2move
        if p2_x < 0:
            p2_x = width
            
    if p2Angle in (0, 45, 315):
        p2_y += pixels2move
        if p2_y > height:
            p2_y = 0
            
    if p2Angle in (135, 180, 225):
        p2_y -= pixels2move
        if p2_y < 0:
            p2_y = height
            
    moveSprite(p2, p2_x, p2_y, True)
  
    if mazeShow and touching(p2, mazeSprite):
        p2_x = holdX
        p2_y = holdY
        moveSprite(p2, p2_x, p2_y, True)
        
    showSprite(p2)
    playSound(e2)
            
def playerFire(fAngle, fx, fy):
    global p1Score
    global p2Score
    
    if fAngle in (45, 135, 225, 315):
        half = p1hyp_half # half of the hypotenuse is used because player is at an angle
    else:
        if fAngle in (90, 270):
            half = p1w_half
        else:
            half = p1h_half

    if fAngle in (225, 315): # These are needed to center the starting point
        fx += (p1hyp_half_half)
    if fAngle in (45, 135):
        fx -= (p1hyp_half_half)
    if fAngle in (45, 315):            
        fy -= (p1hyp_half_half)
    if fAngle in (135, 225):            
        fy += (p1hyp_half_half)
        
    if fx == p1_x:
        sound2play = f1
    else:
        sound2play = f2
        
    fire = True
    fireFirst = True
    
    while fire:                        
        hideSprite(bullet)
        holdX, holdY = fx, fy
        if fAngle in (225, 270, 315):
            if fireFirst:
                fx -= (fire2move + half + 2)
            else:
                fx -= fire2move
            if fx < 0:
                fire = False
            if fire and fireFirst:                
                playSound(sound2play)
                fireFirst = False
                
                
        if fAngle in (45, 90, 135):
            if fireFirst:
                fx += (fire2move + half + 2)
            else:
                fx += fire2move
            if fx > width:
                fire = False
            if fire and fireFirst:                
                playSound(sound2play)
                fireFirst = False
                
        if fAngle in (0, 45, 315):
            if fireFirst:
                fy -= (fire2move + half + 2)
            else:
                fy -= fire2move
            if fy < 0:
                fire = False
            if fire and fireFirst:                
                playSound(sound2play)
                fireFirst = False
                
        if fAngle in (135, 180, 225):
            if fireFirst:
                fy += (fire2move + half + 2)
            else:
                fy += fire2move
            if fy > height:
                fire = False
            if fire and fireFirst:                
                playSound(sound2play)
                fireFirst = False
              
        if fire:
            moveSprite(bullet, fx, fy, True)
            if mazeShow and touching(bullet, mazeSprite):
                fx = holdX
                fy = holdY
                moveSprite(bullet, fx, fy, True)
                fire = False
            showSprite(bullet)
            pause(1) # Needed so you can actually see the bullet

        if fire:
            if touching(p1, bullet):                
                stopSound(f2)
                hideSprite(bullet)
                playSound(ex1)
                moveSprite(burn1, fx, fy, True)
                showSprite(burn1)
                # print("Hit player 1 !")
                pause(fireDelay, True)
                hideSprite(burn1)
                p2Score += 1
                fire = False
                
            if touching(p2, bullet):                
                stopSound(f1)            
                hideSprite(bullet)
                playSound(ex2)
                moveSprite(burn2, fx, fy, True)
                showSprite(burn2)
                playSound(ex2)
                # print("Hit player 2 !")
                pause(fireDelay, True)
                hideSprite(burn2)
                p1Score += 1
                fire = False
        else:                                    
            hideSprite(bullet)
                
""" Main Section """
setAutoUpdate(False) # Prevents screen refresh until updateDisplay()

showLabel(start0)
showLabel(start1)
showLabel(start2)
##showLabel(start2a)
showLabel(start3)
showLabel(start4)
showLabel(start5)
showLabel(start6)
showLabel(start7)
# showLabel(start9)
showLabel(startA)
hideTextBox(inputBox)
showLabel(M)

makeMusic("sounds/F minor.mp3") # Project in F minor - long, mp3 version
playMusic()

wait = True
while wait:
    if joyCnt > 0:
        first = joysticks[0].get_button(0)
    else:
        first = 0
        
    if joyCnt > 1:
        second = joysticks[1].get_button(0)
    else:
        second = 0
        
    if first:
        p1j = 0
        p2j = 1
        print("first ", first)
    if second:
        p1j = 1
        p2j = 0
        print("second", second)
    if first or second:
##        hideLabel(start1a)
##        hideLabel(start2a)
##        showLabel(start1b)
##        showLabel(start2b)
        hideLabel(start1)
        hideLabel(start2)
        showLabel(start1Color)
        showLabel(start2Color)
        wait = False
    if keyPressed("space"):
        wait = False
    if keyPressed("m"): # m is turn off maze card
        if muzik:
            stopMusic()
            muzik = False
            pause(1000)
        else:
            rewindMusic()
            playMusic()
            muzik = True
            pause(1000)
    if not wait:
        showLabel(start8)
        showTextBox(inputBox)
        entry = textBoxInput(inputBox)
        if entry.isnumeric() and int(entry) > 0:
            print("hits2win = ", hits2win)
            hits2win= int(entry)
    updateDisplay()

stopMusic()

muzik = True
            
hideLabel(start0)
hideLabel(start1)
hideLabel(start1Color)
##hideLabel(start1a)
##hideLabel(start1b)
hideLabel(start2)
hideLabel(start2Color)
##hideLabel(start2a)
##hideLabel(start2b)
hideLabel(start3)
hideLabel(start4)
hideLabel(start5)
hideLabel(start6)
hideLabel(start7)
hideLabel(M)
hideLabel(start8)
# hideLabel(start9)
hideLabel(startA)
hideTextBox(inputBox)

gameSetup()

while True:

    if play and keyPressed("m"):
        if mazeShow:
            mazeShow = False
            # setBackgroundImage(grassImg)
            hideSprite(mazeSprite)
        else:
            mazeShow = True
            # setBackgroundImage(mazeImg)
            showSprite(mazeSprite)
        pause(250)

    # For player 1
    if joyCnt > 0:
        ax = round(joysticks[p1j].get_axis(0))
    else:
        ax = 0
    if play and (keyPressed("a") or ax < 0):
        p1Angle = p1Angle - 45
        if p1Angle < 0:
            p1Angle += 360
        transformSprite(p1,p1Angle, 1)
        playSound(r1)    
        spin_p1 = True
        pause(spinSpeed)
    elif play and (keyPressed("d") or ax > 0):
        p1Angle = p1Angle +45
        if p1Angle > 359:
            p1Angle -= 360
        transformSprite(p1, p1Angle, 1)
        playSound(r1)    
        spin_p1 = True
        pause(spinSpeed)

    if joyCnt > 0:
        ax = round(joysticks[p1j].get_axis(1))
    else:
        ax = 0
    if play and (keyPressed("w") or ax < 0):
        player1MoveFwd()
        move_p1 = True
    elif play and (keyPressed("s") or ax > 0):
        player1MoveBak()
        move_p1 = True
        
    # For player 2
    if joyCnt > 1:
        ax = round(joysticks[p2j].get_axis(0))
    else:
        ax = 0
    if play and (keyPressed("left") or ax < 0):
        p2Angle = p2Angle - 45
        if p2Angle < 0:
            p2Angle += 360
        transformSprite(p2,p2Angle, 1)
        playSound(r2)        
        spin_p2 = True
        pause(spinSpeed)
    elif play and (keyPressed("right") or ax > 0):
        p2Angle = p2Angle +45
        if p2Angle > 359:
            p2Angle -= 360
        transformSprite(p2, p2Angle, 1)
        playSound(r2)    
        spin_p2 = True
        pause(spinSpeed)

    if joyCnt > 1:
        ax = round(joysticks[p2j].get_axis(1))
    else:
        ax = 0
    if play and (keyPressed("up") or ax < 0):
        player2MoveFwd()
        move_p2 = True
    elif play and (keyPressed("down") or ax > 0):
        player2MoveBak()
        move_p2 = True
     
    # See if movement caused a collision
    if play and (move_p1 or move_p2 or spin_p1 or spin_p2):
        move_p1 = False
        move_p2 = False
        spin_p1 = False
        spin_p2 = False
        if touching(p1, p2):
            moveSprite(burn1, p1_x, p1_y, True)
            moveSprite(burn2, p2_x, p2_y, True)
            showSprite(burn1)
            showSprite(burn2)            
            playSound(ex2) # No need to play both explosions
            # print("Collision!")
            pause(2000, True)
            hideSprite(burn1)
            hideSprite(burn2)
            p1Score += 1
            p2Score += 1        
    # For player 1
    if play and ((keyPressed("space")) or (joyCnt > 0 and joysticks[p1j].get_button(0))):
        playerFire(p1Angle, p1_x, p1_y)
        
    # For player 2
    if play and (keyPressed("enter") or (joyCnt > 1 and joysticks[p2j].get_button(0))):
        playerFire(p2Angle, p2_x, p2_y)

    changeLabel(p1Display, "Player 1: {0}".format(str(p1Score)))
    changeLabel(p2Display, "Player 2: {0}".format(str(p2Score)))
        
    if p1Score == hits2win:
        changeLabel(p1Display, "Player 1: WINS")
        play = False
    if p2Score == hits2win:
        changeLabel(p2Display, "Player 2: WINS")
        play = False
        
    if play and keyPressed("r"): # undocumented method to restart
        gameSetup()
        
    # if play and keyPressed("t"): # undocumented method to test code
    #     pass
        
    if not play:
        showLabel(endDisplay)        
        if muzik:
            playSound(ndm,loops=100)
            muzik = False
        
        if keyPressed("Y"):
            muzik = True
            stopSound(ndm)        
            hideLabel(endDisplay)
            
            play = True
            gameSetup()
        
    updateDisplay()




