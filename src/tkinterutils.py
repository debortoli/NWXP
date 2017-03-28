# from Tkinter import Tk, Label, Button,Canvas,Frame
import Tkinter as tk
import pdb
import time

class TKBoard:
    def __init__(self, master,boardlogic):
        self.master = master
        master.title("GRID SIMULATOR")




        #create update frame which contains 3 widgets
        self.updateFrame= tk.Frame(master)
        self.updateFrame.pack(side="right",fill="y")
        # self.updateFrame.bind("<Configure>", self.on_resize)
        

        
        self.levelCanvas = tk.Canvas(self.updateFrame,bg="lightgray",highlightthickness=2,highlightbackground="Black",height=100)
        self.levelCanvas.create_text(200,10,fill='black',font="Times 20 italic bold",
                        text="Level Progress")
        self.levelCanvas.pack()#grid(row=0,column=0,sticky='N')
        
        # self.levelTitle=tk.Label(self.levelCanvas,text="LEVEL PROGRESS")
        # self.levelTitle.pack(side='bottom')

        self.pointsCanvas = tk.Canvas(self.updateFrame,bg="lightgray",highlightthickness=2,highlightbackground="Black",height=100)
        self.pointsCanvas.pack()#grid(row=1,column=0,sticky='N')

        self.draggablesCanvas = tk.Canvas(self.updateFrame,bg="lightgray",highlightthickness=2,highlightbackground="Black",height=500)
        self.draggablesCanvas.pack()#grid(row=2,column=0,sticky='NS')


        self.updateFrame.rowconfigure(0,weight=5)
        self.updateFrame.rowconfigure(1,weight=5)
        self.updateFrame.rowconfigure(2,weight=1)




    def greet(self):
        print(self.levelCanvas.winfo_width())
        self.levelCanvas.create_rectangle(0,0,self.levelCanvas.winfo_width(),self.levelCanvas.winfo_height(),width=10)

