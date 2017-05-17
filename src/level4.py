import pygame
from pygame.locals import *
import pdb
import Tkinter as tk
import random

def initLevel4(board,disp,root):
	#set some board logic stuff
	if(len(board.updateQueue)<1):
		board.updateQueue.append(["",0])
		m1="Welcome to the final level: Level 3!"+'\n'+\
			"You're still a Power Administrator, but now there are additional events that deal with "+'\n'+\
			"renewable energy. Renewable energy is a great investment in our  environment and future "+'\n'+\
			"As you will see, renewables introduce unique and exciting challenges into managing the grid.  "+'\n'
		board.updateQueue.append([m1,1])
		# root.after(1,disp.updateMessage)

		m2="When you are ready to begin press the  Continue button below!"
		board.updateQueue.append([m2,2])
		

		disp.nextMessage()

		# root.after(1,disp.updateDisplaysLevel3,root)


def renewLevel(board,disp,root):
	# print board.numEvents
	# print board.numEvents
	if(board.numEvents==6):
		root.after(disp.updateRate,disp.level1End,root)
	runMarket(board,disp,root)
	root.after(disp.updateRate,disp.level3MessageHandler,root)


def runMarket(board,disp,root):
	# print board.cumulGen,board.demandProfile[board.time_period],board.demandProfile[board.time_period][1] 
	#if we have allocated enough energy, move the time period up 1

	r=0
	
	root.after(disp.updateRate,renewLevel,board,disp,root)
		


	
	
