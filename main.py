import numpy as np
import matplotlib.pyplot as plt

# from GUI import GUI, EventTypes
from utils import normalize
from sphere import Sphere
from colors import *
from phong_reflection_model import compute_intensity

class Main:

    def __init__(self, size=501):

        # self.gui = GUI(width=size, height=size)

        self.objects = []

        self.light_pos = np.array([0,8000,0,1])
        self.light_intensity = 0.1

        self.camera_pos = np.array([0,0,-1000])
        self.camera_sensor_pos = np.array([0,0, -100])
        self.camera_sensor_size = 300

        self.size = size

        self.image = np.zeros((size, size, 3))

    def add_object(self, object):
        self.objects.append(object)

    def run(self):
        image = self.ray_tracing()
        plt.imshow(image)
        plt.show()
        # self.gui.draw(image)

        # for event, axis, value in self.gui.loop():

        #     if event == EventTypes.rotation:
        #         ...
        #     elif event == EventTypes.translation:
        #         ...
        #     elif event == EventTypes.light:
        #         ...
        #     elif event == EventTypes.cmd:
        #         ...

        #     # self.gui.draw(self.image)

    def get_color(self, ray):        
        # return self.color
        winner = None, np.inf, None
        for i, o in enumerate(self.objects):
            p = o.point_of_intersection(ray, self.camera_pos)
            if p is None:
                continue
            d = np.linalg.norm(p - self.camera_pos)

            if d < winner[1]:
                winner = i, d, p

            
        if winner[0] is None:
            return None

        i, _, p = winner
        o = self.objects[i]

        L = normalize(self.light_pos[:3] - p)
        light_distance = np.linalg.norm(self.light_pos[:3] - p)
        for j, o2 in enumerate(self.objects):
            if j == i:
                continue 
            p2 = o2.point_of_intersection(L, p)
            
            if p2 is not None:
                light_distance2 = np.linalg.norm(self.light_pos[:3] - p2)
                if light_distance2 < light_distance:
                    return BLACK

        
        N = o.normal_at_point(p)
        R = o.bounce_vector_at_point(p ,self.light_pos, N)
        V = normalize(self.camera_pos[:3] - p)

        intensity = compute_intensity(o.color, o.ks,o.kd, o.a, 
                                      L, N, R, V, 
                                      self.light_intensity) 

        color = o.color * intensity
        color[color < 0] = 0
        # print(max(color))
        color[color > 255] = 255

        return color

    def ray_tracing(self):
        image = np.ones((self.size, self.size, 3)) * 255     
        pixel_size = self.camera_sensor_size / self.size
        center = self.size / 2
        for r in range(self.size):
            for c in range(self.size):
                x = (r - center + 1 / 2) *pixel_size
                y = - (c - center + 1 / 2) *pixel_size
                z = self.camera_sensor_pos[2]
                pixel_pos = np.array([x, y, z])
                # TDOO compute ray
                ray = normalize(pixel_pos - self.camera_pos)

                # Compute color of the pixel
                color = self.get_color(ray)                
                
                if color is not None:
                    image[r, c] = color
                
            
        return image




m = Main(501)
s = Sphere(0, 0, 0, 50, RED, 0.5, 0.5, 1)
s2 = Sphere(50, 100, 0, 50, GREEN, 0.5, 0.5, 1)
m.add_object(s)
m.add_object(s2)


m.run()
