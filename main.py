#Imports
import pygame as pyg
from sys import exit as syexit
from math import sin, cos, radians
from MatrixObj import Matrix, identity3, Basis
from Objs import *

pyg.init()

#Globals
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BG_COLOR=(20,20,20)
SCREEN = pyg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pyg.font.Font(resource_path("Comfortaa-Bold.ttf"), 20)
FONT2 = pyg.font.Font(resource_path("Comfortaa-Bold.ttf"), 13)

#Main
def main():
    clock = pyg.time.Clock()

    Ax,Ay,Az=config['init_angles']
    panning=False
    coords=(0,0)
    prev_coords=(0,0)

    #MAIN LOOP
    run = True
    while run:
        coords=pyg.mouse.get_pos()
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                syexit()
            elif event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    panning=True
                    prev_coords=event.pos
            elif event.type == pyg.MOUSEBUTTONUP:
                if event.button == 1:
                    panning=False
                    Ax+=drag_vector[1]
                    Ay-=drag_vector[0]
            
        if panning:
            drag_vector=[max(-360,min(360,(coords[0]-prev_coords[0])/2)),max(-360,min(360,(coords[1]-prev_coords[1])/2))]
            Ax=Ax%360
            if Ax>90 and Ax<270: drag_vector[0]*=-1
        else:
            drag_vector=(0,0)

        rotX=Matrix('3x3',[[1,0,0],[0,cos(radians(Ax+drag_vector[1])),-sin(radians(Ax+drag_vector[1]))],[0,sin(radians(Ax+drag_vector[1])),cos(radians(Ax+drag_vector[1]))]])
        rotY=Matrix('3x3',[[cos(radians(Ay-drag_vector[0])),0,-sin(radians(Ay-drag_vector[0]))],[0,1,0],[sin(radians(Ay-drag_vector[0])),0,cos(radians(Ay-drag_vector[0]))]])
        rotZ=Matrix('3x3',[[cos(radians(Az)),-sin(radians(Az)),0],[sin(radians(Az)),cos(radians(Az)),0],[0,0,1]])
        rot=rotX@rotY@rotZ

        SCREEN.fill(BG_COLOR)

        Basis.draw_basis(Basis,SCREEN,rot,100,250,250)

        clock.tick(120)
        pyg.display.set_caption(f'Spherical Projection--{int(clock.get_fps())}')
        pyg.display.update()

if __name__=='__main__':
    main()