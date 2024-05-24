import numpy as np
import time
import matplotlib.pyplot as plt
import control as ct
import control.matlab as matlab

class KITTmodel():
    def __init__(self):
        self.velocity_state_vector = np.array([[0.0],[0.0],[0.0]]) ## Z,v,a
        self.position_state_vector = np.array([[0.0],[0.0]])       ## x,y
        self.theta = 0


    def velocity_state(self, F_m, dt):
        b = 5
        m = 5.6

        A = np.array([[0, 1, 0],[0, -b/m, 0], [0, 0, -b/m]])
        B = np.array([[0], [1/m], [0]])
        C = np.array([0, 1, 0])

        dA = np.matmul(A, self.velocity_state_vector)
        dB = B * F_m
        dX = dA + dB

        self.velocity_state_vector += (dX * dt)
        v = self.velocity_state_vector[1][0] ## Basically np.dot(velocity_state_vector, C) but faster
        print(v)
        return(v)

    def steering_state(self, phi, v):
        L = 0.335 #m            ## L is a constant and should just be stored internally
        sin = np.sin(phi)

        if sin == 0:            ## avoid divide by 0 error
            return 0
        
        R = L/sin

        d_theta = (v/R) # differential orientation

        return d_theta
    
    def position_state(self, v, theta, dt):
                                                     ## Rotate unitvector method
        #cos = np.cos(theta)
        #sin = np.sin(theta)                  
        ##rotationVector = np.array([[cos , -sin],
        ##                            [sin , cos]])
        ##unitVector = np.array([[1],[0]])
        ##
        ##directionVector = np.matmul(unitVector, rotationVector)

                                                ## intrinsic unit vector method
        directionVector = np.array([[np.cos(theta)],
                                   [np.sin(theta)]])
                                

        self.position_state_vector += (directionVector * v * dt)
        
        return self.position_state_vector
    
    def return_Theta(self, phi, v, dt):
        self.theta += (self.steering_state(phi, v) * dt)
        return self.theta
    
    def update(self, phi, F_m, dt):
        v = self.velocity_state(F_m,dt)

        Theta = self.return_Theta(phi, v, dt)
        
        self.position_state(v, Theta, dt)

        return self.position_state_vector

