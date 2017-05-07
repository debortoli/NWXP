import pygame
from pygame.locals import *
import pdb
import Tkinter as tk
import random

def initLevel3(board,disp,root):
	#set some board logic stuff
	if(len(board.updateQueue)<1):

		# m1="Welcome to Level 2!"+'\n'+\
		# 	"You will now play the role of a Power Administrator, also called a "+'\n'+\
		# 	"System Operator. Power Administrators are in charge of managing the flow of "+'\n'+\
		# 	"electricity from electric generators to consumers."+'\n'
		# board.updateQueue.append([m1,1])
		# # root.after(1,disp.updateMessage)

		# m2="An example of a hydroelectric dam generator is shown here."+'\n'+\
		# "Hover your mouse over the icon to get information about it!"+'\n'
		# board.updateQueue.append([m2,2])

		# m3="The electric capacity of a generator is how much energy the generator is capable"+'\n'+\
		# "of supplying at any given time. This is typically measure in MegaWatts. For reference "+'\n'+\
		# "1 MegaWatt can supply about enough energy to power 650 homes for an hour."+'\n'
		# board.updateQueue.append([m3,3])

		# m4="Once a generator supplies power to the grid, the Power Administrator coordinates"+'\n'+\
		# "moving that power to consumers, also called the Load. For simplicity we have consolidated"+'\n'+\
		# "the loads into 3 categories: Residential, Commercial, and Industrial. "
		# board.updateQueue.append([m4,4])

		# m45="Here is an example of a Residential load. Notice that demand is typically measured"+'\n'+\
		# "in MegaWattHours (which measures MegaWatts over time)."+'\n'+\
		# "Hover your mouse over the icon to get information about it! "+'\n'
		# board.updateQueue.append([m45,4.5])

		# m5="At any given time, not every generator is supplying power to the electric grid."+'\n'+\
		# "A primary responsibility of the Power Administrator is to run the electric market, which"+'\n'+\
		# " determines the generators supplying power at what time."
		# board.updateQueue.append([m5,5])

		# m55="When selecting generators, there are two main considerations "+'\n'+\
		# "1) The cost of running a generator (the bid rate)"+'\n'+\
		# "2) The demand at any given time (as simplified in this game by "+'\n'+\
		# "the Demand Profile Table)"
		# board.updateQueue.append([m55,5.5])

		# m6="To select generators, click on generators in the Generator Fleet table and press 'Enter'. "+'\n'+\
		# "You will notice that the generator will then get added to the Market Clearing table."+'\n'+\
		# "The capacity of the chosen generator (in MW) is multiplied by the time period duration "+'\n'+\
		# "(in hours) to compute the total amount of power (in MWh) secured for the time period. "
		# board.updateQueue.append([m6,6])

		# m7="Once you have reached the amount needed by the time period, the"+'\n'+\
		# "power is automatically dispatched."
		# board.updateQueue.append([m7,7])

		# m8="In this game there are 5 Demand Periods that must be accounted for."+'\n'+\
		# "The first (Off-Peak AM) and the last two (Daytime 2 and Off-Peak PM) will"+'\n'+\
		# "be filled in automatically. Throughout the game you will be responsible for "+'\n'+\
		# "running the market during the remaining two periods. "+'\n'
		# board.updateQueue.append([m8,8])

		# m9= "Notice how the demand changes throughout the day. During the early"+'\n'+\
		# 	"morning and late evening as people sleep the demand is low."+'\n'+\
		# 	"During the day, especially when consumers come home from work,"+'\n'+\
		# 	"the energy needs are the greatest. "+'\n'
		# board.updateQueue.append([m9,9])

		# m10="Throughout the day, the estimate for the demand may have been"+'\n'+\
		# 	"too low. In order to make up the difference, generators can be designated for"+'\n'+\
		# 	"ancillary services. These generators will be on stand-by during the day, waiting"+'\n'+\
		# 	"in the event that additional generation is needed. "
		# board.updateQueue.append([m10,10])

		# m105="Once all of the dispatch periods have been filled in,"+'\n'+\
		# 	"you will have time to select generators to designate for ancillary services."
		# board.updateQueue.append([m105,10.5])

		# m11="As a power administrator, you must pay these generators to be ready to turn on"+'\n'+\
		# 	"quickly, however securing these services prevents events like black outs"+'\n'+\
		# 	"from occuring. "+'\n'
		# board.updateQueue.append([m11,11])

		m12="Finally, during this level and the next, events will pop up based on decisions"+'\n'+\
			"you make during the game. You will make decisions that affect the reliability of our grid"+'\n'+\
			"and the millions of consumers in the Pacific Northwest. "+'\n'+\
			"Good luck!"+'\n'
		board.updateQueue.append([m12,12])


		# m10=""+'\n'+\
		# 	""+'\n'+\
		# 	""+'\n'+\
		# 	""+'\n'
		# board.updateQueue.append([m10,10])
		disp.updateMessage()

		# root.after(1,disp.updateDisplaysLevel3,root)

def isoLevel(board,disp,root):
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
		
	root.after(disp.updateRate,isoLevel,board,disp,root)
		


	
	
