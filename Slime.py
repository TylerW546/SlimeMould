import math
import random
from Functions import *
from DataMap import DataMap

from main import *

class Slime():
    slimes = []
    
    sensor_angle = 22.5
    sensor_distance = 20
    turn_per_step = 10
    
    deposition_amount = 1
    
    leftSensorVec = [math.cos(math.radians(sensor_angle)), math.sin(math.radians(sensor_angle))]
    rightSensorVec = [math.cos(math.radians(-sensor_angle)), math.sin(math.radians(-sensor_angle))]
    
    vectorLeft = [math.cos(math.radians(turn_per_step)), math.sin(math.radians(turn_per_step))]
    vectorRight = [math.cos(math.radians(-turn_per_step)), math.sin(math.radians(-turn_per_step))]
    
    def __init__(self, x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2, vector=[1,0], angle=None, speed=3):
        self.x = x
        self.y = y
        
        self.vector = vector
        
        self.speed = speed
        self.turningAwayFromWall = None
        
        if angle != None:
            vx = math.cos(math.radians(angle)) * self.speed
            vy = math.sin(math.radians(angle)) * self.speed
            self.vector = [vx, vy]
    
    @staticmethod
    def add(slimeObject):
        Slime.slimes.append(slimeObject)
    
    @staticmethod
    def updateAll():
        for slime in Slime.slimes:
            slime.update()
    
    @staticmethod
    def drawAll():
        for slime in Slime.slimes:
            slime.draw()
    
    def update(self):
        for i in range(self.speed):
            self.sense()
            self.move()
            self.trail(DataMap.trail_map)
    
    def getSensorCoords(self):
        vector = rotateVec(normalize(self.vector, Slime.sensor_distance), Slime.leftSensorVec)
        sensor1 = [int(self.x + vector[0]), int(self.y + vector[1])]
        vector = normalize(self.vector, Slime.sensor_distance)
        sensor2 = [int(self.x + vector[0]), int(self.y + vector[1])]
        vector = rotateVec(normalize(self.vector, Slime.sensor_distance), Slime.rightSensorVec)
        sensor3 = [int(self.x + vector[0]), int(self.y + vector[1])]
        return [sensor1, sensor2, sensor3]
    
    def sense(self):
        sensor_coords = self.getSensorCoords()

        # Describes whether one sensor is out of the wall.
        # Will be set to true if even one sensor is out.
        outing = False
        
        # If front sensor is out
        if Slime.sensorOut(sensor_coords[1]):
            outing = True
            
            # If already turning away
            if self.turningAwayFromWall != None:
                # Check which way was decided to turn, turn that way
                if self.turningAwayFromWall == 0:
                    self.turnLeft()
                else:
                    self.turnRight()
            # Not turning away already
            else:
                # Generate a direction, turn and set turningAwayFromWall to rememeber that direction 
                if random.randint(0,1) == 0:
                    self.turnLeft()
                    self.turningAwayFromWall = 0
                else:
                    self.turnRight()
                    self.turningAwayFromWall = 1
        # Front not out so check other sensors and turn 
        else:
            if Slime.sensorOut(sensor_coords[0]):
                outing = True
                self.turnRight()
            if Slime.sensorOut(sensor_coords[2]):
                outing = True
                self.turnLeft()

        # All sensors in, so DataMap values are checked
        if not outing:
            # Not outing so not turning away from wall anymore, reset turningAwayFromWall
            if self.turningAwayFromWall != None:
                self.turningAwayFromWall = None
            
            # Get values of DataMap at sensor corrds
            sensor_values = [DataMap.trail_map[item[1]][item[0]] for item in sensor_coords]

            # Front > both, do nothing
            if sensor_values[1] > sensor_values[0] and sensor_values[1] > sensor_values[2]:
                pass
            # Front < both, so trails are on both sides, choose one at random
            elif sensor_values[1] < sensor_values[0] and sensor_values[1] < sensor_values[2]:
                if random.randint(0,1) == 0:
                    self.turnLeft()
                else:
                    self.turnRight()
            # Front > one of them, check which one is greater and turn that way
            # Right > Left
            elif sensor_values[2] > sensor_values[0]:
                self.turnRight()
            # Left > Right
            elif sensor_values[0] > sensor_values[2]:
                self.turnLeft()

    @staticmethod
    def sensorOut(sensor):
        if sensor[0] < 0 or sensor[0] >= SCREEN_WIDTH or sensor[1] < 0 or sensor[1] >= SCREEN_HEIGHT:
            return True
        return False
    
    def turnLeft(self):
        self.vector = normalize(rotateVec(self.vector, Slime.vectorLeft),1)
        
    def turnRight(self):
        self.vector = normalize(rotateVec(self.vector, Slime.vectorRight),1)
    
    def trail(self, trail_map):
        for i in range(int(self.y)-Slime.deposition_amount+1, int(self.y)+Slime.deposition_amount):
            for j in range(int(self.x)-Slime.deposition_amount+1, int(self.x)+Slime.deposition_amount):
                try:
                    trail_map[i][j] = 1.25
                except:
                    pass
                
    def move(self):
        self.x += self.vector[0]
        self.y += self.vector[1]
        self.hitWalls()
        
    def hitWalls(self):
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
            
        if self.x > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH
        if self.y > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT
        
    def thruWalls(self):
        if self.x < 0:
            self.x = SCREEN_WIDTH
        if self.y < 0:
            self.y = SCREEN_HEIGHT
            
        if self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y > SCREEN_HEIGHT:
            self.y = 0
        
    def draw(self):
        pygame.draw.rect(screen, white, (int(self.x*SCALE), int(self.y*SCALE), SCALE, SCALE), 0)