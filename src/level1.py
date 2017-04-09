import pygame
from pygame.locals import *
import pdb
import Tkinter as tk
import random

def initLevel1(board):
	board.progress=0
	board.totalPoints=0
	board.loadChangeTime=pygame.time.get_ticks()

def damLevel(board,disp,root):

	board.water_level+=0.01
	if(board.progress<99.5):
		board.progress+=(disp.updateRate/2)/1000./1.2 #amounts to 1/1.2 percent a second * 120 seconds gives 100 percent

		if(board.water_level>99):
			board.progress-=20.
		if(board.water_level>90):
			board.updateQueue.append(["The water level is getting too high!",8])
			root.after(1,disp.updateMessage)
		else:
			#remove the message
			print "removing water level message"
			if(len(board.updateQueue)>0 and board.updateQueue[0][0]==8):
				del board.updateQueue[0]
				root.after(1,disp.updateMessage)

		#update the power produced
		powerProduced(board)
		addPoints(board)

		root.after(disp.updateRate,disp.spinTurbine,root)

		#choose another random load amount every 20 seconds
		if((pygame.time.get_ticks()-board.loadChangeTime)>20*1000):
			board.damLoad=board.possibleLoadLevels[random.randint(0,len(board.possibleLoadLevels))]
			board.loadChangeTime=pygame.time.get_ticks()

	else:
		root.after(disp.updateRate,disp.level1End,root)

def powerProduced(board):

	board.powerProducedDam=int(0.3*board.water_velocity)+50
	if(board.powerProducedDam<0):
		board.powerProducedDam=0
	elif(board.water_velocity==0):
		board.powerProducedDam=0

def addPoints(board):
	if abs(board.powerProducedDam-board.damLoad)<5:
		board.totalPoints+=0.01
	if abs(board.powerProducedDam-board.damLoad)<1:
		board.totalPoints+=0.01