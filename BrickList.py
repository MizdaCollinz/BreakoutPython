class BrickList:

    def __init__(self):
        self.flags = []
        for i in range(12):
            self.flags.append([1] * 4)
    def HitBrick(self,x,y):

        if self.flags[y][x] == 1:
            self.flags[y][x] = 0
            return True
        else:
            return False

    def CheckWin(self):
        for list in self.flags:
            for flag in list:
                if flag == 1:
                    #Found a brick not broken
                    return False

        #No brick is still active
        return True
