# Imports
import pygame, sys, win32api
from pygame.locals import *

pygame.init()

#Frame Rate Assignment
FPS = 60
fpsClock = pygame.time.Clock()
fpsClock.tick(FPS)

#Move Every X Frames
XFRAMES = 2

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
        self.X = 540
        self.Y = 790
        #Size
        self.width = 120
        self.height = 20
        #Movement
        self.moving = False
        self.direction = "Left"

    def Defeat(self):
        win32api.MessageBox(0,  'You ran out of lives!','Defeat')
        pygame.quit()
        sys.exit(0)

class Ball:

    def __init__(self,player,bricklist):
        self.X = 600
        self.Y = 200
        self.Speed = [0,1]
        self.player = player
        self.started = False
        self.move = 0

    def MoveBall(self):
        if self.move < XFRAMES:
            self.move+= 1
            return
        else:
            self.move = 0

        self.X += self.Speed[0]
        if self.X < 10:
            self.X = 10
            self.Speed[0] = -self.Speed[0]
        elif self.X > 1190:
            self.X = 1190
            self.Speed[0] = -self.Speed[0]

        self.Y += self.Speed[1]
        if self.Y < 10:
            self.Y = 10
            self.Speed[1] = -self.Speed[1]
        elif self.Y > 800:
            #ResetBall
            self.resetBall()

        #Check for collisions with other objects
        if self.Y > (770): #WindowSize - Ball Radius - Player Height
            self.CheckPlayer()
        elif self.Y <170:
            self.CheckHit()


    def resetBall(self):
        #Lose a life
        self.player.Lives -= 1
        if self.player.Lives == 0:
            self.player.Defeat()

        #Reset Position and speed
        self.Speed = [0,1]
        self.X = 600
        self.Y = 200

    def CheckPlayer(self):
        self.Corners()
        halfPlayer = self.player.width / 2


        if self.left > (self.player.X + halfPlayer) or self.right < (self.player.X - halfPlayer):
            #No Contact
            print("Ball is completely separate from player")
            pass
        elif self.right > (self.player.X - halfPlayer) and self.left < (self.player.X + halfPlayer):
            #Contact with player
            if self.Speed[1] > 0: #If falling, send ball upward

                print("Contact with player")
                self.Speed[1] = -self.Speed[1]

                #Determine x axis speed change
                #Calculate offset of the hit from the centre of the player brick
                offset = self.X - self.player.X


                print("The offset is {}").format(offset)
                if offset > (halfPlayer*0.75):
                    self.Speed[0]= 3
                elif offset> (halfPlayer*0.50):
                    self.Speed[0]= 2
                elif offset> (halfPlayer*0.25):
                    self.Speed[0] = 1
                elif offset< (-halfPlayer*0.75):
                    self.Speed[0] = -3
                elif offset< (-halfPlayer*0.5):
                    self.Speed[0] = -2
                elif offset< (-halfPlayer*0.25):
                    self.Speed[0] = -1

                #Move to next spot rather than being placed inside the player brick
                self.move = XFRAMES
                self.MoveBall()
        else:
            print "Ball X is {} and Y is {}".format(self.X,self.Y)
            print "Player is at {}".format(self.player.X)

    def CheckHit(self):
        #Find which brick was hit if hit
        self.Corners()

        columns = self.CheckColumn()
        rows = self.CheckRow()

        brickList = []



        for i in range(2):
            for j in range(2):
                if rows[i] < 0 or columns[j] < 0:
                    continue
                else:
                    brickList.append((rows[i],columns[j]))

        return brickList


    def CheckColumn(self):
        #Two modulus 0-10 and 90-100
        if(self.X % 100) < 10:
            column = self.X/100
            columns = (column-1,column)
        elif (self.X % 100) >= 90:
            column = self.X/100
            columns = (column,column+1)
        else:
            columns = (self.X/100,-1)
        return columns

    def CheckRow(self):
        if(self.Y % 40) < 10:
            row = self.Y/40
            rows = (row-1,row)
        elif(self.Y % 40) >= 30:
            row = self.Y/40
            if(row<3):
                rows = (row,row+1)
            else:
                rows = (row,-1)
        else:
            rows = (self.Y/40,-1)

        return rows


    def Corners(self):
        self.left = self.X - 10
        self.right = self.X + 10
        self.top = self.Y -10
        self.bottom = self.Y +10

class BrickList:

    def __init__(self):
        self.flags = []
        for i in range(12):
            self.flags.append([1] * 4)
    def HitBrick(self,x,y):
        if self.flags[x][y] == 1:
            self.flags[x][y] = 0
            return True
        else:
            return False




# Resolution of Display Surface
DISPLAYSURF = pygame.display.set_mode((1200,800))
pygame.display.set_caption('Simple Breakout Game')


#Initialise main objects
player = Player()
flagList = BrickList()
ball = Ball(player,flagList)

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