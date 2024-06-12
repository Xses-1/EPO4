import math
import numpy as np
from shapely.geometry import LineString
from shapely.geometry import Point
from module4 import KITTmodel
from PID import PID

class purePursuit:
    start_point = []
    end_point = []

    def __init__(self): #initialises all variables
        self.intersec_1 = 0
        self.intersec_2 = 0
        self.targetPoint = 0
        self.wheelbase = 0.335
        self.x_location = 0
        self.y_location = 0

    def intersections(self, _location_x, _location_y, _x1, _y1, _x2, _y2):
        """_summary_
            calculates the target point:
                - draws a line using the start and end points
                - creates a circle of radius lookaheaddistance around kitt
                - takes the intersection of the line and the circle
                - returns array of intersections
                uses the shapely library for these calculations
            Args:
                _location_x (_type_): x_position of kitt
                _location_y (_type_): y_position of kitt
                _x1 (_type_): start position x
                _y1 (_type_): start position y
                _x2 (_type_): end position x
                _y2 (_type_): end position y
            Returns:
                _type_: array of intersection coordinates
        """
        _point = Point(_location_x, _location_y)
        _circle = _point.buffer(self.lookAheadDistance)
        _path = LineString([(_x1, _y1), (_x2, _y2)])
        _intersection = _circle.intersection(_path)

        if len(_intersection.coords) == 2:
            return np.array([(_intersection.coords[0]),
                (_intersection.coords[1])])
        elif len(_intersection.coords) == 1:
            return np.array([(_intersection.coords[0])])
        else:
            print("nothing found")
            return  np.array([(0,0), (0,0)])
    
    def steeringAngle(self, _x_tp, _y_tp, orientation):
        """deterimines the steering angle for kitt based on the target point
        Args:
            x_tp (_type_): x coordinate of the target point
            y_tp (_type_): y coordinate of the target point
            orientation  : current orientation of the car
        Returns:
        _   steering_angle: steering angle
        """

        _alpha = np.arctan2((_y_tp - self.y_location), (_x_tp - self.x_location)) - orientation
        
        with open('test.txt', 'a') as f:
            f.write(f' gamma = {_alpha}')
            f.write(f' orientation = {orientation}')
        _angle = np.arctan((2 * self.wheelbase * np.sin(_alpha))/self.lookAheadDistance)

        return _angle

    def distance_calc(self, x2, y2, x1, y1):
        _distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return _distance
    
    def point_selection(self, point_1, point_2, x_destination, y_destination):
        _distance_1 = self.distance_calc(point_1[1], point_1[0], x_destination,
        y_destination)
        _distance_2 = self.distance_calc(point_2[1], point_2[0], y_destination,
        x_destination)
        if _distance_1 <= _distance_2:
            return point_1
        else:
            return point_2
    
    def purepursuit(self, _x_position, _y_position, _x_target, _y_target, orientation):
        """
        Args:
            _x_position: x coordinate of the car
            _y_position: y coordinate of the car
            _x_target:   x coordinate of the target point
            _y_target:   y coordinate of the target point
            orientation: current orientation of the car
        Returns:
            angle      : steering angle in radians
        """
        for multiplier in np.linspace(0.1, 2, 20):
            self.lookAheadDistance = multiplier * self.distance_calc(_x_target, _y_target, _x_position, _y_position) # the radius of the circle
            self.intersection = self.intersections(_x_position, _y_position, self.x_location, self.y_location, _x_target, _y_target)
            #print(self.intersection.shape())
            if self.intersection[0,0] == 0 and self.intersection[1,1] == 0 and self.intersection[1,0] == 0 and self.intersection[0,1] == 0:
                continue
            else:
                break
        with open('test.txt', 'a') as f:
            f.write(f'intersections: {self.intersection}')
        self.Target = self.point_selection(self.intersection[0], self.intersection[1], _x_target, _y_target)

        self.angle = self.steeringAngle(self.Target[0], self.Target[1], orientation)

        return self.angle