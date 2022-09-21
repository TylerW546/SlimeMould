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
    
    # Sensor angle doesn't change, so we can calculate the vector offsets of the sensors beforehand.
    # This way, we can just turn the vectors instead of doing too many math.cos or math.sin calls.
    leftSensorVec = [math.cos(math.radians(sensor_angle)), math.sin(math.radians(sensor_angle))]
    rightSensorVec = [math.cos(math.radians(-sensor_angle)), math.sin(math.radians(-sensor_angle))]
    
    # We can also precalculate the vectors needed to turn left and right so we don't have to call math.cos or math.sin later.
    vectorLeft = [math.cos(math.radians(turn_per_step)), math.sin(math.radians(turn_per_step))]
    vectorRight = [math.cos(math.radians(-turn_per_step)), math.sin(math.radians(-turn_per_step))]
    
    def __init__(self, x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2, velocity=[1,0], angle=None, speed=3):
        self.x = x
        self.y = y
        
        self.velocity = velocity
        
        self.speed = speed
        self.turningAwayFromWall = None
        
        # Translate angle and speed to a velocity vector
        if angle != None:
            vx = math.cos(math.radians(angle)) * self.speed
            vy = math.sin(math.radians(angle)) * self.speed
            self.velocity = [vx, vy]
    
    @staticmethod
    def add(slimeObject):
        """Adds a slime object to the class level slime object list"""
        Slime.slimes.append(slimeObject)
    
    @staticmethod
    def updateAll():
        """Updates all slimes in the class level slime object list"""
        for slime in Slime.slimes:
            slime.update()
    
    @staticmethod
    def drawAll():
        """Draws all slimes in the class level slime object list"""
        for slime in Slime.slimes:
            slime.draw()
    
    def update(self):
        """Updates the slime by sensing, moving, and depositing a trail"""
        for i in range(self.speed):
            self.sense()
            self.move()
            self.trail(DataMap.trail_map)
    
    def getSensorCoords(self):
        """Uses the slime's velocity and the precalculated sensor vectors to generate coordinates of sensors."""
        # Calculate unit vector of slime's velocity multiplied by the sensor distance. This is the relative position of the front facing sensor.
        front_vector = normalizeAndScaleTo(self.velocity, Slime.sensor_distance)
        # Calculate absolute position of the front facing sensor by adding slime's position to the relative position
        front_sensor = [int(self.x + vector2[0]), int(self.y + vector2[1])]
        
        # Calculate relative position of left vector by getting the rotation of the front_vector by the angle of the left sensor vector. 
        left_vector = rotateVec(front_vector, Slime.leftSensorVec)
        # Calculte the absolute position of the left sensor
        left_sensor = [int(self.x + vector1[0]), int(self.y + vector1[1])]

        # Repeat operations using the right sensor vector to get the right sensor coordinates
        right_vector = rotateVec(front_vector, Slime.rightSensorVec)
        right_sensor = [int(self.x + vector3[0]), int(self.y + vector3[1])]

        return [left_sensor, front_sensor, right_sensor]
    
    def sense(self):
        """Senses whether the slime is approaching a wall. If so, turn away. IF not, sense and turn towards the highest value on the DataMap"""
        
        sensor_coords = self.getSensorCoords()

        # Describes whether one sensor is out of the wall boundaries.
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
        """Returns whether the sensor is outside of the screen."""
        if sensor[0] < 0 or sensor[0] >= SCREEN_WIDTH or sensor[1] < 0 or sensor[1] >= SCREEN_HEIGHT:
            return True
        return False
    
    def turnLeft(self):
        """Turns left by rotating velocity by precalculated left turn vector"""
        self.velocity = normalizeAndScaleTo(rotateVec(self.velocity, Slime.vectorLeft),1)
        
    def turnRight(self):
        """Turns left by rotating velocity by precalculated right turn vector"""
        self.velocity = normalizeAndScaleTo(rotateVec(self.velocity, Slime.vectorRight),1)
    
    def trail(self, trail_map):
        """Deposits a value of 1.25 on the DataMap at the slime's position."""
        for i in range(int(self.y)-Slime.deposition_amount+1, int(self.y)+Slime.deposition_amount):
            for j in range(int(self.x)-Slime.deposition_amount+1, int(self.x)+Slime.deposition_amount):
                try:
                    trail_map[i][j] = 1.25
                except:
                    pass
                
    def move(self):
        """Add velocity to position, then handle what happens if the slime hits a wall."""
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.hitWalls()
        #self.thruWalls()
        
    def hitWalls(self):
        """Hitting walls. Slime cannot travel farther than wall coordinates"""
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
            
        if self.x > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH
        if self.y > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT
        
    def thruWalls(self):
        """Slimes pass through wall and come out on the other side of the screen."""
        if self.x < 0:
            self.x = SCREEN_WIDTH
        if self.y < 0:
            self.y = SCREEN_HEIGHT
            
        if self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y > SCREEN_HEIGHT:
            self.y = 0
        
    def draw(self):
        """Draw the slime to the screen"""
        pygame.draw.rect(screen, white, (int(self.x*SCALE), int(self.y*SCALE), SCALE, SCALE), 0)