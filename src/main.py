# -*- coding: utf-8 -*-
import pygame
import numpy as np 
import math
from utils import Board
import time



if __name__ == '__main__':
    
    board=Board()
    # Loop until the user clicks close button
    done = False
    board.clock.tick()
    while done == False:
        print int(pygame.time.get_ticks()/1000.)
        if(int(pygame.time.get_ticks()/1000.)%10==0 and 
            (pygame.time.get_ticks()/1000.)>1):
            board.year+=1
            print "here"
        # write event handlers here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print "button clicked"
                # print event.pos
                for icon in board.dnd:
                    if icon.rect.collidepoint(event.pos):

                        board.update_text+="item is being dragged"+'\n'
                        # print "clicked on icon"
                        
                        icon.click = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for icon in board.dnd:
                    icon.click = False
        # write game logic here
        # if(board.year%10==0 and board.year>0):
        #     board.update_text+="Another 10 years have passed.\n"

        
        board.staticItemsUpdate()
        board.textUpdate()
        board.draggablesUpdate()
        board.checkPowerLineAge()
        
        # write draw code here
     
        # display what’s drawn. this might change.
        pygame.display.update()
        # run at 20 fps
        board.clock.tick(20)
        # time.sleep(2)
     
    # close the window and quit
    pygame.quit()

