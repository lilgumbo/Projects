import os
import sys
import time
import pyautogui
import pydirectinput
import random
from PIL import Image
from main import *

#Starts the application and pauses at initial state
def openApplication():
    os.startfile("Pac-Man\Pac-Man-Game.NES")
    time.sleep(3)
    pydirectinput.click(960, 540)
    time.sleep(1.5)
    pydirectinput.press('enter')
    time.sleep(3.85)
    pydirectinput.press('enter')

#Sets the emulation speed to 50%
def setEmulSpeed():
    NESButton = pyautogui.locateOnScreen('PacScripts\sim_button.png', confidence=0.9)
    NESButton = pyautogui.center(NESButton)
    pydirectinput.click(NESButton.x, NESButton.y)
    EMSButton = pyautogui.locateOnScreen('PacScripts\emul_speed_button.png', confidence=0.9)
    EMSButton = pyautogui.center(EMSButton)
    pydirectinput.click(EMSButton.x, EMSButton.y)
    setSpeedButton = pyautogui.locateOnScreen('PacScripts\set_speed_button.png', confidence=0.9)
    setSpeedButton = pyautogui.center(setSpeedButton)
    pydirectinput.click(setSpeedButton.x, setSpeedButton.y)
    pydirectinput.press('3')
    pydirectinput.press('5')
    pydirectinput.press('enter')

#Returns amount of cells needed to reach point
def findDistance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

#Returns the direction opposite to player
def reverse(direction):
    if(direction == "right"):
        return "left"
    elif(direction == "left"):
        return "right"
    elif(direction == "up"):
        return "down"
    elif(direction == "down"):
        return "up"
    else:
        return -1

#converts a screen pixel coordinate into board coordinate
def convertPosToCoord(position):
    pxFromLeft = position[0] - 505
    pxFromTop = position[1] - 150
    xIndex = pxFromLeft//32.67 
    yIndex = pxFromTop//32.67
    return [xIndex + 1, yIndex + 1]

#determines if two pixels are the same in color (With uncertainty)
def matchPixels(pix1, pix2):
    if(abs(pix1[0] - pix2[0]) < 10 and
       abs(pix1[1] - pix2[1]) < 10 and
       abs(pix1[2] - pix2[2]) < 10):
        return True
    return False 

#moves 2-Dimensionally one space / pos=-1 results in decrement
def increment(direction, _coordinate, pos=1):
    coordinate = _coordinate.copy()
    if(direction == "left"):
        coordinate[0] -= (1 * pos)
    elif(direction == "right"):
        coordinate[0] += (1 * pos)
    elif(direction == "up"):
        coordinate[1] -= (1 * pos)
    else:
        coordinate[1] += (1 * pos)
    return coordinate

#finds the nearest intersection ahead of a coordinate on a 2D grid
def findNearestDecisionPoint(_coordinate, direction, board):
    coordinate = _coordinate.copy()
    #convert to int
    coordinate[0] = int(coordinate[0])
    coordinate[1] = int(coordinate[1])
    while(1):
        coordinate = increment(direction, coordinate)
        if(board[coordinate[1]][coordinate[0]] == 1):
            coordinate = increment(direction, coordinate, -1)
            break 
        intersection = checkIfIntersection(coordinate, direction, board)
        if(intersection):
            break
    return coordinate

#finds the nearest pellet ahead of a coordinate on a 2D grid
def findNearestPellet(_coordinate, direction, board):
    original = _coordinate.copy()
    coordinate = _coordinate.copy()
    #convert to int
    coordinate[0] = int(coordinate[0])
    coordinate[1] = int(coordinate[1])
    while(1):
        coordinate = increment(direction, coordinate)
        if(board[coordinate[1]][coordinate[0]] == 1):
            coordinate = increment(direction, coordinate, -1) 
        intersection = checkIfIntersection(coordinate, direction, board)
        if(intersection):
            options = checkDecisionOptions(coordinate, direction, board)
            #if(len(options) == 1):
            print("ayoooooooooooo")
            print(coordinate)
            print(direction)
            print(options)
            direction = options[0]
            continue
            #else:
            #    #recurse multiple directions
            #    pellets = []
            #    minDist = 1000
            #    for choice in options:
            #        pellets.append(findNearestPellet(coordinate, choice, board))
            #    for coord in pellets:
            #        x = findDistance(original, coord)
            #        if(x < minDist):
            #            minDist = x
            #            coordinate = coord
            #    break 
        if(board[coordinate[1]][coordinate[0]] == 0):
            break 
    return coordinate

