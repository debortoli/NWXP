import pygame
import planes
class Board:
	def __init__(self):
		# initialize game engine
		pygame.init()
		self.size = [1000,1000]#width then height
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption('Grid Simulator')
		self.clock = pygame.time.Clock()

		#init the background stuff
		self.BackGround = Background('../images/wecc_background.jpg', [0,0])
		#init the text stuff
		pygame.font.init()
		self.myfont = pygame.font.SysFont('Courier New', 15)
		#add the dragNdrop options
		self.dnd=[]
		d=DragNDrop((0,900,50,50),'../images/city.jpg')
		self.dnd.append(d)
		self.update_text="Game has begun!\n"
		self.year=0
		self.createCities()
		self.createTransmissionLines()

	def createCities(self):
		self.cities=[]
		c=City('../images/city_small.jpg',[110,180])
		self.cities.append(c)
		c=City('../images/city_small.jpg',[93,240])
		self.cities.append(c)

	def createTransmissionLines(self):
		self.transmissionLines=[]
		t=Transmission('../images/transmission_small.png',[90,205],
			"PortlandCorvallis",0)
		self.transmissionLines.append(t)

	def textUpdate(self):
		#format text
		line=""
		line_num=0
		for char in self.update_text:
			if char=='\n':
				t=self.myfont.render(line, False, (0, 0, 0))
				self.screen.blit(t,(621,0+20*line_num))
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

	def draggablesUpdate(self):
		for i,icon  in enumerate(self.dnd):
			icon.update(self.screen)
			# board.screen.blit(icon,(i*100,700))

	def checkPowerLineAge(self):
		for line in self.transmissionLines:
			# print self.update_text[(len(str(line.name))+1)*-1:-1]
			if(line.age>15 and
				self.update_text[(len(str(line.name))+1)*-1:-1]!=str(line.name)):
				self.update_text+="Powerline out of date: "+str(line.name)+"\n"



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

	