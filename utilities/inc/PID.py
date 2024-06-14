import numpy as np

class PID:
    def __init__(self):
        self.angleIntegral = 0
        self.LastAngleError = 0

        self.distIntegral = 0
        self.LastdistError = 0

        self.maxForce = 8.91
        self.maxAngle = 0.349066
        
        self.ForceList  = [8.91,4.992,1.04,0,-2.71,-6.24,-9.984]
        self.PWMList    = [165,160,156,150,145,140,135]

        self.ForceKp = 0.8
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

        if deltaP > 0.05:
            angle = np.arctan2(y,x)                                 
            deltaTheta = angle - currentAngle

            if abs(deltaTheta) > np.pi:
                deltaTheta = (np.sign(deltaTheta) * 2 * np.pi) + deltaTheta
            
            if abs(deltaTheta) > np.pi/2:
                deltaP = -deltaP
                deltaTheta = (np.sign(deltaTheta) * np.pi) + deltaTheta

            #print(f'deltaP = {deltaP}, deltaTheta = {deltaTheta}')
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

        if abs(Force) > self.maxForce:
            Force = np.sign(Force) * self.maxForce

        #print(f'Force : {Force}')

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
        for i in range(1,len(self.ForceList)):
            if self.ForceList[i-1] >= Force >= self.ForceList[i]:
                PWM1 = self.PWMList[i-1]
                PWM2 = self.PWMList[i]
                Force1 = self.ForceList[i-1]
                Force2 = self.ForceList[i]
                break


        return int(np.round(((PWM2 - PWM1)/(Force2 - Force1)) * (Force - Force1) + PWM1, 0))

    def AngletoPWM(self, Angle):
        return int(np.round(10/6 * Angle + 150, 0))
    
    def RadiansToPWM(self, Angle):
        PWM1   = 100
        PWM2   = 200
        Phi1 = -self.maxAngle
        Phi2 = self.maxAngle
        return int(np.round(((PWM2 - PWM1)/(Phi2 - Phi1)) * (Angle - Phi1) + PWM1, 0))
    
    
