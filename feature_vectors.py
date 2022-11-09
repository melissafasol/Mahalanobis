import os 
import pandas as pd
import numpy as np
import sys

from power_calculations import SleepScorerPowerSpectrum

sys.path.insert(0, '/home/melissa/PROJECT_DIRECTORIES/taini_main/scripts/Preprocessing')
from preproc2_extractbrainstate import ExtractBrainStateIndices
from preproc3_filter import Filter

sys.path.insert(0, '/home/melissa/PROJECT_DIRECTORIES/GRIN2B')
from GRIN2B_constants import start_time_GRIN2B_baseline, end_time_GRIN2B_baseline, br_animal_IDs
from prepare_files import PrepareFiles, LoadFromStart, PrepareGRIN2B, LoadGRIN2B

eeg_power = []
theta_power = []
emg_power = []


directory_path = '/home/melissa/PREPROCESSING/GRIN2B/GRIN2B_numpy'
brain_state_number = 2
channel_number_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,15]


for animal in br_animal_IDs:
    prepare_GRIN2B = PrepareGRIN2B(directory_path, animal)
    recording, brain_state_1, brain_state_2 = prepare_GRIN2B.load_two_analysis_files(seizure = 'False')
    start_time_1, start_time_2 = prepare_GRIN2B.get_two_start_times(start_time_GRIN2B_baseline)
    end_time_1, end_time_2 = prepare_GRIN2B.get_end_times(end_time_GRIN2B_baseline)
    for channelnumber in channel_number_list:
        load_GRIN2B = LoadGRIN2B(recording, start_time_1, start_time_2, end_time_1, end_time_2, channelnumber)
        data_1, data_2 = load_GRIN2B.load_GRIN2B_from_start()
        extract_brain_state_1 = ExtractBrainStateIndices(brainstate_file = brain_state_1, brainstate_number = brain_state_number)
        extract_brain_state_2 = ExtractBrainStateIndices(brainstate_file = brain_state_2, brainstate_number = brain_state_number)
        epoch_indices_1 = extract_brain_state_1.load_brainstate_file()
        epoch_indices_2 = extract_brain_state_2.load_brainstate_file()
        timevalues_array_1 = extract_brain_state_1.get_data_indices(epoch_indices_1)
        timevalues_array_2 = extract_brain_state_2.get_data_indices(epoch_indices_2)
        print('all data loaded for ' + str(animal) + ' channel number ' + str(channelnumber))
        filter_1 = Filter(data_1, timevalues_array_1)
        filter_2 = Filter(data_2, timevalues_array_2)
        filtered_data_1 = filter_1.butter_bandpass()
        filtered_data_2 = filter_2.butter_bandpass()
        print('filtering complete')
        if channelnumber == 1:
            power_1 = SleepScorerPowerSpectrum(filtered_data_1, channel = channelnumber, animal = animal)
            power_2 = SleepScorerPowerSpectrum(filtered_data_2, channel = channelnumber, animal = animal)
            emg_psd_1 = power_1.average_psd()
            emg_psd_2 = power_2.average_psd()
            emg_power.append(emg_psd_1)
            print(emg_power)
            emg_power.append(emg_psd_2)
        else:
            power_1 = SleepScorerPowerSpectrum(filtered_data_1, channel = channelnumber, animal = animal)
            power_2 = SleepScorerPowerSpectrum(filtered_data_2, channel = channelnumber, animal = animal)
            eeg_psd_1, theta_psd_1 = power_1.average_psd()
            eeg_psd_2, theta_psd_2 = power_2.average_psd()
            eeg_power.append(eeg_psd_1)
            print(eeg_power)
            eeg_power.append(eeg_psd_2)
            theta_power.append(theta_psd_1)
            print(theta_power)
            theta_power.append(theta_psd_2)
            
average_emg = pd.concat(emg_power, axis = 0).drop_duplicates().reset_index(drop=True)
average_eeg = pd.concat(eeg_power, axis = 0).drop_duplicates().reset_index(drop=True)
average_theta = pd.concat(theta_power, axis = 0).drop_duplicates().reset_index(drop=True)

os.chdir('/home/melissa/RESULTS/Mahalanobis')
average_emg.to_csv(str(brain_state_number)+ '_average_emg.csv', index=True)
average_eeg.to_csv(str(brain_state_number)+ '_average_eeg.csv', index=True)
average_theta.to_csv(str(brain_state_number)+ '_average_theta.csv', index=True)