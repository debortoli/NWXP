import pygame
from pygame.locals import *
import pdb
import Tkinter as tk
from level1 import damLevel,initLevel1,powerProduced

def tutorialSequence(board,disp,root):
	#on the first iteration, add all of the messages
	if(len(board.updateQueue)<1 and board.progress==0.):
		m1="Welcome to the Grid Simulator Game!"+'\n'+\
			"To start out, your role will be to manage the Bonneville Dam"+'\n'+\
			"right here in the PNW."+'\n'
		board.updateQueue.append([m1,1])
		root.after(1,disp.updateMessage)

		m2="A dam works by converting the energy in flowing water into electricity"+'\n'+\
		"by spinning  a turbine. "+'\n'
		board.updateQueue.append([m2,2])
		#highlight turbine

		m3="Increasing the turbine speed increases the water flow rate through the dam"+"\n"+\
			"and the amount of electricity produced. Try to increase the water velocity"+"\n"+\
		   "to water water flow through the turbine!"
		board.updateQueue.append([m3,3])
		#highlight water velocity slider

		m4="As an electricity generator, your goal is to produce exactly the correct"+"\n"+\
		   "amount of energy that is needed. This amount is indicated by the load sign."+"\n"+\
		    "The load is determined by anyone who uses electricity!"+"\n"+\
		   "Try to increase the power produced until you reach the amount necessary!"+"\n"+\
		   "Then press the continue button to move on."
		board.updateQueue.append([m4,4])
		#highlight load indicator

		m5="The load will vary every 'hour'. An hour (as indicated by the clock in the upper left) is "+"\n"+\
		   "about 20 seconds of real time. The load amount is determined by the energy consumers!"+"\n"+\
		   "The typical unitused while observing generation and loas values is Megawatts. "+"\n"+\
		   "During the night energy consumption is low, and during the late afternoon when everyone "+"\n"+\
		   "comes home energy consumption is the highest."
		board.updateQueue.append([m5,5])

		#highlight the spill button
		m6="One real world challenge is that a lot of rains falls in this area, which raises the "+"\n"+\
		   "level of the incoming water source. Spilling the dam is a necessary process which decreases  "+"\n"+\
		   "the water level in a safe manner. Spilling is necessary to prevent the overflowing of the "+"\n"+\
		   "incoming river. In this game, if the incoming source overflows, the level restarts."
		board.updateQueue.append([m6,6])
		
		m7="Spilling can be done by pressing and holding the button on top of the dam. Try it!"+"\n"+\
		   "While spilling is helpful, unfortunately it has the potential to harm fish populations "+"\n"+\
		   "living in these rivers or lakes. Therefore, we limit the amount of time you can spill the "+"\n"+\
		   "incoming source to 20 seconds."
		board.updateQueue.append([m7,7])

		m8="You gain points in this game by successfully running the dam. This can only be done by "+"\n"+\
		   "producing near the correct amount of power needed by the load. Points are awarded "+"\n"+\
		   "depending on how close your production is to the load."
		board.updateQueue.append([m8,8])

		m9="You have two main goals as a dam manager:"+"\n"+\
		   "1: Keep water flowing in order to avoid spilling water"+"\n"+\
		   "2: Don't flow water so fast that you exceed the generation needed by the load."
		board.updateQueue.append([m9,9])

		m10="You can beat this level of the game by successfully running the dam"+"\n"+\
		   "for 2 minutes. When you are ready press the 'Continue' Button!"
		board.updateQueue.append([m10,10])

	
	
	board.progress+=0.01
	root.after(1,disp.spinTurbine,root)
	powerProduced(board)
	#if we have gone through all of the messages
	if(len(board.updateQueue)<1):
		board.level=1
		initLevel1(board)
		root.after(1,damLevel,board,disp,root)
