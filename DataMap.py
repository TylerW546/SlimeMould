from main import *
from Functions import *

class DataMap():
   trail_map = [[0 for i in range(SCREEN_WIDTH)] for j in range(SCREEN_HEIGHT)]

   diffuse_size = 2 # Radius including middle
   decay_factor = .85
   
   min_value = .05
   
   @staticmethod
   def diffuse():
      """Diffuses the DataMap. Neighboring squares bleed over into each other""" 
      old = []
      for i in range(len(DataMap.trail_map)):
         list = []
         for j in range(len(DataMap.trail_map[i])):
            list.append(DataMap.trail_map[i][j])
            DataMap.trail_map[i][j] = 0
         old.append(list)
   
      for kernel_center_i in range(0,len(old)):
         for kernel_center_j in range(0,len(old[kernel_center_i])):
            total = 0
            for kernel__i in range(kernel_center_i-DataMap.diffuse_size+1, kernel_center_i+DataMap.diffuse_size):
               for kernel__j in range(kernel_center_j-DataMap.diffuse_size+1, kernel_center_j+DataMap.diffuse_size):
                    try:
                        total += old[kernel__i][kernel__j]/9
                    except:
                        pass
            if kernel_center_i > 0 and kernel_center_i < SCREEN_HEIGHT and kernel_center_j > 0 and kernel_center_j < SCREEN_WIDTH:
                DataMap.trail_map[kernel_center_i][kernel_center_j] = total
      
   
   @staticmethod
   def decay():
      """Every value in DataMap decays by a factor (DataMap.decay_factor)"""
      for i in range(len(DataMap.trail_map)):
         for j in range(len(DataMap.trail_map[i])):
            if DataMap.trail_map[i][j] < DataMap.min_value:
               DataMap.trail_map[i][j] = 0 
            else:
               DataMap.trail_map[i][j] *= DataMap.decay_factor 
   
   @staticmethod
   def draw():
      """Draws the DataMap to the screen. Draws every element in the array as rectangles, so it can be laggy at high resolutions"""
      for i in range(len(DataMap.trail_map)):
         for j in range(len(DataMap.trail_map[i])):
               if DataMap.trail_map[i][j] > 0:
                  value = DataMap.trail_map[i][j]
                  percent = min(max(value,0),1)
                  
                  #color = getColor([(255,255,255), (0,0,255), (120,120,0), (0,255,0)], percent)
                  #color = getColor([(0,255,0)], percent)
                  color = (0,255*percent,0)
                  pygame.draw.rect(screen, color, (int(j*SCALE),int(i*SCALE),SCALE,SCALE), 0)
                  #pygame.draw.circle(screen, (0,255*min(max(DataMap.trail_map[i][j],0),1),0), (int(j*SCALE+SCALE*.5), int(i*SCALE+SCALE*.5)), SCALE)
