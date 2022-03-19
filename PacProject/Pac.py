import os
import sys
import time
import pyautogui
import pydirectinput
import random
from PIL import Image 
from main import *
from utils import *

class Pac:
    def __init__(self, state):
        self.coordinate = [10, 20]
        self.position = []
        self.direction = "left"
        self.board = state
        self.route = []
        self.routeCO = []
        self.quadrant = 3
    def update(self):
        print("Updating agent...")
        locations = []
        z = True
        while(locations == []):
            if(not z):
                time.sleep(1)
                z == False
            P1left = pyautogui.locateOnScreen('PacScripts\P1left.png', confidence=0.8)
            P1right = pyautogui.locateOnScreen('PacScripts\P1right.png', confidence=0.8)
            P1up = pyautogui.locateOnScreen('PacScripts\P1up.png', confidence=0.8)
            P1down = pyautogui.locateOnScreen('PacScripts\P1down.png', confidence=0.8)
            P2 = pyautogui.locateOnScreen('PacScripts\P2.png', confidence=0.7)
            locations = list(pyautogui.locateAllOnScreen('PacScripts\P3left.png', confidence=0.8)) #locateAllOnScreen?       
            P3right = pyautogui.locateOnScreen('PacScripts\P3right.png', confidence=0.8)
            P3up = pyautogui.locateOnScreen('PacScripts\P3up.png', confidence=0.8)
            P3down = pyautogui.locateOnScreen('PacScripts\P3down.png', confidence=0.8)
            locations.append(P1left)
            locations.append(P1right)
            locations.append(P1up)
            locations.append(P1down)
            locations.append(P2)
            locations.append(P3right)
            locations.append(P3up)
            locations.append(P3down)
            for i in range(len(locations) - 1):
                if locations[i] != None:
                    pos = pyautogui.center(locations[i])
                    if pos.x > 1150:
                        locations[i] = None
            removeNones = filter(None.__ne__, locations)
            locations = list(removeNones)
        self.position = pyautogui.center(locations[-1])
        self.coordinate = convertPosToCoord(self.position)
        if(self.coordinate[0] >= 10):
            if(self.coordinate[1] >= 13):
                self.quadrant = 3
            else:
                self.quadrant = 1
        else:
            if(self.coordinate[1] >= 13):
                self.quadrant = 2
            else:
                self.quadrant = 0
        print("PacMan updated! pos = " + str(self.coordinate) + "/dir = " + str(self.direction))

    #plots a route that randomly changes direction at each intersection
    #takes used from a paused game and must update state
    def plotRouteRandom(self):
        print("plotting random route...")
        self.update()
        #self.board.update()
        step = self.coordinate.copy()
        #create 5 decisions
        for i in range(5):
            decision = findNearestDecisionPoint(step, self.direction, self.board.state)
            options = checkDecisionOptions(decision, self.direction, self.board.state)
            x = random.randint(0, len(options) - 1)
            choice = options[x]
            self.route.append(choice)
            self.direction = choice 
            step = decision.copy()
            self.routeCO.append(step)
            #print("intersection: " + str(decision))
            #print("options: " + str(options))
            #print("choice: " + choice)
            #print("---------------------------")  

    #plots a route depending on long range ghost avoidance
    def plotRouteGA(self):
        print("plotting GAY route...")
        self.update()
        preferred = []
        nearest = findNearestGhost(self.coordinate, self.board.ghosts)
        if(nearest != None):
            print("Closest ghost: " + str(nearest))
            if(nearest[0] > self.coordinate[0]):
                preferred.append("left")
            if(nearest[0] < self.coordinate[0]):
                preferred.append("right")
            if(nearest[1] > self.coordinate[1]):
                preferred.append("up")
            if(nearest[1] < self.coordinate[1]):
                preferred.append("down")
            if(nearest[1] == self.coordinate[1]):
                preferred.append("up")
                preferred.append("down")
            if(nearest[0] == self.coordinate[0]):
                preferred.append("right")
                preferred.append("left")
        print("Preferred: " + str(preferred))
        step = self.coordinate.copy()
        #create 5 decisions
        for i in range(5):
            decision = findNearestDecisionPoint(step, self.direction, self.board.state)
            options = checkDecisionOptions(decision, self.direction, self.board.state)
            nearestPellet = findNearestPellet(decision, self.direction, self.board.pelletState)
            best = []
            print("Nearest Pellet: " + str(nearestPellet))
            if(nearestPellet[0] > decision[0]):
                best.append("right")
            if(nearestPellet[0] < decision[0]):
                best.append("left")
            if(nearestPellet[1] > decision[1]):
                best.append("down")
            if(nearestPellet[1] < decision[1]):
                best.append("up")
            print("Best: " + str(best))
            choice = best[0]
            optionsPrime = []
            for preference in preferred:
                if(preference in options):
                    optionsPrime.append(preference)
            for p in best:
                if(optionsPrime != []):
                    if(p in optionsPrime):
                        choice = p
                        break 
                else:
                    if(p in options):
                        choice = p
                        break 
            self.route.append(choice)
            self.direction = choice 
            step = decision.copy()
            self.routeCO.append(step)
            print("intersection: " + str(decision))
            print("options: " + str(options))
            print("choice: " + choice)
            print("---------------------------")  

