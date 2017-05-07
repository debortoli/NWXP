import pygame
from pygame.locals import *
import pdb
import time
import csv
import numpy as np
import Tkinter as tk
import ttk

class Board:
	def __init__(self):
		# initialize game engine
		pygame.init()
		self.clock = pygame.time.Clock()


		self.progress=99.4
		self.totalPoints=0.
		#level 0=tutorial
		self.level=1
		self.year=0

		self.updateQueue=[]
		self.UpdateMessageSurface_x=100
		self.UpdateMessageSurface_y=450
		self.water_level=87
		self.powerProducedDam=0.
		self.damLoad=0.
		self.water_velocity=10.
		self.loadChangeTime=pygame.time.get_ticks()
		self.spilledSeconds=0.
		self.time="09:00 AM"


		#for level 2
		self.possibleLoadLevels=[1010.,1020.,1015.,1011.,1010.,1010.,
								 1012.,1020.,1021.,1024.,1024.,1020.,
								 1025.,1030.,1032.,1033.,1039.,1047.,
								 1055.,1050.,1040.,1030.,1025.,1017.,]

		#for level 3
		self.generators=[]#this is a list of all of the generators
		with open('generators.csv', 'rb') as csvfile:
			generator_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for i,row in enumerate(generator_reader):
				if(i>0):
					self.generators.append([row[0],row[1],float(row[2]),
										float(row[3]),float(row[5]),float(row[6])])

		#add the image locations
		#make a list of the generator locations where each index is [x,y,#]
		gen_locs=[]
		with open('genLocations.csv', 'rb') as csvfile:
			gen_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in gen_reader:
				gen_locs.append([row[1],row[3],row[5]])

		for i,gen in enumerate(self.generators):
			for loc in gen_locs:
				try:
					if(gen[-1]==int(loc[-1])):
						self.generators[i] = self.generators[i] + [loc[0]]+[loc[1]]
				except:
					r=0
		

		self.availableGenerators=[]#these are the generators for the time period

		self.dispatchProfile=[["Off Peak AM","--"],["Daytime1","--"],
						  ["Peak","--"],["Daytime2","--"],
						  ["Off-peak PM","--"]]

		self.ancillaryProfile=[["Off Peak AM",0],["Daytime1",0],
						  ["Peak",0],["Daytime2",0],
						  ["Off-peak PM",0]]

		self.demandProfile=[["Off Peak AM",0],["Daytime1",0],
						  ["Peak",0],["Daytime2",0],
						  ["Off-peak PM",0]]
		self.clearingGens=[]

		self.cumulGen=0

		self.events=[]

		self.profilePeriods=[["Off Peak AM",5.5],["Daytime1",4],
							["Peak",5],["Daytime2",4],
							["Off-peak PM",5.5]]

		self.time_period=0
		self.last_time_period=-1

	
	def createCities(self):
		self.cities=[]
		locations=  [[88, 131], [67, 253], [70, 310], [63, 411], [305, 151], [300, 232], 
					[386, 261], [387, 358], [384, 430], [390, 539], [149, 4], [146, 60], [105, 116],[110,180],[93,240], 
					[184, 287], [177, 373], [532, 269], [492, 335], [494, 405], [458,620],[81, 267],[143, 526],[245, 579],[352, 633]]
		for location in locations:
			c=City('../images/city_small.jpg',location)
			self.cities.append(c)

	def createTransmissionLines(self):
		self.transmissionLines=[]
		t=Transmission('../images/transmission_small_vertical.png',[90,205],
			"PortlandCorvallis",0)
		self.transmissionLines.append(t)

	
	def checkPowerLineAge(self):
		for line in self.transmissionLines:
			# print self.update_text[(len(str(line.name))+1)*-1:-1]
			if(line.age>2 and
				self.update_text[(len(str(line.name))+1)*-1:-1]!=str(line.name)):
				if(self.displayMenu==True):
					#setup the screen
					oS_corner_x=30
					oS_corner_y=30
					oS_width=500
					oS_height=600
					optionScreen = pygame.Surface((oS_width,oS_height), pygame.SRCALPHA)   # per-pixel alpha
					optionScreen.fill((255,255,255,200))                         # notice the alpha value in the color
					

					#display the menu options
					t=pygame.font.SysFont('Courier New', 22,bold=True).render("The transmission line from", False, (0, 0, 0))
					optionScreen.blit(t,(oS_corner_x+10, oS_corner_y+10))
					t=pygame.font.SysFont('Courier New', 22,bold=True).render("Corvallis to Portland is aging!", False, (0, 0, 0))
					optionScreen.blit(t,(oS_corner_x+10, oS_corner_y+30))
					
					t=pygame.font.SysFont('Courier New', 22,bold=True).render("What would you like to do?", False, (0, 0, 0))
					optionScreen.blit(t,(oS_corner_x+10, oS_corner_y+50))
					self.menu_options=[]
					options = [Option("Replace line with taxpayer money", (oS_corner_x+10, oS_corner_y+150)), 
					Option("Replace line with utility money", (oS_corner_x+10, oS_corner_y+250)),	
					Option("Allow line to continue aging", (oS_corner_x+10, oS_corner_y+350))]
					for option in options:
						if option.rect.collidepoint(pygame.mouse.get_pos()):
							option.hovered = True
						else:
							option.hovered = False
						option.draw(optionScreen)
						self.menu_options.append(option)

					self.screen.blit(optionScreen, (oS_corner_x,oS_corner_y))

	

	

