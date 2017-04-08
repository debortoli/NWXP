import pygame
from pygame.locals import *
import pdb
import Tkinter as tk
from level1 import damLevel,initLevel1,powerProduced

def tutorialSequence(board,disp,root):
	#on the first iteration, add all of the messages
	if(len(board.updateQueue)<1 and board.progress<1):
		m1="Welcome to the Grid Simulator Game!"+'\n'+\
			"To start out, your role will be to manage the Bonneville Dam"+'\n'+\
			"right here in the PNW."+'\n'
		board.updateQueue.append([m1,1])
		root.after(100,disp.updateMessage)

		m2="A dam works by using the energy in flowing water to spin a turbine. "+'\n'
		board.updateQueue.append([m2,2])
		#highlight turbine

		m3="Running electricity allows the dam to avoid overflowing of the water"+"\n"+\
		   "Try to increase the water velocity to water water flow through the turbine!"
		board.updateQueue.append([m3,3])
		#highlight water velocity slider

		m4="As an electricity generator, your goal is to produce exactly the correct"+"\n"+\
		   "amount of energy that is needed. This amount is indicated by the load sign."+"\n"+\
		   "Try to increase the power produced until you reach the amount necessary!"+"\n"+\
		   "Then press the continue button to move on."
		board.updateQueue.append([m4,4])
		#highlight load indicator

		m5="The required load will change every 20 seconds, so watch the indicator!"
		board.updateQueue.append([m5,5])

		m6="You have two main goals as a dam manager:"+"\n"+\
		   "1: Keep water flowing in order to avoid spilling water"+"\n"+\
		   "2: Don't flow water so fast that you exceed the generation needed by the load."
		board.updateQueue.append([m6,6])

		m7="You can beat this level of the game by successfully running the dam"+"\n"+\
		   "for 2 minutes. When you are ready press the 'Continue' Button"
		board.updateQueue.append([m7,7])

	
	
	board.progress+=0.05
	root.after(100,disp.spinTurbine,root)
	powerProduced(board)
	#if we have gone through all of the messages
	if(len(board.updateQueue)<1):
		board.level=1
		root.after(10,damLevel,board,disp,root)
