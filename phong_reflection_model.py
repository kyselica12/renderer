import numpy as np




def compute_intensity(color, ks, kd, a, L, N, R, V, I):
    '''
    color - base color of an object
    ks - specular reflection constant
    kd - diffuse reflection constant
    a - shininess constant
    L - the direction vector from the point on the surface toward each light source 
    N - the normal at this point on the surface
    R - the direction that a perfectly reflected ray of light would take from this point on the surface
    V - the direction pointing towards the viewer
    '''
    specular = ks * max(0, np.dot(R, V))**a
    diffuse = kd * max(0, np.dot(N, L))

    return  I * (specular + diffuse)
