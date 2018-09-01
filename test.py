# -*- coding: utf-8 -*-

import androidutils as andr
import time
import re
import numpy as np
import matplotlib.pyplot as plt

cycles=20
points_per_cycle=50

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
    width,height=andr.get_screen_matrix(1)
    im=np.random.randint(2, size=(width, height))
    for rs in range(cycles):
        plt.clf()
        plt.axis([0, width, 0, height])
        
        for r in range(points_per_cycle):
            i = np.random.randint(width)
            j = np.random.randint(height)
            if im[i][j]==1:
                andr.send_tap(device,i,j)
                plt.plot(i,j,'o')
                plt.pause(0.1)
        
#------------------------------------------------------------------------------
def do_stored_taps(device,path):
    with open(path,'r') as f:
        for line in f:    
            xh,yh = line.split(' ')
            xh = xh.replace("\n","")
            yh = yh.replace("\n","")
            x = int(xh, 16)
            y = int(yh, 16)
            andr.send_tap(device,x,y)

#------------------------------------------------------------------------------
def process_event_file(path, destination):
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
                    x.append(words[5])
                    doit = doit + 1
                elif doit>0 and w in filter2:    
                    y.append(words[5])
                    doit = doit + 1

                if doit == 3:
                    doit=0                            
                    
    with open(destination,'w') as f1:                    
        for i in range(len(x)):
            f1.writelines(x[i] + " " + y[i] + "\n")
 
    
#------------------------------------------------------------------------------    
def do_test(device):
    stored_evnt_file="dumppoints.log"
    target_data_file="tappoints.log"    
    process_event_file(stored_evnt_file, target_data_file)

    do_login("01", "0001")
    time.sleep(5)
    
    for rs in range(cycles):
        do_stored_taps(device, target_data_file)

#    do_logout()
    time.sleep(5)
    
    do_login("01", "0001")
    time.sleep(5)
    
    for rs in range(cycles):
        do_random_taps(device)
    

#------------------------------------------------------------------------------        
device=1    
do_test(device)



