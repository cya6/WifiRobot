import os
import atexit

FIFO = '/home/pi/WifiRobot/project/robot_fifo'

with open(FIFO) as fifo :
    while True:
        line = fifo.read()
        if len(line) > 2 :
            split_line =  line.split( "\n" )
            for l in split_line :
                t = l.split(":")
                if ( t[0] == "zValue" ) :
                    z = float(t[1])
                    if ( z > 2 ) :
                        print ("forward\n")
                    elif ( z < -1 ):
                        print ("backward\b")
                    else :
                        print ("still\n")
                elif ( t[0] == "yValue" ):
                    x = float(t[1])
                    if ( x < -0.7 ) :
                        print ("right")
                    elif ( x > 0.7 ):
                        print ("left")
                    else :
                        print ("still")
                
