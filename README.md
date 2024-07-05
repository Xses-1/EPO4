# EPO4

## Introduction
The goal of this project was to create a autonymous diriving car system that would compete in a set of challanges. The car was supposed to be controlled via Bluetooth from a computer. This laptop was also connected to a system of microphones that toegether with a beacon on top of the car allowed for an accurate localization of the vehicle.<br>

## Competition
The competition consistet out of a set of challanges:
1. Challange A - accurately going to a given point
2. Challange B - accurately going to 2 given points
3. Challange C - using the built in distance sensors to avoid obstacles
4. Free Challange - bonus points for implementing additional features

## The results
The detailed final report of the entire project can be found in the docs directory of this branch, toegether with the manual of this project.<br>

Due to the time constrains the team was able to finish the challange A with a very high accuracy of 10cm (the length of the car was ~40cm) and attempt the challange B with being able to only get to the first point. Additionally an graphical user interface was implemented to see the position of the car from the simiulation in real time.

## Repository organisation
The entire project consisted out of a few separate modules. Each of them had its own branch and assigned team to it:
1. Comms - communication with the car, sending control signals, recieveing the sensor data
1. Microphones - communication with the soundcard that captures the microphones and processing those data to perform audiolocation
1. Module4 - simulation of the position of the car using an mathematical model
1. Top - a top level code that connects all of the modules and synchronizes them to perform the challanges<br>

Every brach has a inc and src directory that contains the header files and executables according to convention used in C programming. The final executables for the corresponding challanges can be found in the "Top" branch utilities -> src -> A.py | B.py | B.sh | A\_TDOA.py
