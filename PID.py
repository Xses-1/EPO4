from module4 import KITTmodel
import numpy as np

class PID:
    def __init__(self):
        self.angleIntegral = 0
        self.LastAngleError = 0

        self.distIntegral = 0
        self.LastdistError = 0
        

    def CalculateErrors(self, setpointx, setpointy, currx, curry, currentAngle):
        deltaP = np.sqrt((setpointx - currx)**2 + (setpointy - curry)**2)
        if deltaP != 0:
            print(setpointx - currx)
            deltaTheta = np.degrees(np.deg2rad(currentAngle) - np.arctan((setpointy - curry) / (setpointx - currx)))
            print(deltaTheta)
        else:
            return 0.0,0.0

        return deltaP, deltaTheta
    
    def calculateForce(self, deltaP, deltaT):
        Kp = 1.2
        Ki = 0
        Kd = 0

        self.distIntegral += deltaP
        distDiff = (self.LastdistError - deltaP) / deltaT

        self.lastdistError = deltaP

        Force = (Kp * deltaP) + (Ki * self.distIntegral) + (Kd * distDiff)

        return Force
    
    def calculateAngle(self, deltaTheta, deltaT):
        Kp = 1
        Ki = 0
        Kd = 0

        self.angleIntegral += deltaTheta
        angleDiff = (self.LastAngleError - deltaTheta) / deltaT

        self.LastAngleError = deltaTheta

        Angle = (Kp * deltaTheta) + (Ki * self.angleIntegral) + (Kd * angleDiff)

        return Angle
    
    def Update(self, setpointx, setpointy, currx, curry, deltaT):
        deltaP, deltaTheta = self.CalculateErrors(setpointx, setpointy, currx, curry)

        Force = self.calculateForce(deltaP, deltaT)
        Angle = self.calculateAngle(deltaTheta, deltaT)

        return Force, Angle
    
    