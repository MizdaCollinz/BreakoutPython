# Imports
import pygame, sys, os, win32api, Ball, Player, BrickList
from pygame.locals import *

pygame.init()

#Frame Rate Assignment
FPS = 60
fpsClock = pygame.time.Clock()
fpsClock.tick(FPS)


#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
DARKWHITE = (255, 245, 238)
BLUE = (65,105,225)
ICE = (165, 242, 243,100)
DARKICE = (24, 204, 212,100)
RED = (255,0,0)

#Block Sizes
BRICKWIDTH = 100 #12 bricks across, 4 bricks down
BRICKHEIGHT = 40

# Resolution of Display Surface
DISPLAYSURF = pygame.display.set_mode((1200,800))
pygame.display.set_caption('Simple Breakout Game')
print(pygame.font.get_fonts())

#Initialise main objects
player = Player.Player()
flagList = BrickList.BrickList()
ball = Ball.Ball(player,flagList)

#Create Written Text on surface
fontObj = pygame.font.Font(pygame.font.match_font("segoeuiblack"), 32)
fontObj2 = pygame.font.Font(pygame.font.match_font("segoeuiblack"),16)

#Create Title Text Object
textSurfaceObj = fontObj.render('   Breakout    ', True, DARKWHITE, DARKICE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (600, 600)

#Create the background
bgsurface = pygame.image.load(os.path.join('img', 'frost&fog42.jpg'))
bg = bgsurface.convert()
bgrect = bgsurface.get_rect()

#Position Lives Text Rectangle
textRectObj2 = textSurfaceObj.get_rect()
textRectObj2.center = (660, 650)

#Brick Design
brickSurface = pygame.Surface((BRICKWIDTH, BRICKHEIGHT), pygame.SRCALPHA)  # per-pixel alpha
brickSurface.fill((DARKICE))  # notice the alpha value in the color

while True: #Game Loop
    # Draw on surface
    DISPLAYSURF.blit(bg,bgrect)

    #Create Player lives text object
    textSurfaceObj2 = fontObj2.render('   {} lives  '.format(player.Lives), True, DARKWHITE, DARKICE)


    #Present the two text objects, Game title and the number of Player Lives
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)

    #Draw unbroken Bricks
    for i in range(12):
        for j in range(4):
            if (flagList.flags[i][j] == 1):
                brickRect = pygame.Rect(i*BRICKWIDTH,j*BRICKHEIGHT,BRICKWIDTH,BRICKHEIGHT)
                DISPLAYSURF.blit(brickSurface, brickRect)
                pygame.draw.rect(DISPLAYSURF, WHITE, (brickRect),1)


    #Draw player controlled block
    playerRect = pygame.Rect(player.X-(player.width/2),player.Y-10,player.width,player.height)
    playerSurface = pygame.draw.rect(DISPLAYSURF, DARKICE, playerRect)
    playerBorder = pygame.draw.rect(DISPLAYSURF,WHITE,playerRect,1)

    #Draw Ball
    if ball.started:
        ball.MoveBall()
        ballGraphic = pygame.draw.circle(DISPLAYSURF,WHITE,(ball.X,ball.Y),10)

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


#Unused Currently - Sound Code
def PlaySound():
    soundObj = pygame.mixer.Sound('beeps.wav')
    soundObj.play()
    import time
    time.sleep(1) # wait and let the sound play for 1 second
    soundObj.stop()

#