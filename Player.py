# Imports
import pygame, sys, win32api
from pygame.locals import *


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

    def MovePlayer(self):
        if self.direction == "Left":
            self.X -= 1
            if (self.X < 60):
                self.X = 60
        elif self.direction == "Right":
            self.X += 1
            if (self.X > 1140):
                self.X = 1140

    def Defeat(self):
        win32api.MessageBox(0,  'You ran out of lives!','Defeat')
        pygame.quit()
        sys.exit(0)

    def Victory(self):
        win32api.MessageBox(0, 'You somehow got them all, Bravo!', 'Victory')
        pygame.quit()
        sys.exit(0)