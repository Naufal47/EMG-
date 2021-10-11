from LibMyo import *

model = joblib.load('modeltanpawindow.pkl') 
modelpca = joblib.load('pcatanpawindow.pkl')

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
        emgX = pd.DataFrame(emgX)
        
        emg_data = np.array([x[1] for x in emg_data]).T
        emgS = emg_data.shape
        if emgS[0] > 0:
            data = emg_data
            emg = data.reshape(-1,8)
            save_emg = pd.DataFrame(emg)
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
           

        #WINDOWING 
        
            #x_train = windowing(datafilter)
            X = np.array(datafilter)
            #datawindow = np.array(x_train)
            #print(x_train)
            #dwX = datawindow.reshape(-1,40*8)
            
        #STD & PCA
            dnewX = modelpca.transform(X)
            realtime = model.predict(dnewX)
            print(realtime.reshape(-1,1))

        #print(pd.DataFrame(emg))
        for g, data in zip(self.graphs, emg_data):
            if len(data) < self.n:
                # Fill the left side with zeroes.
                data = np.concatenate([np.zeros(self.n - len(data)), data])
            g.set_ydata(data)
        plt.tight_layout()
        plt.draw()
    
    def main(self):
        while True:
            self.update_plot()
            plt.pause(1.0 / 30)

def main():
    myo.init()
    hub = myo.Hub()
    listener = EmgCollector(200)
    with hub.run_in_background(listener.on_event):
        Plot(listener).main()
    
   
while True :
    main()
#if __name__ == '__main__':

    


