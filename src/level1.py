import pygame
import planes
from pygame.locals import *
import pdb
import Tkinter as tk

def tutorialSequence(board):
	#on the first iteration, add all of the messages
	if(len(board.updateQueue)<1):
		one=UpdateMessageSurface(board,"Welcome to the Grid Simulator Game!"+'\n'+
								 "To start out your role will be to manage the Bonneville Dam"+'\n'+
								 "right here in the PNW."+'\n')
		board.updateQueue.append(one)
	

	board.updateQueue[0].update(board)
	board.screen.blit(board.updateQueue[0].messageSurface,(board.UpdateMessageSurface_x,board.UpdateMessageSurface_y))

	root = tk.Tk()
	explanation = """At present, only GIF and PPM/PGM
	formats are supported, but an interface 
	exists to allow additional image file
	formats to be added easily."""
	w2 = tk.Label(root, 
	           padx = 10, 
	           text=explanation).pack(side="left")
	board.screen.blit(root,(100,100))
