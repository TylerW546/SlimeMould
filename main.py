import math
import pygame
from pygame.locals import *
import random
import time

SCREEN_WIDTH = 90
SCREEN_HEIGHT = 90
SCALE = 1

white = (255, 255, 255)
black = (0,0,0)
red = (255,0,0)
blue = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH * SCALE,SCREEN_HEIGHT * SCALE))

def main():
    from Slime import Slime
    from DataMap import DataMap

    slimePercent = .07
    slimeCount = int(SCREEN_WIDTH*SCREEN_HEIGHT*slimePercent)

    for i in range(slimeCount):
        # Random Pos, Random Angle
        Slime.add(Slime(x=random.randrange(5,SCREEN_WIDTH-5), y=random.randrange(5,SCREEN_HEIGHT-5), angle=random.randrange(0,360)))
        # Center, Random Angle
        #Slime.add(Slime(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, angle=random.randrange(0,360)))
        # Random Pos, = angle
        #Slime.add(Slime(x=random.randrange(5,SCREEN_WIDTH-5), y=random.randrange(5,SCREEN_HEIGHT-5)))
        # Center, = angle
        #Slime.add(Slime(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2))
        # Center, all to corner
        #Slime.add(Slime(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, vector = [1,1]))
    
    pause = False
    viewDataMap = True
    while (True):
        decay = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not(pause)
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    viewDataMap = not viewDataMap
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            decay = True
        
        screen.fill(black)

        if not pause:
            DataMap.diffuse()
            DataMap.decay()
            Slime.updateAll()
            
        if decay and viewDataMap:
            DataMap.diffuse()
            DataMap.decay()
        
        if viewDataMap:
            DataMap.draw()
        else:
            Slime.drawAll()

        pygame.display.update()
        
        time.sleep(.001)

if __name__ == "__main__":
    main()