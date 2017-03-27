import pygame
import planes
from pygame.locals import *
import pdb
from utils import UpdateMessageSurface

def tutorialSequence(board):
	# thing=pygame.Surface((450,200), pygame.SRCALPHA)
	# thing.fill((255,255,255,200))
	one=UpdateMessageSurface("This is a message to start"+'\n'+ "About a thing."+'\n')
	board.updateQueue.append(one)
	one.update()
	board.screen.blit(one.messageSurface,(100,450))
