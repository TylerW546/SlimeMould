import math
import pygame
from pygame.locals import *
import random
import time

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
SCALE = 1

white = (255, 255, 255)
black = (0,0,0)
red = (255,0,0)
blue = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH * SCALE,SCREEN_HEIGHT * SCALE))

colorCodes = [-1,0]



def main():
    from Slime import Slime
    from DataMap import DataMap

    # Slimes are generated based on a percentage of the overall screen area.
    slimePercent = .03
    slimeCount = int(SCREEN_WIDTH*SCREEN_HEIGHT*slimePercent)

    Slime.genSlimes(slimeCount)
    
    # Pause will be toggled when the user presses space. This will stop all movement so the user can see the frame clearly
    pause = False
    # viewDataMap will be toggled by the arrow keys. If true, it will show the trails left behind by the organisms.
    # If false, it will only show the organisms
    viewDataMap = True

    for i in range(2000):
        if i % 2000 == 0:
            drawCode = [random.choice(colorCodes), random.choice(colorCodes), random.choice(colorCodes)]
            if -1 not in drawCode:
                drawCode[random.choice([0,1,2])] = -1
            DataMap.clear()
            Slime.genSlimes(slimeCount)
            
        
        # When true, decay will speed up the decaying process. Decaying will happen slower when decay is false.
        decay = False
        # Loop over pygame events
        for event in pygame.event.get():
            # If the screen should quit, quit.
            if event.type == QUIT:
                pygame.quit()
                exit()
            # If a key is pressed
            if event.type == KEYDOWN:
                # If that key is the space bar
                if event.key == pygame.K_SPACE:
                    pause = not(pause)
                # If the key is left or right arrow
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    viewDataMap = not viewDataMap
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            decay = True
        
        screen.fill(black)

        # Update the datamap and all slimes if the screen is not paused
        if not pause:
            DataMap.diffuse()
            DataMap.decay()
            Slime.updateAll()
        
        # If extra decay should happen
        if decay and viewDataMap:
            DataMap.diffuse()
            DataMap.decay()

        # Draw what should be drawn        
        if viewDataMap:
            DataMap.draw(drawCode)
        else:
            Slime.drawAll()

        # Update display
        pygame.display.update()
        
        #pygame.image.save(screen, "output_frames/frame-" + str(i) + ".jpeg")
        
        # Wait some time before next frame
        # time.sleep(.001)

if __name__ == "__main__":
    main()