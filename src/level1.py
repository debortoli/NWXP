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

		m2="Managing a damn involves controlling the dam bypass "+'\n'+\
		   "and the turbine throttle (to control water flow. The"+'\n'+\
		   "goal is to manage these in response to load demand and resevoir level"+'\n'
		board.updateQueue.append(m2)
		#explain the responses with message and visuals
		
	root.after(200,disp.updateMessage)
