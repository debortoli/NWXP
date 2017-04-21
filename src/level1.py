import pygame
from pygame.locals import *
import pdb
import Tkinter as tk
import random

def initLevel1(board):
	board.progress=0
	board.totalPoints=0
	board.loadChangeTime=pygame.time.get_ticks()
	board.time="09:00 AM"
	board.damLoad=board.possibleLoadLevels[int(board.time[:2])-1]
	board.spilledSeconds=0
	board.water_level=87

def damLevel(board,disp,root):

	board.water_level+=0.018
	if(board.progress<99.5):
		if(board.water_level>99):
			board.progress-=20.
		if(board.water_level>95):
			board.updateQueue.append(["The water level is getting high. \n Consider spilling!",8])
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
			
			board.loadChangeTime=pygame.time.get_ticks()

			#increment the hour
			if(int(board.time[:2])==11 and board.time[-2:]=='AM'):
				board.time="12:00 PM"
			elif(int(board.time[:2])==11 and board.time[-2:]=='PM'):
				board.time="12:00 AM"
			elif(int(board.time[:2])==12):
				board.time="01:00 "+str(board.time[-2:])
			else:
				if(int(board.time[:2])+1<10):
					board.time="0"+str(int(board.time[:2])+1)+":00 "+str(board.time[-2:])
				else:
					board.time=str(int(board.time[:2])+1)+":00 "+str(board.time[-2:])
			#choose the load level based on the time
			if(str(board.time[-2:])=='AM'):
				if(int(board.time[:2])==12):
					board.damLoad=board.possibleLoadLevels[0]
				else:
					board.damLoad=board.possibleLoadLevels[int(board.time[:2])]

			else:
				if(int(board.time[:2])==12):
					board.damLoad=board.possibleLoadLevels[12]
				else:
					board.damLoad=board.possibleLoadLevels[int(board.time[:2])+12]
		else:
			#increment the seconds
			#to make the single digit seconds include a 0
			if(int((pygame.time.get_ticks()-board.loadChangeTime)*3/1000.)<10):
				secs=":0"+str(int((pygame.time.get_ticks()-board.loadChangeTime)*3/1000.))
			else:
				secs=":"+str(int((pygame.time.get_ticks()-board.loadChangeTime)*3/1000.))

			board.time=board.time[:2]+secs+" "+str(board.time[-2:])


	else:
		#same code as above kind of. possible some ineffeciencies in coding here
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
	board.powerProducedDam=int(board.water_velocity)+900
	if(board.powerProducedDam<0):
		board.powerProducedDam=0
	elif(board.water_velocity==0):
		board.powerProducedDam=0

def addPoints(board,disp):
	if abs(board.powerProducedDam-board.damLoad)<5:
		board.progress+=(disp.updateRate/2)/1000./3 #/1.2  amounts to 1/1.2 percent a second * 120 seconds gives 100 percent
		board.totalPoints+=0.01
	if abs(board.powerProducedDam-board.damLoad)<1:
		board.totalPoints+=0.01