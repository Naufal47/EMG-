import socket
import json
import time
import numpy as np
import pandas as pd

msgFromClient       = "200"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 20000
UDPClientSocket     = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def out():
    dat =[]
    for i in range(1):
        for i in range(10):
            
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
            

            x = a,b,c,d,e,f,g,h   
            dat.append(x)

            
        dat = np.array(dat)
        df = pd.DataFrame(dat)
        df.columns = ['data1','data2','data3','data4','data5','data6','data7','data8']
        print(df)
 
  

while True :
    out()
   