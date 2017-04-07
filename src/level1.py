import pygame
from pygame.locals import *
import pdb
import Tkinter as tk

def damLevel(board,disp,root):

	board.water_level+=0.01
	if(board.progress<99.5):
		board.progress+=0.1
		if(board.water_level>99):
			board.progress-=20.
		if(board.water_level>90):
			board.updateQueue.append(["The water level is getting too high!",8])
			root.after(100,disp.updateMessage)
		else:
			#remove the message
			if(len(board.updateQueue)>0 and board.updateQueue[0][0]==8):
				del board.updateQueue[0]
				root.after(100,disp.updateMessage)

		root.after(100,disp.spinTurbine,root)
	else:
		root.after(100,disp.level0End,root)