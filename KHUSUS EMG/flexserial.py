import serial
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ser = serial.Serial('com8',baudrate=9600, timeout=1)
while True:
    data = []
    for i in range(10):
        arduinoData = ser.readline().decode('ascii').strip()
        #data.append(arduinoData)
        x = np.array(arduinoData)
        print(x)
          # If you want outputs separated by newlines
        
    data = np.array(data)
    dat = pd.DataFrame(data)
    
    with open("output.txt", "w") as f:
            f.write(arduinoData)
            #f.write("\n")
            f.close()
    #dat.columns=["t1","t2","t3","t4","t5"]
    #dat.to_csv('target.csv',)
    #print(dat)


