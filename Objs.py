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

def dist_3d(pnt1,pnt2):
    return sqrt((pnt1.matrix[0][0]-pnt2.matrix[0][0])**2+(pnt1.matrix[1][0]-pnt2.matrix[1][0])**2+(pnt1.matrix[2][0]-pnt2.matrix[2][0])**2)

def get_color(dist,color):
    #l=200/(dist+100)
    l=150/(dist+25)
    return (min(255,l*color[0]),min(255,l*color[1]),min(255,l*color[2]))

class Point:
    def __init__(self):
        pass

if __name__=='__main__':
   pass