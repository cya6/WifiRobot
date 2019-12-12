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
for_1_d = 1.65/21.65
for_1_f = 1/0.02165
back_1_d = 1.38/21.38
back_1_f = 1/0.02138

#direction clockwise = 1, stop = 0, counter = -1
def full_speed (servo, direction) :
    if ( direction == 1 ) :
        if ( servo == 1 ) :
            p1.ChangeDutyCycle(for_1_d*100)
            p1.ChangeFrequency(for_1_f)
        if ( servo == 2 ):
            p2.ChangeDutyCycle(back_1_d*100) 
            p2.ChangeFrequency(back_1_f)
    if ( direction == 0 ) :
        if ( servo == 1 ) :
            p1.ChangeDutyCycle(stop_d) 
            p1.ChangeFrequency(stop_f) 
        if ( servo == 2 ):
            p2.ChangeDutyCycle(stop_d)
            p2.ChangeFrequency(stop_f)
    if ( direction == -1 ) :
        if ( servo == 1 ) :
            p1.ChangeDutyCycle(back_1_d*100)
            p1.ChangeFrequency(back_1_f)
        if ( servo == 2 ) :
            p2.start(for_1_d*100) 
            p2.ChangeFrequency(for_1_f)

def left_turn():
    start = time.time()
    while ( time.time() - start < 0.5 ) :
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
    while ( time.time() - start < 0.5) :
        full_speed(2,0)
        full_speed(1,1)

def stop():
    full_speed(2,0)
    full_speed(1,0)

FIFO = '/home/pi/WifiRobot/project/robot_fifo'
cal = 30
still = 0
try :
    run = True
    fifo = open(FIFO)
    side = 0
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
                    
                    if cal > 0 :
                        if ( t[0] == "zValue") :
                            still_z = float(t[1]) 
                        elif ( t[0] == "xValue" ) :
                            still_x = float(t[1]);
                        cal = cal - 1;

                    #Move forward or backwards depending on the ZValue
                    elif ( t[0] == "zValue" ) :
                        z = float(t[1])
                        if ( (z > still_z + 0.1) and (side < still_x - 0.1) ) :
                            fw_bw = fw_bw + 1
                            if ( fw_bw > 2 ) :
                                forward()
                                print ("forward\n")
                        elif ( (z < still_z - 0.1) and (side > still_x + 0.1)):
                            fw_bw = fw_bw + 1
                            if ( fw_bw > 2 ) :
                                backward()
                                print ("backward\n")
                        else :
                            fw_bw = 0
                            if ( lf_rg == 0 ) :
                                stop()
                                print ("still\n")

                    #Move left or right
                    elif ( t[0] == "xValue" and fw_bw == 0 ):

                        print("legal turn, x= "+(str(t[1])))
                        side = float(t[1])
                        if ( side < still_x - 0.1 ) :
                            lf_rg = lf_rg + 1
                            if ( lf_rg > 2 ) : 
                                right_turn()
                                lf_rg = 0 
                                print ("right\n")
                        elif ( side >= still_x + 0.05 ):
                            lf_rg = lf_rg + 1
                            if ( lf_rg > 2 ) :
                                left_turn()
                                lf_rg= 0
                                print ("left\n")
                        else :
                            lf_rg = 0
                            if ( fw_bw == 0 ) :
                                stop()
                                print ("still\n")

            

except KeyboardInterrupt:
    p1.stop()
    p2.stop()
    GPIO.cleanup()

