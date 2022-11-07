import numpy as np
import matplotlib.pyplot as plt

# from GUI import GUI, EventTypes
from utils import *
from f_rep_objects import Sphere

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

    def get_closest_object(self, ray):
        winner = {"obj": None, "distance": np.inf, "point": None}
        for o in self.objects:
            p = o.point_of_intersection(ray, self.camera_pos)
            if p is None:
                continue
            d = np.linalg.norm(p - self.camera_pos)

            if d < winner["distance"]:
                winner["obj"] = o
                winner["distance"] = d
                winner["point"] = p

        return winner["obj"], winner["point"]

    def is_visible(self, obj, p):
        light_distance = np.linalg.norm(self.light_pos[:3] - p)
        light_direction = normalize(self.light_pos[:3] - p)
        
        for o2 in self.objects:
            if o2 == obj:
                continue 
            
            p2 = o2.point_of_intersection(light_direction, p)
            
            if p2 is not None:
                light_distance2 = np.linalg.norm(self.light_pos[:3] - p2)
                
                if light_distance2 < light_distance:
                    return False
        
        return True

    def phong_reflection_model(self, o, p, ray, visible):
        '''
        ka - ambient reflection constant
        ks - specular reflection constant
        kd - diffuse reflection constant
        a - shininess constant
        L - the direction vector from the point on the surface toward each light source 
        N - the normal at this point on the surface
        R - the direction that a perfectly reflected ray of light would take from this point on the surface
        V - the direction pointing towards the viewer
        '''

        ambient = o.ka * self.light_intensity

        if visible:
            L = normalize(self.light_pos[:3] - p)
            N = o.normal_at_point(p)
            R = o.bounce_vector_at_point(p ,self.light_pos, N)
            V = -ray

            specular = o.ks * max(0, np.dot(R, V))**o.a
            diffuse = o.kd * max(0, np.dot(N, L))
        else:
            specular = 0
            diffuse = 0

        return self.light_intensity * (ambient + diffuse + specular) 

    def get_color(self, ray):        
        o, p = self.get_closest_object(ray)

        if o is None:
            return None

        visible = self.is_visible(o, p)

        intensity = self.phong_reflection_model(o, p, ray, visible)

        color = o.color * intensity
        color[color < 0] = 0
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


if __name__ == "__main__":
    m = Main(501)
    s = Sphere(0, 0, 0, 50, RED, 0.5, 0.5, 0.05, 1)
    s2 = Sphere(50, 100, 0, 50, GREEN, 0.5, 0.5, 0.05, 1)
    m.add_object(s)
    m.add_object(s2)


m = Main(201)
s = Sphere(0, 0, 0, 50, RED, 0.5, 0.5, .05, 10)
s2 = Sphere(50, 100, 0, 50, GREEN, 0.5, 0.5, .05, 10)
m.add_object(s)
m.add_object(s2)


m.run()
