import os
import sys
import time
import pyautogui
import pydirectinput
import random
from PIL import Image 
from main import *
from utils import *

class Ghost:
    def __init__(self):
        pass
    def update(self):
        if(self.coordinate[0] > 8 and self.coordinate[0] < 14 and
           self.coordinate[1] > 11 and self.coordinate[1] < 14):
            self.trapped = True 
        else:
            self.trapped = False
    def printDetails(self):
        print(self.name + ": " + str(self.coordinate) + " trapped: " + str(self.trapped))

class Blinky(Ghost):
    def __init__(self):
        self.coordinate = [10, 10]
        self.trapped = False
        self.name = "Blinky"
        self.color = "red"
            
class Pinky(Ghost):
    def __init__(self):
        self.coordinate = [10,12]
        self.trapped = True 
        self.name = "Pinky"
        self.color = "pink"
    
class Inky(Ghost):
    def __init__(self):
        self.coordinate = [10,12]
        self.trapped = True 
        self.name = "Inky"
        self.color = "blue"

class Clyde(Ghost):
    def __init__(self):
        self.coordinate = [10,12]
        self.trapped = True 
        self.name = "Clyde"
        self.color = "brown"
    