import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import csv
import os 
import sys
import random 
import numpy as np
import tkinter as tk  
import webbrowser
import plotly.express as px
import plotly.graph_objects as go 
import pandas as pd
//removed to avoid other accessing my account
username = ''
client_id =''
client_secret = ''

redirect_uri = 'http://localhost:7777/callback'
scope = 'user-top-read user-read-currently-playing'
token = util.prompt_for_user_token(username=username, 
                                   scope=scope, 
                                   client_id=client_id,   
                                   client_secret=client_secret,     
                                   redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth = token)

class SpWindow:
    def __init__(self, prompt):
        self.window = self.configureWindow()
        self.images = [tk.PhotoImage(file='guiScripts/toggle-button-on.png'), tk.PhotoImage(file='guiScripts/toggle-button-off.png'), tk.PhotoImage(file='guiScripts/recommend-button.png'), tk.PhotoImage(file='guiScripts/playButton.png'), tk.PhotoImage(file='guiScripts/discardButton.png')]
        self.artistIds = []
        self.artistVar = []
        self.dislikeButtons = [None] * 9
        self.previewButtons = [None] * 9
        self.configureButtons()
        self.sliders = []
        self.configureSliders()
        self.songIds = [None] * 9
        self.songVar = [None] * 9
        self.songWidgets = [None] * 9
        self.discardedSongs = []
        self.previousIds = [None] * 9
        self.keptIds = []
        self.recCount = 0
        self.dislikeCount = 0
        self.keepCount = 0
        self.previousFeatures = [0.5] * 5
        self.featureChange = [1] * 5
        self.previousArtistVar = [0] * 15
        self.artistInteraction = 0
        self.playButtonInteract = 0
        print(prompt)

    def configureWindow(self):
        window = tk.Tk()
        window.geometry('1000x620')
        window.resizable(width=False, height=False)
        window.configure(bg='black')
        window.columnconfigure(0, weight=3)
        window.columnconfigure(1, weight=6)
        window.columnconfigure(2, weight=3)
        window.columnconfigure(3, weight=1)
        window.columnconfigure(4, weight=1)
        return window

    def configureButtons(self):

        #configure output textbox
        log = tk.Text(self.window, bg='black', fg='white')
        log.place(x=320, y=460, width=560, height=140)
        sys.stdout = Redirect(log)

        #configure entry box for searching artists
        query = tk.StringVar()
        ent = tk.Entry(self.window, textvariable=query)
        ent.place(x=50, y=580)
        submit = tk.Button(self.window, text='Search for artist', command= lambda: self.searchArtists(query))
        submit.place(x=50, y=550)

        #configure artist buttons
        #for i in range(len(self.artistIds)):


        #configure recommendation button
        calc = tk.Button(self.window, text='Calculate Recommendations', command= lambda: self.executeRecommendations(), font=('Comic Sans MS', 12), bg='black', activebackground='black', activeforeground='white', fg='white', relief='raised')
        calc.place(x=300, y=410, width=300, height=40)  

        #configure preview / discard buttons
        self.dislikeButtons[0] = tk.Button(self.window, text='discard', image=self.images[4], command= lambda: self.removeRec(self.songWidgets[0]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.dislikeButtons[0].place(x=900, y=0, width=50, height=50)
        self.previewButtons[0] = tk.Button(self.window, text='preview', image=self.images[3], command= lambda: self.previewSong(self.songWidgets[0]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.previewButtons[0].place(x=950, y=0, width=50, height=50)

        self.dislikeButtons[1] = tk.Button(self.window, text='discard', image=self.images[4], command= lambda: self.removeRec(self.songWidgets[1]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.dislikeButtons[1].place(x=900, y=50, width=50, height=50)
        self.previewButtons[1] = tk.Button(self.window, text='preview', image=self.images[3], command= lambda: self.previewSong(self.songWidgets[1]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.previewButtons[1].place(x=950, y=50, width=50, height=50)

        self.dislikeButtons[2] = tk.Button(self.window, text='discard', image=self.images[4], command= lambda: self.removeRec(self.songWidgets[2]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.dislikeButtons[2].place(x=900, y=100, width=50, height=50)
        self.previewButtons[2] = tk.Button(self.window, text='preview', image=self.images[3], command= lambda: self.previewSong(self.songWidgets[2]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.previewButtons[2].place(x=950, y=100, width=50, height=50)

        self.dislikeButtons[3] = tk.Button(self.window, text='discard', image=self.images[4], command= lambda: self.removeRec(self.songWidgets[3]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.dislikeButtons[3].place(x=900, y=150, width=50, height=50)
        self.previewButtons[3] = tk.Button(self.window, text='preview', image=self.images[3], command= lambda: self.previewSong(self.songWidgets[3]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.previewButtons[3].place(x=950, y=150, width=50, height=50)

        self.dislikeButtons[4] = tk.Button(self.window, text='discard', image=self.images[4], command= lambda: self.removeRec(self.songWidgets[4]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.dislikeButtons[4].place(x=900, y=200, width=50, height=50)
        self.previewButtons[4] = tk.Button(self.window, text='preview', image=self.images[3], command= lambda: self.previewSong(self.songWidgets[4]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.previewButtons[4].place(x=950, y=200, width=50, height=50)

        self.dislikeButtons[5] = tk.Button(self.window, text='discard', image=self.images[4], command= lambda: self.removeRec(self.songWidgets[5]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.dislikeButtons[5].place(x=900, y=250, width=50, height=50)
        self.previewButtons[5] = tk.Button(self.window, text='preview', image=self.images[3], command= lambda: self.previewSong(self.songWidgets[5]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.previewButtons[5].place(x=950, y=250, width=50, height=50)

        self.dislikeButtons[6] = tk.Button(self.window, text='discard', image=self.images[4], command= lambda: self.removeRec(self.songWidgets[6]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.dislikeButtons[6].place(x=900, y=300, width=50, height=50)
        self.previewButtons[6] = tk.Button(self.window, text='preview', image=self.images[3], command= lambda: self.previewSong(self.songWidgets[6]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.previewButtons[6].place(x=950, y=300, width=50, height=50)

        self.dislikeButtons[7] = tk.Button(self.window, text='discard', image=self.images[4], command= lambda: self.removeRec(self.songWidgets[7]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.dislikeButtons[7].place(x=900, y=350, width=50, height=50)
        self.previewButtons[7] = tk.Button(self.window, text='preview', image=self.images[3], command= lambda: self.previewSong(self.songWidgets[7]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.previewButtons[7].place(x=950, y=350, width=50, height=50)

        self.dislikeButtons[8] = tk.Button(self.window, text='discard', image=self.images[4], command= lambda: self.removeRec(self.songWidgets[8]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.dislikeButtons[8].place(x=900, y=400, width=50, height=50)
        self.previewButtons[8] = tk.Button(self.window, text='preview', image=self.images[3], command= lambda: self.previewSong(self.songWidgets[8]), font=('Comic Sans MS', 10), bg='black', fg='white', bd=0)
        self.previewButtons[8].place(x=950, y=400, width=50, height=50)   

        #configure submit button
        submitBut = tk.Button(self.window, text='Submit', command= lambda: self.printStats())
        submitBut.place(x=930, y=470, width=50, height=50)

    def configureSliders(self):
        #sliders
        acoSlider = tk.Scale(self.window, from_=0, to=100, orient='horizontal', label='Acousticness', font=('Comic Sans MS', 14), fg='white', bg='black', troughcolor='grey', activebackground='black', highlightbackground='black')
        acoSlider.set(50)
        acoSlider.place(x=300, y=0, width=300, height=80)
        insSlider = tk.Scale(self.window, from_=0, to=100, orient='horizontal', label='Instrumentalness', font=('Comic Sans MS', 14), fg='white', bg='black', troughcolor='grey', activebackground='black', highlightbackground='black')
        insSlider.set(50)
        insSlider.place(x=300, y=80, width=300, height=80)
        danSlider = tk.Scale(self.window, from_=0, to=100, orient='horizontal', label='Danceability', font=('Comic Sans MS', 14), fg='white', bg='black', troughcolor='grey', activebackground='black', highlightbackground='black')
        danSlider.set(50)
        danSlider.place(x=300, y=160, width=300, height=80)
        valSlider = tk.Scale(self.window, from_=0, to=100, orient='horizontal', label='Valence', font=('Comic Sans MS', 14), fg='white', bg='black', troughcolor='grey', activebackground='black', highlightbackground='black')
        valSlider.set(50)
        valSlider.place(x=300, y=240, width=300, height=80)
        eneSlider = tk.Scale(self.window, from_=0, to=100, orient='horizontal', label='Energy', font=('Comic Sans MS', 14), fg='white', bg='black', troughcolor='grey', activebackground='black', highlightbackground='black')
        eneSlider.set(50)
        eneSlider.place(x=300, y=320, width=300, height=80)
        self.sliders = [acoSlider, insSlider, danSlider, valSlider, eneSlider]

    def executeRecommendations(self):
        #remove unwanted widgets
        for i in range(len(self.songWidgets)):
            if self.songWidgets[i] != None:
                if not (self.songVar[i].get()):
                    self.songWidgets[i].destroy()
                    self.songWidgets[i] = None
                    self.songVar[i] = None
        
        #find values from gui
        artists = []
        features = []
        for idx, var in enumerate(self.artistVar):
            if(var.get()):
                artists.append(self.artistIds[idx])

        #ERROR HANDLING MUST BE 0 < x < 6
        if(len(artists) > 5):
            print('Please limit to 5 artists')
            return
        if(len(artists) == 0):
            print('Please select at least one artist')
            return
        self.recCount += 1

        for slider in self.sliders:
            features.append(slider.get())
        for i in range(len(features)):
            features[i] /= 100

        for i in range(len(self.artistIds)):
            if self.previousArtistVar[i] == self.artistVar[i].get():
                pass
            else:
                self.artistInteraction += 1

        for i in range(5):
            if features[i] != self.previousFeatures[i]:
                self.featureChange[i] += 1

        #avoid discarded / previous recommendations
        songs = self.getRecommendations(artists, features)
        recIds = []
        for s in songs:
            recIds.append(s.get('id'))
        finalIds = [i for i in recIds if i not in self.discardedSongs]
        finalIds = [i for i in finalIds if i not in self.previousIds]
        for i in range(len(finalIds)):
            finalIds[i] = sp.track(finalIds[i])
   
        #create song recommendation widgets
        for i in range(9):
            if(self.songVar[i] == None):
                # avoid index out of range when too many songs discarded
                try:
                    self.songIds[i] = finalIds[i].get('id')
                    self.songVar[i] = tk.IntVar()
                    self.songWidgets[i] = tk.Checkbutton(self.window, font=('Comic Sans MS', 12), anchor='nw', bd=0, image=self.images[1], selectimage=self.images[0], variable=self.songVar[i], text=(finalIds[i].get('name')+'\n'+finalIds[i].get('artists')[0].get('name')), justify='left', indicatoron=False, compound='left', bg='black', activebackground='black', activeforeground='white', selectcolor='black', fg='white', relief='raised')
                    self.songWidgets[i].place(x=600, y=i*50, width=300, height=50)
                except IndexError:
                    break
            else:
                if self.songIds[i] not in self.keptIds:
                    self.keptIds.append(self.songIds[i])
                    self.keepCount += 1
        self.previousIds = self.songIds[:]
        self.previousFeatures = features[:]   
        self.previousArtistVar = [i.get() for i in self.artistVar]           

        print('Recommendations Found')

    def removeRec(self, w):
        if w == None:
            return
        self.dislikeCount += 1
        idx = self.songWidgets.index(w)
        self.discardedSongs.append(self.songIds[idx])
        w.destroy()
        self.songWidgets[idx] = None
        self.songVar[idx] = None 
        print('Song Discarded (should not appear again)')

    def previewSong(self, w):
        if w == None:
            return
        self.playButtonInteract += 1
        idx = self.songWidgets.index(w)
        song = sp.track(self.songIds[idx])
        try:
            url = song.get('preview_url')
            webbrowser.open(url)
            print('Opening preview in browser')
        except:
            print('Preview Unavailable')

    def getTopArtists(self, limit=15):
        #print(sp.search('CAKE', limit=3, type='artist'))
        artists = sp.current_user_top_artists(limit=limit)
        artists = artists.get('items')
        for i in range(len(artists)):
            artists[i] = artists[i].get('id')
        return artists

    def getRecommendations(self, topArtists, sliderVals, limit=25):
        songs = sp.recommendations(seed_artists=topArtists, 
                                   target_acousticness=sliderVals[0],
                                   target_instrumentalness=sliderVals[1],
                                   target_danceability=sliderVals[2],
                                   target_valence=sliderVals[3],
                                   target_energy=sliderVals[4], 
                                   limit=limit)
        return songs.get('tracks')

    def printStats(self):
        for i in range(9):
            #tryblock for case of pressing submit with no recs
            try:
                if self.songVar[i].get():
                    continue
                else:
                    print('Please select 9 songs')
                    return
            except:
                print('Please select 9 songs')
                return
        print('----------------------------------')
        print('RECORD THESE VALUES IN GOOGLE FORM')
        print('----------------------------------')
        print('RecCount = ' + str(self.recCount), end=' / ')
        print('DislikeCount = ' + str(self.dislikeCount), end=' / ')
        print('KeepCount = ' + str(self.keepCount))
        print('FeatureChange = ' + str(self.featureChange), end=' / ')
        print('ArtistInteract = ' + str(self.artistInteraction))
        print('PlaybuttonInteract = ' + str(self.playButtonInteract), end='')

    def searchArtists(self, query):
        try:
            results = sp.search(query.get(), limit=1, type='artist')
            results = results.get('artists').get('items')[0].get('id')
            if results in self.artistIds:
                print('Cannot duplicate artist')
                return
            i = len(self.artistIds)
            if i < 13:
                self.artistIds.append(results)
                self.artistVar.append(tk.IntVar())
                button = tk.Checkbutton(self.window, anchor='nw', variable=self.artistVar[i], image=self.images[1], selectimage=self.images[0], bd=0, text=sp.artist(self.artistIds[i]).get('name'), font=('Comic Sans MS', 12), indicatoron=False, compound='left', bg='black', activebackground='black', activeforeground='white', selectcolor='black', fg='white', relief='raised')
                button.place(x=0, y=i*40, width=300, height=40)
            else:
                print('Maximum artists!!')
        except:
            print('Please provide a search query')

class RadarWindow(SpWindow):
    def __init__(self, prompt):
        self.window = self.configureWindow()
        self.images = [tk.PhotoImage(file='guiScripts/toggle-button-on.png'), tk.PhotoImage(file='guiScripts/toggle-button-off.png'), tk.PhotoImage(file='guiScripts/recommend-button.png'), tk.PhotoImage(file='guiScripts/playButton.png'), tk.PhotoImage(file='guiScripts/discardButton.png')]
        self.artistIds = []
        self.artistVar = []
        self.c = [None] * 5
        self.dislikeButtons = [None] * 9
        self.previewButtons = [None] * 9
        self.configureButtons()
        self.sliders = [None] * 5
        self.canvas = tk.Canvas(self.window, width=300, height=300, background='black', highlightthickness=0)
        self.configureRadar()
        self.songIds = [None] * 9
        self.songVar = [None] * 9
        self.songWidgets = [None] * 9
        self.discardedSongs = []
        self.currentSlider = None
        self.grid = None
        self.previousIds = [None] * 9
        self.keptIds = []
        self.recCount = 0
        self.dislikeCount = 0
        self.keepCount = 0
        self.previousFeatures = [0.5] * 5
        self.featureChange = [0, 0, 0, 0, 0]
        self.previousArtistVar = [0] * 15
        self.artistInteraction = 0
        self.playButtonInteract = 0
        print(prompt)

    def configureRadar(self):
        self.canvas.create_polygon(150, 0, 300, 120, 230, 300, 70, 300, 0, 120, fill='grey')
        self.canvas.create_line(150, 0, 150, 150, fill='black')
        self.canvas.create_line(300, 120, 150, 150, fill='black')
        self.canvas.create_line(230, 300, 150, 150, fill='black')
        self.canvas.create_line(70, 300, 150, 150, fill='black')
        self.canvas.create_line(0, 120, 150, 150, fill='black')

        self.canvas.create_text(100, 50, text='Acousticness', fill='white')
        self.canvas.create_text(250, 100, text='Instrumentalness', fill='white')
        self.canvas.create_text(230, 200, text='Danceability', fill='white')
        self.canvas.create_text(70, 200, text='Valence', fill='white')
        self.canvas.create_text(25, 100, text='Energy', fill='white')

        ### INITIALIZE SELF.C FOR IMMEDIATE RECOMMENDATION ###
        aco = self.canvas.create_oval(145, 70, 155, 80, fill='red', outline='red')
        self.c[0] = [145, 70, 155, 80]
        ins = self.canvas.create_oval(220, 130, 230, 140, fill='red', outline='red')
        self.c[1] = [220, 130, 230, 140]
        dan = self.canvas.create_oval(185, 220, 195, 230, fill='red', outline='red')
        self.c[2] = [185, 220, 195, 230]
        val = self.canvas.create_oval(105, 220, 115, 230, fill='red', outline='red')
        self.c[3] = [105, 220, 115, 230]
        ene = self.canvas.create_oval(70, 130, 80, 140, fill='red', outline='red')
        self.c[4] = [70, 130, 80, 140]

        self.sliders = [aco, ins, dan, val, ene]
        self.canvas.bind("<Button-1>", self.grabSlider)
        self.canvas.bind("<B1-Motion>", self.adjustSlider)
        self.canvas.bind("<ButtonRelease-1>", self.releaseSlider)
        self.canvas.place(x=300, y=20)

    def grabSlider(self, event):
        #Reset coords and update click pos
        for i in range(len(self.sliders)):
            self.c[i] = self.canvas.coords(self.sliders[i])
        curx, cury = event.x, event.y

        #Grab aco slider by clicking line
        if (curx > 140 and curx < 160) and (cury > 5 and cury < 135):
            self.currentSlider = self.sliders[0]
            diffy = cury - self.c[0][1] - 5
            self.canvas.move(self.sliders[0], 0, diffy)
        #ins slider
        elif curx > 160 and curx < 290 and np.abs(cury - (-0.2*curx + 180)) < 10:
            self.currentSlider = self.sliders[1]
            diffx = curx - self.c[1][0] - 5
            self.canvas.move(self.sliders[1], diffx, -0.2*diffx)
        #dan slider
        elif curx > 152 and curx < 228 and np.abs(cury - (1.875*curx - 131.25)) < 10:
            self.currentSlider = self.sliders[2]
            diffx = curx - self.c[2][0] - 5
            self.canvas.move(self.sliders[2], diffx, 1.875*diffx)
        #val slider
        elif curx > 72 and curx < 148 and np.abs(cury - (-1.875*curx + 431.25)) < 10:
            self.currentSlider = self.sliders[3]
            diffx = curx - self.c[3][0] - 5
            self.canvas.move(self.sliders[3], diffx, -1.875*diffx)
        #ene slider
        elif curx > 10 and curx < 140 and np.abs(cury - (0.2*curx + 120)) < 10:
            self.currentSlider = self.sliders[4]
            diffx = curx - self.c[4][0] - 5
            self.canvas.move(self.sliders[4], diffx, 0.2*diffx)
        else:
            pass

    def adjustSlider(self, event):
        #must update coords for each call
        for i in range(len(self.sliders)):
            self.c[i] = self.canvas.coords(self.sliders[i])
        curx, cury = event.x, event.y
        #Movement for aco slider
        if self.currentSlider == self.sliders[0]:
            #movement bounds
            if cury < 5 or cury > 135:
                pass
            else:
                diffy = cury - self.c[0][1] - 5
                self.canvas.move(self.sliders[0], 0, diffy)
        #movement for ins slider
        if self.currentSlider == self.sliders[1]:
            if curx < 165 or curx > 295:
                pass
            else:
                diffx = curx - self.c[1][0] - 5
                self.canvas.move(self.sliders[1], diffx, -0.2*diffx)
        #movement for dan slider
        if self.currentSlider == self.sliders[2]:
            if curx < 160 or curx > 228:
                pass
            else:
                diffx = curx - self.c[2][0] - 5
                self.canvas.move(self.sliders[2], diffx, 1.875*diffx)
        #movement for val slider
        if self.currentSlider == self.sliders[3]:
            if curx < 72 or curx > 140:
                pass
            else:
                diffx = curx - self.c[3][0] - 5
                self.canvas.move(self.sliders[3], diffx, -1.875*diffx)
        #movement for ene slider
        if self.currentSlider == self.sliders[4]:
            if curx < 5 or curx > 135:
                pass
            else:
                diffx = curx - self.c[4][0] - 5
                self.canvas.move(self.sliders[4], diffx, 0.2*diffx)

    def releaseSlider(self, event):
        for i in range(len(self.sliders)):
            self.c[i] = self.canvas.coords(self.sliders[i])
        self.currentSlider = None
        self.canvas.delete(self.grid)
        #print(self.c)
        self.grid = self.canvas.create_polygon(self.c[0][0]+5, self.c[0][1]+5, self.c[1][0]+5, self.c[1][1]+5, self.c[2][0]+5, self.c[2][1]+5, self.c[3][0]+5, self.c[3][1]+5, self.c[4][0]+5, self.c[4][1]+5, fill='', outline='black')

    def executeRecommendations(self):
        #remove unwanted widgets
        for i in range(len(self.songWidgets)):
            if self.songWidgets[i] != None:
                if not (self.songVar[i].get()):
                    self.songWidgets[i].destroy()
                    self.songWidgets[i] = None
                    self.songVar[i] = None
        
        #find values from gui
        artists = []
        features = []
        for idx, var in enumerate(self.artistVar):
            if(var.get()):
                artists.append(self.artistIds[idx])

        #ERROR HANDLING MUST BE 0 < x < 6
        if(len(artists) > 5):
            print('Please limit to 5 artists')
            return
        if(len(artists) == 0):
            print('Please select at least one artist')
            return
        self.recCount += 1

        features.append(100 * ((100 - self.c[0][1] + 5) / 125) + 20)
        features.append(100 * ((self.c[1][0] - 145) / 130) - 10)
        features.append(100 * ((self.c[2][1] - 145) / 130) - 10)
        features.append(100 * ((self.c[3][1] - 145) / 130) - 10)
        features.append(100 * ((100 - self.c[4][0] + 5) / 130) + 20)
        
        #handle sloppy slider math
        for i in range(len(features)):
            if features[i] > 100:
                features[i] = 100
            if features[i] < 0:
                features[i] = 0
            features[i] /= 100

        for i in range(len(self.artistIds)):
            if self.previousArtistVar[i] == self.artistVar[i].get():
                pass
            else:
                self.artistInteraction += 1

        for i in range(5):
            if features[i] != self.previousFeatures[i]:
                self.featureChange[i] += 1

        #avoid discarded / previous recommendations
        songs = self.getRecommendations(artists, features)
        recIds = []
        for s in songs:
            recIds.append(s.get('id'))
        finalIds = [i for i in recIds if i not in self.discardedSongs]
        finalIds = [i for i in finalIds if i not in self.previousIds]
        for i in range(len(finalIds)):
            finalIds[i] = sp.track(finalIds[i])
   
        #create song recommendation widgets
        for i in range(9):
            if(self.songVar[i] == None):
                # avoid index out of range when too many songs discarded
                try:
                    self.songIds[i] = finalIds[i].get('id')
                    self.songVar[i] = tk.IntVar()
                    self.songWidgets[i] = tk.Checkbutton(self.window, font=('Comic Sans MS', 12), anchor='nw', bd=0, image=self.images[1], selectimage=self.images[0], variable=self.songVar[i], text=(finalIds[i].get('name')+'\n'+finalIds[i].get('artists')[0].get('name')), justify='left', indicatoron=False, compound='left', bg='black', activebackground='black', activeforeground='white', selectcolor='black', fg='white', relief='raised')
                    self.songWidgets[i].place(x=600, y=i*50, width=300, height=50)
                except IndexError:
                    break
            else:
                if self.songIds[i] not in self.keptIds:
                    self.keptIds.append(self.songIds[i])
                    self.keepCount += 1
        self.previousIds = self.songIds[:]
        self.previousFeatures = features[:]
        self.previousArtistVar = [i.get() for i in self.artistVar]      

        print('Recommendations Found')

#redirection class to output to tkinter log
class Redirect():
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert('end', text)
        self.widget.see('end') # autoscroll

    def flush(self):
        pass

