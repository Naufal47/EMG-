
#from _typeshed import Self
from matplotlib import pyplot as plt
from collections import deque
from threading import Lock, Thread
import pandas as pd

import myo
import numpy as np

import socket
import json
import pandas as pd


localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

class EmgCollector(myo.DeviceListener):
    """
    Collects EMG data in a queue with *n* maximum number of elements.
    """

    def __init__(self, n):
        self.n = n
        self.lock = Lock()
        self.emg_data_queue = deque(maxlen=n)

    def get_emg_data(self):
        with self.lock:
            return list(self.emg_data_queue)

    # myo.DeviceListener

    def on_connected(self, event):
        event.device.stream_emg(True)

    def on_emg(self, event):
        with self.lock:
            self.emg_data_queue.append((event.timestamp, event.emg))

class Plot(object):
    def __init__(self, listener):
        self.n = listener.n
        self.listener = listener
        self.fig = plt.figure()
        self.axes = [self.fig.add_subplot('81' + str(i)) for i in range(1, 9)]
        [(ax.set_ylim([-100, 100])) for ax in self.axes]
        self.graphs = [ax.plot(np.arange(self.n), np.zeros(self.n))[0] for ax in self.axes]
        plt.ion()

    def update_plot(self):

        emg_data = self.listener.get_emg_data()
      
        emgX = ([x[1] for x in emg_data])
     
        


        emg_data = np.array([x[1] for x in emg_data]).T
        emgS = emg_data.shape
        if emgS[0] > 0:
            data = emg_data
            emg = data.reshape(-1,8)
            save_emg = pd.DataFrame(emg)
            save_emg.columns = ['ch1', 'ch2', 'ch3','ch4','ch5','ch6','ch7','ch8']
           
     
        for g, data in zip(self.graphs, emg_data):
            if len(data) < self.n:
                # Fill the left side with zeroes.
                data = np.concatenate([np.zeros(self.n - len(data)), data])
            g.set_ydata(data)
            #print(pd.DataFrame(data))
        #plt.tight_layout()
        plt.draw()
        

    def main(self):
        while True:
            
            self.update_plot()
            plt.pause(1.0 / 30)
            emg_data = self.listener.get_emg_data()
            emgX1 = ([x[1] for x in emg_data])
            emgX = pd.DataFrame(emgX1)
            oi = emgX.shape
            if oi[0]>0:
                bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
                message = bytesAddressPair[0]
                address = bytesAddressPair[1]
                d1 = emgX1[0][0]
                d2 = emgX1[1][0]
                d3 = emgX1[2][0]
                d4 = emgX1[3][0]
                d5 = emgX1[4][0]
                d6 = emgX1[5][0]
                d7 = emgX1[6][0]
                d8 = emgX1[7][0]
            
                datM = json.dumps({"d1": d1, "d2": d2, "d3": d3, 
                "d4": d4, "d5": d5, "d6": d6, "d7": d7, "d8":d8})
                datM2 = str.encode(datM)
                UDPServerSocket.sendto(datM2, address)
                print(datM)
            


def main():
    myo.init()
    hub = myo.Hub()
    listener = EmgCollector(200)
    
    with hub.run_in_background(listener.on_event):
        Plot(listener).main()


if __name__ == '__main__':
    
    main()

