import os 
import numpy as np 
import matplotlib.pyplot as plt
from scipy import signal 
import sys
import mne
import pandas as pd

sys.path.insert(0, '/home/melissa/PROJECT_DIRECTORIES/GRIN2B/scripts')
from GRIN2B_constants import start_time_GRIN2B_baseline, end_time_GRIN2B_baseline, br_animal_IDs, seizure_free_IDs, GRIN_het_IDs
from prepare_files import PrepareGRIN2B, LoadGRIN2B, br_seizure_files, one_second_timebins
from filter import Filter


directory_npy_path = '/home/melissa/PREPROCESSING/GRIN2B/GRIN2B_numpy'
seizure_br_path = '/home/melissa/PREPROCESSING/GRIN2B/seizures'
channel_number_list =  [0,2,3,4,5,6,7,8,9,10,11,12,13,15]
save_path = '/home/melissa/RESULTS/Mahalanobis/FFT'
save_file_as = 'animal_364_fft.npy'
seizure_df = []

sampling_rate = 250.4
nperseg = 250

br_animal_IDs = ['364']
for animal in br_animal_IDs:
    prepare_GRIN2B = PrepareGRIN2B(directory_npy_path, animal)
    recording = prepare_GRIN2B.load_two_analysis_files(seizure = 'True')
    start_time_1, start_time_2 = prepare_GRIN2B.get_two_start_times(start_time_GRIN2B_baseline)
    end_time_1, end_time_2 = prepare_GRIN2B.get_end_times(end_time_GRIN2B_baseline)
    os.chdir(seizure_br_path)
    br_1 = pd.read_csv('GRIN2B_' + str(animal) + '_BL1_Seizures.csv')
    br_2 = pd.read_csv('GRIN2B_' + str(animal) + '_BL2_Seizures.csv')
    zipped_timevalues_1 = br_seizure_files(br_1, sampling_rate)
    if len(zipped_timevalues_1) > 0:
        for channelnumber in channel_number_list:
            load_GRIN2B = LoadGRIN2B(recording, start_time_1, start_time_2, end_time_1, end_time_2, channelnumber)
            data_1, data_2 = load_GRIN2B.load_GRIN2B_from_start()
            timevalues_1 = one_second_timebins(zipped_timevalues_1,  epoch_length = int(250.4))
            filter_1 = Filter(data_1, timevalues_1)
            filtered_data_1 = filter_1.butter_bandpass(seizure = 'True')
print('data filtered')

fft_entire_signal = []
for array in filtered_data_1:
    windowed_entire_signal = [np.hamming(250)*array for array in filtered_data_1]
    slices = np.vstack(windowed_entire_signal)
    X = np.fft.fft(slices, axis = 0)
    log_X = np.log(np.abs(X))
    fft_entire_signal.append(log_X)
    print('fft calculated' + str([array]))

fft_concat = np.vstack(fft_entire_signal)
os.chdir(save_path)
np.save(save_file_as, fft_concat)
print('files saved')