import numpy as np
import matplotlib.pyplot as plt

# from GUI import GUI, EventTypes
from utils import *
from f_rep_objects import Sphere, FObject

class Main:

    def __init__(self, size=501):

        self.object = Sphere(0, 0, 0, 50, RED, 0.5, 0.5, .05, 10)

        self.light_pos = np.array([0,8000,0])
        self.light_intensity = 0.1

        self.camera_pos = np.array([0,0,-1000])
        self.camera_sensor_pos = np.array([0,0, -100])
        self.camera_sensor_size = 300

        self.size = size

        self.image = np.zeros((size, size, 3))


    def render(self):
        image = self.ray_tracing()
        plt.imshow(image)
        plt.show()


    def phong_reflection_model(self, o: FObject, p, ray, visible):
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
        if p == None:
            return 0

        # TODO
        ka = o.ka
        kd = o.kd
        ks = o.ks
        alpha = o.a

        I = self.light_intensity

        N = o.normal_at_point(p)
        L = None # self.light_pos
        V = None
        R = None
        
        specular = ka * I
        diffuse = I * kd * ...
        ambient = I * ka * ...
        
        return self.light_intensity * (ambient + diffuse + specular) 

    def get_color(self, ray):        
        o = self.object
        p = o.point_of_intersection(ray, self.camera_pos)

        intensity = self.phong_reflection_model(o, p, ray)

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

                # TODO
                ray = np.array([0,0])

                # Compute color of the pixel
                color = self.get_color(ray)                
                
                if color is not None:
                    image[r, c] = color
                
            
        return image


if __name__ == "__main__":
    m = Main(501)

    m.render()
