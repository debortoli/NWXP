# -*- coding: utf-8 -*-
import pygame
import numpy as np 
import math
from utils import Board,textUpdate,backgroundUpdate
 






if __name__ == '__main__':
    
    board=Board()
    # Loop until the user clicks close button
    done = False
    while done == False:
        
        # write event handlers here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        # write game logic here
     
        
        backgroundUpdate(board)
        textUpdate(board,"text to display")
        
        # write draw code here
     
        # display what’s drawn. this might change.
        pygame.display.update()
        # run at 20 fps
        board.clock.tick(20)
     
    # close the window and quit
    pygame.quit()

