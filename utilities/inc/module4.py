import numpy as np
import time
import matplotlib.pyplot as plt
import control as ct
import control.matlab as matlab

class KITTmodel():
    def __init__(self): ## Should probably input the starting position and shit
        self.velocity_state_vector = np.array([[0.0],[0.0],[0.0]]) ## Z,v,a
        self.position_state_vector = np.array([[0.0],[0.0]])       ## x,y
        self.theta = 90.0

        self.maxPhi = 30
        self.maxForce = 7.16


    def velocity_state(self, F_m, dt):
        b = 4.15
        m = 5.6

        A = np.array([[0, 1, 0],[0, -b/m, 0], [0, 0, -b/m]])
        B = np.array([[0], [1/m], [0]])
        #C = np.array([0, 1, 0])

        dX = (np.matmul(A, self.velocity_state_vector)) + (B * F_m)

        self.velocity_state_vector += (dX * dt)
        v = self.velocity_state_vector[1][0] ## Basically np.dot(velocity_state_vector, C) but faster
        return(v)

    def steering_state(self, phi, v):
        L = 0.335 #m            ## L is a constant and should just be stored internally
        sin = np.tan(np.deg2rad(phi))

        if sin == 0:            ## avoid divide by 0 error
            return 0
        
        R = L/sin

        d_theta = (v/R) # differential orientation

        with open('test.txt', 'a') as f:
            f.write(f' delta Theta = {d_theta}')

        return np.degrees(d_theta)
    
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

        with open('test.txt', 'a') as f:
            f.write(f' theta = {theta}')
        print(theta)
        directionVector = np.array([[np.cos(np.deg2rad(theta))],
                                   [np.sin(np.deg2rad(theta))]])
        print(directionVector)
        self.position_state_vector += (directionVector * v * dt)
        
        return self.position_state_vector
    
    def return_Theta(self, phi, v, dt):
        self.theta += (self.steering_state(phi, v) * dt)
        if self.theta >= 360:
            self.theta -= 360
        return self.theta
    
    def update(self, phi, F_m, dt):

        if abs(phi) > self.maxPhi:
            phi = np.sign(phi) * self.maxPhi

        if abs(F_m) > self.maxForce:
            F_m = np.sign(F_m) * self.maxForce

        v = self.velocity_state(F_m,dt)

        Theta = self.return_Theta(phi, v, dt)
        
        self.position_state(v, Theta, dt)

        with open('test.txt', 'a') as f:
            f.write(f'\n \n')

        return self.position_state_vector, Theta

