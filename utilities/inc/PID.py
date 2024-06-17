import numpy as np

class PID:
    def __init__(self):
        self.angleIntegral = 0
        self.LastAngleError = 0

        self.distIntegral = 0
        self.LastdistError = 0

        self.minForce = 1.04
        self.maxForce = 8.91
        self.minAngle = 0.0872665
        self.maxAngle = 0.349066
        
        self.ForceList  = [8.91,4.992,1.04,1.03,0,-2.70,-2.71,-6.24,-9.984]
        self.PWMList    = [165,160,156,150,150,150,146,140,135]

        self.ForceKp = 2
        self.ForceKi = 0.0
        self.ForceKd = 0.0

        self.AngleKp = 0.8
        self.AngleKi = 0.0
        self.AngleKd = 0.0
        
        
        ## test values
        self.angle = 0


    def CalculateErrors(self, setpointx, setpointy, currx, curry, currentAngle):
        ## (x,y) is Vector pointing from current position to setpoint
        x = setpointx - currx
        y = setpointy - curry
        deltaP = np.sqrt((x)**2 + (y)**2)

        ## Prevent rounding errors 
        if deltaP < 0.1:
            deltaP = 0.0

        ## Angle of pointing vector
        angle = np.arctan2(y,x)        
        ## DeltaTheta is the angle between the direction vector and the pointing vector                   
        deltaTheta = angle - currentAngle

        ## Limit deltaTheta between -pi and pi
        while not ( -np.pi <= deltaTheta <= np.pi):
            deltaTheta = -(np.sign(deltaTheta) * 2 * np.pi) + deltaTheta

        if abs(deltaTheta) > np.pi/2:
            deltaP = -deltaP
            deltaTheta = (np.sign(deltaTheta) * np.pi) + deltaTheta
            
        ## Limit deltaTheta between -pi and pi
        while not ( -np.pi <= deltaTheta <= np.pi):
            deltaTheta = -(np.sign(deltaTheta) * 2 * np.pi) + deltaTheta

        return deltaP, deltaTheta
    
    def calculateForce(self, deltaP, deltaT):
        self.distIntegral += deltaP * deltaT
        distDiff = (deltaP - self.LastdistError ) / deltaT
        self.lastdistError = deltaP

        Force = (self.ForceKp * deltaP) + (self.ForceKi * self.distIntegral) + (self.ForceKd * distDiff)

        if abs(Force) > self.maxForce:
            Force = np.sign(Force) * self.maxForce

        if abs(Force) != 0.0:
            if abs(Force) > self.maxForce:
                Force = np.sign(Force) * self.maxForce
            elif abs(Force) < self.minForce:
                Force = 0.0

        return Force
    
    def calculateAngle(self, deltaTheta, deltaT):
        self.angleIntegral += deltaTheta * deltaT
        angleDiff = (deltaTheta - self.LastAngleError)
        self.LastAngleError = deltaTheta


        Angle = (self.AngleKp * deltaTheta) + (self.AngleKi * self.angleIntegral) + (self.AngleKd * angleDiff)
        
        if abs(Angle) < self.minAngle:
            Angle = 0
        elif abs(Angle) > self.maxAngle:
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
    
    
