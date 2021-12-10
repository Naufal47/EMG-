import serial
import joblib
import pandas as pd
import numpy as np
import myo
import matplotlib.pyplot as plt
import pyautogui as pg
import time
import os
import sys

#from sklearn.preprocessing import MinMaxScaler
#from sklearn.preprocessing import StandardScaler
#from sklearn.preprocessing import Normalizer


from libRMS import *
#MinMaxScaler(feature_range=(0, 1))
model1 = joblib.load('jempolNaufalRMSkecil.pkl')
model2 = joblib.load('telunjukNaufalRMSkecil.pkl')
model3 = joblib.load('tengahNaufalRMSkecil.pkl')
model4 = joblib.load('manisNaufalRMSkecil.pkl')
model5 = joblib.load('kelingkingNaufalRMSkecil.pkl')
modelscaler = joblib.load('scalerkecil.pkl')
#arduino = serial.Serial('com6',9600)
#modelpca = joblib.load('pcawindowbaru.pkl')
#arduino = serial.Serial("com10", 9600)
#print(modelscaler)
#print(modelscaler)
class Plot(object):
    def __init__(self, listener):
        self.n = listener.n
        self.listener = listener
        #self.fig = plt.figure()
        #self.axes = [self.fig.add_subplot('81' + str(i)) for i in range(1, 9)]
        #[(ax.set_ylim([-100, 100])) for ax in self.axes]
        #self.graphs = [ax.plot(np.arange(self.n), np.zeros(self.n))[0] for ax in self.axes]
        #plt.ion()
    

    ##def update_plot(self):
        #print('isisne kosong')
        '''for g, data in zip(self.graphs, emg_data):
            if len(data) < self.n:
                # Fill the left side with zeroes.
                data = np.concatenate([np.zeros(self.n - len(data)), data])
            g.set_ydata(data)
        plt.tight_layout()
        plt.draw()'''
    
    def main(self):
        while True:

            #self.update_plot()
            plt.pause(1/ 30)
            emg_data = self.listener.get_emg_data()
            emgX1 = ([x[1] for x in emg_data])
            emgX = pd.DataFrame(emgX1)

            oi = emgX.shape
            if oi[0] > 39:
                data = np.array(emgX).reshape(-1,8)

                #print(data)
                #emg = np.array(data).reshape(-1,8)

                save_emg = pd.DataFrame(data)
                save_emg.columns = ['ch1', 'ch2', 'ch3','ch4','ch5','ch6','ch7','ch8']
                #print(save_emg)
                datafituran = prep(save_emg)
                #print(datafituran)
                X1 = modelscaler.transform(datafituran)
                
                              
                realtime1 = model1.predict(X1)*100
                realtime2 = model2.predict(X1)*100
                realtime3 = model3.predict(X1)*100
                realtime4 = model4.predict(X1)*100
                realtime5 = model5.predict(X1)*100
                a = realtime1.tolist()
                b = realtime2.tolist()
                c = realtime3.tolist()
                d = realtime4.tolist()
                e = realtime5.tolist()

                wesurutan = [a,b,c,d,e]
                datapred = np.array(wesurutan).reshape(1,-1)
               
                
                
                #print(realtime1,realtime2,realtime3,realtime4,realtime5)
                while True:
                    os.startfile("tangan baru 2.blend")
                    oi = datapred.mean()
                    print(oi)
                    if oi < 20:
                        pg.keyDown('a')
                        time.sleep(2)
                    if oi > 40 :
                        pg.keyDown('b')
                        time.sleep(6)
                        pg.keyDown('d')
                        time.sleep(6)
                        pg.keyDown('g')
                        time.sleep(6)
                    
                    
               

                

def main():
    myo.init()
    hub = myo.Hub()
    listener = EmgCollector(40)
    with hub.run_in_background(listener.on_event):
        Plot(listener).main()
    
   
#while True :
    #main()

if __name__ == '__main__':
    main()
