import pygame
from pygame.locals import *
import pdb
import Tkinter as tk
import random

def initLevel3(board,disp,root):
	#set some board logic stuff
	if(len(board.updateQueue)<1):
		m1="Welcome to Level 2!"+'\n'+\
			"You will now play the role of a Power Administrator, also called a System Operator. System Operators are in charge"+'\n'+\
			"of managing the flow of electricity from electric generators to consumers."+'\n'
		board.updateQueue.append([m1,1])
		root.after(1,disp.updateMessage)

		m2="An example of a hydroelectric dam generator is shown here."+'\n'+\
		"Hover your mouse over the icon to get information about it!"+'\n'
		board.updateQueue.append([m2,2])

		m3="The electric capacity of a generator is how much energy the generator is capable"+'\n'+\
		"of supplying at any given time. This is typically measure in MegaWatts. For reference 1 MegaWatt can supply about enough energy"+'\n'+\
		"to power 650 homes for an hour."+'\n'
		board.updateQueue.append([m3,3])

		m4="Once a generator supplies power to the grid, the System Operator coordinates"+'\n'+\
		"moving that power to consumers, also called the Load. For simplicity we have consolidated the "+'\n'+\
		"loads into 3 categories: Residential, Commercial, and Industrial. Here is an example of a  "+'\n'+\
		"Residential load. Notice that demand is typically measured in MegaWattHours (which measures MegaWatts over time)."+'\n'+\
		"Hover your mouse over the icon to get information about it! "+'\n'
		board.updateQueue.append([m4,4])

		m5="At any given time, not every generator is supplying power to the electric grid."+'\n'+\
		"Another responsibility of the System Operator is to run the electric market, which determines the generators "+'\n'+\
		"supplying power at what time.  There are two main considerations when selecting generators:"+'\n'+\
		"1) The cost of running a generator (the bid rate)"+'\n'+\
		"2) The demand at any given time (as simplified in this game by the Demand Profile Table)"+'\n'
		board.updateQueue.append([m5,5])

		m6="To select generators, click on generators in the Generator Fleet table and press 'Enter'. "+'\n'+\
		"You will notice that the generator will then get added to the Market Clearing table."+'\n'+\
		"The capacity of the chosen generator (in MW) is multiplied by the time period duration (in hours) to compute"+'\n'+\
		"the total amount of power (in MWh) secured for the time period. "
		board.updateQueue.append([m6,6])

		m7="Once you have reached the amount needed by the time period, the power is automatically dispatched."+'\n'+\
		"Hover your mouse over the icon to get information about it!"+'\n'
		board.updateQueue.append([m7,7])

		# m8="An example of a hydro dam generator is shown here."+'\n'+\
		# "Hover your mouse over the icon to get information about it!"+'\n'
		# board.updateQueue.append([m8,8])

		root.after(1,disp.updateDisplaysLevel3,root)

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
		


	
	
