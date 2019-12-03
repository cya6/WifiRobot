import RPi.GPIO as GPIO
import time
import pygame
import sys
from pygame.locals import *
import os
stop_d = 0#(1.5/21.5)*100
stop_f = 1/(0.0215)
d1 = 1.5
d2 = 1.5
freq1 = 21.5
freq2 = 21.5
panic = 1
run = True

#CONTROL INITIALIZATION--------------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)

#left
p1 = GPIO.PWM(16, 46.1)
p1.start(0)

#right
p2 = GPIO.PWM(5, 46.1)
p2.start(0)
#--------------------------------------------------

#Screen Init--------------------------------------

#direction clockwise = 1, stop = 0, counter = -1
def full_speed (servo, direction) :
    if ( direction == 1 ) :
        if ( servo == 1 ) :
            p1.ChangeDutyCycle((1.7/21.7)*100)
            p1.ChangeFrequency(1/0.0217)
        if ( servo == 2 ):
            p2.ChangeDutyCycle((1.3/21.3)*100) 
            p2.ChangeFrequency(1/0.0213)
    if ( direction == 0 ) :
        if ( servo == 1 ) :
            p1.ChangeDutyCycle(stop_d) 
            p1.ChangeFrequency(stop_f) 
        if ( servo == 2 ):
            p1.ChangeDutyCycle(stop_d)
            p2.ChangeFrequency(stop_f)
    if ( direction == -1 ) :
        if ( servo == 1 ) :
            p1.ChangeDutyCycle((1.3/21.3)*100)
            p1.ChangeFrequency(1/0.0213)
        if ( servo == 2 ) :
            p2.start((1.7/21.7)*100) 
            p2.ChangeFrequency(1/0.0217)

def left_turn():
    start = time.time()
    while ( time.time() - start < 1.3 ) :
        full_speed(1, 0)
        full_speed(2, 1)

def forward() :
    full_speed(1,1)
    full_speed(2,1)

def backward():
    full_speed(1,-1)
    full_speed(2,-1)

def right_turn():
    start = time.time()
    while ( time.time() - start < 1.3) :
        full_speed(2,0)
        full_speed(1,1)

def stop():
    full_speed(2,0)
    full_speed(1,0)

FIFO = '/home/pi/WifiRobot/project/robot_fifo'

try :
    run = True
    fifo = open(FIFO)
    x = 0 
    y = 0
    z = 0
    while run :
        time.sleep(0.2)
        while True:                              
            line = fifo.read()
            if len(line) > 2 :
                split_line =  line.split( "\n" )
                for l in split_line :
                    t = l.split(":")
                    if ( t[0] == "zValue" ) :
                        z = float(t[1])
                        if ( z > 2 ) :
                            z = 1
                            forward()
                            print ("forward\n")
                        elif ( z < -1 ):
                            z = -1
                            backward()
                            print ("backward\b")
                        else :
                            z = 0 
                            if ( x == 0 ) :
                                stop()
                                print ("still\n")
                    elif ( t[0] == "yValue" ):
                        x = float(t[1])
                        if ( x < -0.5 ) :
                            x = 1
                            right_turn()
                            forward()
                            print ("right")
                        elif ( x > 0.7 ):
                            x = -1
                            left_turn()
                            forward()
                            print ("left")
                        else :
                            x = 0
                            if ( z == 0 ) :
                                stop()
                                print ("still")

            

except KeyboardInterrupt:
    p1.stop()
    p2.stop()
    GPIO.cleanup()

