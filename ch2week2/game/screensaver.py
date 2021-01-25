import pygame
import random
import math

class Vec2d():
    """
    Class of vectors.  Zero point of vectors - [0,0]
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, obj):
        return Vec2d((self.x + obj.x),(self.y + obj.y))

    def __sub__(self, obj):
        return Vec2d((self.x - obj.x),(self.y - obj.y))

    def __mul__(self, k):
        return Vec2d((self.x * k),(self.y * k))

    def __len__(self):
        return int(math.sqrt(self.x * self.x + self.y * self.y))
    
    def int_pair(self):
        return (int(self.x), int(self.y))

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __eq__(self, obj):
        if (self.x == obj.x) and (self.y == obj.y):
            return True
        else:
            return False

class Polyline():
    pass