#determines whether or not a coordinate is an intersection given the board
def checkIfIntersection(coordinate, direction, board):
    #convert to int
    coordinate[0] = int(coordinate[0])
    coordinate[1] = int(coordinate[1])
    #horizontal
    if(direction == "left" or direction == "right"):
        if(board[coordinate[1]][coordinate[0] + 1] == 0 and
           board[coordinate[1]][coordinate[0] - 1] == 0):
            if(board[coordinate[1] + 1][coordinate[0]] == 1 and
               board[coordinate[1] - 1][coordinate[0]] == 1):
                return False
    #vertical
    else:
        if(board[coordinate[1] + 1][coordinate[0]] == 0 and
           board[coordinate[1] - 1][coordinate[0]] == 0):
            if(board[coordinate[1]][coordinate[0] + 1] == 1 and
               board[coordinate[1]][coordinate[0] - 1] == 1):
                return False
    return True

#finds the open path routes for a given intersection on a 2D board
def checkDecisionOptions(coordinate, direction, board):
    #convert to int
    print(coordinate)
    print(direction)
    coordinate[0] = int(coordinate[0])
    coordinate[1] = int(coordinate[1])
    options = []
    if(board[coordinate[1]][coordinate[0] - 1] == 0):
        options.append("left")
    if(board[coordinate[1] + 1][coordinate[0]] == 0):
        options.append("down")
    if(board[coordinate[1] - 1][coordinate[0]] == 0):
        options.append("up")
    if(board[coordinate[1]][coordinate[0] + 1] == 0):
        options.append("right")
    opposite = reverse(direction)
    if(opposite in options):
        options.remove(opposite)
    return options

def locateGhosts():
    locations = []
    for i in range(4):
        locations.append(pyautogui.locateCenterOnScreen('PacScripts/red' + str(i+1) + '.png', confidence=0.5, grayscale=True))
        locations.append(pyautogui.locateCenterOnScreen('PacScripts/blue' + str(i+1) + '.png', confidence=0.5, grayscale=True))
        locations.append(pyautogui.locateCenterOnScreen('PacScripts/pink' + str(i+1) + '.png', confidence=0.5, grayscale=True))
        locations.append(pyautogui.locateCenterOnScreen('PacScripts/brown' + str(i+1) + '.png', confidence=0.5, grayscale=True))
    removeNones = filter(None.__ne__, locations)
    locations = list(removeNones)
    if(locations == []):
        return None
    else:
        return locations

#finds direction to maxQuad
def findProximity(pacQuad, maxQuad):
    directions = []
    if(pacQuad == maxQuad):
        return directions 
    if(pacQuad == 0):
        if(maxQuad == 1 or maxQuad == 3):
            directions.append("right")
        if(maxQuad == 2 or maxQuad == 3):
            directions.append("down")
    elif(pacQuad == 1):
        if(maxQuad == 0 or maxQuad == 2):
            directions.append("left")
        if(maxQuad == 2 or maxQuad == 3):
            directions.append("down")
    elif(pacQuad == 2):
        if(maxQuad == 1 or maxQuad == 3):
            directions.append("right")
        if(maxQuad == 0 or maxQuad == 1):
            directions.append("up")
    else:
        if(maxQuad == 0 or maxQuad == 2):
            directions.append("left")
        if(maxQuad == 0 or maxQuad == 1):
            directions.append("up")
    return directions

def findNearestGhost(coordinate, ghosts):
    closest = []
    maxVal = 11
    for i in range(len(ghosts) - 1):
        if(ghosts[i].trapped == False):
            dist = findDistance(ghosts[i].coordinate, coordinate)
            if(dist < maxVal):
                closest = ghosts[i].coordinate 
                maxVal = dist
    if(closest == []):
        return None 
    else:
        return closest 