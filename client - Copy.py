import socket
import json
import time
import numpy as np
import pandas as pd
import serial
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


msgFromClient       = "200"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 20000
UDPClientSocket     = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def out():
    dat =[]
   
    for i in range(50):
        
            f = open("output.txt","r")
            z = (f.read()) 
            z = z.split(',')
            z = np.array(z)
            t1 = z[0]
            t2 =z[1]
            t3 = z[2]
            t4 = z[3]
            t5 = z[4]

                  
            #x.columns = ['s1', 's2', 's3', 's4', 's5']
            
            
           
           
            
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            dec = json.loads(msgFromServer[0].decode())
            
            a = dec.get("d1")
            b = dec.get("d2")
            c = dec.get("d3")
            d = dec.get("d4")
            e = dec.get("d5")
            f = dec.get("d6")
            g = dec.get("d7")
            h = dec.get("d8")
            
            
            
            x = a,b,c,d,e,f,g,h,t1,t2,t3,t4,t5 
            dat.append(x)
            print(x)

            
    dat = np.array(dat)
    df = pd.DataFrame(dat)
    df.columns = ['data1','data2','data3','data4','data5','data6','data7','data8','l1','l2','l3','l4','l5']
    df.to_csv('sf.csv')
    print(df)
 
  

#while True :
for i in range (1):
    out()
   