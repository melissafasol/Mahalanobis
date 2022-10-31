import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d



#1. calculate three power variables 

#power_1 
#power_2
#power_3

#375 - LOAD DATA 
os.chdir('/home/melissa/RESULTS/GRIN2B')

REM = pd.read_csv('baseline_REM_power.csv')
REM_375_eeg = REM[(REM['Animal_ID'] == 375) &  (REM['Channel'] == 4)]
os.chdir('/home/melissa/RESULTS/GRIN2B/mahalanobis')
REM_375_emg = pd.read_csv('emg_REM_power_375.csv')


os.chdir('/home/melissa/RESULTS/GRIN2B')
nonREM = pd.read_csv('baseline_nonREM_power.csv')
nonREM_375_eeg = nonREM[(nonREM['Animal_ID'] == 375) &  (nonREM['Channel'] == 4)]
os.chdir('/home/melissa/RESULTS/GRIN2B/mahalanobis')
nonREM_375_emg = pd.read_csv('emg_nonREM_power_375.csv')


os.chdir('/home/melissa/RESULTS/GRIN2B')
wake = pd.read_csv('baseline_wake_power.csv')
wake_375_eeg = wake[(wake['Animal_ID'] == 375) &  (wake['Channel'] == 4)]
os.chdir('/home/melissa/RESULTS/GRIN2B/mahalanobis')
wake_375_emg = pd.read_csv('emg_wake_power_375.csv')

#filter the data into (1) 1 - 20Hz, (2) 5.8 - 8.2, (3) emg 60-90

REM_eeg_20_cutoff =  REM_375_eeg[(REM_375_eeg['Frequency']>1) & (REM_375_eeg['Frequency'] < 20)]
nREM_eeg_20_cutoff = nonREM_375_eeg[(nonREM_375_eeg['Frequency']>1) & (nonREM_375_eeg['Frequency'] < 20)]
wake_eeg_20_cutoff = wake_375_eeg[(wake_375_eeg['Frequency']>1) & (wake_375_eeg['Frequency'] < 20)]

theta_REM_cutoff = REM_375_eeg[(REM_375_eeg['Frequency']>5.8) & (REM_375_eeg['Frequency'] < 8.2)]
theta_nREM_cutoff = nonREM_375_eeg[(nonREM_375_eeg['Frequency']>5.8) & (nonREM_375_eeg['Frequency'] < 8.2)]
theta_wake_cutoff = wake_375_eeg[(wake_375_eeg['Frequency']>5.8) & (wake_375_eeg['Frequency'] < 8.2)]

emg_cutoff_REM = wake_375_emg[(REM_375_emg['Frequency']>60) & (REM_375_emg['Frequency'] < 90)]
emg_cutoff_nREM = wake_375_emg[(nonREM_375_emg['Frequency']>60) & (nonREM_375_emg['Frequency'] < 90)]
emg_cutoff_wake = wake_375_emg[(wake_375_emg['Frequency']>60) & (wake_375_emg['Frequency'] < 90)]


#2. transform the data from a 2d input space to a 3D feature space to separate data linearly

#create 3 dimensional vectors with averages to plot on 3d plot in matplotlib
r_20_npy = REM_eeg_20_cutoff['Power'].to_numpy().mean()
r_theta_npy = theta_REM_cutoff['Power'].to_numpy().mean()
r_emg_npy = emg_cutoff_REM['Power'].to_numpy().mean()


print(r_20_npy, r_theta_npy, r_emg_npy)


#fig = plt.figure()
#ax.scatter3D(r_emg_reshape, r_20_reshape, r_theta_npy, c=r_theta_npy, cmap='Greens')
#ax = plt.axes(projection='3d')
#plt.show()

#3. find the centroid of each variable 



#4. fit the Gaussian distribution



#5. from Gaussian distribution find the covariance matrices



#6. calculate Mahalonobis distance from a given epoch to each cluster