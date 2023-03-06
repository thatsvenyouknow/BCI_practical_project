import numpy as np
import pandas as pd
from scipy.signal import filtfilt


def filter(data, filter_coeffs):
    '''
    Applies lowpass (42Hz), highpass (2Hz), and notchfilters (50 & 100Hz)

    Input:
    - data: 1d numpy array (1 channel)
    - filter_coeffs: dictionary containing filter coefficients for each filter

    Output:
    - filtered_data = filtered channel
    '''
    filtered_data = data
    for filter in filter_coeffs.keys():
        if type(filter_coeffs[filter]) == tuple:
            b, a = filter_coeffs[filter]
            filtered_data = filtfilt(b, a, filtered_data)
        else:
            filtered_data = filtfilt(filter_coeffs[filter], 1.0, filtered_data)
    return filtered_data


def preprocess(data_path, event_path, label_path, markers, chan_select, filter_coeffs, before = 0, fs = 250):
    '''
    Function for channel selection, filtering, segmenting data, and local baseline subtraction
    
    Input:
    - data_path: path to data of one subject (.npy)
    - event_path: path to events of same subject (.csv)
    - label_path: path to labels of same subject (.csv)
    - markers: dictionary containing the markers for each condition
    - chan_select: channels to be selected
    - filter_coeffs: filter coefficients to build and apply filtering
    - fs: sampling frequency

    Output:
    - segmented, corrected, and channel-selected data
    '''
    #load data & events
    data = np.load(data_path, allow_pickle=True)
    events = pd.read_csv(event_path)
    labels = pd.read_csv(label_path).values
    n_chan = chan_select.shape[0]

    #Select channels
    chans_bool = np.in1d(labels, chan_select)
    data = data[chans_bool, :]

    #Apply filtering
    for i in range(n_chan):
        data[i,:] = filter(data[i,:], filter_coeffs = filter_coeffs)

    #Create container for data
    segmented_data = {
        "control": [],
        "explosion": [],
        "fire": []
        }

    #iterate over 3 conditions and get time stamps
    for marker in markers.keys():
        index = np.where(events.values == markers[marker])[0]
        timings = events.samples[index].to_numpy() #timings of event

        #split data into samples (and subtract mean of signal 0.5s before)
        for time in timings:
            mean_before = np.reshape(np.mean(data[:,time-125:time-1], axis=1), (n_chan, 1))
            segmented_data[marker].append(data[:,time-before:time+250]-mean_before)
    
    return segmented_data