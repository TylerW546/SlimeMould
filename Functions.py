import math

def distance(p1, p2):
   """Gets distance between two vector arrays"""
   return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

def normalizeAndScaleTo(vector, targetDistance):
   # Divide components of the vector by its magnitude, then multiply by the target distance
   realDist = distance([0,0],vector)
   fraction = targetDistance / realDist
   return([vector[0] * fraction, vector[1] * fraction])

def rotateVec(vec1, vec2):
   """Takes in two vectors, and rotates vector 1 by the angle of vector 2"""
   # This calculation uses the properties of imaginary numbers to rotate one vector by the angle of another without using trig.
   # Convert vectors (a,b) and (c, d) to a + bi and c + di.
   # A rotation on the imaginary plane is done by multiplying the two complex numbers together
   # Real component resulting from rotation = ac + bdi^2 or       ac - bd
   # Imaginary component resulting from rotation = adi + bci or   i(ad + bc)
   # Resulting number is ac-bd + i(ad+bc), so resulting vector is (ac-bd, ad+bc)
   x = vec1[0] * vec2[0] - vec1[1] * vec2[1]
   y = vec1[0] * vec2[1] + vec1[1] * vec2[0]
   return [x,y]

def getColor(colors, percent):
   """Returns a color from a list of colors. Picks based on a percentage, where percentage is the amount through the list that it travels."""
   # This is used for drawing different colors based on the intensity of the trails in DataMap.
   index = int(percent*len(colors))-1
   colorBase = colors[index]
   return (colorBase[0] * percent, colorBase[1] * percent, colorBase[2] * percent)