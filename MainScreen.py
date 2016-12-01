# Imports
import pygame, sys


from pygame.locals import *

pygame.init()

FPS = 60 # frames per second setting
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

class Player:
    def __init__(self):
        self.Lives = 3
        #Position
        self.X = 0
        self.Y = 780
        #Size
        self.width = 80
        self.height = 20
        #Movement
        self.moving = False
        self.direction = "Left"

    def Defeat(self):
        #win32api.MessageBox(0, 'hello', 'title')
        pass

class Ball:
    def __init__(self,player):
        self.X = 600
        self.Y = 400
        self.Speed = [0,1]
        self.player = player

    def MoveBall(self):
        self.X += self.Speed[0]
        if self.X < 0:
            self.X = 1
            self.Speed[0] = -self.Speed[0]
        elif self.X > 1200:
            self.X = 1199
            self.Speed[0] = -self.Speed[0]

        self.Y += self.Speed[1]
        if self.Y < 0:
            self.Y = 1
            self.speed[1] = -self.speed[1]
        elif self.Y > 800:
            #ResetBall
            self.resetBall()
            pass

    def resetBall(self):
        #Lose a life
        self.player.Lives -= 1
        if self.player.Lives == 0:
            self.player.Defeat()

        #Reset Position and speed
        self.speed = [0,1]
        self.X = 600
        self.Y = 400

#Brick Flags - Setup
brickFlagList = []
for i in range(12):
        brickFlagList.append([1] * 4)

# Resolution of Display Surface
DISPLAYSURF = pygame.display.set_mode((1200,800))
pygame.display.set_caption('Simple Breakout Game')



fontObj = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj = fontObj.render('Hello world!', True, WHITE, BLUE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (300, 16)

#Initialise main objects

player = Player()
ball = Ball(player)

while True: #Game Loop
    # Draw on surface
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    #Draw unbroken Bricks
    for i in range(12):
        for j in range(4):
            if (brickFlagList[i][j] == 1):
                brickRect = pygame.Rect(i*BRICKWIDTH,j*BRICKHEIGHT,BRICKWIDTH,BRICKHEIGHT)
                brickSurface = pygame.draw.rect(DISPLAYSURF,BLUE,(brickRect))
                brickSurface = pygame.draw.rect(DISPLAYSURF, BORDERBLUE, (brickRect),1)


    #Draw player controlled block
    playerRect = pygame.Rect(player.X,player.Y,player.width,player.height)
    playerSurface = pygame.draw.rect(DISPLAYSURF, BLUE, playerRect)

    #Draw Ball
    ball.MoveBall()
    ballGraphic = pygame.draw.circle(DISPLAYSURF,BLACK,(ball.X,ball.Y),10)

    #Move the Player's position
    if player.moving:
        if player.direction == "Left":
            player.X -= 1
            if (player.X < 0):
                player.X = 0
        elif player.direction == "Right":
            player.X += 1
            if (player.X > 1120):
                player.X = 1120


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