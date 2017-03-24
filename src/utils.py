import pygame
import planes
from pygame.locals import *
import pdb
class Board:
	def __init__(self):
		# initialize game engine
		pygame.init()
		self.size = [1000,700]#width then height
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption('Grid Simulator')
		self.clock = pygame.time.Clock()

		#init the background stuff
		self.BackGround = Background('../images/wecc_background2.jpg', [0,0])
		#init the text stuff
		pygame.font.init()
		self.myfont = pygame.font.SysFont('Courier New', 15)
		#add the dragNdrop options
		self.dnd=[]
		d1=DragNDrop((10,650,50,50),'../images/city.jpg')
		self.dnd.append(d1)
		d2=DragNDrop((130,650,50,50),'../images/transmission.png')
		self.dnd.append(d2)
		d3=DragNDrop((250,650,50,50),'../images/hydro.png')
		self.dnd.append(d3)
		d4=DragNDrop((370,650,50,50),'../images/solar.png')
		self.dnd.append(d4)
		d5=DragNDrop((490,650,50,50),'../images/wind.jpg')
		self.dnd.append(d5)

		self.update_text="Game has started!\n"
		self.year=0
		self.createCities()
		self.createTransmissionLines()
		self.displayMenu=False
		self.menu_options=[]

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
			icon.update(self.screen)
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
		self.rend = pygame.font.SysFont('Courier New', 20,bold=True).render(self.text, True, self.get_color())
		
	def get_color(self):
		if self.hovered:
			return (150, 150, 150)
		else:
			return (0, 0, 0)
		
	def set_rect(self):
		self.set_rend()
		self.rect = self.rend.get_rect()
		self.rect.topleft = self.pos



	