#!/usr/bin/env python3

import socket
import subprocess
import os
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '10.132.0.42'  # The server's hostname or IP address
PORT = 2000        # The port used by the server

time.sleep(7)
s.connect((HOST, PORT))

FIFO = '/home/pi/WifiRobot/project/robot_fifo'

while True : 
    data = s.recv(1024)
    text = data.decode("ascii")
    with open(FIFO, 'a') as fifo :
        fifo.write(text)
