import spWindow
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import csv
import os 
import random 
import numpy as np 
import tkinter as tk 

def main():
    prompt1 = 'Please construct a playlist to listen to while traveling'
    prompt2 = 'Please construct a playlist to listen to during personal maintenance'

    frameRadar = spWindow.RadarWindow(prompt1)
    frameRadar.window.mainloop()

    frameSlider = spWindow.SpWindow(prompt2)
    frameSlider.window.mainloop()

#Runs main
if __name__ == "__main__":
    main()

### STUDY PROCEDURE ###
# Prompt user to allow access to Spotify account's top artists (adjusted so that artists are hand-picked)
# Demographic Questions
#   Age / Gender / Music sophistication / Visual working memory / 
#   tech-saviness / Spotify Usage / familiarity with rec-systems / 
#   attitude towards rec-systems
# Have user create playlist for travelling
# Have user create playlist for personal maintenance (Latin Square counterbalance)
# Evaluation Questions (7-point likert scale)
#    The songs recommended to me are of various kinds
#    The songs recommended to me are similar to each other
#    This recommender system helped me discover new songs
#    I haven't heard of some songs in the list before
#    This recommender system helped me find ideal songs
#    Using this recommender system to find what I like was easy
#    This recommender system gave me good suggestions
#    Overall, I am satisfied with this recommender system
#    I am convinced of the songs recommended to me
#    This recommender system made me more confident about my selection/decision
#    I will use this recommender system again
#    I will tell my friends about this recommender system
#    I will keep the songs recommended to that I can listen again
# Open-ended exit questions
#    Liklihood of attribute usage for all 14 attribute available
#    Suggestions for other visual techniques
#
### INTERACTION LOG ###
# Number of times a musical attribute was changed
# Number of times individual attributes were changed
# Number of times the "Calculate Rec" button was clicked
# Number of times the dislike button was clicked
# Number of times the "keep" button was clicked
# Total number of clicks on all componenets of the interface
#