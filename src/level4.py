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

		# m4="Once a generator supplies power to the grid, the Power Administrator coordinates "+\
		# "moving that power to consumers, also called the Load. For simplicity we have consolidated "+\
		# "the loads into 3 categories: Residential, Commercial, and Industrial. "
		# board.updateQueue.append([m4,4])

		# m45="Here is an example of a Residential load. Notice that demand is typically measured "+\
		# "in MegaWattHours (which measures MegaWatts over time). "+\
		# "Hover your mouse over the icon to get information about it! "
		# board.updateQueue.append([m45,4.5])

		# m47="At any given time, not every generator is supplying power to the electric grid. "+\
		# 	 "Which generators are running is determined by an energy market. In this market "+\
		# 	 "generators say how much they can produce electricity for (their Bid Rate)."
		# board.updateQueue.append([m47,4.7])


		# m5="During any given time period (Daytime1 or Peak) you must:"+\
		#    "1) Choose the generators which produce electricity at the cheapest rate and "+\
		#    "2) You must select enough generators to meet the demand at that given time period"
		# board.updateQueue.append([m5,5])

		


		# m10=""+'\n'+\
		# 	""+'\n'+\
		# 	""+'\n'+\
		# 	""+'\n'
		# board.updateQueue.append([m10,10])
		disp.nextMessage()

		# root.after(1,disp.updateDisplaysLevel3,root)


def renewLevel(board,disp,root):
	# print board.numEvents
	print board.numEvents
	if(board.numEvents==1):
		root.after(disp.updateRate,disp.level1End,root)
	runMarket(board,disp,root)
	root.after(disp.updateRate,disp.level3MessageHandler,root)


def runMarket(board,disp,root):
	# print board.cumulGen,board.demandProfile[board.time_period],board.demandProfile[board.time_period][1] 
	#if we have allocated enough energy, move the time period up 1

	r=0

	# if((board.cumulGen>=board.demandProfile[board.time_period][1]) or (board.dispatchProfile[board.time_period][1]==board.demandProfile[board.time_period][1])):
	# 	if(board.time_period<4):
	# 		disp.clearTimePeriod()
	# 		board.time_period+=1
	# 		board.last_time_period=board.time_period
			
	# #if we're in an autofill period
	# if(board.time_period==3):
	# 	disp.updateDispatchProfile()
	# 	root.after(disp.updateRate,disp.updateDisplaysLevel3,root)
	# if(board.time_period==4):
	# 	disp.updateDispatchProfile()
	# 	disp.clearTimePeriod()
	# 	board.time_period+=1
	# 	root.after(disp.updateRate,disp.updateDisplaysLevel3,root)
		
	root.after(disp.updateRate,renewLevel,board,disp,root)
		


	
	
