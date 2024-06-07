from module4 import KITTmodel
import numpy as np

class PID:
    def __init__(self):
        self.angleIntegral = 0
        self.LastAngleError = 0

        self.distIntegral = 0
        self.LastdistError = 0

        self.maxForce = 7.16
        self.maxAngle = 30
        
        self.ForceList  = [7.16,4.06,0.49,0,-1,47,-3.38,-7.16]
        self.PWMList    = [165,160,156,150,145,140,135]

        self.ForceKp = 2
        self.ForceKi = 0
        self.ForceKd = 0

        self.AngleKp = 1
        self.AngleKi = 0
        self.AngleKd = 0
        
        
        ## test values
        self.angle = 0


    def CalculateErrors(self, setpointx, setpointy, currx, curry, currentAngle):
        x = setpointx - currx
        y = setpointy - curry
        deltaP = np.sqrt((x)**2 + (y)**2)

        if deltaP != 0:
            angle = np.arctan2(y,x)                                 
            deltaTheta1 = angle - currentAngle
            deltaTheta2 = angle + np.pi - currentAngle

            if deltaTheta1 == 360:
                deltaTheta1 = 0
            if deltaTheta2 == 360:
                deltaTheta2 = 0
            
            
            if deltaTheta1 <= deltaTheta2:
                deltaTheta = deltaTheta1
            else:
                deltaTheta = deltaTheta2
                deltaP = -deltaP

        else:
            return 0.0,0.0
        return deltaP, deltaTheta
    
    def calculateForce(self, deltaP, deltaT):
        ## Ku = 55529.223

        self.distIntegral += deltaP/deltaT
        distDiff = (self.LastdistError - deltaP) / deltaT

        self.lastdistError = deltaP

        #print(deltaP, self.distIntegral, distDiff)
        Force = (self.ForceKp * deltaP) + (self.ForceKi * self.distIntegral) + (self.ForceKd * distDiff)
        #print(Force)

        if abs(Force) > self.maxForce:
            Force = np.sign(Force) * self.maxForce

        return Force
    
    def calculateAngle(self, deltaTheta, deltaT):
        self.angleIntegral += deltaTheta
        angleDiff = (self.LastAngleError - deltaTheta) / deltaT

        self.LastAngleError = deltaTheta

        Angle = (self.AngleKp * deltaTheta) + (self.AngleKi * self.angleIntegral) + (self.AngleKd * angleDiff)

        if abs(Angle) > self.maxAngle:
            Angle = np.sign(Angle) * self.maxAngle

        return Angle
    
    def Update(self, setpointx, setpointy, currx, curry, currentAngle, deltaT):
        deltaP, deltaTheta = self.CalculateErrors(setpointx, setpointy, currx, curry, currentAngle)

        Force = self.calculateForce(deltaP, deltaT)
        Angle = self.calculateAngle(deltaTheta, deltaT)

        return Force, Angle
    


    def ForcetoPWM(self, Force):
        for i in range(1,self.ForceList):
            if self.ForceList[i-1] <= Force <= self.ForceList[i]:
                PWM1 = self.PWMList[i-1]
                PWM2 = self.PWMList[i]
                Force1 = self.ForceList[i-1]
                Force2 = self.ForceList[i]
                break


        return int(np.round((PWM2 - PWM1)/(Force2 - Force1) (Force - Force1) + PWM1,))

    def AngletoPWM(self, Angle):
        return int(np.round(10/6 * Angle + 150, 0))
    
    def RadiansToPWM(self, Angle):
        return int(np.round(300/np.pi * Angle + 150))
    
    