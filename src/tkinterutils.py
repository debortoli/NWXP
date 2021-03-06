# from Tkinter import Tk, Label, Button,Canvas,Frame
import Tkinter as tk
import pdb
import time
import ttk
from logicmain import gameLogic
from level1 import initLevel1
from level3 import initLevel3, isoLevel
from level4 import initLevel4, renewLevel
import ttk
from PIL import Image, ImageTk
import random
import numpy as np
import csv
from utils import Tooltip
import locale

class TKBoard:
	def __init__(self, master,boardlogic):
		self.master = master
		master.title("GRID SIMULATOR")
		master.minsize(width=1300,height=800)
		master.maxsize(width=1300,height=800)


		self.boardlogic=boardlogic
		self.root=self.master

		#create update frame which contains 3 widgets
		self.updateFrame= tk.Frame(master)
		self.updateFrame.pack(side="right",fill="y")
		# self.updateFrame.bind("<Configure>", self.on_resize)
		

		#level canvas
		self.levelCanvas = tk.Canvas(self.updateFrame,bg="lightgray",highlightthickness=2,highlightbackground="Black",height=250)
		self.levelCanvas.pack(fill='x')#grid(row=0,column=0,sticky='N')

		self.levelTitle=   tk.Label(self.levelCanvas,bg='lightgray',text="LEVEL PROGRESS",font=("Helvetica", 16))
		self.levelTitle.pack(side='top',pady=15)
		
		self.progress = ttk.Progressbar(self.levelCanvas,style="green.Horizontal.TProgressbar", orient="horizontal", length=300, mode="determinate", maximum=100, value=1)
		self.progress.pack(side='bottom',pady=10)
		self.progress["value"]=boardlogic.progress
		
		

		#points canvas
		self.pointsCanvas = tk.Canvas(self.updateFrame,bg="lightgray",highlightthickness=2,highlightbackground="Black",height=100)
		self.pointsCanvas.pack(fill='x')#grid(row=1,column=0,sticky='N')

		self.pointsTitle=   tk.Label(self.pointsCanvas,bg='lightgray',text="TOTAL POINTS",font=("Helvetica", 16))
		self.pointsTitle.pack(side='top',pady=10)

		self.points = tk.Label(self.pointsCanvas,bg='lightgray',text=str(boardlogic.totalPoints),font=("Helvetica", 25),fg="#309933")
		self.points.pack(side='top',pady=10)

		#draggables canvas
		self.draggablesCanvas = tk.Canvas(self.updateFrame,bg="lightgray",highlightthickness=2,highlightbackground="Black",height=700)
		self.draggablesCanvas.pack()#grid(row=2,column=0,sticky='NS')

		#the game canvas
		self.gameFrame=tk.Frame(master,bg="white",highlightthickness=0)
		self.gameFrame.pack(fill='both',expand=True)

		self.gameCanvas=tk.Canvas(self.gameFrame,bg="white",highlightthickness=0)
		

		#draw constraints for water
		self.damRectangle=[0,150,300,500]

		#compute height of dam
		self.dam_height=self.damRectangle[3]-self.damRectangle[1]

		#draw the top of the dam
		self.dam_width=400
		self.dam_triangle_h=self.dam_height*0.6
		self.tower_height=self.dam_height*0.3
		self.block_width=100
		self.block_height=80
		self.tower_width=100
		self.tower_elevation=50
		self.powerhouse_height=50
		self.powerhouse_width=100
		self.damTopPolygon=self.gameCanvas.create_polygon( self.damRectangle[2],self.damRectangle[1],
													  self.damRectangle[2],self.damRectangle[1]+self.tower_height,
													  self.damRectangle[2]+self.dam_width-self.block_width,self.damRectangle[1]+self.dam_triangle_h,
													  self.damRectangle[2]+self.dam_width,self.damRectangle[1]+self.dam_triangle_h,
													  self.damRectangle[2]+self.dam_width,self.damRectangle[1]+self.dam_triangle_h-self.block_height,
													  self.damRectangle[2]+self.dam_width-self.block_width,self.damRectangle[1]+self.dam_triangle_h-self.block_height,
													  self.damRectangle[2]+self.dam_width-self.block_width,self.damRectangle[1]+self.dam_triangle_h-self.block_height-self.powerhouse_height,
													  self.damRectangle[2]+self.dam_width-self.block_width-self.powerhouse_width,self.damRectangle[1]+self.dam_triangle_h-self.block_height-self.powerhouse_height,
													  self.damRectangle[2]+self.dam_width-self.block_width-self.powerhouse_width,self.damRectangle[1]+self.dam_triangle_h-self.block_height,
													  self.damRectangle[2]+self.tower_width,self.damRectangle[1]+50,
													  self.damRectangle[2]+self.tower_width,self.damRectangle[1],
												  fill="#c0c0c0",width=0)
		#extension to the top of the dam
		self.dam_extension_width=200
		self.damTopExtension=self.gameCanvas.create_rectangle(self.gameCanvas.coords(self.damTopPolygon)[8],
															  self.gameCanvas.coords(self.damTopPolygon)[9],
															  self.gameCanvas.coords(self.damTopPolygon)[8]+self.dam_extension_width,
															  self.gameCanvas.coords(self.damTopPolygon)[7],
															  fill="#c0c0c0",width=0)


		
		#draw the bottom of the dam
		self.penstock_diameter=50
		self.damBottomPolygon=self.gameCanvas.create_polygon(self.damRectangle[2],self.damRectangle[1]+self.tower_height+self.penstock_diameter,
														self.damRectangle[2],self.damRectangle[3],
														self.damRectangle[2]+self.dam_width,self.damRectangle[3],
														self.damRectangle[2]+self.dam_width,self.damRectangle[1]+self.dam_triangle_h+self.penstock_diameter,
														self.damRectangle[2]+self.dam_width-self.block_width,self.damRectangle[1]+self.dam_triangle_h+self.penstock_diameter,
														fill="#c0c0c0",width=0)

		#create the water down the penstock
		self.penstockPolygon=self.gameCanvas.create_polygon(self.gameCanvas.coords(self.damBottomPolygon)[0],self.gameCanvas.coords(self.damBottomPolygon)[1],
														self.gameCanvas.coords(self.damBottomPolygon)[8],self.gameCanvas.coords(self.damBottomPolygon)[9],
														self.gameCanvas.coords(self.damBottomPolygon)[6],self.gameCanvas.coords(self.damBottomPolygon)[7],
														self.gameCanvas.coords(self.damTopPolygon)[6],self.gameCanvas.coords(self.damTopPolygon)[7],
														self.gameCanvas.coords(self.damTopPolygon)[4],self.gameCanvas.coords(self.damTopPolygon)[5],
														self.gameCanvas.coords(self.damTopPolygon)[2],self.gameCanvas.coords(self.damTopPolygon)[3],
														fill="#0000aa",width=0)

		#create the water after the penstock
		self.river_width=350
		self.riverAfterDam=self.gameCanvas.create_rectangle(self.damRectangle[2]+self.dam_width,
															self.damRectangle[1]+self.dam_triangle_h,
															self.damRectangle[2]+self.dam_width+self.river_width,
															self.damRectangle[3],
															fill="#0000aa",width=0)
		
		#flowing of the water
		[self.kneePointx,self.kneePointy]=[self.gameCanvas.coords(self.damTopPolygon)[4],self.gameCanvas.coords(self.damTopPolygon)[5]]
		[self.startx,self.starty]=[self.gameCanvas.coords(self.damTopPolygon)[2],self.gameCanvas.coords(self.damTopPolygon)[3]]
		[self.diffx,self.diffy]=[self.kneePointx-self.startx,self.kneePointy-self.starty]
		self.wave_width=1/15.
		self.wavePolygon=self.gameCanvas.create_polygon(self.startx,self.starty,
														self.startx+self.diffx*self.wave_width,self.starty+self.diffy*self.wave_width,
														self.gameCanvas.coords(self.damBottomPolygon)[0]+self.diffx*self.wave_width,self.gameCanvas.coords(self.damBottomPolygon)[1]+self.diffy*self.wave_width,
														self.gameCanvas.coords(self.damBottomPolygon)[0],self.gameCanvas.coords(self.damBottomPolygon)[1],
														fill="#0000dd",width=0)

		[self.kneePointx1,self.kneePointy1]=[self.gameCanvas.coords(self.damTopPolygon)[4],self.gameCanvas.coords(self.damTopPolygon)[5]]
		[self.startx1,self.starty1]=[self.gameCanvas.coords(self.damTopPolygon)[2],self.gameCanvas.coords(self.damTopPolygon)[3]]
		[self.diffx1,self.diffy1]=[self.kneePointx1-self.startx1,self.kneePointy1-self.starty1]
		self.wave_width=1/15.
		self.wavePolygon2=self.gameCanvas.create_rectangle(self.kneePointx,
														  self.kneePointy,
														  self.kneePointx+self.diffx*self.wave_width,
														  self.kneePointy+self.penstock_diameter,
														fill="#0000dd",width=0)

		#add generator
		self.generator_buffer_x=10
		self.generator_buffer_y=10
		self.generator=self.gameCanvas.create_rectangle(self.gameCanvas.coords(self.damTopPolygon)[16]+self.generator_buffer_x,self.gameCanvas.coords(self.damTopPolygon)[17]-self.generator_buffer_y,
														self.gameCanvas.coords(self.damTopPolygon)[12]-self.generator_buffer_x,self.gameCanvas.coords(self.damTopPolygon)[13]+self.generator_buffer_y,
														fill="#808080",width=0)

		#add power station
		self.p_station_height=80
		self.p_station_width=50
		self.power_line_length=40
		pstationRect=self.gameCanvas.create_rectangle(self.gameCanvas.coords(self.generator)[2]+self.power_line_length,
													self.damRectangle[1]+self.dam_triangle_h-self.block_height-self.p_station_height,
													self.gameCanvas.coords(self.generator)[2]+self.power_line_length+self.p_station_width,
													self.damRectangle[1]+self.dam_triangle_h-self.block_height,
												  fill="#808080",width=0)

		#add the power lines from the generator to the power station
		self.line1=self.gameCanvas.create_line(self.gameCanvas.coords(self.generator)[2],
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2-10,
											   self.gameCanvas.coords(self.generator)[2]+self.power_line_length,
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2-10,
											   fill="#ffff00",width=4)

		self.line2=self.gameCanvas.create_line(self.gameCanvas.coords(self.generator)[2],
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2,
											   self.gameCanvas.coords(self.generator)[2]+self.power_line_length,
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2,
											   fill="#ffff00",width=4)

		self.line3=self.gameCanvas.create_line(self.gameCanvas.coords(self.generator)[2],
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2+10,
											   self.gameCanvas.coords(self.generator)[2]+self.power_line_length,
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2+10,
											   fill="#ffff00",width=4)

		#add the power lines from the power station to the power indicator
		self.power_line_lengthb=60
		self.line1b=self.gameCanvas.create_line(self.gameCanvas.coords(self.generator)[2]+self.power_line_length+self.p_station_width,
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2-10,
											   self.gameCanvas.coords(self.generator)[2]+self.power_line_length+self.p_station_width+self.power_line_lengthb,
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2-10,
											   fill="#ffff00",width=4)

		self.line2b=self.gameCanvas.create_line(self.gameCanvas.coords(self.generator)[2]+self.power_line_length+self.p_station_width,
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2,
											   self.gameCanvas.coords(self.generator)[2]+self.power_line_length+self.p_station_width+self.power_line_lengthb,
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2,
											   fill="#ffff00",width=4)

		self.line3b=self.gameCanvas.create_line(self.gameCanvas.coords(self.generator)[2]+self.power_line_length+self.p_station_width,
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2+10,
											   self.gameCanvas.coords(self.generator)[2]+self.power_line_length+self.p_station_width+self.power_line_lengthb,
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2+10,
											   fill="#ffff00",width=4)

		#add the indicator of power produced
		self.powerIndicator=tk.Label(self.gameCanvas,text="Hi",bg='#00aa00',font=("Helvetica", 17))
		self.powerIndicator_x=self.gameCanvas.coords(self.generator)[2]+self.power_line_length+self.p_station_width+self.power_line_lengthb
		self.powerIndicator_y=(self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2-15
		self.powerIndicator_width=65
		self.powerIndicator.place(x=self.powerIndicator_x,y=self.powerIndicator_y, width=self.powerIndicator_width,height=30)
		#add the post below it
		post_width=10
		self.gameCanvas.create_rectangle(self.powerIndicator_x+32-post_width/2,
										self.powerIndicator_y+30,
										self.powerIndicator_x+32+post_width/2,
										self.powerIndicator_y+40,
										fill="#c0c0c0",width=0)

		#add the label for the powerIndicator
		self.pILabel=tk.Label(self.gameCanvas,text="Power Produced",bg='white',font=("Helvetica", 10))
		self.pILabel.place(x=self.powerIndicator_x-20,y=self.powerIndicator_y-25)

		#add the power lines from the power indicator to the load
		self.power_line_lengthc=40
		self.line1c=self.gameCanvas.create_line(self.powerIndicator_x+self.powerIndicator.winfo_width()+self.powerIndicator_width-1,
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2-10,
											   self.powerIndicator_x+self.powerIndicator.winfo_width()+self.powerIndicator_width-1+self.power_line_lengthc,
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2-10,
											   fill="#ffff00",width=4)

		self.power_line_lengthc=40
		self.line2c=self.gameCanvas.create_line(self.powerIndicator_x+self.powerIndicator.winfo_width()+self.powerIndicator_width-1,
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2,
											   self.powerIndicator_x+self.powerIndicator.winfo_width()+self.powerIndicator_width-1+self.power_line_lengthc,
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2,
											   fill="#ffff00",width=4)

		self.power_line_lengthc=40
		self.line3c=self.gameCanvas.create_line(self.powerIndicator_x+self.powerIndicator.winfo_width()+self.powerIndicator_width-1,
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2+10,
											   self.powerIndicator_x+self.powerIndicator.winfo_width()+self.powerIndicator_width-1+self.power_line_lengthc,
											   (self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2+10,
											   fill="#ffff00",width=4)
		#add the load
		self.LoadIndicator=tk.Label(self.gameCanvas,text="Hi",bg='#00e600',font=("Helvetica", 17))
		self.Load_x=self.powerIndicator_x+self.powerIndicator.winfo_width()+64+self.power_line_lengthc
		self.Load_y=(self.gameCanvas.coords(self.generator)[1]+self.gameCanvas.coords(self.generator)[3])/2-15
		self.LoadIndicator.place(x=self.Load_x,y=self.Load_y, width=65,height=30)
		#add the post below it
		post_width=10
		self.gameCanvas.create_rectangle(self.Load_x+32-post_width/2,
										self.Load_y+30,
										self.Load_x+32+post_width/2,
										self.Load_y+40,
										fill="#c0c0c0",width=0)

		#add the label for the load
		self.LoadLabel=tk.Label(self.gameCanvas,text="Load",bg='white',font=("Helvetica", 10))
		self.LoadLabel.place(x=self.Load_x+15,y=self.Load_y-25)

		
		#add shaft
		self.generator_width=self.gameCanvas.coords(self.generator)[2]-self.gameCanvas.coords(self.generator)[0]
		self.shaft_width=self.generator_width/5.
		self.shaft_height=90
		self.shaft=self.gameCanvas.create_rectangle(self.gameCanvas.coords(self.generator)[0]+2*self.shaft_width,
													self.gameCanvas.coords(self.damTopPolygon)[17]-self.generator_buffer_y,
													self.gameCanvas.coords(self.generator)[0]+self.shaft_width*3,
													self.gameCanvas.coords(self.damTopPolygon)[17]-self.generator_buffer_y+self.shaft_height,
														fill="#808080",width=0)
		

		#add turbine
		self.turbine_width=10
		self.turbine_height=15
		self.turbine=self.gameCanvas.create_rectangle(self.gameCanvas.coords(self.shaft)[0]-self.turbine_width,self.gameCanvas.coords(self.shaft)[3],
													self.gameCanvas.coords(self.shaft)[2]+self.turbine_width,self.gameCanvas.coords(self.shaft)[3]+self.turbine_height,
														fill="#808080",width=0)


		#draw the blade
		self.blade_width=10
		self.blade=self.gameCanvas.create_rectangle(self.gameCanvas.coords(self.turbine)[0]+2,
													self.gameCanvas.coords(self.turbine)[1]-5,
													self.gameCanvas.coords(self.turbine)[0]+self.blade_width,
													self.gameCanvas.coords(self.turbine)[3]+5,
													fill="#0000aa",width=0)


		
		[self.original_blade_x0,self.original_blade_y0,self.original_blade_x1,self.original_blade_y1]=self.gameCanvas.coords(self.blade)

		wall_width=4#width of wall on the right side
		# self.gameCanvas.create_line(self.damRectangle[2]+wall_width/2,self.damRectangle[3],self.damRectangle[2]+wall_width/2,self.damRectangle[1],width=wall_width)
		

		#one rectangle which shows the filling of water		
		#compute how many pixels need to be filled
		self.fill_start=self.damRectangle[3]-boardlogic.water_level/100.*self.dam_height
		self.fillRect=self.gameCanvas.create_rectangle(self.damRectangle[0],
												  self.fill_start,
												  self.damRectangle[2],
												  self.damRectangle[3],
												  fill="#0000aa",width=0)

		
		

	   
		

		#one rectangle which is the ground
		ground_width=self.dam_width+self.damRectangle[2]+self.river_width
		groundRect=self.gameCanvas.create_rectangle(self.damRectangle[0],
												  self.damRectangle[3],
												  ground_width+self.damRectangle[0],
												  self.damRectangle[3]+50,
												  fill="#7B3523",width=0)
		self.gameCanvas.pack(fill='both',expand=True)


		#put in slider for user to set water velocity
		self.water_slider_label=tk.Label(self.gameCanvas,bg='white',text="Water Flow Rate (m^3/s)",font=("Helvetica",15))
		self.water_slider_label.place(x=655,y=10)

		self.water_slider=tk.Scale(self.gameCanvas,from_=0, to=50,length=270,orient='horizontal',command=self.updateWaterVelocity,showvalue=0)
		self.water_slider.place(x=630,y=40)

		#put in the level end button
		self.level1endbutton=tk.Button(self.gameFrame,bg='#00ff00',text="     Move     \n     on!     \n",command=self.nextLevel)
		# self.level1endbutton.pack_forget()
		

		#updateCanvas
		self.updateMessageCanvas=tk.Canvas(self.gameFrame,bg="lightgray",highlightthickness=0)
		self.updateMessageCanvas.pack(fill='y',side='bottom')
		self.updateMessageLabel =  tk.Label(self.updateMessageCanvas,bg='#ddf4c2',text="Loading....",font=("Helvetica", 15))
		self.updateMessageLabel.pack(fill='y',pady=10)
		self.continueButton=tk.Button(self.updateMessageCanvas,text='Continue',bg='#00ff00',command=self.nextMessage)
		self.continueButton.pack()

		#for resizing
		self.updateFrame.rowconfigure(0,weight=5)
		self.updateFrame.rowconfigure(1,weight=5)
		self.updateFrame.rowconfigure(2,weight=1)

		#for water flowing in the animation
		self.waterAnimationSpeed=0.

		#to set how long cycles should go for
		self.updateRate=200#its in ms

		#spill button
		self.spillRepeatInterval=100
		self.spillbutton=tk.Button(self.gameCanvas,bg='#c0c0c0',text="Spill Water!",command=self.spill,repeatdelay=10,repeatinterval=self.spillRepeatInterval,relief='groove')
		self.spillbutton.place(x=self.gameCanvas.coords(self.damTopPolygon)[0],y=self.gameCanvas.coords(self.damTopPolygon)[1]-27)

		#time indicator
		self.timeIndicator=tk.Label(self.gameCanvas,bg='white',text="time",font=("Helvetica", 15),fg="#bb0000")
		self.timeIndicator.place(x=15,y=15)

		#for printing currency
		locale.setlocale(locale.LC_ALL,'')



	def updateDisplays(self,root):
		if(self.boardlogic.level==0 or self.boardlogic.level == 1):
			self.updateDisplaysLevel1(root)
		elif(self.boardlogic.level==3):
			self.updateDisplaysLevel3(root)

	def updateDisplaysLevel1(self,root):

		#level progress and total points earned
		self.progress["value"]=self.boardlogic.progress
		self.points["text"]=str(int(self.boardlogic.totalPoints))
		self.timeIndicator["text"]=str(self.boardlogic.time)

		#fill level of dam
		if(self.boardlogic.level==0 or self.boardlogic.level==1):
			self.gameCanvas.delete(self.fillRect)
			self.dam_height=self.damRectangle[3]-self.damRectangle[1]

			#compute how many pixels need to be filled
			self.boardlogic.water_level-=self.waterAnimationSpeed*1.15#decrease the filling by the water velocity
			self.fill_level=self.damRectangle[3]-self.boardlogic.water_level/100.*self.dam_height

			#ensure that the water level does not go below the chute height
			if self.fill_level>self.gameCanvas.coords(self.damTopPolygon)[3]:
				self.fill_level=self.gameCanvas.coords(self.damTopPolygon)[3]

			#ensure the water level does not go over the side of the dam
			if self.boardlogic.water_level>99.:
				self.boardlogic.water_level=80
				self.boardlogic.updateQueue=[]

				#in order for the message to stay up fo a while, we add a bunch of them
				for i in range(50):
					self.boardlogic.updateQueue.append(["Water level got too high! Level restarted.",99])
				self.updateMessage()
				initLevel1(self.boardlogic)

			else:
				if(len(self.boardlogic.updateQueue)>0 and self.boardlogic.updateQueue[0][1]==99):
					self.nextMessage()

				#delete the "you've spilled too much" message
				if(len(self.boardlogic.updateQueue)>0 and self.boardlogic.updateQueue[0][1]==199):
					self.nextMessage()
				


			self.fillRect=self.gameCanvas.create_rectangle(self.damRectangle[0],
												  self.fill_level,
												  self.damRectangle[2],
												  self.damRectangle[3],
												  fill="#0000aa",width=0)

		self.powerIndicator['text']=str(self.boardlogic.powerProducedDam)
		self.LoadIndicator['text']=str(int(self.boardlogic.damLoad))

		#logic for highlighting specific widgets
		if (self.boardlogic.level==0 and len(self.boardlogic.updateQueue)>0):
			

			if(self.boardlogic.updateQueue[0][1]==2):#highlight the turbine
				# print 
				# self.gameCanvas.itemconfig("circle",fill="orange")
				self.gameCanvas.create_oval(self.gameCanvas.coords(self.turbine)[0]+2-40,
											 self.gameCanvas.coords(self.turbine)[1]-5-40,
											 self.gameCanvas.coords(self.turbine)[0]+2,
											 self.gameCanvas.coords(self.turbine)[1]-5,fill="#ff6600",width=0,tag="circle")
				self.waterAnimationSpeed=50./12000.
				# self.gameCanvas.move("circle",10,20)

			elif(self.boardlogic.updateQueue[0][1]==3):#highlight the water slider
				if(self.gameCanvas.coords("circle")[0]==self.gameCanvas.coords(self.turbine)[0]+2-40):#if this message has just been chosen
					self.waterAnimationSpeed=0.

				if(self.gameCanvas.coords("circle")[0]<610):
					self.gameCanvas.move("circle",10,-20)

			elif(self.boardlogic.updateQueue[0][1]==4):#highlight the load label
				if(self.gameCanvas.coords("circle")[0]<830):
					self.gameCanvas.move("circle",30,20)

			elif(self.boardlogic.updateQueue[0][1]==6):#highlight the spill button
				if(self.gameCanvas.coords("circle")[0]>420):
					self.gameCanvas.move("circle",-25,-3.5)

			elif(self.boardlogic.updateQueue[0][1]==8):
				self.gameCanvas.delete("circle")

				

		#handle the coloring of the power produced indicator
		if(abs(self.boardlogic.powerProducedDam-self.boardlogic.damLoad)>10):
			self.powerIndicator.configure(bg='#ed0000')
		elif(abs(self.boardlogic.powerProducedDam-self.boardlogic.damLoad)<10)and (abs(self.boardlogic.powerProducedDam-self.boardlogic.damLoad)>5):
			self.powerIndicator.configure(bg='#ff0000')
		elif (abs(self.boardlogic.powerProducedDam-self.boardlogic.damLoad)<=5) and (abs(self.boardlogic.powerProducedDam-self.boardlogic.damLoad)>1):
			self.powerIndicator.configure(bg='#ff8000')
		elif(abs(self.boardlogic.powerProducedDam-self.boardlogic.damLoad)<=1):
			self.powerIndicator.configure(bg='#00ee00')

		
		root.after(self.updateRate,gameLogic,self,self.boardlogic,root)


	def updateDisplaysLevel3(self,root):
		# print time.time()
		
		#delete the items
		self.tableGens.delete(*self.tableGens.get_children())
		#decide on the available generators
		self.updateDemandProfile()
		# self.updateDispatchProfile()
		self.updateAvailableGenerators()


		#add the updated ones		
		row_tag='oddrow'#for alternating colors
		for gen in self.boardlogic.availableGenerators:
			if(row_tag=='oddrow'):
				row_tag='evenrow'
				self.tableGens.insert("",0,values=(gen[0],gen[1],gen[2],gen[3],locale.currency(gen[4])),tags=row_tag)
			else:
				row_tag='oddrow'
				self.tableGens.insert("",0,values=(gen[0],gen[1],gen[2],gen[3],locale.currency(gen[4])),tags=row_tag)
		self.tableGens.tag_configure('oddrow', background='#b8b894')


		#update the dispatch table
		row_tag='oddrow'#for alternating colors
		for gen in reversed(self.boardlogic.dispatchProfile):
			if(row_tag=='oddrow'):
				row_tag='evenrow'
				self.tableDispatch.insert("",0,values=(gen[0],gen[1]),tags=row_tag)
			else:
				row_tag='oddrow'
				self.tableDispatch.insert("",0,values=(gen[0],gen[1]),tags=row_tag)
		self.tableDispatch.tag_configure('oddrow', background='#b8b894')

		#update the ancillary table
		#delete the items
		self.tableAncillary.delete(*self.tableAncillary.get_children())
		#add the updated ones
		row_tag='oddrow'#for alternating colors
		for gen in reversed(self.boardlogic.ancillaryProfile):
			if(row_tag=='oddrow'):
				row_tag='evenrow'
				self.tableAncillary.insert("",0,values=(gen[0],gen[1]),tags=row_tag)
			else:
				row_tag='oddrow'
				self.tableAncillary.insert("",0,values=(gen[0],gen[1]),tags=row_tag)
		self.tableAncillary.tag_configure('oddrow', background='#b8b894')

		#update the market clearing table
		#delete the items
		self.tableClearing.delete(*self.tableClearing.get_children())
		#add the updated ones
		row_tag='oddrow'#for alternating colors
		for gen in reversed(self.boardlogic.clearingGens):
			if(row_tag=='oddrow'):
				row_tag='evenrow'
				self.tableClearing.insert("",0,values=(gen[0],gen[1],gen[2]),tags=row_tag)
			else:
				row_tag='oddrow'
				self.tableClearing.insert("",0,values=(gen[0],gen[1],gen[2]),tags=row_tag)
		self.tableClearing.tag_configure('oddrow', background='#b8b894')

		#reset the cumulative generation for the clearing table
		# self.boardlogic.cumulGen=0

		#update the event stuff if some exist
		if(len(self.boardlogic.events)>0):
			# self.eventCanvas.place(x=10,y=400)
			self.boardlogic.numEvents+=1
			self.eventTitle.pack(side='top',fill='x')
			self.eventMessage.pack(side='left',fill='both')	
			self.eventMenu.pack(side='right',fill='both')	

			#reformat the message to look nice
			eventMessage="    "
			num_words=0
			for char in self.boardlogic.events[0][0]:
				if (char == ' '):
					num_words+=1
					if(num_words>4):
						eventMessage+='    \n    '
						num_words=0
					else:
						eventMessage+=' '
				else:
					eventMessage+=char

			self.eventMessage['text']=eventMessage
			self.eventMessage.configure(bg='lightgray')
			self.eventTitle.configure(bg='lightgray')

			for child in self.eventMenu.winfo_children():
				child.destroy()

			for i,option in enumerate(self.boardlogic.events[0]):
				if(i in [1,2,3]):
					#format the option
					option_formatted=""
					num_words=0
					for char in option:
						if (char == ' '):
							num_words+=1
							if(num_words>5):
								option_formatted+='\n '
								num_words=0
							else:
								option_formatted+=' '
						else:
							option_formatted+=char
					if(i==1):
						self.opt=tk.Button(self.eventMenu,text=option_formatted, font=("Helvetica", 14), command=lambda: self.choseEventOption(1),bd=2).pack(side='top',fill='x')
					elif(i==2):
						self.opt=tk.Button(self.eventMenu,text=option_formatted, font=("Helvetica", 14), command=lambda: self.choseEventOption(2),bd=2).pack(side='top',fill='x')
					elif(i==3):
						self.opt=tk.Button(self.eventMenu,text=option_formatted, font=("Helvetica", 14), command=lambda: self.choseEventOption(3),bd=2).pack(side='top',fill='x')
					# self.opt.
			

			#compute the window width
			window_width = self.eventMessage.winfo_width()+self.eventMenu.winfo_width()

			#make the x of the window 750/2.-width/2.
			self.eventCanvas.place(x=300,y=200)

		#update the points display
		self.points["text"]=str(int(self.boardlogic.totalPoints))

		#update the market clearing price in the title
		#find the highest clearing price
		highest_price=0
		for gen in self.boardlogic.clearingGens:        
			if(float(gen[-1][1:])>highest_price):
				highest_price=float(gen[-1][1:])

		#update the time period and the clearing price
		price = locale.currency(highest_price)
		if(self.boardlogic.time_period<4):
			time_period=self.boardlogic.demandProfile[self.boardlogic.time_period][0]
		else:
			
			time_period="Ancillary Services"
			if(self.boardlogic.time_period==5 and self.boardlogic.last_time_period==5 and self.boardlogic.enteredAncillaryMarket==False):
				
				#give them 50 points for successfully dispatching gens
				self.boardlogic.totalPoints+=50

				#enable the buttons
				self.skipAncillaryButton.configure(bg='#dd0000')
				self.enterAncillaryButton.configure(bg='#00dd00')

				#disable the table
				self.tableGens.configure(selectmode="none")

				#discolor the options
				row_tag='oddrow'#for alternating colors
				for gen in self.boardlogic.availableGenerators:
					self.tableGens.insert("",0,values=(gen[0],gen[1],gen[2],gen[3],locale.currency(gen[4])),tags=row_tag)
				self.tableGens.tag_configure('oddrow', background='gray')

				#fill in the gensSelected periods that were autofilled
				self.boardlogic.gensSelected[0]=self.boardlogic.gensSelected[1]
				self.boardlogic.gensSelected[3]=self.boardlogic.gensSelected[2]
				self.boardlogic.gensSelected[4]=self.boardlogic.gensSelected[2]


				if(len(self.boardlogic.updateQueue)>0):
					if(self.boardlogic.updateQueue[-1][1]!=99):#avoid adding the message multiple times
						self.boardlogic.updateQueue.append(["You can now choose generators to designate for Ancillary Services!\n "+\
															"It is suggested that you secure at least 10% of the dispatch power\n "+\
															"for each time period. You must select generators that have a ramp rate\n "+\
															"greater than the median of the available generators. \n"+\
															"Press the 'Secure Ancillary' Button to begin, or the 'Skip Ancillary' Button",99])

				else:
					self.boardlogic.updateQueue.append(["You can now choose generators to designate for Ancillary Services!\n "+\
														"It is suggested that you secure at least 10% of the dispatch power\n "+\
														"for each time period. You must select generators that have a ramp rate\n "+\
														"greater than the median of the available generators. \n"+\
														"Press the 'Secure Ancillary' Button to begin, or the 'Skip Ancillary' Button",99])

				
				self.updateMessage()
				self.chooseNewGenerators()

			# elif(self.boardlogic.time_period==6 and self.boardlogic.last_time_period==6):
				#randomly grab an event, wait some random amount of time, and start
				# self.boardlogic.events.append(random.choice(self.boardlogic.possibleEvents))



		self.timeTitle['text']="Time Period: "+time_period+ "\t\t Clearing Price: "+price

		root.after(self.updateRate,gameLogic,self,self.boardlogic,root)

		# root.after(self.updateRate,gameLogic,self,self.boardlogic,root)

		
	def choseEventOption(self,option):
		if(option==1):
			messageIndex=4
			pointIndex=5
		elif(option==2):
			messageIndex=6
			pointIndex=7
		elif(option==3):
			messageIndex=8
			pointIndex=9


		#place the menu 40 miles away
		self.eventCanvas.place(x=10000,y=10000)


		#updates the message panel with the message
		eventMessage=""
		num_words=0

		for char in self.boardlogic.events[0][messageIndex]:
			if (char == ' '):
				num_words+=1
				if(num_words>8):
					eventMessage+='\n '
					num_words=0
				else:
					eventMessage+=' '
			else:
				eventMessage+=char


		#decrement the points
		self.boardlogic.totalPoints+=int(float(str(self.boardlogic.events[0][pointIndex])))


		
		#reset a bunch of the tables

		self.boardlogic.availableGenerators=[]#these are the generators for the time period

		self.boardlogic.dispatchProfile=[["Off Peak AM","--"],["Daytime1","--"],
						  ["Peak","--"],["Daytime2","--"],
						  ["Off-peak PM","--"]]

		self.boardlogic.ancillaryProfile=[["Off Peak AM",0],["Daytime1",0],
						  ["Peak",0],["Daytime2",0],
						  ["Off-peak PM",0]]

		self.boardlogic.demandProfile=[["Off Peak AM",0],["Daytime1",0],
						  ["Peak",0],["Daytime2",0],
						  ["Off-peak PM",0]]
		self.boardlogic.clearingGens=[]

		self.boardlogic.cumulGen=0

		self.boardlogic.events=[]

		self.boardlogic.profilePeriods=[["Off Peak AM",5.5],["Daytime1",4],
							["Peak",5],["Daytime2",4],
							["Off-peak PM",5.5]]

		self.boardlogic.time_period=0
		self.boardlogic.ancillary_period=0
		self.boardlogic.last_time_period=-1

		self.updateDemandProfile()
		self.updateDispatchProfile()

		self.dispatchButton['text']="Dispatch Gens!\n"

		#uncolor the generators
		for gen in self.boardlogic.generators:
			for child in self.master.children:
				try:
					if(self.master.children[child]['text']==gen[1]):
						self.master.children[child].configure(bd=0,bg="#ffffff")
				except:
					r=0
		
		row_tag='oddrow'#for alternating colors
		for i,gen in enumerate(reversed(self.boardlogic.demandProfile)):
			if(row_tag=='oddrow'):
				row_tag='evenrow'
				self.tableDemand.insert("",0,values=(gen[0],gen[1],self.boardlogic.profilePeriods[4-i][1]),tags=row_tag)
			else:
				row_tag='oddrow'
				self.tableDemand.insert("",0,values=(gen[0],gen[1],self.boardlogic.profilePeriods[4-i][1]),tags=row_tag)
		self.tableDemand.tag_configure('oddrow', background='#b8b894')

		self.tableDemand['show'] = 'headings'#get rid of the empty column on the left
		self.tableDemand.place(x=515,y=20)

		

		#somewhere in here put level 3 end stuff
		

		self.boardlogic.gensSelected=[[],[],[],[],[]]
		self.boardlogic.enteredAncillaryMarket=False
		

		#remove the event from the event queue
		self.boardlogic.events=[]

		#make the table selectable again
		self.tableGens.configure(selectmode="extended")

		self.enterAncillaryButton.configure(bg="gray")
		self.skipAncillaryButton.configure(bg="gray")

		self.boardlogic.updateQueue.append([eventMessage,120])
		self.boardlogic.updateQueue.append(["The next Day-Ahead Market has begun! \nSelect generators to meet the demand!",12])
		self.updateMessage()





	def updateMessage(self):
		
		if(self.boardlogic.level<4):
			self.updateMessageCanvas.pack()
			self.updateMessageLabel['text']=self.boardlogic.updateQueue[0][0]
			self.updateMessageLabel.pack(side='top',pady=10)
		elif(self.boardlogic.level==4):
			self.updateMessageCanvas.pack(side='bottom')
			self.updateMessageLabel['text']=self.boardlogic.updateQueue[0][0]
			self.updateMessageLabel.pack(side='top',pady=10)

	def nextMessage(self):
		if(self.boardlogic.level<3):
			del self.boardlogic.updateQueue[0]
			if(len(self.boardlogic.updateQueue)==0):
				#stop providing update messages
				self.updateMessageCanvas.pack_forget()
			else:
				if(self.boardlogic.updateQueue[0][1]==4):#highlighting the water slider
					if(self.waterAnimationSpeed==0.):
						self.boardlogic.updateQueue = [["Move the water by moving the slider!",3]] + self.boardlogic.updateQueue

				if(self.boardlogic.updateQueue[0][1]==5):#highlight the load label
					if(self.boardlogic.powerProducedDam!=self.boardlogic.damLoad):
						self.boardlogic.updateQueue = [["Match the load exactly!",4]]+self.boardlogic.updateQueue
				#display the next message
				self.updateMessage()

		elif(self.boardlogic.level==3):#we're in level 3 or 4
			if(self.boardlogic.updateQueue[0][1]==12):
				self.boardlogic.time_period=1
				self.boardlogic.clearingGens=[]
				self.updateDisplaysLevel3(self.master)

			del self.boardlogic.updateQueue[0]
			if(len(self.boardlogic.updateQueue)==0):
				#stop providing update messages
				self.updateMessageCanvas.pack_forget()
			else:
				#reformat the message to look nice
				eventMessage="    "
				num_words=0
				for char in self.boardlogic.updateQueue[0][0]:
					if (char == ' '):
						num_words+=1
						if(num_words>7):
							eventMessage+='    \n    '
							num_words=0
						else:
							eventMessage+=' '
					else:
						eventMessage+=char

				self.boardlogic.updateQueue[0][0]=eventMessage
				self.updateMessage()

		elif(self.boardlogic.level==4):
			if(self.boardlogic.updateQueue[0][1]==0):
				self.updateMessageCanvas.pack(side='top')
			if(self.boardlogic.updateQueue[0][1]==1):
				self.boardlogic.time_period=1
				self.boardlogic.clearingGens=[]
				self.updateDisplaysLevel3(self.master)

			del self.boardlogic.updateQueue[0]
			if(len(self.boardlogic.updateQueue)==0):
				#stop providing update messages
				self.updateMessageCanvas.pack_forget()
			else:
				#reformat the message to look nice
				eventMessage="    "
				num_words=0
				for char in self.boardlogic.updateQueue[0][0]:
					if (char == ' '):
						num_words+=1
						if(num_words>7):
							eventMessage+='    \n    '
							num_words=0
						else:
							eventMessage+=' '
					else:
						eventMessage+=char

				self.boardlogic.updateQueue[0][0]=eventMessage
				self.updateMessage()

	def updateWaterVelocity(self,value):
		if(float(value)!=0):
			self.boardlogic.water_velocity=float(value)+100
		else:
			self.boardlogic.water_velocity=0
		self.waterAnimationSpeed=float(value)/1800


	def spinTurbine(self,root):
		#get position of blade
		try:
			[x0,y0,x1,y1]=self.gameCanvas.coords(self.blade)
			# print self.original_blade_x-x0
			if((x0-self.original_blade_x0)>25):
				x0=self.original_blade_x0
				x1=self.original_blade_x1
				y0=self.original_blade_y0
				y1=self.original_blade_y1

			#delete the old blade
			self.gameCanvas.delete(self.blade)

			#add a new blade
			self.blade=self.gameCanvas.create_rectangle(x0+self.waterAnimationSpeed*70.,y0,
														x1+self.waterAnimationSpeed*70.,y1,
														fill="#000000")

			self.moveWaves()
		except:
			r=0
		root.after(1,self.updateDisplays,root)

	def moveWaves(self):
		#get position of leading edge of wave
		[x0,y0]=[self.gameCanvas.coords(self.wavePolygon)[2],self.gameCanvas.coords(self.wavePolygon)[3]]
		wave_velocity= self.waterAnimationSpeed 
		if(x0>self.kneePointx or y0>self.kneePointy)and(x0<self.gameCanvas.coords(self.damTopPolygon)[6]-3):
			if(self.gameCanvas.coords(self.wavePolygon)[0]<self.kneePointx):#we're just turning the corner
				self.gameCanvas.delete(self.wavePolygon)
				self.wavePolygon=self.gameCanvas.create_polygon(self.kneePointx,self.kneePointy,
															self.kneePointx+self.diffx*self.wave_width,self.kneePointy,
															self.kneePointx+self.diffx*self.wave_width,self.kneePointy+self.penstock_diameter,
															self.kneePointx,self.kneePointy+self.penstock_diameter,
															fill="#0000dd",width=0)

			self.gameCanvas.move(self.wavePolygon,self.diffx*wave_velocity/2.,0)

		elif(x0>self.gameCanvas.coords(self.damTopPolygon)[6]-3):
			self.gameCanvas.delete(self.wavePolygon)
			self.wavePolygon=self.gameCanvas.create_polygon(self.startx,self.starty,
														self.startx+self.diffx*self.wave_width,self.starty+self.diffy*self.wave_width,
														self.gameCanvas.coords(self.damBottomPolygon)[0]+self.diffx*self.wave_width,self.gameCanvas.coords(self.damBottomPolygon)[1]+self.diffy*self.wave_width,
														self.gameCanvas.coords(self.damBottomPolygon)[0],self.gameCanvas.coords(self.damBottomPolygon)[1],
														fill="#0000dd",width=0)

		else:#its moving down the chute
			self.gameCanvas.move(self.wavePolygon,self.diffx*wave_velocity,self.diffy*wave_velocity)

		#get position of leading edge of wave
		[x0,y0]=[self.gameCanvas.coords(self.wavePolygon2)[2],self.gameCanvas.coords(self.wavePolygon2)[3]]
		wave_velocity=self.waterAnimationSpeed
		if(x0>self.kneePointx or y0>self.kneePointy)and(x0<self.gameCanvas.coords(self.damTopPolygon)[6]-3):
			if(self.gameCanvas.coords(self.wavePolygon2)[0]<self.kneePointx):#we're just turning the corner
				self.gameCanvas.delete(self.wavePolygon2)
				self.wavePolygon2=self.gameCanvas.create_polygon(self.kneePointx,self.kneePointy,
															self.kneePointx+self.diffx*self.wave_width,self.kneePointy,
															self.kneePointx+self.diffx*self.wave_width,self.kneePointy+self.penstock_diameter,
															self.kneePointx,self.kneePointy+self.penstock_diameter,
															fill="#0000dd",width=0)

			self.gameCanvas.move(self.wavePolygon2,self.diffx*wave_velocity/2.,0)

		elif(x0>self.gameCanvas.coords(self.damTopPolygon)[6]-3):
			self.gameCanvas.delete(self.wavePolygon2)
			self.wavePolygon2=self.gameCanvas.create_polygon(self.startx,self.starty,
														self.startx+self.diffx*self.wave_width,self.starty+self.diffy*self.wave_width,
														self.gameCanvas.coords(self.damBottomPolygon)[0]+self.diffx*self.wave_width,self.gameCanvas.coords(self.damBottomPolygon)[1]+self.diffy*self.wave_width,
														self.gameCanvas.coords(self.damBottomPolygon)[0],self.gameCanvas.coords(self.damBottomPolygon)[1],
														fill="#0000dd",width=0)

		else:#its moving down the chute
			self.gameCanvas.move(self.wavePolygon2,self.diffx*wave_velocity,self.diffy*wave_velocity)


	def level1End(self,root):
		if(self.boardlogic.level==1):
			self.level1endbutton.place(x=500,y=40)
			root.after(self.updateRate,self.spinTurbine,root)

		elif((self.boardlogic.level==3 or self.boardlogic.level==4) and self.boardlogic.numEvents>0):
			try:
				self.level1endbutton.place(x=570,y=40)
			except:
				self.level1endbutton=tk.Button(self.imageCanvas,bg='#00ff00',text="     Move     \n     on!     \n",command=self.nextLevel)
				self.level1endbutton.place(x=570,y=40)

	def spill(self):
		self.boardlogic.spilledSeconds+=self.spillRepeatInterval/1000.
		if(self.boardlogic.spilledSeconds>10.):
			self.boardlogic.updateQueue.append(["Cannot spill for more than 20 seconds!",199])
			self.boardlogic.updateQueue.append(["Cannot spill for more than 20 seconds!",199])
			self.updateMessage()

		else:
			self.boardlogic.water_level-=0.1

	def nextLevel(self):
		if(self.boardlogic.level==1):
			#clear the board
			self.clearBoard()
			self.boardlogic.level=3

			#set the board
			self.setBoard()
			self.root.after(self.updateRate,initLevel3,self.boardlogic,self,self.root)

		elif(self.boardlogic.level==3):
			self.boardlogic.numEvents=0
			self.boardlogic.level=4
			self.level1endbutton.destroy()

			with open('level4events.csv', 'rb') as csvfile:
				event_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for i,row in enumerate(event_reader):
					if(i!=0):
						self.boardlogic.possibleEvents.append(row)

			initLevel4(self.boardlogic,self,self.master)

		elif(self.boardlogic.level==4):
			
			self.gameEnd()

	def gameEnd(self):
		self.clearBoard()
		self.doneCanvas = tk.Canvas(self.master,bg="#0dad27",height=600, width=600)
		self.doneCanvas.pack(fill='both')

		self.eventTitle   =   tk.Label(self.doneCanvas,bg='#0dad27',text="'YOU\'VE \nWON!'",font=("Helvetica", 50))
		self.eventTitle.pack(fill='both')



		


	def clearBoard(self):
		#gameFrame and updateFrame
		if(self.boardlogic.level==1):
			self.gameFrame.destroy()
			self.updateFrame.destroy()
		elif(self.boardlogic.level==4):
			for child in self.infoCanvas.winfo_children():
				child.destroy()
			for child in self.generatorCanvas.winfo_children():
				child.destroy()
			for child in self.imageCanvas.winfo_children():
				child.destroy()

	def setBoard(self):
		if(self.boardlogic.level==3):
			#intialize the points
			self.boardlogic.totalPoints = self.boardlogic.totalPoints*100

			self.generatorFrame= tk.Frame(self.master,bg="grey")
			self.generatorFrame.pack(side="right",fill="y")

			self.generatorCanvas = tk.Canvas(self.generatorFrame,bg="lightgray")
			self.generatorCanvas.pack(fill='x')

			self.createGensTable()

			self.infoFrame= tk.Frame(self.master,bg="grey",width=1)
			self.infoFrame.pack(side="top",fill="x")

			self.infoCanvasHeight=150
			self.infoCanvas = tk.Canvas(self.infoFrame,bg="lightgray",height=self.infoCanvasHeight)
			self.infoCanvas.pack(side="top",fill='x')


			self.createInfoTables()

			self.imageCanvas = tk.Canvas(self.master,bg="lightgray",width=750,height=650)
			self.imageCanvas.place(x=0,y=self.infoCanvasHeight)

			#add the background
			self.createImage()
		
			#add the generator and transmission imagery
			self.addGenerators()
			self.addLoads()


			#event panel
			#make this a canvas
			self.eventCanvas = tk.Canvas(self.master,bg="lightgray",highlightthickness=0)

			self.eventCanvas.place(x=10000,y=50000)
			# self.eventCanvas.pack_forget()

			self.eventTitle   =   tk.Label(self.eventCanvas,bg='lightgray',text="An event has occurred!",font=("Helvetica", 28))			
			self.eventMessage = tk.Label(self.eventCanvas,bg='lightgray',font=("Helvetica", 19))
			self.eventMenu    = tk.Canvas(self.eventCanvas,bg="lightgray")

			#the message board
			self.updateMessageCanvas=tk.Canvas(self.master,bg="lightgray",highlightthickness=0)
			self.updateMessageCanvas.pack(side='bottom')
			self.updateMessageLabel =  tk.Label(self.updateMessageCanvas,bg='#ddf4c2',text="Loading....",font=("Helvetica", 15))
			self.updateMessageLabel.pack()
			self.continueButton=tk.Button(self.updateMessageCanvas,text='Continue',bg='#00ff00',command=self.nextMessage)
			self.continueButton.pack()

			self.updateDisplaysLevel3(self.master)


			# initLevel3()


	def treeview_sort_column(self,tv, col, reverse):
		l = [(tv.set(k, col), k) for k in tv.get_children('')]
		try:
			l = sorted(l,key=lambda x: int(float(x[0])),reverse=reverse)
		except:
			l = sorted(l,key=lambda x: x[0],reverse=reverse)

		# rearrange items in sorted positions
		for index, (val, k) in enumerate(l):
			tv.move(k, '', index)

		# reverse sort next time
		tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

	def createGensTable(self):
		#generator table
		self.genTitle=   tk.Label(self.generatorCanvas,bg='lightgray',text="Generator Fleet",font=("Helvetica", 15))
		self.genTitle.pack(side='top',pady=1)

		self.tableGens = ttk.Treeview(self.generatorCanvas,height=26,selectmode='extended')#height may be in number of items!
		self.tableGens["columns"]=("Type","Name","Capacity(MW)","Ramp Rate(MW/min)","Bid($/MWh)")
		self.tableGens.column("Type", width=50 ,anchor=tk.CENTER)
		self.tableGens.column("Name", width=155,anchor=tk.CENTER)
		self.tableGens.column("Capacity(MW)", width=100 ,anchor=tk.CENTER)
		self.tableGens.column("Ramp Rate(MW/min)", width=140,anchor=tk.CENTER)
		self.tableGens.column("Bid($/MWh)", width=100 ,anchor=tk.CENTER)

		# self.tableGens.heading("type", text="Type")
		# self.tableGens.heading("name", text="Name")
		# self.tableGens.heading("cap",  text="Capacity")
		# self.tableGens.heading("ramp", text="Ramp Rate(MW/s)")
		# self.tableGens.heading("Bid($/MWh)",  text="Bid($/MWh)")

		#decide on the available generators
		self.updateDemandProfile()#first we do the demand profile because it relies on the level being -1. The level is updated in updateAvailableGenerators
		self.updateAvailableGenerators()

		row_tag='oddrow'#for alternating colors
		for gen in self.boardlogic.availableGenerators:
			if(row_tag=='oddrow'):
				row_tag='evenrow'
				self.tableGens.insert("",0,values=(gen[0],gen[1],gen[2],gen[3],locale.currency(gen[4])),tags=row_tag)
			else:
				row_tag='oddrow'
				self.tableGens.insert("",0,values=(gen[0],gen[1],gen[2],gen[3],locale.currency(gen[4])),tags=row_tag)
		self.tableGens.tag_configure('oddrow', background='#b8b894')

		self.tableGens['show'] = 'headings'#get rid of the empty column on the left

		for col in self.tableGens['columns']:
			 self.tableGens.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(self.tableGens, _col, False))
		self.tableGens.pack(side='top')

		#bind it to a double click so you can add what has been pressed to the clearing table
		self.tableGens.bind("<Return>", self.gensClick)
		self.tableGens.bind("<ButtonRelease-1>",self.gensHover)

		#Market clearing price

		self.tableClearing = ttk.Treeview(self.generatorCanvas,height=5)
		self.tableClearing["columns"]=("gen","cumul","cost")
		self.tableClearing.column("gen", width=150 ,anchor=tk.CENTER)
		self.tableClearing.column("cumul", width=120,anchor=tk.CENTER)
		self.tableClearing.column("cost", width=70 ,anchor=tk.CENTER)

		self.tableClearing.heading("gen", text="Generator")
		self.tableClearing.heading("cumul", text="Cumulative MWh")
		self.tableClearing.heading("cost",  text="$/MWhr")
		row_tag='oddrow'#for alternating colors

		self.buttonCanvas = tk.Canvas(self.generatorCanvas,bg="lightgray")
		self.buttonCanvas.pack(side='bottom',fill='x')

		self.dispatchButton=   tk.Button(self.buttonCanvas,bg='#00dd00',text="Dispatch Gens!\n",command=self.dispatchGens)
		self.dispatchButton.pack(side='left',padx=2)

		self.deleteLastGen=   tk.Button(self.buttonCanvas,bg='#dd0000',text="Delete Last \nGenerator",command=self.deleteLastGen)
		self.deleteLastGen.pack(side='left',padx=2)

		self.skipAncillaryButton=   tk.Button(self.buttonCanvas,bg='gray',text="Skip Ancillary\n",command=self.skipAncillary)
		self.skipAncillaryButton.pack(side='right',padx=2)

		self.enterAncillaryButton=   tk.Button(self.buttonCanvas,bg='gray',text="Secure Ancillary \nGens",command=self.enterAncillary)
		self.enterAncillaryButton.pack(side='right',padx=2)

		

		self.tableClearing['show'] = 'headings'#get rid of the empty column on the left
		self.tableClearing.pack(side='bottom',pady=3,fill='x')

		self.timeTitle=   tk.Label(self.generatorCanvas,bg='lightgray',text="Time Period: Off-peak AM \t\t Clearing Price: $0.00",font=("Helvetica", 12))
		self.timeTitle.pack(side='bottom',pady=1,fill='x')

		self.clearingTitle=   tk.Label(self.generatorCanvas,bg='gray60',text="Market Clearing Table",font=("Helvetica", 15),bd=1)
		self.clearingTitle.pack(side='bottom',pady=3,fill='x')

	def skipAncillary(self):
		if(self.boardlogic.time_period>4):
			self.boardlogic.enteredAncillaryMarket=False
			self.boardlogic.time_period=6

			#add an event
			if(len(self.boardlogic.events)<1):
				self.boardlogic.events.append(random.choice(self.boardlogic.possibleEvents))
				self.updateDisplaysLevel3(self.master)

	def enterAncillary(self):
		if(self.boardlogic.time_period>4):
			#decrement 10 points
			self.boardlogic.totalPoints-=5

			self.boardlogic.enteredAncillaryMarket=True

			self.boardlogic.updateQueue.append(["Please choose your ancillary generators \nfrom the Gen Fleet Table!",312])
			self.updateMessage()

			#enable the table
			self.tableGens.configure(selectmode="extended")

			#change the label text
			self.dispatchButton['text']="Secure Ancillary \nGenerator!"

			self.boardlogic.time_period = 0

			#recolor the options in tableGens
			row_tag='oddrow'#for alternating colors
			for gen in self.boardlogic.availableGenerators:
				if(row_tag=='oddrow'):
					row_tag='evenrow'
					self.tableGens.insert("",0,values=(gen[0],gen[1],gen[2],gen[3],locale.currency(gen[4])),tags=row_tag)
				else:
					row_tag='oddrow'
					self.tableGens.insert("",0,values=(gen[0],gen[1],gen[2],gen[3],locale.currency(gen[4])),tags=row_tag)
			self.tableGens.tag_configure('oddrow', background='#b8b894')

			

	def deleteLastGen(self):	
		if(self.boardlogic.time_period<5):#we're not in the ancillary market
			last_gen=self.boardlogic.clearingGens[-1]
			new_cumul_mw=self.boardlogic.clearingGens[-2][1]

			#add it to the gensTables
			for gen in self.boardlogic.generators:
				if(gen[1]==last_gen[0]):
					self.boardlogic.availableGenerators.append(gen)

			#remove it from the selected generators
			del self.boardlogic.gensSelected[self.boardlogic.time_period][-1]



			#delete it from the market clearing table and decrement the cumulative mw
			genList=self.boardlogic.clearingGens
			self.boardlogic.clearingGens=[]
			for gen in genList:
				if(gen[0]!=last_gen[0]):
					self.boardlogic.clearingGens.append(gen)

			#uncolor the generator
			for child in self.master.children:
					try:
						if(self.master.children[child]['text']==last_gen[0]):
							self.master.children[child].configure(bd=0,bg="#ffffff")
					except:
						r=0

			self.boardlogic.cumulGen=new_cumul_mw

		else:
			last_gen=self.boardlogic.clearingGens[-1]
			new_cumul_mw=self.boardlogic.clearingGens[-2][1]

			#add it to the gensTables
			for gen in self.boardlogic.generators:
				if(gen[1]==last_gen[0]):
					self.boardlogic.availableGenerators.append(gen)

			#remove it from the selected generators
			del self.boardlogic.gensSelected[self.boardlogic.ancillary_period][-1]



			#delete it from the market clearing table and decrement the cumulative mw
			genList=self.boardlogic.clearingGens
			self.boardlogic.clearingGens=[]
			for gen in genList:
				if(gen[0]!=last_gen[0]):
					self.boardlogic.clearingGens.append(gen)

			#uncolor the generator
			for child in self.master.children:
					try:
						if(self.master.children[child]['text']==last_gen[0]):
							self.master.children[child].configure(bd=0,bg="#ffffff")
					except:
						r=0

			self.boardlogic.cumulGen=new_cumul_mw


		self.updateDisplaysLevel3(self.master)


	
	def dispatchGens(self):
		if(self.boardlogic.time_period<5 and self.boardlogic.enteredAncillaryMarket==False):#we're not in ancillary services
			board=self.boardlogic
			if(len(board.updateQueue)>0):
				self.nextMessage()

			#check that they are grabbing the lowest priced generators

			# if((board.cumulGen=board.demandProfile[board.time_period][1] and 
			# 	board.cumulGen<board.demandProfile[board.time_period][1]+board.demandProfile[board.time_period][1]*0.1) or #if its within a threshold of the amount needed
			# 	(board.dispatchProfile[board.time_period][1]==board.demandProfile[board.time_period][1])):
				

			if(board.cumulGen<board.demandProfile[board.time_period][1]):
				m13="Not enough generation has been secured!"+'\n'
				board.updateQueue.append([m13,13])
				self.updateMessage()

			if(board.cumulGen>board.demandProfile[board.time_period][1]):
				#determine the last generator added
				last_gen_name=self.boardlogic.clearingGens[-1][0]
				#find the capacity of this generator
				for gen in self.boardlogic.generators:
					if(gen[1]==last_gen_name):
						last_gen_mwh=float(str(gen[2]))*self.boardlogic.profilePeriods[board.time_period][1]

				#if the last generator was not necessary, then complain
				if(self.boardlogic.cumulGen-last_gen_mwh>board.demandProfile[board.time_period][1]):
					m13="Too much generation has been secured!"+'\n'
					board.updateQueue.append([m13,13])
					self.updateMessage()

				elif(board.time_period<4):#its in the right range
						# self.updateDispatchProfile()
						self.clearTimePeriod()

						#uncolor the generators
						for gen in self.boardlogic.generators:
							for child in self.master.children:
								try:
									if(self.master.children[child]['text']==gen[1]):
										self.master.children[child].configure(bd=0,bg="#ffffff")
								except:
									r=0

						board.time_period+=1
						board.last_time_period=board.time_period
						self.updateDisplaysLevel3(self.master)
				
			#if we're in an autofill period

			if(board.time_period==3):
				self.updateDispatchProfile()
				self.master.after(self.updateRate,self.updateDisplaysLevel3,self.master)
				board.time_period+=1
				# self.updateDispatchProfile()
				self.updateDisplaysLevel3(self.master)
				self.clearTimePeriod()
				board.time_period+=1
				self.master.after(self.updateRate,self.updateDisplaysLevel3,self.master)

		elif(self.boardlogic.enteredAncillaryMarket==True):#we're in ancillary services
			# if(board.time_period)

			board=self.boardlogic
			if(len(board.updateQueue)>0):
				self.nextMessage()
			if(self.boardlogic.cumulGen>=int(self.boardlogic.dispatchProfile[self.boardlogic.time_period][1]*0.1)):
				#if we're in an autofill period
				self.updateAncillaryProfile()
				self.clearTimePeriod()
				board.time_period+=1
				board.last_time_period+=1
				self.master.after(self.updateRate,self.updateDisplaysLevel3,self.master)

				self.boardlogic.ancillary_period+=1

				if(board.time_period==5):
					self.boardlogic.enteredAncillaryMarket=False
					self.boardlogic.time_period=6

				#add an event
				if(self.boardlogic.events)<1:
					self.boardlogic.events.append(random.choice(self.boardlogic.possibleEvents))
					self.updateDisplaysLevel3(self.master)
			else:
				if(len(self.boardlogic.updateQueue)>0):
					if(self.boardlogic.updateQueue[-1][1]!=98):#avoid adding the error message multiple times
						self.boardlogic.updateQueue.append(["Please add more generators to reach a cumulative\n generation of: "+\
														str(int(self.boardlogic.dispatchProfile[self.boardlogic.time_period][1]*0.1)),98])
						self.updateMessage()
				else:
					self.boardlogic.updateQueue.append(["Please add more generators to reach a cumulative\n generation of: "+\
														str(int(self.boardlogic.dispatchProfile[self.boardlogic.time_period][1]*0.1)),98])
					self.updateMessage()

		if(self.boardlogic.level==3):	
			self.master.after(self.updateRate,isoLevel, self.boardlogic,self,self.master)
		elif(self.boardlogic.level==4):	
			self.master.after(self.updateRate,renewLevel, self.boardlogic,self,self.master)
		
	def gensHover(self,event):
		#remove the border from the other generators
		for child in self.master.children:
				try:
					self.master.children[child].configure(bd=0,bg="#ffffff")
				except:
					r=0

		rows = self.tableGens.selection()
		for row_id in rows:
			row=self.tableGens.item(row_id,'values')
			#highlight the appropriate generator icons
			for child in self.master.children:
				try:
					if(self.master.children[child]['text']==row[1]):
						self.master.children[child].configure(bd=6,bg="#ffa500")
				except:
					r=0


	def gensClick(self,event):
		

		#remove the border from the other generator icons
		for child in self.master.children:
				try:
					self.master.children[child].configure(bd=0,bg="#ffffff")
				except:
					r=0

		rows = self.tableGens.selection()
		for row in rows:
			row_id = row
			row=self.tableGens.item(row_id,'values')

			min_bid_rate=50000
			for gen in self.boardlogic.availableGenerators:
					if(float(str(gen[4]))<min_bid_rate):
						min_bid_rate=float(str(gen[4]))

			ramp_list=[]
			for gen in self.boardlogic.availableGenerators:
				ramp_list.append(float(str(gen[3])))

			median_ramp_rate = np.median(np.array(ramp_list))

			if(self.boardlogic.time_period<5 and self.boardlogic.enteredAncillaryMarket==False):#we're not in ancillary services
				min_bid_rate=float(str(locale.currency(min_bid_rate)[1:]))

				if(float(str(row[-1][1:]))==min_bid_rate):
					genList=self.boardlogic.availableGenerators
					self.boardlogic.availableGenerators=[]
					for gen in genList:
						if(gen[1]!=row[1]):
							self.boardlogic.availableGenerators.append(gen)
						else:
							self.boardlogic.gensSelected[self.boardlogic.time_period].append(gen)

					# self.boardlogic.availableGenerators = np.delete(self.boardlogic.availableGenerators,np.where(self.boardlogic.availableGenerators[:,1] == row[1])[0][0])
					

					self.boardlogic.cumulGen+=float(str(row[2]))*self.boardlogic.profilePeriods[self.boardlogic.time_period][1]#to account for the amount of time this will be online
					self.boardlogic.clearingGens.append([row[1],self.boardlogic.cumulGen,row[4]])

					#highlight the appropriate generator icons
					for child in self.master.children:
						try:
							if(self.master.children[child]['text']==row[1]):
								self.master.children[child].configure(bd=6,bg="#ffa500")
						except:
							r=0
				else:
					if(len(self.boardlogic.updateQueue)>0):
						if(self.boardlogic.updateQueue[-1][1]!=98):#avoid adding the error message multiple times
							self.boardlogic.updateQueue.append(["A generator could not be added as it did\nnot have the minimum bid rate",98])
							self.updateMessage()
					else:
						self.boardlogic.updateQueue.append(["A generator could not be added as it did\nnot have the minimum bid rate",98])
						self.updateMessage()

			else:#we're in ancillary services
				
				#check if the ramp rate is correct
				if(float(str(row[3]))>=median_ramp_rate):


					#check the the price is minimal
					min_bid_rate=50000
					for gen in self.boardlogic.availableGenerators:
							if(float(str(gen[4]))<min_bid_rate):
								min_bid_rate=float(str(gen[4]))

					if(float(str(row[-1][1:]))==min_bid_rate):
						
							genList=self.boardlogic.availableGenerators
							self.boardlogic.availableGenerators=[]
							for gen in genList:
								if(gen[1]!=row[1]):
									self.boardlogic.availableGenerators.append(gen)

							self.boardlogic.cumulGen+=float(str(row[2]))*self.boardlogic.profilePeriods[self.boardlogic.ancillary_period][1]#to account for the amount of time this will be online
							self.boardlogic.clearingGens.append([row[1],self.boardlogic.cumulGen,row[4]])

							#highlight the appropriate generator icons
							for child in self.master.children:
								try:
									if(self.master.children[child]['text']==row[1]):
										self.master.children[child].configure(bd=6,bg="#ffa500")
								except:
									r=0
						# else:
						# 	if(len(self.boardlogic.updateQueue)>0):
						# 		if(self.boardlogic.updateQueue[-1][1]!=98):#avoid adding the error message multiple times
						# 			self.boardlogic.updateQueue.append(["Please add more generators to reach a cumulative\n generation of: "+\
						# 											str(int(self.boardlogic.demandProfile[self.boardlogic.time_period][1]*0.1)),98])
						# 			self.updateMessage()
						# 	else:
						# 		self.boardlogic.updateQueue.append(["Please add more generators to reach a cumulative\n generation of: "+\
						# 											str(int(self.boardlogic.demandProfile[self.boardlogic.time_period][1]*0.1)),98])
						# 		self.updateMessage()

					else:
						if(len(self.boardlogic.updateQueue)>0):
							if(self.boardlogic.updateQueue[-1][1]!=98):#avoid adding the error message multiple times
								self.boardlogic.updateQueue.append(["A generator could not be added as it did\nnot have the minimum bid rate",98])
								self.updateMessage()
						else:
							self.boardlogic.updateQueue.append(["A generator could not be added as it did\nnot have the minimum bid rate",98])
							self.updateMessage()

				else:
					if(len(self.boardlogic.updateQueue)>0):
						if(self.boardlogic.updateQueue[-1][1]!=198):#avoid adding the error message multiple times
							self.boardlogic.updateQueue.append(["A generator could not be added as it did\nnot have the minimum ramp rate of "+str(median_ramp_rate),198])
							self.updateMessage()
					else:
						self.boardlogic.updateQueue.append(["A generator could not be added as it did\nnot have the minimum ramp rate of "+str(median_ramp_rate),198])
						self.updateMessage()

		if(len(self.boardlogic.clearingGens)>self.tableClearing['height']-1):
			diff=len(self.boardlogic.clearingGens)-(self.tableClearing['height']-1)
			if(self.tableGens['height']-diff>5):
				self.tableClearing['height']+=diff
				self.tableGens['height']-=diff




		self.root.after(1,self.updateDisplaysLevel3,self.root)


	def createInfoTables(self):	
		#points system
		self.pointsTitle=   tk.Label(self.infoCanvas,bg='lightgray',text="Total Points",font=("Helvetica", 12))
		self.pointsTitle.place(x=10,y=0)

		self.points = tk.Label(self.infoCanvas,bg='lightgray',text=str(int(self.boardlogic.totalPoints)),font=("Helvetica", 20),fg="#309933")
		self.points.place(x=20,y=50)


		#ancillary services
		self.ancillaryTitle=   tk.Label(self.infoCanvas,bg='lightgray',text="Ancillary Services",font=("Helvetica", 12))
		self.ancillaryTitle.place(x=160,y=0)

		self.tableAncillary = ttk.Treeview(self.infoCanvas,height=5)
		self.tableAncillary["columns"]=("segment","generation")
		self.tableAncillary.column("segment", width=80 ,anchor=tk.CENTER)
		self.tableAncillary.column("generation" , width=100,anchor=tk.CENTER)

		self.tableAncillary.heading("segment", text="Segment")
		self.tableAncillary.heading("generation" , text="Gen. (MWh)")

		row_tag='oddrow'#for alternating colors
		for gen in reversed(self.boardlogic.ancillaryProfile):
			if(row_tag=='oddrow'):
				row_tag='evenrow'
				self.tableAncillary.insert("",0,values=(gen[0],gen[1]),tags=row_tag)
			else:
				row_tag='oddrow'
				self.tableAncillary.insert("",0,values=(gen[0],gen[1]),tags=row_tag)
		self.tableAncillary.tag_configure('oddrow', background='#b8b894')

		self.tableAncillary['show'] = 'headings'#get rid of the empty column on the left
		self.tableAncillary.place(x=125,y=20)

		#dispatch
		self.dispatchTitle=   tk.Label(self.infoCanvas,bg='lightgray',text="Dispatch",font=("Helvetica", 12))
		self.dispatchTitle.place(x=380,y=0)

		self.tableDispatch = ttk.Treeview(self.infoCanvas,height=5)
		self.tableDispatch["columns"]=("segment","generation")
		self.tableDispatch.column("segment", width=80 ,anchor=tk.CENTER)
		self.tableDispatch.column("generation" , width=100,anchor=tk.CENTER)

		self.tableDispatch.heading("segment", text="Segment")
		self.tableDispatch.heading("generation" , text="Gen. (MWh)")

		self.updateDispatchProfile()
		row_tag='oddrow'#for alternating colors
		for gen in reversed(self.boardlogic.dispatchProfile):
			if(row_tag=='oddrow'):
				row_tag='evenrow'
				self.tableDispatch.insert("",0,values=(gen[0],gen[1]),tags=row_tag)
			else:
				row_tag='oddrow'
				self.tableDispatch.insert("",0,values=(gen[0],gen[1]),tags=row_tag)
		self.tableDispatch.tag_configure('oddrow', background='#b8b894')

		self.tableDispatch['show'] = 'headings'#get rid of the empty column on the left
		self.tableDispatch.place(x=320,y=20)

		#demand profile
		self.demandTitle=   tk.Label(self.infoCanvas,bg='lightgray',text="Demand Profile",font=("Helvetica", 12))
		self.demandTitle.place(x=580,y=0)

		self.tableDemand = ttk.Treeview(self.infoCanvas,height=5)
		self.tableDemand["columns"]=("segment","generation","duration")
		self.tableDemand.column("segment", width=80 ,anchor=tk.CENTER)
		self.tableDemand.column("generation" , width=100,anchor=tk.CENTER)
		self.tableDemand.column("duration" , width=50,anchor=tk.CENTER)

		self.tableDemand.heading("segment", text="Segment")
		self.tableDemand.heading("generation" , text="Gen. (MWh)")
		self.tableDemand.heading("duration" , text="Hrs.")


		

		row_tag='oddrow'#for alternating colors
		for i,gen in enumerate(reversed(self.boardlogic.demandProfile)):
			if(row_tag=='oddrow'):
				row_tag='evenrow'
				self.tableDemand.insert("",0,values=(gen[0],gen[1],self.boardlogic.profilePeriods[4-i][1]),tags=row_tag)
			else:
				row_tag='oddrow'
				self.tableDemand.insert("",0,values=(gen[0],gen[1],self.boardlogic.profilePeriods[4-i][1]),tags=row_tag)
		self.tableDemand.tag_configure('oddrow', background='#b8b894')

		self.tableDemand['show'] = 'headings'#get rid of the empty column on the left
		self.tableDemand.place(x=515,y=20)

		

	def createImage(self):
		#resize the canvas, not that everything else has been placed
		image = Image.open("../images/level3_old.png")
		image=image.resize((750,800-self.infoCanvasHeight))#750,700-self.infoCanvasHeight
		# image.save('../images/level3_label.png')

		photo = ImageTk.PhotoImage(image)
		self.master.photo=photo
		self.background = self.imageCanvas.create_image((0,0),image=photo,anchor='nw')
		# self.imgLabel = tk.Label(self.imageCanvas,image=photo)
		# self.imgLabel.image = photo # keep a reference!
		# self.imgLabel.place(x=0,y=0)

	def updateAvailableGenerators(self):

		if(self.boardlogic.time_period!=self.boardlogic.last_time_period):
			self.boardlogic.availableGenerators=[]

			#choose randomly 20 generators
			num_to_choose = 35
			genList=range(len(self.boardlogic.generators))
			random.shuffle(genList)
			genList = genList[:num_to_choose]
			for i in genList:
				self.boardlogic.availableGenerators.append(self.boardlogic.generators[i])

			self.boardlogic.last_time_period=self.boardlogic.time_period

	def chooseNewGenerators(self):
		self.boardlogic.availableGenerators=[]

		#choose randomly 20 generators
		num_to_choose = 35
		genList=range(len(self.boardlogic.generators))
		random.shuffle(genList)
		gensNotChosen=genList[num_to_choose:]
		genList = genList[:num_to_choose]

		for i in genList:
			if(self.boardlogic.time_period==5):#if we're in ancillary services, don't serve up a generator that has already been selected
				if(self.boardlogic.generators[i] in self.boardlogic.gensSelected[self.boardlogic.ancillary_period]):
					#choose a new generator
					while True:
						k=random.choice(range(len(self.boardlogic.generators)))
						if(self.boardlogic.generators[k] not in self.boardlogic.gensSelected[self.boardlogic.ancillary_period]) and \
														(self.boardlogic.generators[k] not in self.boardlogic.availableGenerators):
							self.boardlogic.availableGenerators.append(self.boardlogic.generators[k])
							break
				else:
					self.boardlogic.availableGenerators.append(self.boardlogic.generators[i])
			else:
				self.boardlogic.availableGenerators.append(self.boardlogic.generators[i])

		self.boardlogic.last_time_period=self.boardlogic.time_period

	def updateDemandProfile(self):
		if((self.boardlogic.time_period==0 or self.boardlogic.time_period==4) and (self.boardlogic.time_period!=self.boardlogic.last_time_period) and\
																											self.boardlogic.enteredAncillaryMarket==False):
			# alpha=2
			# beta=5
			timePeriodMeans=[   [80500	,90500,124320],
								[124520	,138520,142006],
								[142206	,145720,217244],
								[124520	,138520,142006],
								[80500	,90500,124520]
							]

			for i in range(5):
				k =  int(np.random.normal(timePeriodMeans[i][1], 5000, 1)[0])
				if (k<timePeriodMeans[i][0]):
					k=timePeriodMeans[i][1]+random.randint(0,200)
				elif(k>timePeriodMeans[i][2]):
					k=timePeriodMeans[i][1]+random.randint(0,200)

				self.boardlogic.demandProfile[i][1] = k

	def updateDispatchProfile(self):
		#autofill the dispatch
		self.boardlogic.dispatchProfile[self.boardlogic.time_period][1] = self.boardlogic.demandProfile[self.boardlogic.time_period][1]

	def updateAncillaryProfile(self):
		#autofill the dispatch
		self.boardlogic.ancillaryProfile[self.boardlogic.ancillary_period][1] = int(self.boardlogic.dispatchProfile[self.boardlogic.time_period][1]*0.1)#self.boardlogic.demandProfile[self.boardlogic.ancillary_period][1]


	def clearTimePeriod(self):
		if(self.boardlogic.time_period<5):#we're not in the ancillary market
			if(self.boardlogic.enteredAncillaryMarket==False):
				self.boardlogic.dispatchProfile[self.boardlogic.time_period][1]=self.boardlogic.demandProfile[self.boardlogic.time_period][1]#self.boardlogic.cumulGen
			self.boardlogic.cumulGen=0
			# self.updateDispatchProfile()

			#wipe the market clearing board
			# self.tableAncillary.delete(*self.tableAncillary.get_children())
			self.boardlogic.clearingGens=[]

			#choose new generators
			self.chooseNewGenerators()

			#adjust height of tables
			self.tableGens['height']=26
			self.tableClearing['height']=5

		else:#we're in the ancillary market
			self.boardlogic.ancillaryProfile[self.boardlogic.ancillary_period][1]=int(self.boardlogic.cumulGen)#self.boardlogic.demandProfile[self.boardlogic.ancillary_period][1]#self.boardlogic.cumulGen
			self.boardlogic.cumulGen=0
			# self.updateDispatchProfile()

			#wipe the market clearing board
			# self.tableAncillary.delete(*self.tableAncillary.get_children())
			self.boardlogic.clearingGens=[]

			#choose new generators
			self.chooseNewGenerators()

			#adjust height of tables
			self.tableGens['height']=26
			self.tableClearing['height']=5

		self.updateDisplaysLevel3(self.master)

	def addGenerators(self):
		#make a label with an image for each generator. The generator name is in the text, which is not visible,
		#but can be used to reference it later
		img_height=800-self.infoCanvasHeight
		img_width= 750
		icon_size=(25,25)
		background_image_start=[0,self.infoCanvasHeight]

		self.genIcons=[]
		for i,gen in enumerate(self.boardlogic.generators):
			#image determined by type of generator
			if(gen[0]=='Coal' or gen[0]=='Coal '):
				img=Image.open('../images/coal.png')
			elif(gen[0]=='Gas' or gen[0]=='Gas '):
				img=Image.open('../images/gas.png')
			elif(gen[0]=='Hydro' or gen[0]=='Hydro '):
				img=Image.open('../images/hydro.png')
			elif(gen[0]=='Nuclear' or gen[0]=='Nuclear '):
				img=Image.open('../images/nuclear.png')
			img=img.resize(icon_size)
			img=ImageTk.PhotoImage(img)

			genLabel = tk.Label(self.master,image=img, height=icon_size[0], width=icon_size[1],text=str(gen[1]),font=("Helvetica", 1), bd=0,bg="#ffffff")
			genLabel.image=img#keep a reference!
			#for tool tips
			tool_tip = Tooltip(genLabel,  text="Gen type: "+str(gen[0])+"\nName: "+str(gen[1])+"\nCapacity: "+str(gen[2])+"MW")
			# genLabel.description="This is"+str(gen[1])
			# genLabel.bind("<Enter>",self.genToolTip)


			x_loc=background_image_start[0]+(float(gen[-2])-0.01)*img_width
			y_loc=background_image_start[1]+(float(gen[-1])-0.01)*img_height
			genLabel.place(x=x_loc,y=y_loc)

			self.genIcons.append(genLabel)

	def addLoads(self):
		#add the load icons to the map
		img_height=800-self.infoCanvasHeight
		img_width= 750
		icon_size=(30,30)
		background_image_start=[0,self.infoCanvasHeight]

		gen_locs=[]
		with open('genLocations.csv', 'rb') as csvfile:
			load_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in load_reader:
				if(row[-1]=='money'):
					img=Image.open('../images/commercial_load.jpg')
					capacity=random.randint(52325-5000,52325+2000)
					load_type = "Commercial"

				elif(row[-1]=='house'):
					img=Image.open('../images/residential_load.jpg')
					capacity=random.randint(85995-5000,85995+2000)
					load_type = "Residential"

				elif(row[-1]=='industrial'):
					img=Image.open('../images/industrial_load.png')
					capacity = random.randint(42210-5000,42210+2000)
					load_type = "Industrial"

				try:
					img=img.resize(icon_size)
					img=ImageTk.PhotoImage(img)

					loadLabel = tk.Label(self.master,image=img, height=icon_size[0], width=icon_size[1],text=str(row[1]),font=("Helvetica", 1), bd=0,bg="#ffffff")
					loadLabel.image=img#keep a reference!

					
					tool_tip = Tooltip(loadLabel,  text="Load type: "+str(load_type)+"\nDemand: "+str(capacity)+"MWh")

					x_loc=background_image_start[0]+(float(row[-4])-0.01)*img_width
					y_loc=background_image_start[1]+(float(row[-3])-0.01)*img_height
					loadLabel.place(x=x_loc,y=y_loc)
				except:
					r=0


	def level3MessageHandler(self,root):
		#display message if there is any

		# 2-hydro dam
		# 4-residential load
		# 5-generator fleet
		# 6-market clearing table
		# 7-dispatch table
		# 8-Demand profile table
		# 10-ancillary services

		#display the little attention icon
		if (self.boardlogic.level==3 and len(self.boardlogic.updateQueue)>0):
			
			if(self.boardlogic.updateQueue[0][1]==1):
				self.imageCanvas.create_oval(500,500,540,540,fill="#ff6600",width=0,tag="circle")

			if(self.boardlogic.updateQueue[0][1]==2):#hydro dam
				if(self.imageCanvas.coords("circle")[0]>75):
					self.imageCanvas.move("circle",-21,-20)

			elif(self.boardlogic.updateQueue[0][1]==4):#residential load
				if(self.imageCanvas.coords("circle")[0]<500):
					self.imageCanvas.move("circle",20,1)

			elif(self.boardlogic.updateQueue[0][1]==5):#generator fleet
				if(self.imageCanvas.coords("circle")[0]<700):
					self.imageCanvas.move("circle",10,0)

			elif(self.boardlogic.updateQueue[0][1]==6):#market clearing table
				if(self.imageCanvas.coords("circle")[1]<500):
					self.imageCanvas.move("circle",0,20)

			elif(self.boardlogic.updateQueue[0][1]==7):#dispatch
				if(self.imageCanvas.coords("circle")[0]>420):
					self.imageCanvas.move("circle",-12,-21)

			elif(self.boardlogic.updateQueue[0][1]==8):#demand profile
				if(self.imageCanvas.coords("circle")[0]<600):
					self.imageCanvas.move("circle",10,0)

			elif(self.boardlogic.updateQueue[0][1]==10):#ancillary services
				if(self.imageCanvas.coords("circle")[0]>200):
					self.imageCanvas.move("circle",-20,0)

			elif(self.boardlogic.updateQueue[0][1]==11):#highlight the turbine
				try:
					if(self.imageCanvas.coords("circle")[0]>70):
						self.imageCanvas.delete("circle")
				except:
					r=0
		

