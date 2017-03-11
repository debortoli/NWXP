# -*- coding: utf-8 -*-
import pygame
import numpy as np 
import math
from utils import Board,textUpdate,backgroundUpdate,draggablesUpdate



if __name__ == '__main__':
    
    board=Board()
    # Loop until the user clicks close button
    done = False
    while done == False:
        
        # write event handlers here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print "button clicked"
                for icon in board.dnd:
                    if icon.rect.collidepoint(event.pos):
                        board.update_text+="item is being dragged"+'\n'
                        # print "clicked on icon"
                        
                        icon.click = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for icon in board.dnd:
                    icon.click = False
        # write game logic here
     
        
        backgroundUpdate(board)
        textUpdate(board,board.update_text)
        draggablesUpdate(board)
        
        # write draw code here
     
        # display what’s drawn. this might change.
        pygame.display.update()
        # run at 20 fps
        board.clock.tick(20)
     
    # close the window and quit
    pygame.quit()

