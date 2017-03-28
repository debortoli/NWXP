# from Tkinter import Tk, Label, Button,Canvas,Frame
import Tkinter as tk
import pdb
import time
import ttk

class TKBoard:
    def __init__(self, master,boardlogic):
        self.master = master
        master.title("GRID SIMULATOR")


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

        self.points = tk.Label(self.pointsCanvas,bg='lightgray',text=str(boardlogic.level),font=("Helvetica", 25),fg="green")
        self.points.pack(side='top',pady=10)

        #draggables canvas
        self.draggablesCanvas = tk.Canvas(self.updateFrame,bg="lightgray",highlightthickness=2,highlightbackground="Black",height=500)
        self.draggablesCanvas.pack()#grid(row=2,column=0,sticky='NS')

        #for resizing
        self.updateFrame.rowconfigure(0,weight=5)
        self.updateFrame.rowconfigure(1,weight=5)
        self.updateFrame.rowconfigure(2,weight=1)

        # self.butt=tk.Button(master,command=lambda: self.greet(boardlogic))
        # self.butt.pack()



    def updateDisplays(self):
        self.progress["value"]=self.boardlogic.progress
        self.points['text']=self.boardlogic.totalPoints

