import pygame

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
		self.size = [1000,00]#width then height
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption('Grid Simulator')
		self.clock = pygame.time.Clock()

		#init the background stuff
		self.BackGround = Background('wecc_background.jpg', [0,0])
		#init the text stuff
		pygame.font.init()
		self.myfont = pygame.font.SysFont('Courier New', 15)

def textUpdate(board,input_text):
	textsurface = board.myfont.render(input_text, False, (0, 0, 0))
	board.screen.blit(textsurface,(621,0))

def backgroundUpdate(board):
	board.screen.fill([255, 255,255])
	board.screen.blit(board.BackGround.image, board.BackGround.rect)
