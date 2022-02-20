#Thumby Snake by OblivionCreator, 2022.

import time
import thumby
import math
import random

# BITMAP: width: 4, height: 4
snake_V = bytearray([14,15,15,14])
snake_H = bytearray([15,15,15,6])
snake_B = bytearray([15,15,15,15])
apple = bytearray([4,14,5,1])
appleSprite = thumby.Sprite(4, 4, apple, key=0)
thumby.display.fill(0) # Fill canvas to black
thumby.display.drawText('preload...', 0, 0, 1)
gameState = 1

offsetTime = 210

playSize = (18, 10)

class Snake:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.applePos = (0, 0)
        self.direction = 'right'
        self.body = [(self.x, self.y)]
        self.dMap = {
            'down': (0, 1, 'up'),
            'up': (0, -1, 'down'),
            'left': (-1, 0, 'right'),
            'right': (1, 0, 'left')
        }
        self.length = 3

    def changeDir(self, newDir):
        x, y, opp = self.dMap[newDir]
        if self.direction is not opp:
            self.direction = newDir
        
    def move(self):
        global gameState
        tempDirection = self.direction
        startTime = time.ticks_ms()
        while time.ticks_ms() < (startTime + offsetTime):
            tempDirection = self.inputHandler(tempDirection)
        self.changeDir(tempDirection)
        dX, dY, unususedlol = self.dMap[self.direction]
        self.x += dX
        self.y += dY
        self.body.insert(0, (self.x, self.y))
        self.body = self.body[0:self.length]

        if (self.x < 0) or (self.x >= 18) or (self.y < 0) or (self.y >= 10):
            gameState = 2
            return
        aX, aY = self.applePos
        if [self.x, self.y] == [aX, aY]:
            self.GenerateApple()
            self.length += 1
        
        for i in self.body[1:]:
            x, y = i
            if (x == self.x and y == self.y):
                gameState = 2
                return

    def inputHandler(self, tempDirection):
        if (thumby.buttonL.pressed()):
            return 'left'
        elif (thumby.buttonR.pressed()):
            return 'right'
        elif (thumby.buttonU.pressed()):
            return 'up'
        elif (thumby.buttonD.pressed()):
            return 'down'
        else:
            return tempDirection

    def draw(self):
        
        for i in self.body:
            x, y = i
            trueX = x*4
            trueY = y*4
            if self.body.index(i) == 0:
                snDir = {
                    'up': (snake_V, 0,0),
                    'down': (snake_V, 0,1),
                    'right': (snake_H, 0,0),
                    'left': (snake_H, 1,0)
                }
                
                sprite, mX, mY = snDir[self.direction]
                
                snakePart = thumby.Sprite(4, 4, sprite, key=0, mirrorX=mX, mirrorY=mY)
            else:
                snakePart = thumby.Sprite(4, 4, snake_B, key=0)
            snakePart.x = trueX
            snakePart.y = trueY
            aX, aY = self.applePos
            appleSprite.x, appleSprite.y = aX*4, aY*4
            thumby.display.drawSprite(appleSprite)
            thumby.display.drawSprite(snakePart)
            
    def GenerateApple(self):
        global offsetTime
        Valid = False
        tempX, tempY = 0,0
        while not Valid:
            tempX, tempY = random.randrange(0, 17), random.randrange(0, 9)
            Valid = True
            for x, y in self.body:
                if [tempX, tempY] == [x, y]:
                    Valid = False
                    break
        self.applePos = (tempX, tempY)
        if offsetTime > 105:
            offsetTime = offsetTime-5
    
    
# Begin main game loop that runs for the course of the game
snake = Snake()
loop = 0

snake.GenerateApple()
while gameState == 1:
    thumby.display.fill(0) # Fill canvas to black

    # DISPLAY SPRITES & UPDATE SCREEN
    snake.move()
    snake.draw()
    thumby.display.update()
