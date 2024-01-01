import json
from math import sin, cos, radians, sqrt
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

def get_color(dist,color):
    #l=200/(dist+100)
    l=150/(dist+25)
    return (min(255,l*color[0]),min(255,l*color[1]),min(255,l*color[2]))

if __name__=='__main__':
   pass