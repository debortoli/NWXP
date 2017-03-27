# -*- coding: utf-8 -*-
import pygame
import numpy as np 
import math
from utils import Board
import time
from pygame.locals import *
import pdb
from level1 import tutorialSequence



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

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if(board.updateQueue[0].buttonClicked=True)
            #         board.updateQueue[0].buttonClicked=True

            elif event.type==VIDEORESIZE:
                board.screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                # pdb.set_trace()
                thing=pygame.transform.scale(board.screen,event.dict['size'])
                board.levelCompleteSurface=pygame.transform.scale(board.levelCompleteSurface,(event.dict['size'][0]/3,event.dict['size'][0]/5))
                
                board.resizeSurfaces(event.dict['size'])
                # board.screen.blit(thing,(0,0))
                # board.levelCompleteSurface.fill([224,224,224])


                pygame.display.flip()


        
        # write draw code here

        board.blitSurfaces()
        if(board.level==0):
            tutorialSequence(board)

        # display what’s drawn. this might change.
        pygame.display.update()
        # run at 20 fps
        board.clock.tick(20)
        # time.sleep(2)
     
    # close the window and quit
    pygame.quit()

