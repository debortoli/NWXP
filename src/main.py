# -*- coding: utf-8 -*-
import pygame
import numpy as np 
import math
from utils import Board
import time
from pygame.locals import *
import pdb



if __name__ == '__main__':
    
    board=Board()
    done = False
    board.clock.tick()
    while done == False:
        # print int(pygame.time.get_ticks()/1000.)
        if(int(pygame.time.get_ticks()/1000.)%10==0 and 
            (pygame.time.get_ticks()/1000.)>1):
            board.year+=1
            # board.progress+=0.1

        # write event handlers here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


        
        # write draw code here

        board.blitSurfaces()
        # board.updateLevelSurface(board.progress)

        # display what’s drawn. this might change.
        pygame.display.update()
        # run at 20 fps
        board.clock.tick(20)
        # time.sleep(2)
     
    # close the window and quit
    pygame.quit()

