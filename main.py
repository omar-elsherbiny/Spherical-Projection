# Imports
import pygame as pyg
from sys import exit as syexit
from math import sin, cos, radians
from helpers import *

import numpy as np

pyg.init()

# Globals
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BG_COLOR = (20, 20, 20)
SCREEN = pyg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pyg.font.Font(resource_path("Comfortaa-Bold.ttf"), 20)
FONT2 = pyg.font.Font(resource_path("Comfortaa-Bold.ttf"), 13)


class Basis:
    vects = [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])]
    def __init__(self, scale, x, y):
        self.s, self.x, self.y = scale, x, y
    def draw_basis(self, screen, matrix):
        pyg.draw.line(screen, (255, 10, 50), (self.x, self.y), (int((matrix@self.vects[0]*self.s)[0])+self.x, -int((matrix@self.vects[0]*self.s)[1])+self.y), 3)
        pyg.draw.line(screen, (50, 255, 10), (self.x, self.y), (int((matrix@self.vects[1]*self.s)[0])+self.x, -int((matrix@self.vects[1]*self.s)[1])+self.y), 3)
        pyg.draw.line(screen, (10, 50, 255), (self.x, self.y), (int((matrix@self.vects[2]*self.s)[0])+self.x, -int((matrix@self.vects[2]*self.s)[1])+self.y), 3)

# Main
def main():
    clock = pyg.time.Clock()

    light_source = np.array(config['light_source'])
    Ax, Ay, Az = config['init_angles']
    R = config['radius']
    dot_size = config['dot_size']

    basis = Basis(config['basis_scale'], config['basis_offset_x'], config['basis_offset_y'])

    panning = False
    coords = (0, 0)
    prev_coords = (0, 0)

    pnts = []
    for phi in range(0, 360, round(360/config['sphere_density_y'])):
        rY = np.array([[cos(radians(phi)), 0, -sin(radians(phi))],[0, 1, 0], [sin(radians(phi)), 0, cos(radians(phi))]])
        for theta in range(0, 360, round(360/config['sphere_density_xz'])):
            pnts.append(rY@np.array([0, R*sin(radians(theta)), R*cos(radians(theta))]))

    clipping_len = round(len(pnts)*(1-config['z_clipping']))
    print(f'no. of points: {len(pnts)}\nz_clipped: {clipping_len}\nremaining: {len(pnts)-clipping_len}')
    rot_pnts = pnts
    rot = np.ones((3, 3))

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
        else:
            drag_vector = (0, 0)

        SCREEN.fill(BG_COLOR)

        rotX = np.array([[1, 0, 0], [0, cos(radians(Ax+drag_vector[1])), -sin(radians(Ax+drag_vector[1]))],[0, sin(radians(Ax+drag_vector[1])), cos(radians(Ax+drag_vector[1]))]])
        rotY = np.array([[cos(radians(Ay-drag_vector[0])), 0, -sin(radians(Ay-drag_vector[0]))],[0, 1, 0], [sin(radians(Ay-drag_vector[0])), 0, cos(radians(Ay-drag_vector[0]))]])
        rotZ = np.array([[cos(radians(Az)), -sin(radians(Az)), 0],[sin(radians(Az)), cos(radians(Az)), 0], [0, 0, 1]])
        nrot = rotX@rotY@rotZ

        if np.any(nrot != rot):
            rot = nrot
            rot_pnts = list(map(lambda x: rot@x, pnts))
            rot_pnts.sort(key=lambda x: x[2])
            rot_pnts = np.array(rot_pnts[clipping_len:])

        for pnt in rot_pnts:
            dist = np.linalg.norm(pnt - light_source)
            pyg.draw.circle(SCREEN, get_color(dist, (220, 220, 220)), (int(pnt[0]+250), int(-pnt[1]+250)), dot_size)

        basis.draw_basis(SCREEN, rot)

        clock.tick(120)
        pyg.display.set_caption(f'Spherical Projection--{int(clock.get_fps())}')
        pyg.display.update()


if __name__ == '__main__':
    main()
