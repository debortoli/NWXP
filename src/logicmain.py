# -*- coding: utf-8 -*-
import pygame
import numpy as np 
import math
from utils import Board
import time
from pygame.locals import *
import pdb
from level1 import tutorialSequence


def initGameLogic():
	board=Board()
	board.clock.tick()
	return board

def gameLogic(disp,board,root):
	if(int(pygame.time.get_ticks()/1000.)%2==0 and 
		(pygame.time.get_ticks()/1000.)>1):
		board.water_level+=1
	root.after(500,disp.updateDisplays,root)

	
	# self.after(0,)
	