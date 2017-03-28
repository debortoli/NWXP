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



if __name__ == '__main__':
    
    board=Board()

    root = tk.Tk()
    my_gui = TKBoard(root,board)
    root.style=Style()
    root.configure(background='white')
    root.style.theme_use("clam")
    root.rowconfigure(0,weight=1)
    root.mainloop()


    
        # run at 20 fps
    board.clock.tick(20)
        # time.sleep(2)
     
    # close the window and quit
    # pygame.quit()

