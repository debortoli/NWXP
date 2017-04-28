import pygame
from pygame.locals import *
import pdb
import Tkinter as tk
import random

def initLevel3(board,root):
	#set some board logic stuff
	p=0

def isoLevel(board,disp,root):
	runMarket(board,disp,root)
	# root.after(disp.updateRate,disp.updateDisplaysLevel3,root)

def runMarket(board,disp,root):
	# print board.cumulGen,board.demandProfile[board.time_period],board.demandProfile[board.time_period][1] 
	#if we have allocated enough energy, move the time period up 1

	if((board.cumulGen>=board.demandProfile[board.time_period][1]) or (board.dispatchProfile[board.time_period][1]==board.demandProfile[board.time_period][1])):
		if(board.time_period<4):
			disp.clearTimePeriod()
			board.time_period+=1
			board.last_time_period=board.time_period
			
	#if we're in an autofill period
	if(board.time_period==3):
		disp.updateDispatchProfile()
		root.after(disp.updateRate,disp.updateDisplaysLevel3,root)
	if(board.time_period==4):
		disp.updateDispatchProfile()
		disp.clearTimePeriod()
		board.time_period+=1
		root.after(disp.updateRate,disp.updateDisplaysLevel3,root)
		
	root.after(disp.updateRate,isoLevel,board,disp,root)
		


	
	
