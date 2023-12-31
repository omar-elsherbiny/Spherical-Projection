# Imports
import pygame as pyg
from sys import exit as syexit
from math import sin, cos, radians
from MatrixObj import Matrix, identity3, Basis
from Objs import *

pyg.init()

# Globals
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BG_COLOR = (20, 20, 20)
SCREEN = pyg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pyg.font.Font(resource_path("Comfortaa-Bold.ttf"), 20)
FONT2 = pyg.font.Font(resource_path("Comfortaa-Bold.ttf"), 13)

# Main


def main():
    clock = pyg.time.Clock()

    light_source = Matrix('3x1',[[0],[50],[200]])
    Ax, Ay, Az = config['init_angles']
    R = config['radius']

    panning = False
    coords = (0, 0)
    prev_coords = (0, 0)

    pnts = []
    for phi in range(0,360,8):
        rY=Matrix('3x3',[[cos(radians(phi)),0,-sin(radians(phi))],[0,1,0],[sin(radians(phi)),0,cos(radians(phi))]])
        for theta in range(0,360,8):
            pnts.append(rY@Matrix('3x1',[[0],[R*sin(radians(theta))],[R*cos(radians(theta))]]))

    clipping_len = round(len(pnts)*(1-config['z_clipping']))
    rot_pnts = pnts
    rot = identity3

    # MAIN LOOP
    run = True
    while run:
        coords = pyg.mouse.get_pos()
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                syexit()
            elif event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    panning = True
                    prev_coords = event.pos
            elif event.type == pyg.MOUSEBUTTONUP:
                if event.button == 1:
                    panning = False
                    Ax += drag_vector[1]
                    Ay -= drag_vector[0]

        if panning:
            drag_vector = [max(-360, min(360, (coords[0]-prev_coords[0])/2)),
                           max(-360, min(360, (coords[1]-prev_coords[1])/2))]
            Ax = Ax % 360
            if Ax > 90 and Ax < 270:
                drag_vector[0] *= -1
        else: drag_vector = (0, 0)

        rotX = Matrix('3x3', [[1,0,0], [0,cos(radians(Ax+drag_vector[1])),-sin(radians(Ax+drag_vector[1]))], [0,sin(radians(Ax+drag_vector[1])),cos(radians(Ax+drag_vector[1]))]])
        rotY = Matrix('3x3', [[cos(radians(Ay-drag_vector[0])),0,-sin(radians(Ay-drag_vector[0]))], [0,1,0], [sin(radians(Ay-drag_vector[0])),0,cos(radians(Ay-drag_vector[0]))]])
        rotZ = Matrix('3x3', [[cos(radians(Az)),-sin(radians(Az)),0],[sin(radians(Az)),cos(radians(Az)),0], [0,0,1]])
        nrot = rotX@rotY@rotZ


        if nrot != rot:
            rot = nrot
            rot_pnts = list(map(lambda x: rot@x, pnts))
            rot_pnts.sort(key=lambda x: x.matrix[2][0])
            rot_pnts = rot_pnts[clipping_len:]

        SCREEN.fill(BG_COLOR)

        for pnt in rot_pnts:
            dist=dist_3d(pnt,light_source)
            pyg.draw.circle(SCREEN,get_color(dist,(220,220,220)),(int(pnt.matrix[0][0]+250),int(-pnt.matrix[1][0]+250)),6)

        Basis.draw_basis(Basis, SCREEN, rot, 70, 420, 420)

        clock.tick(120)
        pyg.display.set_caption(f'Spherical Projection--{int(clock.get_fps())}')
        pyg.display.update()


if __name__ == '__main__':
    main()
