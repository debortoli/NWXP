import pygame
from pygame.locals import *
import pdb
import Tkinter as tk
import random

def initLevel1(board):
	board.progress=0
	board.loadChangeTime=pygame.time.get_ticks()

def damLevel(board,disp,root):

	board.water_level+=0.01
	if(board.progress<99.5):
		if(board.water_level>99):
			board.progress-=20.
		if(board.water_level>90):
			board.updateQueue.append(["The water level is getting too high. \n Increase the water flow rate!",8])
			root.after(1,disp.updateMessage)
		else:
			#remove the message
			if(len(board.updateQueue)>0 and board.updateQueue[0][1]==8):
				del board.updateQueue[0]
				root.after(1,disp.nextMessage)

		#update the power produced
		powerProduced(board)
		addPoints(board,disp)

		root.after(disp.updateRate,disp.spinTurbine,root)

		#choose another random load amount every 20 seconds
		if((pygame.time.get_ticks()-board.loadChangeTime)>20*1000):
			board.damLoad=board.possibleLoadLevels[random.randint(0,len(board.possibleLoadLevels)-1)]
			board.loadChangeTime=pygame.time.get_ticks()

	else:
		#same code as above kind of. possible some ineffeciencies in coding here
		if(board.water_level>99):
			board.progress-=20.
		if(board.water_level>90):
			board.updateQueue.append(["The water level is getting too high. \n Increase the water flow rate!",8])
			root.after(1,disp.updateMessage)
		else:
			#remove the message
			if(len(board.updateQueue)>0 and board.updateQueue[0][1]==8):
				del board.updateQueue[0]
				root.after(1,disp.nextMessage)

		#update the power produced
		powerProduced(board)
		addPoints(board,disp)

		root.after(disp.updateRate,disp.level1End,root)

def powerProduced(board):
	board.powerProducedDam=int(0.3*board.water_velocity)+50
	if(board.powerProducedDam<0):
		board.powerProducedDam=0
	elif(board.water_velocity==0):
		board.powerProducedDam=0

def addPoints(board,disp):
	if abs(board.powerProducedDam-board.damLoad)<5:
		board.progress+=(disp.updateRate/2)/1000./1.2 #amounts to 1/1.2 percent a second * 120 seconds gives 100 percent
		board.totalPoints+=0.01
	if abs(board.powerProducedDam-board.damLoad)<1:
		board.totalPoints+=0.01