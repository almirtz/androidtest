# -*- coding: utf-8 -*-

import androidutils as andr
import androiddevice as adev
import time
import re
import numpy as np
import matplotlib.pyplot as plt

cycles=1
points_per_cycle=20

#------------------------------------------------------------------------------
def do_login(code,pin):
    andr.send_numbers(code)
    andr.send_enter()
    andr.send_numbers(pin)
    
#------------------------------------------------------------------------------    
def do_logout():
    time.sleep(120)

#------------------------------------------------------------------------------
def do_point(x,y):
    time.sleep(120)
    
#------------------------------------------------------------------------------
def do_random_taps(device):
    step = 100
    width,height = device.get_screen_matrix_size()
    width,height = width // step, height // step
    points = points_per_cycle
    if points > width*height:
        points = width*height
        
    disable_repeat = True

    if disable_repeat:
        im=np.zeros((width, height))

    plt.clf()
    plt.axis([0, width, 0, height])
    
    for r in range(points):
        x = np.random.randint(width)
        y = np.random.randint(height)

        if disable_repeat:
            for rr in range(points):
                if im[x][y] == 0:
                    break;
                x = np.random.randint(width)
                y = np.random.randint(height)
                
            if im[x][y] == 1:
                for i in range(width):
                    for j in range (height):
                        if im[i,j] == 0:
                            x,y = i,j
                            break;
                    if im[x,y] == 0:
                        break;
                
        
        im[x][y] = 1
    
        andr.send_tap(device, x*step, y*step)
        plt.plot(x, y, 'o')
        plt.pause(0.1)
    
#------------------------------------------------------------------------------
def do_stored_taps(device,path):
    with open(path,'r') as f:
        for line in f:    
            xh,yh = line.split(' ')
            xh = xh.replace("\n","")
            yh = yh.replace("\n","")
            x = int(xh)
            y = int(yh)
            andr.send_tap(device,x,y)

#------------------------------------------------------------------------------
def process_event_file(device, path, destination):
    x=[]
    y=[]
    filter1=["ABS_MT_POSITION_X"]
    filter2=["ABS_MT_POSITION_Y"]
    with open(path,'r') as f:
        doit=0
        for line in f:
            words = re.findall("\w+",line)
            for w in words:
                if w in ["DOWN"]:       
                    doit = 1
                
                if doit>0 and w in filter1:       
                    x.append(device.px_to_dp(int(words[5],16)))
                    doit = doit + 1
                elif doit>0 and w in filter2:    
                    y.append(device.px_to_dp(int(words[5],16)))
                    doit = doit + 1

                if doit == 3:
                    doit=0                            
                    
    with open(destination,'w') as f1:                    
        for i in range(len(x)):
            f1.writelines(str(x[i]) + " " + str(y[i]) + "\n")
 
    
#------------------------------------------------------------------------------    
def do_test(device):
    stored_evnt_file="dumppoints.log"
    target_data_file="tappoints.log"    
    process_event_file(device, stored_evnt_file, target_data_file)

    do_login("01", "0001")
    time.sleep(5)
    
    for rs in range(cycles):
        do_stored_taps(device, target_data_file)

    do_logout()
    time.sleep(5)
    
    do_login("01", "0001")
    time.sleep(5)
    
    for rs in range(cycles):
        do_random_taps(device)
   
#------------------------------------------------------------------------------        
device=adev.DeviceHTCM8()
do_test(device)