#plots a route depending on long range ghost avoidance and pellet density 
    def plotRouteGAPD(self):
        print("plotting EPIC route...")
        self.update()
        preferred = []
        nearest = findNearestGhost(self.coordinate, self.board.ghosts)
        if(nearest != None):
            print("Closest ghost: " + str(nearest))
            if(nearest[0] > self.coordinate[0]):
                preferred.append("left")
            if(nearest[0] < self.coordinate[0]):
                preferred.append("right")
            if(nearest[1] > self.coordinate[1]):
                preferred.append("up")
            if(nearest[1] < self.coordinate[1]):
                preferred.append("down")
            if(nearest[1] == self.coordinate[1]):
                preferred.append("up")
                preferred.append("down")
            if(nearest[0] == self.coordinate[0]):
                preferred.append("right")
                preferred.append("left")
        print("Preferred: " + str(preferred))
        pellets = self.board.weighQuadrants()
        maxVal = max(pellets)
        maxQuad = pellets.index(maxVal)
        toMax = findProximity(self.quadrant, maxQuad)
        print("pac: " + str(self.quadrant) + "/max: " + str(maxQuad))
        print("ToMax: " + str(toMax))
        step = self.coordinate.copy()
        #create 5 decisions
        for i in range(5):
            decision = findNearestDecisionPoint(step, self.direction, self.board.state)
            options = checkDecisionOptions(decision, self.direction, self.board.state)
            x = random.randint(0, len(options) - 1)
            choice = options[x]
            optionsPrime = []
            for preference in preferred:
                if(preference in options):
                    optionsPrime.append(preference)
            if(toMax != []):
                for best in toMax:
                    if(optionsPrime != []):
                        if(best in optionsPrime):
                            choice = best
                            break 
                    else:
                        if(best in options):
                            choice = best
                            break 
            self.route.append(choice)
            self.direction = choice 
            step = decision.copy()
            self.routeCO.append(step)
            print("intersection: " + str(decision))
            print("options: " + str(options))
            print("choice: " + choice)
            print("---------------------------")  

    #Starts from paused game state and executes current route
    def executeRoute(self):
        print("executing route...")
        rDist = []
        xTime = 0.407
        #print(self.routeCO)

        d = float(findDistance(self.coordinate, self.routeCO[0]))
        rDist.append(d * xTime)
        for i in range(len(self.route) - 1):
            d = float(findDistance(self.routeCO[i], self.routeCO[i+1]))
            rDist.append(d * xTime)
        print(rDist)             
        pydirectinput.keyDown(self.route[0])
        for i in range(len(self.route)):
            if(i == 0):
                pydirectinput.press('enter')
                time.sleep(float(rDist[0]))
                pydirectinput.keyUp(self.route[0])
            else:
                pydirectinput.keyDown(self.route[i])
                time.sleep(float(rDist[i]))
                pydirectinput.keyUp(self.route[i])
                self.direction = self.route[i]
        pydirectinput.press('enter')
        print("Route Executed")
        self.board.update()
        self.route = []
        self.routeCO = []
   