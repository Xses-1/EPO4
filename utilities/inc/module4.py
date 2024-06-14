import numpy as np

class KITTmodel():
    def __init__(self): ## Should probably input the starting position and shit
        self.velocity = 0
        self.accelleration = 0
        self.position_state_vector = np.array([[0.0],[0.0]])       ## x,y
        self.theta = np.pi/2

        self.maxPhi = 0.523599
        self.maxForce = 7.16


    def velocity_state(self, F_m, dt):
        #b = 4.15
        b = 4.15
        m = 5.6

        self.accelleration =  (F_m - (b * self.velocity))/m
        self.velocity += self.accelleration * dt

        return self.velocity

    def steering_state(self, phi, v):
        '''
            Takes in steering angle in radians and velocity in m/s

            return the differential of the steering angle
        '''
        L = 0.335 #m            ## L is a constant and should just be stored internally
        sin = np.tan(phi)

        if sin == 0:            ## avoid divide by 0 error
            return 0
        
        R = L/sin

        d_theta = (v/R) # differential orientation

        return d_theta
    
    def position_state(self, v, dt):
                                                     ## Rotate unitvector method
        #cos = np.cos(theta)
        #sin = np.sin(theta)                  
        ##rotationVector = np.array([[cos , -sin],
        ##                            [sin , cos]])
        ##unitVector = np.array([[1],[0]])
        ##
        ##directionVector = np.matmul(unitVector, rotationVector)

                                                ## intrinsic unit vector method
                                                
        directionVector = np.array([[np.cos(self.theta)],
                                   [np.sin(self.theta)]])
        
        self.position_state_vector += (directionVector * v * dt)
        
        return self.position_state_vector
    
    def update_Theta(self, phi, v, dt):
        self.theta += (self.steering_state(phi, v) * dt)
        if self.theta >= np.pi:
            self.theta -= 2 * np.pi
        return self.theta
    
    def update(self, phi, F_m, dt):

        if abs(phi) > self.maxPhi:
            phi = np.sign(phi) * self.maxPhi

        if abs(F_m) > self.maxForce:
            F_m = np.sign(F_m) * self.maxForce

        v = self.velocity_state(F_m,dt)

        self.update_Theta(phi, v, dt)
        
        self.position_state(v, dt)

        return self.position_state_vector, self.theta

