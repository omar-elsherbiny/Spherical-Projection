import json
from math import sin, cos, radians, sqrt
from MatrixObj import Matrix, identity3
import pygame as pyg
import sys
import os

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

f=open(resource_path('config.json'),'r')
config=json.load(f)
f.close()

#import config

def dist_3d_mp(pntm,pntp):
    return sqrt((pntm.matrix[0][0]-pntp[0])**2+(pntm.matrix[1][0]-pntp[1])**2+(pntm.matrix[2][0]-pntp[2])**2)
def dist_2d_mp(pntm,pntp):
    return sqrt((pntm.matrix[0][0]-pntp[0])**2+(pntm.matrix[1][0]-pntp[1])**2)

def get_color(dist,color):
    l=200/(dist+100)
    return (min(255,l*color[0]),min(255,l*color[1]),min(255,l*color[2]))



if __name__=='__main__':
   pass