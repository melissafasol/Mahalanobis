import numpy as np
import pandas as pd 
import scipy 
from statistics import mean

class SleepScorerPowerSpectrum:
    
    sampling_rate = 250.4
    nperseg = 1252
    
    def __init__(self, data_without_noise, channel, animal):
        self.data_without_noise = data_without_noise
        self.channel = channel
        self.animal = animal
        self.eeg_feature_df = []
        self.theta_feature_df = []
        self.emg_feature_df = []
        
    def average_psd(self):
        for data_array in self.data_without_noise:
            power_arrays = scipy.signal.welch(data_array, self.sampling_rate, window = 'hann', nperseg = self.nperseg) 
            power_array = power_arrays[1]
            frequency_array = power_arrays[0]
            power_data_1_20 = mean(power_array[0:100])
            power_data_5_9 = mean(power_array[29:41])
            if self.channel == 1:
                emg_feature = {'Frequency': [frequency_array[300:450]], 'EMG_Power': [power_array[300:450]],
                               'Animal_ID': [[self.animal]*150], 'Channel': [[self.channel]*150]}
                emg_feature_df = pd.DataFrame(data = emg_feature)
                return emg_feature_df
            else:
                eeg_feature = {'Frequency': [frequency_array[0:100]], 'EEG_Power': [power_array[0:100]],
                               'Animal_ID': [[self.animal]*100], 'Channel': [[self.channel]*100]}
                theta_feature = {'Frequency': [frequency_array[29:41]], 'Theta_Power': [power_array[29:41]],
                                 'Animal_ID': [[self.animal]*12], 'Channel': [[self.channel]*12]}
                eeg_feature_df = pd.DataFrame(data = eeg_feature)
                theta_feature_df = pd.DataFrame(data = theta_feature)
                return eeg_feature_df, theta_feature_df


class FeatureExtractionMahalanobis():
    
    def __init__(self, psd_per_epoch, frequency):
        self.psd_per_epoch = psd_per_epoch
        self.frequency = frequency 
    
    def bandpass_1_20(psd_per_epoch):
        pass
    
    def bandpass_theta(psd_per_epoch):
        pass 
    
    def emg_power(psd_per_epoch):
        pass