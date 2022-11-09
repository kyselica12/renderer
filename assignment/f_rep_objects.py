import numpy as np
from utils import normalize

from abc import ABC, abstractmethod

class FObject(ABC):

    @abstractmethod
    def point_of_intersection(self, ray_V, P0):
        pass

    @abstractmethod
    def normal_at_point(self, point):
        pass

    
    def bounce_vector_at_point(self, point, light_pos, N):
        # TODO  
        bounce_vector = np.array([])
        return normalize(bounce_vector)



class Sphere(FObject):

    def __init__(self, x, y, z, r, color, ks, kd, ka, a):
        
        self.center = np.array([x,y,z,1])
        self.radius = r

        self.color = color
        self.ks = ks
        self.kd = kd
        self.ka = ka
        self.a = a
    
    def point_of_intersection(self, ray_V, P0):
        # TODO
        p = np.array([])
        
        return p

    
    def normal_at_point(self, point):
        N = normalize(point - self.center[:3])
        return N

        
