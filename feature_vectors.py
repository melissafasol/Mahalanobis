import os 
import pandas as pd
import numpy as np
import sys

sys.path.insert(0, '/home/melissa/PROJECT_DIRECTORIES/taini_main/scripts')
from GRIN2B_constants import start_time_GRIN2B_baseline, end_time_GRIN2B_baseline, br_animal_IDs
from preproc2_extractbrainstate import ExtractBrainStateIndices
from preproc1_preparefiles import PrepareFiles, LoadFromStart, PrepareGRIN2B, LoadGRIN2B
from preproc3_filter import Filter
from preproc4_power_spectrum_analysis import PowerSpectrum


directory_path = '/home/melissa/PREPROCESSING/GRIN2B/GRIN2B_numpy'
brain_state_number = 2
channel_number_list = [0,2,3,4,5,6,7,8,9,10,11,12,13,15]
power_two_brainstate_df = []
spectral_slope_two_brainstate_df = [] 

for animal in br_animal_IDs:
    prepare_GRIN2B = PrepareGRIN2B(directory_path, animal)
    recording, brain_state_1, brain_state_2 = prepare_GRIN2B.load_two_analysis_files()
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
        print(timevalues_array_1)
        print('all data loaded for ' + str(animal) + ' channel number ' + str(channelnumber))
        filter_1 = Filter(data_1, timevalues_array_1)
        filter_2 = Filter(data_2, timevalues_array_2)
        filtered_data_1 = filter_1.butter_bandpass()
        filtered_data_2 = filter_2.butter_bandpass()
        print('filtering complete')
        power_1 = PowerSpectrum(filtered_data_1)
        power_2 = PowerSpectrum(filtered_data_2)
        per_epoch_psd_1, frequency_1 = power_1.average_psd(average = 'False')
        per_epoch_psd_2, frequency_2 = power_2.average_psd(average = 'False')
        
        #need to add a function directly to power spectrum class to calculate features for sleep scorer 
        
        print(len(per_epoch_psd_1))
        print(len(frequency_1))
    