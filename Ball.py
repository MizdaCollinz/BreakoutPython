# Move Every X Frames
XFRAMES = 1

class Ball:
    def __init__(self,player,bricklist):
        self.X = 600
        self.Y = 200
        self.Speed = [0,1]
        self.player = player
        self.bricklist = bricklist
        self.started = False
        self.move = 0

    def MoveBall(self):
        global XFRAMES
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
            bricksHit = self.CheckHit()
            oldxspeed = self.Speed[0]
            oldyspeed = self.Speed[1]

            for brick in bricksHit:
                hit = self.bricklist.HitBrick(brick[0],brick[1])
                if hit is True:
                    oldx = self.X - self.Speed[0]
                    oldy = self.Y - self.Speed[1]
                    columns = self.CheckColumn(oldx)
                    rows = self.CheckRow(oldy)

                    if brick[0] in rows:
                        self.Speed[0] = - oldxspeed
                    if brick[1] in columns:
                        self.Speed[1] = - oldyspeed




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
                elif offset> (halfPlayer*0.20):
                    self.Speed[0] = 1
                elif offset< (-halfPlayer*0.75):
                    self.Speed[0] = -3
                elif offset< (-halfPlayer*0.5):
                    self.Speed[0] = -2
                elif offset< (-halfPlayer*0.20):
                    self.Speed[0] = -1

                #Move to next spot rather than being placed inside the player brick
                self.move = XFRAMES
                self.MoveBall()
        else:
            print "Invalid ball/player interaction"

    def CheckHit(self):
        #Find which brick was hit if hit
        self.Corners()

        columns = self.CheckColumn(self.X)
        rows = self.CheckRow(self.Y)

        brickList = []



        for i in range(2):
            for j in range(2):
                if rows[i] < 0 or columns[j] < 0:
                    continue
                else:
                    brickList.append((rows[i],columns[j]))
        return brickList


    def CheckColumn(self,X):
        #Two modulus 0-10 and 90-100
        if(X % 100) < 10:
            column = X/100

            if column == 0:
                columns = (0,-1)
            else:
                columns = (column-1,column)
        elif (X % 100) >= 90:
            column = X/100

            if column == 11:
                columns = (11,-1)
            else:
                columns = (column,column+1)
        else:
            columns = (X/100,-1)
        return columns

    def CheckRow(self,Y):
        if(Y % 40) < 10:
            row = Y/40
            if row == 4:
                rows = (3,-1)
            else:
                rows = (row-1,row)

        elif(Y % 40) >= 30:
            row = Y/40
            if(row < 3):
                rows = (row,row+1)

            else:
                rows = (row,-1)
        else:
            rows = (Y/40,-1)
        return rows


    def Corners(self):
        self.left = self.X - 10
        self.right = self.X + 10
        self.top = self.Y -10
        self.bottom = self.Y +10
