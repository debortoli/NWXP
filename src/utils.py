import pygame
from pygame.locals import *
import pdb
import time
import csv
import numpy as np

class Board:
	def __init__(self):
		# initialize game engine
		pygame.init()
		self.clock = pygame.time.Clock()

		# # #add the dragNdrop options
		# self.dnd=[]
		# d1=DragNDrop((80,100,50,50),'../images/city.jpg')
		# self.dnd.append(d1)
		# d2=DragNDrop((180,100,50,50),'../images/city.jpg')
		# self.dnd.append(d2)
		# d3=DragNDrop((80,240,50,50),'../images/city.jpg')
		# self.dnd.append(d3)
		# d4=DragNDrop((180,240,50,50),'../images/city.jpg')
		# self.dnd.append(d4)
		# d5=DragNDrop((80,380,50,50),'../images/city.jpg')
		# self.dnd.append(d5)

		# self.draggablesUpdate()

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
			for row in generator_reader:
				self.generators.append([row[0],row[1],float(row[2]),
										float(row[3]),float(row[4])])
		

		self.availableGenerators=[]#these are the generators for the time period

		self.dispatchProfile=[["Off Peak AM",0],["Daytime1",0],
						  ["Peak",0],["Daytime2",0],
						  ["Off-peak PM",0]]

		self.ancillaryProfile=[["Off Peak AM",0],["Daytime1",0],
						  ["Peak",0],["Daytime2",0],
						  ["Off-peak PM",0]]

		self.demandProfile=[["Off Peak AM",0],["Daytime1",0],
						  ["Peak",0],["Daytime2",0],
						  ["Off-peak PM",0]]
		self.clearingGens=[]

		self.cumulGen=0

		self.events=[["This is a sample\nmessage.\nThis is a sample\nmessage. This is a sample\nmessage.\nThis is a sample\nmessage.",
					["Sample Option 1","Sample Option 2","Sample Option 3"]]]

		self.profilePeriods=[["Off Peak AM",5],["Daytime1",5],
							["Peak",4],["Daytime2",5],
							["Off-peak PM",5]]

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
