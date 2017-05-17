# -*- coding: utf-8 -*-
import pygame
import numpy as np 
import math
from utils import Board
import time
from pygame.locals import *
import pdb
# from level1 import tutorialSequence
from tkinterutils import TKBoard
import Tkinter as tk
from ttk import *
from logicmain import initGameLogic, gameLogic
import sys



if __name__ == '__main__':
    
    try:
        skip1=float(sys.argv[1])
    except:
        skip1=0
    boardlogic=initGameLogic(skip1)

    root = tk.Tk()
    my_gui = TKBoard(root,boardlogic)
    root.style=Style()
    root.configure(background='white')
    root.style.theme_use("classic")
    root.style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
    root.rowconfigure(0,weight=1)
    root.after(0,my_gui.updateDisplays,root)
    root.mainloop()


    
        # run at 20 fps
        # time.sleep(2)
     
    # close the window and quit
    # pygame.quit()

