import pygame
import planes
from pygame.locals import *
import pdb
import time

class Board:
	def __init__(self):
		# initialize game engine
		pygame.init()
		# self.size = [1000,700]#width then height
		# self.screen = pygame.display.set_mode(self.size,RESIZABLE)
		# pygame.display.set_caption('Grid Simulator')
		self.clock = pygame.time.Clock()

		# #init the background stuff
		# self.BackGround = Background('../images/dam.jpg', [0,0])

		# #init all apropriate surfaces
		# self.levelCompleteSurface = pygame.Surface((300,100),1)
		# self.levelCompleteSurface.fill([224,224,224])

		# self.totalPointsSurface = pygame.Surface((300,100))
		# self.totalPointsSurface.fill([224,224,224])

		# self.dragablesSurface = pygame.Surface((300,500))
		# self.dragablesSurface.fill([224,224,224])
		# # self.blitSurfaces()



		# #init the text STUFF
		# # pygame.font.init()
		# # self.myfont = pygame.font.SysFont('Courier New', 15)


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

		self.progress=0.8
		self.totalPoints=20
		#level 0=tutorial
		self.level=0

		# self.update_text="Game has started!\n"
		self.year=0

		self.updateQueue=[]
		self.UpdateMessageSurface_x=100
		self.UpdateMessageSurface_y=450

		# self.poppinsFont=pygame.font.SysFont('../fonts/Poppins-Regular.ttf',25)
		# # self.createCities()
		# # self.createTransmissionLines()
		# self.displayMenu=True
		# self.menu_options=[]

	def blitSurfaces(self):
		self.screen.blit(self.BackGround.image, self.BackGround.rect)

		levelx,levely=[0.7*self.screen.get_width(),0]
		pointsx,pointsy=[0.7*self.screen.get_width(),self.screen.get_height()/7.]
		iconsx,iconsy=[0.7*self.screen.get_width(),pointsy*2]

		#update surface info
		self.updateLevelSurface(self.progress)
		self.updatePointsSurface()
		self.updateDraggablesSurface()

		#
		self.screen.blit(self.levelCompleteSurface, (levelx,levely))
		self.screen.blit(self.totalPointsSurface,   (pointsx,pointsy))
		self.screen.blit(self.dragablesSurface,     (iconsx,pointsy*2))
		if(len(self.updateQueue)>0):
			self.screen.blit(self.updateQueue[0].messageSurface,(self.UpdateMessageSurface_x,self.UpdateMessageSurface_y))

		#draw borders around surfaces
		pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(levelx,levely,self.screen.get_width()-levelx,pointsy),2)
		pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(pointsx,pointsy,self.screen.get_width()-pointsx,pointsy),2)
		pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(iconsx,pointsy*2,self.screen.get_width()-pointsx,pointsy*5),2)

	def updateLevelSurface(self,progress):
		#clear the surface
		self.levelCompleteSurface.fill((224,224,224))

		maxwidth=0.8*self.levelCompleteSurface.get_width()
		left=0.03*self.levelCompleteSurface.get_width()
		top=0.4*self.levelCompleteSurface.get_height()
		height=0.25*self.levelCompleteSurface.get_height()
		bar=pygame.draw.rect(self.levelCompleteSurface, (0,255,0), pygame.Rect(left,top,maxwidth*progress,height))
		outline=pygame.draw.rect(self.levelCompleteSurface, (0,0,0), pygame.Rect(left,top,maxwidth,height),3)

		fontsizelevel=int(0.1*self.levelCompleteSurface.get_width())
		title=pygame.font.SysFont('../fonts/Poppins-Regular.ttf',fontsizelevel).render("Level Progress", False, (0, 0, 0))
		title_rect = title.get_rect(center=(self.levelCompleteSurface.get_width()/2.2, self.levelCompleteSurface.get_height()*0.4/2))
		self.levelCompleteSurface.blit(title,title_rect)

	def updatePointsSurface(self):
		#clear the surface
		self.totalPointsSurface.fill((224,224,224))

		fontsizepoint=int(0.1*self.totalPointsSurface.get_width())
		title=pygame.font.SysFont('../fonts/Poppins-Regular.ttf',fontsizepoint).render("Total Points", False, (0, 0, 0))
		title_rect = title.get_rect(center=(self.totalPointsSurface.get_width()/2.2, self.totalPointsSurface.get_height()*0.4/2))
		self.totalPointsSurface.blit(title,title_rect)

		points=pygame.font.SysFont('../fonts/Poppins-Regular.ttf',55).render(str(self.totalPoints), False, (0, 128, 0))
		self.totalPointsSurface.blit(points,(title_rect[0]+title_rect[0]/2.,title_rect[1]*4.))

	def updateDraggablesSurface(self):
		#clear the surface
		self.dragablesSurface.fill((224,224,224))
		self.draggablesUpdate()

		fontsizepoint=int(0.1*self.dragablesSurface.get_width())
		# title=pygame.font.SysFont('../fonts/Poppins-Regular.ttf',fontsizepoint).render("Total Points", False, (0, 0, 0))
		# title_rect = title.get_rect(center=(self.dragablesSurface.get_width()/2, self.dragablesSurface.get_height()*0.4/2))
		# self.totalPointsSurface.blit(title,title_rect)

		# points=pygame.font.SysFont('../fonts/Poppins-Regular.ttf',55).render(str(self.totalPoints), False, (0, 128, 0))
		# self.totalPointsSurface.blit(points,(140,45))


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
		


	def textUpdate(self):
		#format text
		line=""
		line_num=0
		for char in self.update_text:
			if char=='\n':
				t=self.myfont.render(line, False, (0, 0, 0))
				self.screen.blit(t,(621,20*line_num))
				line=""
				line_num+=1
			else:
				line+=char

	def staticItemsUpdate(self):
		#BELOW IS OLD STUFF RELATING TO CITIES, ETC.
		#background image
		self.screen.fill([255, 255,255])
		self.screen.blit(self.BackGround.image, self.BackGround.rect)

		#cities
		for city in self.cities:
			self.screen.blit(city.image,city.rect)

		#powerlines
		for line in self.transmissionLines:
			line.update(self)
			self.screen.blit(line.image,line.rect)

		#the below is a placeholder until I redefine transmission lines
		end_points=[[121, 126], [313, 160], [115, 189], [309, 242], [309, 242], [551, 275], 
		 [73, 268], [192, 290], [77, 323], [79, 317], [185, 380], [390, 437], [399, 448], [510, 411], [314, 246], [394, 269], 
		 [394, 269], [398, 368], [398, 368], [495, 343], [399, 366], [398, 439], [498, 344], [506, 418], [506, 418], [403, 549], 
		 [396, 441], [403, 546], [403, 546], [465, 624], [80, 265], [81, 324], [81, 317], [79, 425], [98, 147], [121, 185], [156, 71], 
		 [124, 126], [167, 12], [152, 76], [195, 294], [186, 383], [105, 253], [81, 267], [78, 421], [143, 526], [143, 526], 
		 [245, 579], [245, 579], [352, 633], [352, 633], [470, 635]]
		i=0
		while i <len(end_points):
			pygame.draw.lines(self.screen, (0,0,0), False, [end_points[i],end_points[i+1]], 3)
			i+=2

	def draggablesUpdate(self):
		for i,icon  in enumerate(self.dnd):
			icon.update(self.dragablesSurface)
			# board.screen.blit(icon,(i*100,700))

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

	def resizeSurfaces(self,screenSize):
		self.levelCompleteSurface=pygame.transform.scale(self.levelCompleteSurface,(screenSize[0]/3,screenSize[1]/5))
		self.totalPointsSurface=pygame.transform.scale(self.totalPointsSurface,(screenSize[0]/3,screenSize[1]/5))
		self.dragablesSurface=pygame.transform.scale(self.dragablesSurface,(screenSize[0]/3,screenSize[1]/5*3))
		self.resizeUpdateMessages()
		#update icons
		self.dnd=[]
		d1=DragNDrop((8/30.*self.dragablesSurface.get_width(),1/5.*self.dragablesSurface.get_height(),50,50),'../images/city.jpg')
		self.dnd.append(d1)
		d2=DragNDrop((18/30.*self.dragablesSurface.get_width(),1/5.*self.dragablesSurface.get_height(),50,50),'../images/city.jpg')
		self.dnd.append(d2)
		d3=DragNDrop((8/30.*self.dragablesSurface.get_width(),0.5*self.dragablesSurface.get_height(),50,50),'../images/city.jpg')
		self.dnd.append(d3)
		d4=DragNDrop((18/30.*self.dragablesSurface.get_width(),0.5*self.dragablesSurface.get_height(),50,50),'../images/city.jpg')
		self.dnd.append(d4)
		d5=DragNDrop((8/30.*self.dragablesSurface.get_width(),38/50.*self.dragablesSurface.get_height(),50,50),'../images/city.jpg')
		self.dnd.append(d5)

	def resizeUpdateMessages(self):
		self.UpdateMessageSurface_y=0.65*self.screen.get_height()
		self.UpdateMessageSurface_x=0.1*self.screen.get_width()
		if(len(self.updateQueue)>0):
			for message in self.updateQueue:
				#surface resizing
				message.messageSurface.fill([224,224,224])
				message.messageSurface=pygame.transform.scale(message.messageSurface,(int(0.5*self.screen.get_width()),int(0.25*self.screen.get_height())))
				#button resizing
				message.buttonx=message.messageSurface.get_width()-message.messageSurface.get_width()*0.2+1
				message.buttonw=message.messageSurface.get_width()-message.buttonx
				message.buttonh=message.messageSurface.get_height()*0.15
		

			
	
