import pygame
import planes

class Background(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

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
		self.update_text=""

def textUpdate(board,input_text):
	textsurface = board.myfont.render(input_text, False, (0, 0, 0))
	board.screen.blit(textsurface,(621,0))

def backgroundUpdate(board):
	board.screen.fill([255, 255,255])
	board.screen.blit(board.BackGround.image, board.BackGround.rect)

def draggablesUpdate(board):
	for i,icon  in enumerate(board.dnd):
		# print board.dnd
		icon.update(board.screen)
		# board.screen.blit(icon,(i*100,700))
	return None
	# city_im=pygame.image.load()
	# p=planes.Plane("City",city_im)

class DragNDrop:
    def __init__(self,rect,filename):
        self.rect = pygame.Rect(rect)
        self.click = False
        self.image = pygame.image.load(filename)
    def update(self,surface):
        if self.click:
            self.rect.center = pygame.mouse.get_pos()
        surface.blit(self.image,self.rect)