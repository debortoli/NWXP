import pygame
import planes
from pygame.locals import *
import pdb
import Tkinter as tk

def tutorialSequence(board,disp,root):
	#on the first iteration, add all of the messages
	if(len(board.updateQueue)<1):
		m1="Welcome to the Grid Simulator Game!"+'\n'+\
						"To start out, your role will be to manage the Bonneville Dam"+'\n'+\
								 "right here in the PNW."+'\n'
		board.updateQueue.append(m1)
		root.after(100,disp.updateMessage)

		m2="Managing a damn involves controlling the dam bypass "+'\n'+\
		   "and the turbine throttle (to control water flow. The"+'\n'+\
		   "goal is to manage these in response to load demand and resevoir level"+'\n'
		board.updateQueue.append(m2)
		#explain the responses with message and visuals

	board.water_level+=0.1
	if(board.progress<99.5):
		board.progress+=0.1
		if(board.water_level>99):
			board.progress-=20.
		root.after(100,disp.spinTurbine,root)
	else:
		root.after(100,disp.level1End,root)
