# -*- coding: utf-8 -*-
import pygame
import numpy as np 
import math
from utils import Board
import time
from pygame.locals import *
import pdb
from level0 import tutorialSequence
from level1 import damLevel
from level3 import isoLevel
from level4 import renewLevel


def initGameLogic(skip1):
	board=Board(skip1)
	board.clock.tick()
	return board

def gameLogic(disp,board,root):
	# if(int(pygame.time.get_ticks()/1000.)%2==0 and 
	# 	(pygame.time.get_ticks()/1000.)>1):
	# 	board.water_level+=1
	# root.after(500,disp.updateDisplays,root)
	
	if(board.level==0):
		tutorialSequence(board,disp,root)
	if(board.level==1):
		damLevel(board,disp,root)
	if(board.level==3):
		isoLevel(board,disp,root)
	if(board.level==4):
		renewLevel(board,disp,root)
	# if(board.level==4):
	# 	isoLevel(board,disp,root)
	# print board.level
	

	
	# self.after(0,)
	