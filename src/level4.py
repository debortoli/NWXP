import pygame
from pygame.locals import *
import pdb
import Tkinter as tk
import random

def initLevel4(board,disp,root):
	#set some board logic stuff
	if(len(board.updateQueue)<1):

		# m1="Welcome to Level 2!"+'\n'+\
		# 	"You will now play the role of a Power Administrator, also called a "+'\n'+\
		# 	"System Operator. Power Administrators are in charge of managing "+'\n'+\
		# 	"the flow of electricity from electric generators to consumers."+'\n'
		# board.updateQueue.append([m1,1])
		# # root.after(1,disp.updateMessage)

		# m2="An example of a hydroelectric dam generator is shown here. "+\
		# "Hover your mouse over the icon to get information about it!"
		# board.updateQueue.append([m2,2])

		# m3="The electric capacity of a generator is how much energy the generator is capable "+\
		# "of supplying at any given time. This is typically measure in MegaWatts. For reference "+\
		# "1 MegaWatt can supply about enough energy to power 650 homes for an hour."
		# board.updateQueue.append([m3,3])

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

		# m55="To select generators, click on generators in the Generator Fleet table and press 'Enter'. "+\
		#     "Try to add a cheap generator with a Bid Rate of $12! "
		# board.updateQueue.append([m55,5.5])

		# m6="You will notice that the generator will then get added to the Market Clearing table. "+\
		# "The capacity of the chosen generator (in MW) is multiplied by the time period duration "+\
		# "(in hours) to compute the total amount of power (in MWh) secured for the time period. "
		# board.updateQueue.append([m6,6])

		# m65="Your goal will be to to select enough generators (as indicated by the 'Cumulative MWh column)"+\
		# "to meet the load for that time period. You must select at least enough generators, but also not more"+\
		# "than you need. You can delete selected generators by clicking the red button. "
		# board.updateQueue.append([m65,6.5])

		# m7="Once you have reached the amount needed by the time period, the "+\
		# "power is automatically dispatched."
		# board.updateQueue.append([m7,7])

		# m8="In this game there are 5 Demand Periods that must be accounted for. "+\
		# "The first (Off-Peak AM) and the last two (Daytime 2 and Off-Peak PM) will "+\
		# "be filled in automatically. Throughout the game you will be responsible for "+\
		# "running the market during the Daytime1 and Peak time periods."
		# board.updateQueue.append([m8,8])

		# m9= "Notice how the demand changes throughout the day. During the early "+\
		# 	"morning and late evening as people sleep the demand is low. "+\
		# 	"During the day, especially when consumers come home from work, "+\
		# 	"the energy needs are the greatest. "
		# board.updateQueue.append([m9,9])

		# m10="What has just been described is a market that real engineers run the day before (thus it is called the 'Day-Ahead' Market.)"+\
		# 	"On the day of, the estimate for the demand may have been "+\
		# 	"too low. In order to make up the difference, generators can be designated for "+\
		# 	"'Ancillary Services'. These generators will not run unless they are needed, but must be ready"+\
		# 	"in the event that additional generation is needed. "
		# board.updateQueue.append([m10,10])

		# m11="As a power administrator, you must pay these generators to be ready to turn on "+\
		# 	"quickly (in the game you will lose a small number of points). However securing these services"+\
		# 	"prevents events like black outs from occuring. During the game not having Ancillary Services"+\
		# 	"leaves open the possibility to lose a lot of points."
		# board.updateQueue.append([m11,11])

		# m105="Once all of the dispatch periods have been filled in, "+\
		# 	"you will have time to select generators to designate for ancillary services."
		# board.updateQueue.append([m105,10.5])


		m12="Finally, during this level and the next, events will pop up based on the conditions of "+\
			"the grid. After you complete a certain number of events you will be able to move onto the next "+\
			"level. You will make decisions that affect the reliability of our grid "+\
			"and the millions of consumers in the Pacific Northwest. "+\
			"Good luck!"
		board.updateQueue.append([m12,12])


		# m10=""+'\n'+\
		# 	""+'\n'+\
		# 	""+'\n'+\
		# 	""+'\n'
		# board.updateQueue.append([m10,10])
		disp.updateMessage()

		# root.after(1,disp.updateDisplaysLevel3,root)

def renewLevel(board,disp,root):
	# print board.numEvents
	
	if(board.numEvents==6):
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
		


	
	