class UpdateMessageSurface():
	def __init__(self,board,message):
		#make the semi-transparent surface
		# self.messageSurface_width=
		self.messageSurface=pygame.Surface((0.5*board.screen.get_width(),0.25*board.screen.get_height()), pygame.SRCALPHA)
		self.messageSurface.fill((255,255,255,200))

		#display the message
		self.text=message

		#make the button
		self.buttonColor=(0,200,0)
		self.buttonx=self.messageSurface.get_width()-self.messageSurface.get_width()*0.2+1
		self.buttony=0
		self.buttonw=self.messageSurface.get_width()-self.buttonx
		self.buttonh=self.messageSurface.get_height()*0.15
		pygame.draw.rect(self.messageSurface, self.buttonColor,(self.buttonx,self.buttony,self.buttonw,self.buttonh))
		t=pygame.font.SysFont('comicsansms', 25).render("Continue", False, (0, 0, 0))
		self.messageSurface.blit(t,(self.buttonx+10,self.buttony))
		self.buttonClicked = False

	def update(self,board):
		#dim the color as the mouse goes over it
		buttonRect=pygame.Rect(board.UpdateMessageSurface_x+board.updateQueue[0].buttonx,
									   board.UpdateMessageSurface_y+board.updateQueue[0].buttony,
										board.updateQueue[0].buttonw,
										board.updateQueue[0].buttonh)
		if(buttonRect.collidepoint(pygame.mouse.get_pos())):
			self.buttonColor=(0,150,0)
		else:
			self.buttonColor=(0,200,0)
			

		#display button
		pygame.draw.rect(self.messageSurface, self.buttonColor,(self.buttonx,self.buttony,self.buttonw,self.buttonh))
		t=pygame.font.SysFont('comicsansms', 25).render("Continue", False, (0, 0, 0))
		self.messageSurface.blit(t,(self.buttonx+10,self.buttony+5))
		

		#format the text
		line_num=0
		line=""
		for char in self.text:
			if char=='\n':
				t=pygame.font.SysFont('comicsansms', 25).render(line, False, (0, 0, 0))
				self.messageSurface.blit(t,(10,20*line_num+5))
				line=""
				line_num+=1
			else:
				line+=char


		

class DragNDrop:
	def __init__(self,rect,filename):
		self.rect = pygame.Rect(rect)
		self.click = False
		self.image = pygame.image.load(filename)
	def update(self,surface):
		if self.click:
			self.rect.center = pygame.mouse.get_pos()
		surface.blit(self.image,self.rect)


class Background(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

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

#Class Option credits to: https://gist.github.com/ohsqueezy/2802185
class Option:
	hovered = False
	def __init__(self, text, pos):
		self.text = text
		self.pos = pos
		self.set_rect()
		# self.draw()
			
	def draw(self,screen):
		self.set_rend()
		screen.blit(self.rend, self.rect)
		
	def set_rend(self):
		self.rend = pygame.font.SysFont('Courier New', 18,bold=True).render(self.text, True, self.get_color())
		
	def get_color(self):
		if self.hovered:
			return (150, 150, 150)
		else:
			return (0, 0, 0)
		
	def set_rect(self):
		self.set_rend()
		self.rect = self.rend.get_rect()
		self.rect.topleft = self.pos



