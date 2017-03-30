# from Tkinter import Tk, Label, Button,Canvas,Frame
import Tkinter as tk
import pdb
import time
import ttk
from logicmain import gameLogic

class TKBoard:
	def __init__(self, master,boardlogic):
		self.master = master
		master.title("GRID SIMULATOR")
		master.minsize(width=1400,height=700)


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

		self.points = tk.Label(self.pointsCanvas,bg='lightgray',text=str(boardlogic.totalPoints),font=("Helvetica", 25),fg="green")
		self.points.pack(side='top',pady=10)

		#draggables canvas
		self.draggablesCanvas = tk.Canvas(self.updateFrame,bg="lightgray",highlightthickness=2,highlightbackground="Black",height=500)
		self.draggablesCanvas.pack()#grid(row=2,column=0,sticky='NS')

		#the game canvas
		self.gameFrame=tk.Frame(master,bg="white",highlightthickness=0)
		self.gameFrame.pack(fill='both',expand=True)

		self.gameCanvas=tk.Canvas(self.gameFrame,bg="white",highlightthickness=0)
		

		#draw constraints for water
		self.damRectangle=[0,150,400,500]

		#compute height of dam
		self.dam_height=self.damRectangle[3]-self.damRectangle[1]

		#draw the top of the dam
		self.dam_width=450
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
		
		#flowing of the water
		[self.kneePointx,self.kneePointy]=[self.gameCanvas.coords(self.damTopPolygon)[4],self.gameCanvas.coords(self.damTopPolygon)[5]]
		[self.startx,self.starty]=[self.gameCanvas.coords(self.damTopPolygon)[2],self.gameCanvas.coords(self.damTopPolygon)[3]]
		[self.diffx,self.diffy]=[self.kneePointx-self.startx,self.kneePointy-self.starty]
		self.wave_width=1/15.
		self.wavePolygon=self.gameCanvas.create_polygon(self.startx,self.starty,
														self.startx+self.diffx*self.wave_width,self.starty+self.diffy*self.wave_width,
														self.gameCanvas.coords(self.damBottomPolygon)[0]+self.diffx*self.wave_width,self.gameCanvas.coords(self.damBottomPolygon)[1]+self.diffy*self.wave_width,
														self.gameCanvas.coords(self.damBottomPolygon)[0],self.gameCanvas.coords(self.damBottomPolygon)[1],
														fill="#0000cc",width=0)

		#add generator
		self.generator_buffer_x=10
		self.generator_buffer_y=10
		self.generator=self.gameCanvas.create_rectangle(self.gameCanvas.coords(self.damTopPolygon)[16]+self.generator_buffer_x,self.gameCanvas.coords(self.damTopPolygon)[17]-self.generator_buffer_y,
														self.gameCanvas.coords(self.damTopPolygon)[12]-self.generator_buffer_x,self.gameCanvas.coords(self.damTopPolygon)[13]+self.generator_buffer_y,
														fill="#808080",width=0)
		

		#add shaft
		self.generator_width=self.gameCanvas.coords(self.generator)[2]-self.gameCanvas.coords(self.generator)[0]
		self.shaft_width=self.generator_width/3.
		self.shaft_height=90
		self.shaft=self.gameCanvas.create_rectangle(self.gameCanvas.coords(self.generator)[0]+self.shaft_width,self.gameCanvas.coords(self.damTopPolygon)[17]-self.generator_buffer_y,
													self.gameCanvas.coords(self.generator)[0]+self.shaft_width*2,self.gameCanvas.coords(self.damTopPolygon)[17]-self.generator_buffer_y+self.shaft_height,
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
		fillRect=self.gameCanvas.create_rectangle(self.damRectangle[0],
												  self.fill_start,
												  self.damRectangle[2],
												  self.damRectangle[3],
												  fill="#0000aa",width=0)

		
		

	   
		#add power station
		self.p_station_height=120
		self.p_station_width=50
		pstationRect=self.gameCanvas.create_rectangle(self.damRectangle[2]+self.dam_width+self.powerhouse_width+70,
													self.damRectangle[1]+self.tower_height+self.dam_triangle_h-20,
													self.damRectangle[2]+self.dam_width+self.powerhouse_width+self.p_station_width,
													self.damRectangle[1]+self.tower_height+self.dam_triangle_h-self.p_station_height ,
												  fill="#808080",width=0)

		#one rectangle which is the ground
		ground_width=self.dam_width+self.damRectangle[2]+200
		groundRect=self.gameCanvas.create_rectangle(self.damRectangle[0],
												  self.damRectangle[3],
												  ground_width+self.damRectangle[0],
												  self.damRectangle[3]+50,
												  fill="#7B3523",width=0)
		self.gameCanvas.pack(fill='both',expand=True)


		

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


		# self.butt=tk.Button(master,command=lambda: self.greet(boardlogic))
		# self.butt.pack()



	def updateDisplays(self,root):
		#level progress and total points earned
		self.progress["value"]=self.boardlogic.progress
		self.points['text']=self.boardlogic.totalPoints

		#fill level of dam
		if(self.boardlogic.level==1):
			# self.gameCanvas.clear('fillRect')
			self.dam_height=self.damRectangle[3]-self.damRectangle[1]

			#compute how many pixels need to be filled
			self.fill_start=self.damRectangle[3]-self.boardlogic.water_level/100.*self.dam_height
			fillRect=self.gameCanvas.create_rectangle(self.damRectangle[0],
												  self.fill_start,
												  self.damRectangle[2],
												  self.damRectangle[3],
												  fill="#0000aa",width=0)

		
		root.after(10,gameLogic,self,self.boardlogic,root)

	def updateMessage(self):
		self.updateMessageCanvas.pack()
		self.updateMessageLabel['text']=self.boardlogic.updateQueue[0]
		self.updateMessageLabel.pack(side='top',pady=10)

	def nextMessage(self):
		del self.boardlogic.updateQueue[0]
		if(len(self.boardlogic.updateQueue)==0):
			#stop providing update messages
			self.updateMessageCanvas.pack_forget()
		else:
			#display the next message
			self.updateMessage()


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
		self.blade=self.gameCanvas.create_rectangle(x0+1,y0,
													x1+1,y1,
													fill="#000000")

		#get position of leading edge of wave
		[x0,y0]=[self.gameCanvas.coords(self.wavePolygon)[2],self.gameCanvas.coords(self.wavePolygon)[3]]
		wave_velocity=1/40.
		if(x0>self.kneePointx or y0>self.kneePointy)and(x0<self.gameCanvas.coords(self.damTopPolygon)[6]-3):
			if(self.gameCanvas.coords(self.wavePolygon)[0]<self.kneePointx):#we're just turning the corner
				self.gameCanvas.delete(self.wavePolygon)
				self.wavePolygon=self.gameCanvas.create_polygon(self.kneePointx,self.kneePointy,
															self.kneePointx+self.diffx*self.wave_width,self.kneePointy,
															self.kneePointx+self.diffx*self.wave_width,self.kneePointy+self.penstock_diameter,
															self.kneePointx,self.kneePointy+self.penstock_diameter,
															fill="#0000cc",width=0)

			self.gameCanvas.move(self.wavePolygon,self.diffx*wave_velocity/2.,0)

		elif(x0>self.gameCanvas.coords(self.damTopPolygon)[6]-3):
			self.gameCanvas.delete(self.wavePolygon)
			self.wavePolygon=self.gameCanvas.create_polygon(self.startx,self.starty,
														self.startx+self.diffx*self.wave_width,self.starty+self.diffy*self.wave_width,
														self.gameCanvas.coords(self.damBottomPolygon)[0]+self.diffx*self.wave_width,self.gameCanvas.coords(self.damBottomPolygon)[1]+self.diffy*self.wave_width,
														self.gameCanvas.coords(self.damBottomPolygon)[0],self.gameCanvas.coords(self.damBottomPolygon)[1],
														fill="#0000cc",width=0)

		else:#its moving down the chute
			self.gameCanvas.move(self.wavePolygon,self.diffx*wave_velocity,self.diffy*wave_velocity)

		

		#delete the old wave
		# self.gameCanvas.delete(self.wavePolygon)

		#add a new wave
		# wave_velocity=1/10.
		# [start_wavex,start_wavey]=[x0+self.diffx*wave_velocity,y0+diffy*self.wave_velocity]
		# [bottom_wavex,bottom_wavey]=[x1+self.diffx*wave_velocity,y1+diffy*self.wave_velocity]
		# self.blade=self.gameCanvas.create_polygon(start_wavex,start_wavey,
		# 										  start_wavex+diffx*self.wave_width,start_wavey+diffy*self.wave_width,
		# 										  bottom_wavex+diffx*self.wave_width,bottom_wavey+diffy*self.wave_width,
		# 										  bottom_wavex,bottom_wavey,
		# 											fill="#0000cc",width=0)


		root.after(10,self.updateDisplays,root)

