import numpy as np

RED = np.array([255,10,10])
GREEN = np.array([10,255,10])
BLUE = np.array([1,1,255])

WHITE = np.array([255,255,255])
BLACK = np.array([0,0,0])

def normalize(v):
    return v / np.linalg.norm(v)