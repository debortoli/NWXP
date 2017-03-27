import pygame
import planes
from pygame.locals import *
import pdb
from utils import UpdateMessageSurface

def tutorialSequence(board):
	#on the first iteration, add all of the messages
	if(len(board.updateQueue)<1):
		one=UpdateMessageSurface(board,"Welcome to the Grid Simulator Game!"+'\n'+
								 "To start out your role will be to manage the Bonneville Dam"+'\n'+
								 "right here in the PNW."+'\n')
		board.updateQueue.append(one)
	

	board.updateQueue[0].update(board)
	board.screen.blit(board.updateQueue[0].messageSurface,(board.UpdateMessageSurface_x,board.UpdateMessageSurface_y))
