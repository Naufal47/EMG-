from matplotlib import pyplot as plt
from collections import deque
from threading import Lock, Thread
from numpy.core.numeric import full
import pandas as pd
import joblib
import myo
import numpy as np

#Filtering
import scipy.signal
from scipy import signal


def bandpass (data,chanel,pole,low,high ):
    
    samp_freq = 100  # Sample frequency (Hz)
    notch_freq = 50.0  # Frequency to be removed from signal (Hz)
    quality_factor = 10.0 # Quality factor
    #quality_factor = 100.0  # Quality factor
    b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)
    outputSignal = signal.filtfilt(b_notch, a_notch, chanel)
    
    b, a    = scipy.signal.butter(pole, [low, high], btype='band')
    filters = scipy.signal.lfilter(b, a, outputSignal)
    filters = np.array(filters)
    filters = pd.DataFrame(filters)
    
    '''plt.rcParams["figure.figsize"] = (15,5)
    plt.subplot(121)
    plt.plot(chanel, label ='nofilter');
    plt.legend();
    plt.subplot(122)
    plt.plot(filters);
    plt.legend();'''

    return filters

pole          = 5
low           = 0.8e-2
high          = 0.4166   #mengikuti arahan 500 Hz

#WINDOWING

def windowing(values, time_steps=40):
    output = []
    for i in range(len(values) - time_steps + 1):
        output.append(values[i : (i + time_steps)])
    return np.stack(output)
    #return output

#STANDARD SCALER
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA





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
