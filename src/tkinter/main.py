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



if __name__ == '__main__':
    
    board=Board()

    root = tk.Tk()
    my_gui = TKBoard(root,board)
    root.mainloop()

    
        # run at 20 fps
    board.clock.tick(20)
        # time.sleep(2)
     
    # close the window and quit
    pygame.quit()

