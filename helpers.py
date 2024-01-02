import json
from math import sin, cos, radians, sqrt
import pygame as pyg
import sys
import os
import numpy as np


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


f = open(resource_path('config.json'), 'r')
config = json.load(f)
f.close()


def get_color(dist, color):
    # l=200/(dist+100)
    l = 150/(dist+25)
    return (min(255, l*color[0]), min(255, l*color[1]), min(255, l*color[2]))

class Basis:
    vects = [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])]
    def __init__(self, scale, x, y):
        self.s, self.x, self.y = scale, x, y
    def draw_basis(self, screen, matrix):
        pyg.draw.line(screen, (255, 10, 50), (self.x, self.y), (int((matrix@self.vects[0]*self.s)[0])+self.x, -int((matrix@self.vects[0]*self.s)[1])+self.y), 3)
        pyg.draw.line(screen, (50, 255, 10), (self.x, self.y), (int((matrix@self.vects[1]*self.s)[0])+self.x, -int((matrix@self.vects[1]*self.s)[1])+self.y), 3)
        pyg.draw.line(screen, (10, 50, 255), (self.x, self.y), (int((matrix@self.vects[2]*self.s)[0])+self.x, -int((matrix@self.vects[2]*self.s)[1])+self.y), 3)

class Node():
    def __init__(self, pos, color=(220, 220, 220)):
        self.pos = np.array(pos)
        self.color = color

    def __matmul__(self, other):
        if isinstance(other, np.ndarray):
            new_pos = other @ self.pos
            return Node(new_pos, color=self.color)
        else:
            raise ValueError("Unsupported operation. Matrix multiplication is only supported with NumPy arrays.")
    
    def __sub__(self, other):
        if isinstance(other, np.ndarray):
            return self.pos - other
        else:
            raise TypeError("Unsupported operand type for subtraction")

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.pos[index]
        else:
            raise TypeError("Index must be an integer")


if __name__ == '__main__':
    a = np.array([1, 2, 3])
    b = Node([3, 2, 1], color=(220, 0, 0))
    print(b@a)
