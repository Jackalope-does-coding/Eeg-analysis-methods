#Sandra Nitchi 2025
#This code creates individual slices of eeg around each displayed stimulus

import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

# Load EEG and stimulus data
eeg_df = pd.read_csv("EEG_recording_full.csv") #replace this with the filepath to your eeg recording csv
stim_df = pd.read_csv("psychopy_data.csv") #replace this with the filepath to your psychopy data csv

# EEG timestamps: convert Unix to datetime
eeg_df['timestamps'] = pd.to_datetime(eeg_df['timestamps'], unit='s')
eeg_df.set_index('timestamps', inplace=True)

# Stimulus timestamps: also convert Unix to datetime
stim_df['Aligned Timestamp'] = pd.to_datetime(stim_df['Marker Timestamp'], unit='s')


# Normalize EEG (excluding auxiliary channel)
channels = [ch for ch in eeg_df.columns if ch != 'Right AUX']
normalized_df = eeg_df[channels].apply(lambda x: (x - x.mean()) / x.std())

# Define time window around each stimulus
pre_time = pd.Timedelta(seconds=1)
post_time = pd.Timedelta(seconds=1.5)

# Loop through each stimulus and plot EEG segment
for _, row in stim_df.iterrows():
    ts = row['Aligned Timestamp']
    label = row['Stimulus']
    window_start = ts - pre_time
    window_end = ts + post_time
    segment_df = normalized_df.loc[window_start:window_end]

    plt.figure(figsize=(12, 6))
    for i, ch in enumerate(channels):
        offset = i * 10
        plt.plot(segment_df.index, segment_df[ch] + offset, label=ch)

    plt.axvline(x=ts, color='red', linestyle='--', label='Stimulus Marker')
    plt.title(f"EEG Around Stimulus '{label}' at {ts.time()}")
    plt.xlabel("Time")
    plt.ylabel("Normalized EEG (Offset)")
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()
