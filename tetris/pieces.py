import random
import numpy as np

I = [[0, 0, 0, 0],
     [1, 1, 1, 1],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]
J = [[2, 0, 0],
     [2, 2, 2],
     [0, 0, 0]]
L = [[0, 0, 3],
     [3, 3, 3],
     [0, 0, 0]]
O = [[4, 4],
     [4, 4]]
S = [[0, 5, 5],
     [5, 5, 0],
     [0, 0, 0]]
T = [[0, 6, 0],
     [6, 6, 6],
     [0, 0, 0]]
Z = [[7, 7, 0],
     [0, 7, 7],
     [0, 0, 0]]

SHAPES = {
    'I': I,
    'J': J,
    'L': L,
    'O': O,
    'S': S,
    'T': T,
    'Z': Z,
}

COLOURS = {
    0: (0, 0, 0),
    1: (0, 240, 240),
    2: (0, 0, 240),
    3: (240, 160, 0),
    4: (240, 240, 0),
    5: (0, 240, 0),
    6: (160, 240, 0),
    7: (240, 0, 0),
}

ROTATION_TABLE = {
    'I': I,
    'J': J,
    'L': L,
    'O': O,
    'S': S,
    'T': T,
    'Z': Z,
}

class Piece:

    def __init__(self, shape):
        self.shape = shape
        self.x = 0
        self.y = 0
        self.piece = np.array(SHAPES[shape])
        self.value = self.piece[1, 1]
        self.coords = self._get_initial_coords()

    def rotate(self, k=1):
        self.piece = np.rot90(self.piece, k=k)
        self.coords = self._get_initial_coords()
        self.coords[1] = self.coords[1] + self.x
        self.coords[0] = self.coords[0] + self.y

    def _get_initial_coords(self):
        return list(np.where(self.piece != 0))

    def move(self, x, y):
        self.x += x
        self.y += y
        self.coords[1] = self.coords[1] + x
        self.coords[0] = self.coords[0] + y

    def __repr__(self):
        return self.shape
