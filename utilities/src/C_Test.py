import numpy as np

def locationToIndex(locX, locY):
    if locX > 4.6:
        print("overflow in X, slamming down")
        locX = 4.6
    elif locX < 0:
        print("overflow in X, slamming Up")
        locX = 0

    if locY > 4.6:
        print("overflow in Y, slamming down")
        locY = 4.6
    elif locY < 0:
        print("overflow in Y, slamming Up")
        locY = 0

    indX = int(np.round(locX * 10))
    indY = int(np.round(locY * 10))

    return indX, indY

def indexToLocations(indX, indY):

    if indX > 460:
        print("overflow in X, slamming down")
        indX = 460
    elif indX < 0:
        print("overflow in X, slamming Up")
        indX = 0

    if indX > 460:
        print("overflow in Y, slamming down")
        indX = 460
    elif indX < 0:
        print("overflow in Y, slamming Up")
        indX = 0

    locX = int(np.round(indX / 10))
    locY = int(np.round(indX / 10))

    return locX, locY


def ones(Map):
    indeces = []
    for i in range(0,460):
        for j in range(0,460):
            if Map[j][i] == 1:
                indeces.append([j,i])
    return indeces

carX = 0
carY = 0
CarTheta = np.pi/2

sensorLDetect = 1

Map = np.zeros((460,460))

ObstrucionLocation = np.array([np.cos(CarTheta),np.sin(CarTheta)]) * sensorLDetect

print(Map)

print(ObstrucionLocation)

if 0 < ObstrucionLocation[0] < 4.6 and 0 < ObstrucionLocation[1] < 4.6:
    indX, indY = locationToIndex(ObstrucionLocation[0], ObstrucionLocation[1])

    print(indX, indY)
    Treshold = 3

    XRange = range(indX - Treshold, indX + Treshold)
    YRange = range(indY - Treshold, indY + Treshold)

    

    for i in XRange:
        if not 0 <= i <= 460:
            continue
        for j in YRange:
            if not 0 <= j <= 460:
                continue
            Map[j][i] = 1

    print(ones(Map))


