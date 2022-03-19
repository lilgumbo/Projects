import os
import sys
import time
import pyautogui
import pydirectinput
import cv2
from Pac import *
from Board import *
from utils import *
import random
from signal import signal, SIGINT
from sys import exit 

start = 0
finish = 0

def main():
    #has-a composition relationship with ghosts but not pacman
    game = Board()
    #agent uses board object as map of enemies
    agent = Pac(game)
    openApplication()    
    setEmulSpeed()

    start = time.perf_counter()
    #while(1):
    for i in range(2):
        #agent.plotRouteRandom()
        agent.plotRouteGA()
        #agent.plotRouteGAPD()
        print("ROUTE: " + str(agent.route))
        agent.executeRoute()

#TAKEN FROM DEVDUNGION.COM
def handler(signal_received, frame):
    # Handle any cleanup here
    print("-----------------------------------")
    print("CTRL-C detected. Exiting gracefully")
    finish = time.perf_counter()
    gameTime = finish - start
    print("GAME TIME: " + str(gameTime))
    exit(0)

#Runs main
if __name__ == "__main__":
    signal(SIGINT, handler)
    main()