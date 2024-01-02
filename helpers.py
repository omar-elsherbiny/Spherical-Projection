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


def range_lerp(a_end, b_end, val, a_start=0, b_start=0):
    t = (val-a_start)/(a_end-a_start)
    return (1-t)*b_start + t*b_end


class Basis:
    vects = [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])]

    def __init__(self, scale, x, y):
        self.s, self.x, self.y = scale, x, y

    def draw_basis(self, screen, matrix):
        pyg.draw.line(screen, (255, 10, 50), (self.x, self.y), (int((matrix@self.vects[0]*self.s)[0])+self.x, -int((matrix@self.vects[0]*self.s)[1])+self.y), 3)
        pyg.draw.line(screen, (50, 255, 10), (self.x, self.y), (int((matrix@self.vects[1]*self.s)[0])+self.x, -int((matrix@self.vects[1]*self.s)[1])+self.y), 3)
        pyg.draw.line(screen, (10, 50, 255), (self.x, self.y), (int((matrix@self.vects[2]*self.s)[0])+self.x, -int((matrix@self.vects[2]*self.s)[1])+self.y), 3)


class Node():
    def __init__(self, pos, color=(0,0,0)):
        self.pos = np.array(pos)
        self.color = color

    def __matmul__(self, other):
        if isinstance(other, np.ndarray):
            new_pos = other @ self.pos
            return Node(new_pos, color=self.color)
        else:
            raise ValueError(
                "Unsupported operation. Matrix multiplication is only supported with NumPy arrays.")

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


class SphereImage:
    def __init__(self, filename, res):
        with open('maps/'+filename+'.txt', 'r') as f:
            self.filename = filename
            data = f.read().replace('\n', '').split(';')[:-1]
            self.res = (int(data[0]), int(data[1]))
            if res != self.res:
                raise ValueError("Given res does not match map res")

            self.color_map = {k: tuple(map(int, v[1:-1].split(','))) for k, v in [i.split(':') for i in data[3:3+int(data[2])]]}
            self.map = list(map(list, data[3+int(data[2]):]))[::-1]
            if len(self.map) != int(self.res[0]/2) or len(self.map[0]) != self.res[1]*2:
                raise ValueError("Given res does not match actual file res")

    def get_color(self, c, r):
        c = self.map[r][c]
        if c in self.color_map:
            return self.color_map[c]
        return (0,0,0)


if __name__ == '__main__':
    p = SphereImage('temp',(config['sphere_density_xz'],config['sphere_density_y']))
    print(p.map)
