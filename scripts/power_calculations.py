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


    def harmonics_psd(self):
        for data_array in self.data_without_noise:
            power_arrays = scipy.signal.welch(data_array, self.sampling_rate, window = 'hann', nperseg = self.nperseg) 
            power_array = power_arrays[1]
            frequency_array = power_arrays[0]
            power_data_theta = mean(power_array[30:40])
            power_data_2_harmonic = mean(power_array[60:80])
            power_data_3_harmonic = mean(power_array[120:160])
            theta_feature = {'Frequency': [6], 'Theta_Power': [power_data_theta],
                               'Animal_ID': [self.animal], 'Channel': [self.channel]}
            harmonic_2_feature = {'Frequency': [12], 'Theta_Power': [power_data_2_harmonic],
                                 'Animal_ID': [self.animal], 'Channel': [self.channel]}
            harmonic_3_feature = {'Frequency': [24], 'Theta_Power': [power_data_3_harmonic],
                                 'Animal_ID': [self.animal], 'Channel': [self.channel]}
            theta_feature_df = pd.DataFrame(data = theta_feature)
            harmonic_2_feature_df = pd.DataFrame(data = harmonic_2_feature)
            harmonic_3_feature_df = pd.DataFrame(data = harmonic_3_feature)
            return theta_feature_df, harmonic_2_feature_df, harmonic_3_feature_df



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