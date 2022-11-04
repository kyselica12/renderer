import numpy as np
from phong_reflection_model import compute_intensity
from utils import normalize

class Sphere:

    def __init__(self, x, y, z, r, color, ks, kd, a):
        
        self.center = np.array([x,y,z,1])
        self.radius = r

        self.color = color
        self.ks = ks
        self.kd = kd
        self.a = a
    
    def point_of_intersection(self, ray_V, P0):
        a = 1
        b = np.dot(2*ray_V, P0[:3] - self.center[:3])
        c = np.linalg.norm(P0[:3] - self.center[:3])**2 - self.radius**2

        
        D = (b**2 - 4*a*c)
        if D < 0:
            return None
        
        
        t1 = (-b + D**0.5) / (2*a)
        t2 = (-b - D**0.5) / (2*a)

        t = min(t1, t2)

        
        return P0 + ray_V * t

    
    def normal_at_point(self, point):
        N = normalize(point - self.center[:3])
        return N

    
    def bounce_vector_at_point(self, point, light_pos, N):
        # TODO
        R1 = normalize(light_pos[:3] - point)

        Rr = 2*N*(np.dot(R1,N)) - R1

        return normalize(Rr)
        
