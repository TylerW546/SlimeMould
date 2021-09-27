import math

def distance(p1, p2):
   return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

def normalize(vector, targetDistance):
   realDist = distance([0,0],vector)
   fraction = targetDistance / realDist
   return([vector[0] * fraction, vector[1] * fraction])

def rotateVec(vec1, vec2):
   x = vec1[0] * vec2[0] - vec1[1] * vec2[1]
   y = vec1[0] * vec2[1] + vec1[1] * vec2 [0]
   return [x,y]

def getColor(colors, percent):
   index = int(percent*len(colors))-1
   colorBase = colors[index]
   
   return (colorBase[0] * percent, colorBase[1] * percent, colorBase[2] * percent)