import numpy as np
import time
import matplotlib.pyplot as plt
import control as ct
import control.matlab as matlab

class KITTmodel():
    def velocity_state():
        b = 5
        m = 5.6

        A = np.array([[0, 1, 0],[0, -b/m, 0], [0, 0, -b/m]])
        B = np.array([[0], [1/m], [0]])
        C = np.array([0, 1, 0])

        vel = ct.ss(A, B, C, 0)
        print(vel)
        return(vel)

    def steering_state(L, phi, v, self):
        R = L/np.sin(phi)

        current_time = time.perf_counter()

        if self.prev_time is None:
            self.prev_time = current_time
            return
        
        dt = current_time - self.prev_time


        d_theta = (v/R)*dt # differential orientation

        return d_theta
    
    def update(self):
        self.steering_state()

