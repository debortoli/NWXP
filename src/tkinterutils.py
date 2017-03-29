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
        self.damRectangle=[0,200,400,500]

        #compute height of dam
        self.dam_height=self.damRectangle[3]-self.damRectangle[1]

        #draw thw actual dam
        self.dam_width=200
        self.dam_triangle_h=150
        self.tower_height=self.dam_height*0.3
        self.tower_width=100
        self.tower_elevation=50
        damPolygon=self.gameCanvas.create_polygon(self.damRectangle[2],self.damRectangle[1],
                                                  self.damRectangle[2],self.damRectangle[1]+self.tower_height,
                                                  self.damRectangle[2]+self.dam_width,self.damRectangle[1]+self.tower_height+self.dam_triangle_h,
                                                  self.damRectangle[2]+self.dam_width,self.damRectangle[1]+self.tower_height+self.tower_elevation,
                                                  self.damRectangle[2]+self.tower_width,self.damRectangle[1]+self.tower_height,
                                                  self.damRectangle[2]+self.tower_width,self.damRectangle[1],
                                                  self.damRectangle[2],self.damRectangle[1],
                                                  fill="#c0c0c0",width=0)

        #draw the bottom of the dam
        self.penstock_diameter=50
        self.turbine_elevation=30
        damBottomPolygon=self.gameCanvas.create_polygon(self.damRectangle[2],self.damRectangle[1]+self.tower_height+self.penstock_diameter,
                                                        self.damRectangle[2],self.damRectangle[3],
                                                        self.damRectangle[2]+self.dam_width,self.damRectangle[3],
                                                        self.damRectangle[2]+self.dam_width,self.damRectangle[1]+self.tower_height+self.dam_triangle_h+self.penstock_diameter,
                                                        fill="#c0c0c0",width=0)

        #draw the powerhouse
        self.powerhouse_width=150
        self.powerhouse_height=150
        powerhousePolygon=self.gameCanvas.create_polygon(self.damRectangle[2]+self.dam_width,self.damRectangle[1]+self.tower_height+self.dam_triangle_h,
                                                         self.damRectangle[2]+self.dam_width+self.powerhouse_width,self.damRectangle[1]+self.tower_height+self.dam_triangle_h,
                                                         self.damRectangle[2]+self.dam_width+self.powerhouse_width,self.damRectangle[1]+self.tower_height+self.dam_triangle_h-self.powerhouse_height,
                                                         self.damRectangle[2]+self.dam_width,self.damRectangle[1]+self.tower_height+self.dam_triangle_h-self.powerhouse_height,
                                                        fill="#d0d0d0",width=0)

        #draw the generator
        self.generator_buffer_width=self.powerhouse_width*0.15
        self.generator_buffer_height=self.powerhouse_height*0.35
        generatorPolygon=self.gameCanvas.create_polygon(self.damRectangle[2]+self.dam_width+self.generator_buffer_width,self.damRectangle[1]+self.tower_height+self.dam_triangle_h-self.generator_buffer_height,
                                                         self.damRectangle[2]+self.dam_width+self.powerhouse_width-self.generator_buffer_width,self.damRectangle[1]+self.tower_height+self.dam_triangle_h-self.generator_buffer_height,
                                                         self.damRectangle[2]+self.dam_width+self.powerhouse_width-self.generator_buffer_width,self.damRectangle[1]+self.tower_height+self.dam_triangle_h-self.powerhouse_height+self.generator_buffer_height,
                                                         self.damRectangle[2]+self.dam_width+self.generator_buffer_width,self.damRectangle[1]+self.tower_height-self.powerhouse_height+self.dam_triangle_h+self.generator_buffer_height,
                                                        fill="#808080",width=0)

        #draw the shaft
        self.shaft_height=self.damRectangle[1]+self.tower_height+self.dam_triangle_h+30
        self.shaft_buffer_width=(self.powerhouse_width-self.generator_buffer_width*2)/2.5
        self.turbine_buffer_height=0.2*self.penstock_diameter
        shaftPolygon=self.gameCanvas.create_polygon(self.damRectangle[2]+self.dam_width+self.generator_buffer_width+self.shaft_buffer_width,self.shaft_height,#damRectangle[1]+self.tower_height+self.dam_triangle_h-self.generator_buffer_height+self.shaft_height,
                                                        self.damRectangle[2]+self.dam_width+self.powerhouse_width-self.generator_buffer_width-self.shaft_buffer_width,self.shaft_height,#self.damRectangle[1]+self.tower_height+self.dam_triangle_h-self.generator_buffer_height+self.shaft_height,
                                                        self.damRectangle[2]+self.dam_width+self.powerhouse_width-self.generator_buffer_width-self.shaft_buffer_width,self.damRectangle[1]+self.tower_height+self.dam_triangle_h-self.generator_buffer_height,
                                                        self.damRectangle[2]+self.dam_width+self.generator_buffer_width+self.shaft_buffer_width,self.damRectangle[1]+self.tower_height+self.dam_triangle_h-self.generator_buffer_height,
                                                        fill="#808080",width=0)

        #draw the turbine
        self.turbine_height=20
        self.turbine_buffer_width=20
        turbinePolygon=self.gameCanvas.create_polygon(self.damRectangle[2]+self.dam_width+self.generator_buffer_width+self.shaft_buffer_width-self.turbine_buffer_width,self.shaft_height+self.turbine_height,
                                                        self.damRectangle[2]+self.dam_width+self.powerhouse_width-self.generator_buffer_width-self.shaft_buffer_width+self.turbine_buffer_width,self.shaft_height+self.turbine_height,   
                                                        self.damRectangle[2]+self.dam_width+self.powerhouse_width-self.generator_buffer_width-self.shaft_buffer_width+self.turbine_buffer_width,self.shaft_height,
                                                        self.damRectangle[2]+self.dam_width+self.generator_buffer_width+self.shaft_buffer_width-self.turbine_buffer_width,self.shaft_height,
                                                        fill="#808080",width=0)
        #draw the blade
        self.blade_height=self.turbine_height+4
        self.blade_width=12
        self.blade=self.gameCanvas.create_rectangle(self.damRectangle[2]+self.dam_width+self.generator_buffer_width+self.shaft_buffer_width-self.turbine_buffer_width+5,self.shaft_height+self.turbine_height+2,
                                                    self.damRectangle[2]+self.dam_width+self.generator_buffer_width+self.shaft_buffer_width-self.turbine_buffer_width+self.blade_width,self.shaft_height+self.turbine_height-self.turbine_height-2,
                                                    fill="#000000")
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

        #one rectangle which is the ground
        ground_width=800
        groundRect=self.gameCanvas.create_rectangle(self.damRectangle[0],
                                                  self.damRectangle[3],
                                                  ground_width+self.damRectangle[0],
                                                  self.damRectangle[3]+100,
                                                  fill="#7B3523",width=0)
        self.gameCanvas.pack(fill='both',expand=True)


        

        #updateCanvas
        self.updateMessageCanvas=tk.Canvas(self.gameFrame,bg="lightgray",highlightthickness=0)
        self.updateMessageCanvas.pack(fill='y')
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

            #
        root.after(100,gameLogic,self,self.boardlogic,root)

    def updateMessage(self):
        self.updateMessageCanvas.pack(side='left')
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
        root.after(10,self.updateDisplays,root)

        #move it over a couple of pixels
