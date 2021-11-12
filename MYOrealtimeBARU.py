from LibMyo import *
import serial

model1 = joblib.load('jempolBAGUS.pkl') 
model2 = joblib.load('telunjukBAGUS.pkl')
model3 = joblib.load('tengahBAGUS.pkl')
model4 = joblib.load('manisBAGUS.pkl')
model5 = joblib.load('kelingkingBAGUS.pkl')
modelpca = joblib.load('pcawindowBAGUS.pkl')
arduino = serial.Serial("com10", 9600)

class Plot(object):
    def __init__(self, listener):
        self.n = listener.n
        self.listener = listener
        #self.fig = plt.figure()
        #self.axes = [self.fig.add_subplot('81' + str(i)) for i in range(1, 9)]
        #[(ax.set_ylim([-100, 100])) for ax in self.axes]
        #self.graphs = [ax.plot(np.arange(self.n), np.zeros(self.n))[0] for ax in self.axes]
        #plt.ion()
    

    def update_plot(self):
        print('isisne kosong')
        '''for g, data in zip(self.graphs, emg_data):
            if len(data) < self.n:
                # Fill the left side with zeroes.
                data = np.concatenate([np.zeros(self.n - len(data)), data])
            g.set_ydata(data)
        plt.tight_layout()
        plt.draw()'''
    
    def main(self):
        while True:

            self.update_plot()
            plt.pause(1/ 1000)
            emg_data = self.listener.get_emg_data()
            emgX1 = ([x[1] for x in emg_data])
            emgX = pd.DataFrame(emgX1)

            oi = emgX.shape
            if oi[0] > 40:
                data = np.array(emgX).reshape(-1,8)

                #print(data)
                #emg = np.array(data).reshape(-1,8)

                save_emg = pd.DataFrame(data)
                save_emg.columns = ['ch1', 'ch2', 'ch3','ch4','ch5','ch6','ch7','ch8']
                #FILTERING

                ch1 = bandpass(save_emg, save_emg.ch1 ,pole,low,high)
                ch2 = bandpass(save_emg, save_emg.ch2 ,pole,low,high)
                ch3 = bandpass(save_emg, save_emg.ch3 ,pole,low,high)
                ch4 = bandpass(save_emg, save_emg.ch4 ,pole,low,high)
                ch5 = bandpass(save_emg, save_emg.ch5 ,pole,low,high)
                ch6 = bandpass(save_emg, save_emg.ch6 ,pole,low,high)
                ch7 = bandpass(save_emg, save_emg.ch7 ,pole,low,high)
                ch8 = bandpass(save_emg, save_emg.ch8 ,pole,low,high)

                datafilter = pd.concat([ch1,ch2,ch3,ch4,ch5,ch6,ch7,ch8], axis=1)
                datafilter.columns = ['ch1','ch2','ch3','ch4','ch5','ch6','ch7','ch8']
                #print(datafilter)

        #SPLIT DATA
                data_x = np.array(datafilter)
                #print(data_x.shape)
        #WINDOWING 
        
                x_train = windowing(data_x)
                #print(x_train)
                X = np.array(x_train)
                #datawindow = np.array(x_train)
                #print(x_train)
                dwX = X.reshape(-1,40*8)
            
        #STD & PCA
                dnewX = modelpca.transform(dwX)
                #print(dnewX)
                realtime1 = model1.predict(dnewX)[0]
                realtime2 = model2.predict(dnewX)[0]
                realtime3 = model3.predict(dnewX)[0]
                realtime4 = model4.predict(dnewX)[0]
                realtime5 = model5.predict(dnewX)[0]
                wesurutan = [realtime1,realtime2,realtime3,realtime4,realtime5]
                #print(realtime1)
                #metune = []
                for i in wesurutan:
                    print(i)
                    
                    #for i in range(10):
                    #arduinoterima = arduino.readline().decode('ascii').strip()
                    arduinokirim  = arduino.write(i)
                    #arduino.flush()
                    #print(arduinoterima)
                    #jenenge = (arduinokirim,arduinoterima)
                    #arduino
                    #metune.append(jenenge)
                #print(metune)      
                #b = arduino.readline().decode('ascii').rstrip()

                

def main():
    myo.init()
    hub = myo.Hub()
    listener = EmgCollector(50)
    with hub.run_in_background(listener.on_event):
        Plot(listener).main()
    
   
while True :
    main()
#if __name__ == '__main__':

    