class DragNDrop:
	def __init__(self,rect,filename):
		self.rect = pygame.Rect(rect)
		self.click = False
		self.image = pygame.image.load(filename)
	def update(self,surface):
		if self.click:
			self.rect.center = pygame.mouse.get_pos()
		surface.blit(self.image,self.rect)


class City(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

class Transmission(pygame.sprite.Sprite):
	def __init__(self, image_file, location,name,age):
		pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location
		self.initial_age=age
		self.age=age
		self.name=name
	def update(self,board):
		self.age=self.initial_age+board.year



class Tooltip:

    def __init__(self, master, text, delay=300, showTime=10000,
            background="lightyellow"):
        self.master = master
        self.text = text
        self.delay = delay
        self.showTime = showTime
        self.background = background
        self.timerId = None
        self.tip = None
        self.master.bind("<Enter>", self.enter, "+")
        self.master.bind("<Leave>", self.leave, "+")

    
    def enter(self, event=None):
        if self.timerId is None and self.tip is None:
            self.timerId = self.master.after(self.delay, self.show)
        

    def leave(self, event=None):
        if self.timerId is not None:
            id = self.timerId
            self.timerId = None
            self.master.after_cancel(id)
        self.hide()


    def hide(self):
        if self.tip is not None:
            tip = self.tip
            self.tip = None
            tip.destroy()


    def show(self):
        self.leave()
        self.tip = tk.Toplevel(self.master)
        self.tip.withdraw() # Don't show until we have the geometry
        self.tip.wm_overrideredirect(True) # No window decorations etc.
       
        label = ttk.Label(self.tip, text=self.text, padding=1,
                background=self.background, wraplength=480,
                relief=tk.GROOVE)
        label.pack()
        x, y = self.position()
        self.tip.wm_geometry("+{}+{}".format(x, y))
        self.tip.deiconify()
        if self.master.winfo_viewable():
            self.tip.transient(self.master)
        self.tip.update_idletasks()
        self.timerId = self.master.after(self.showTime, self.hide)

    
    def position(self):
        tipx = self.tip.winfo_reqwidth()
        tipy = self.tip.winfo_reqheight()
        width = self.tip.winfo_screenwidth()
        height = self.tip.winfo_screenheight()
        y = self.master.winfo_rooty() + self.master.winfo_height()
        if y + tipy > height:
            y = self.master.winfo_rooty() - tipy
        x = self.tip.winfo_pointerx()
        if x < 0:
            x = 0
        elif x + tipx > width:
            x = width - tipx
        return x, y

