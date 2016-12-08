# Imports
import pygame, sys, win32api, Ball, Player, BrickList
from pygame.locals import *

pygame.init()

#Frame Rate Assignment
FPS = 60
fpsClock = pygame.time.Clock()
fpsClock.tick(FPS)


#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BORDERBLUE = (25,25,112)
BLUE = (65,105,225)

#Block Sizes
BRICKWIDTH = 100 #12 bricks across, 4 bricks down
BRICKHEIGHT = 40

# Resolution of Display Surface
DISPLAYSURF = pygame.display.set_mode((1200,800))
pygame.display.set_caption('Simple Breakout Game')


#Initialise main objects
player = Player.Player()
flagList = BrickList.BrickList()
ball = Ball.Ball(player,flagList)

#Create Written Text on surface
fontObj = pygame.font.Font('freesansbold.ttf', 32)
fontObj2 = pygame.font.Font('freesansbold.ttf',20)
textSurfaceObj = fontObj.render('   Breakout    ', True, WHITE, BLUE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (600, 600)



while True: #Game Loop
    # Draw on surface
    DISPLAYSURF.fill(WHITE)

    textSurfaceObj2 = fontObj2.render('   {} lives  '.format(player.Lives), True, WHITE, BLUE)
    textRectObj2 = textSurfaceObj.get_rect()
    textRectObj2.center = (660, 632)

    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)

    #Draw unbroken Bricks
    for i in range(12):
        for j in range(4):
            if (flagList.flags[i][j] == 1):
                brickRect = pygame.Rect(i*BRICKWIDTH,j*BRICKHEIGHT,BRICKWIDTH,BRICKHEIGHT)
                brickSurface = pygame.draw.rect(DISPLAYSURF,BLUE,(brickRect))
                brickSurface = pygame.draw.rect(DISPLAYSURF, BORDERBLUE, (brickRect),1)


    #Draw player controlled block
    playerRect = pygame.Rect(player.X-(player.width/2),player.Y-10,player.width,player.height)
    playerSurface = pygame.draw.rect(DISPLAYSURF, BLUE, playerRect)

    #Draw Ball
    if ball.started:
        ball.MoveBall()
        ballGraphic = pygame.draw.circle(DISPLAYSURF,BLACK,(ball.X,ball.Y),10)

    #Move the Player's position
    if player.moving:
        ball.started = True
        player.MovePlayer()

    # Check for victory
    if flagList.CheckWin():
        player.Victory()

    #Resolve user input events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            #Left
            if event.key == pygame.K_LEFT:
                print("Moving left")
                player.moving = True
                player.direction = "Left"
            #Right
            if event.key == pygame.K_RIGHT:
                print("Moving right")
                player.moving = True
                player.direction = "Right"
        elif event.type == KEYUP:
            if event.key == pygame.K_LEFT:
                print("Stop left")
                if(player.direction == "Left"):
                    player.moving = False
            elif event.key == pygame.K_RIGHT:
                print("Stop right")
                if(player.direction == "Right"):
                    player.moving = False

    pygame.display.update()


#BLEH
def PlaySound():
    soundObj = pygame.mixer.Sound('beeps.wav')
    soundObj.play()
    import time
    time.sleep(1) # wait and let the sound play for 1 second
    soundObj.stop()