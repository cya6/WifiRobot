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
            p2.ChangeDutyCycle(stop_d)
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
    y = 0
    z = 0
    fw_bw = 0
    lf_rg = 0

    while run :
        time.sleep(0.2)
        #Read from FIFO
        while True:                              
            line = fifo.read()
            if len(line) > 2 :
                
                #Move robot according to accelerometer readings
                split_line =  line.split( "\n" )
                for l in split_line :
                    t = l.split(":")

                    #Move forward or backwards depending on the ZValue
                    if ( t[0] == "zValue" ) :
                        z = float(t[1])
                        if ( z > 2 ) :
                            fw_bw = fw_bw + 1
                            if ( fw_bw > 3 ) :
                                forward()
                                print ("forward\n")
                        elif ( z < -1 ):
                            fw_bw = fw_bw + 1
                            if ( fw_bw > 3 ) :
                                backward()
                                print ("backward\n")
                        else :
                            fw_bw = 0
                            if ( lf_rg == 0 ) :
                                stop()
                                print ("still\n")

                    #Move left or right
                    elif ( t[0] == "yValue" ):
                        y = float(t[1])
                        if ( y < -0.5 ) :
                            lf_rg = lf_rg + 1
                            if ( lf_rg > 3 ) : 
                                right_turn()
                                print ("right")
                        elif ( y > 0.7 ):
                            lf_rg = lf_rg + 1
                            if ( lf_rg > 3 ) :
                                left_turn()
                                print ("left")
                        else :
                            lf_rg = 0
                            if ( fw_bw == 0 ) :
                                stop()
                                print ("still")

            

except KeyboardInterrupt:
    p1.stop()
    p2.stop()
    GPIO.cleanup()

