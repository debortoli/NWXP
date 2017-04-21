# from Tkinter import Tk, Label, Button,Canvas,Frame
import Tkinter as tk
import pdb
import time
import ttk
from logicmain import gameLogic
from level1 import initLevel1

class TKBoard:
	def __init__(self, master,boardlogic):
		self.master = master
		master.title("GRID SIMULATOR")
		master.minsize(width=1300,height=700)
		master.maxsize(width=1300,height=700)


		self.boardlogic=boardlogic

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
		self.draggablesCanvas = tk.Canvas(self.updateFrame,bg="lightgray",highlightthickness=2,highlightbackground="Black",height=500)
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
		self.water_slider_label.place(x=670,y=10)

		self.water_slider=tk.Scale(self.gameCanvas,from_=0, to=350,orient='horizontal',command=self.updateWaterVelocity,showvalue=0)
		self.water_slider.place(x=700,y=40)

		#put in the level end button
		self.level1endbutton=tk.Button(self.gameFrame,bg='#00ff00',text="     Move     \n     on!     \n")
		self.level1endbutton.pack_forget()
		

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
		self.updateRate=100#its in ms

		#spill button
		self.spillRepeatInterval=100
		self.spillbutton=tk.Button(self.gameCanvas,bg='#c0c0c0',text="Spill Water!",command=self.spill,repeatdelay=10,repeatinterval=self.spillRepeatInterval,relief='groove')
		self.spillbutton.place(x=self.gameCanvas.coords(self.damTopPolygon)[0],y=self.gameCanvas.coords(self.damTopPolygon)[1]-27)

		#time indicator
		self.timeIndicator=tk.Label(self.gameCanvas,bg='white',text="time",font=("Helvetica", 15),fg="#bb0000")
		self.timeIndicator.place(x=15,y=15)



	def updateDisplays(self,root):
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

				if(self.gameCanvas.coords("circle")[0]<630):
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

	def updateMessage(self):
		self.updateMessageCanvas.pack()
		self.updateMessageLabel['text']=self.boardlogic.updateQueue[0][0]
		self.updateMessageLabel.pack(side='top',pady=10)

	def nextMessage(self):
		
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

	def updateWaterVelocity(self,value):
		self.boardlogic.water_velocity=float(value)
		self.waterAnimationSpeed=float(value)/12000


	def spinTurbine(self,root):
		#get position of blade
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
		self.level1endbutton.place(x=500,y=40)
		root.after(1,self.spinTurbine,root)

	def spill(self):
		self.boardlogic.spilledSeconds+=self.spillRepeatInterval/1000.
		if(self.boardlogic.spilledSeconds>10.):
			self.boardlogic.updateQueue.append(["Cannot spill for more than 20 seconds!",199])
			self.boardlogic.updateQueue.append(["Cannot spill for more than 20 seconds!",199])
			self.updateMessage()

		else:
			self.boardlogic.water_level-=0.1
		
		
