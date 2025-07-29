#Sandra Nitchi 2025
#This code analyses the data and displays only the overlapping time as a plot

import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

# === Load EEG Data ===
eeg_df = pd.read_csv("EEG_recording_full.csv") #replace this text with the filepath to your egg csv

# === Load Markers  ===
stim_df = pd.read_csv("psychopy_data.csv") #replace this text with the filepath to your psychopy csv

# EEG timestamps: convert Unix to datetime
eeg_df['timestamps'] = pd.to_datetime(eeg_df['timestamps'], unit='s')
eeg_df.set_index('timestamps', inplace=True)

# Stimulus timestamps: also convert Unix to datetime
stim_df['Aligned Timestamp'] = pd.to_datetime(stim_df['Marker Timestamp'], unit='s')


# === Normalize EEG Channels ===
channels = [ch for ch in eeg_df.columns if ch != 'Right AUX']
normalized_df = eeg_df[channels].apply(lambda x: (x - x.mean()) / x.std())

# === Dynamically set task window based on markers ===
start_time = stim_df['Aligned Timestamp'].min()
end_time = stim_df['Aligned Timestamp'].max()

# === Filter EEG and stimulus data to actual task window ===
task_eeg_df = normalized_df.loc[start_time:end_time]
task_stim_df = stim_df[(stim_df['Aligned Timestamp'] >= start_time) &
                       (stim_df['Aligned Timestamp'] <= end_time)]

# === Plotting ===
plt.figure(figsize=(15, 8))

for i, ch in enumerate(channels):
    offset = i * 10
    plt.plot(task_eeg_df.index, task_eeg_df[ch] + offset, label=ch)

for _, row in task_stim_df.iterrows():
    ts = row['Aligned Timestamp']
    label = row['Stimulus']
    color = 'blue'
    plt.axvline(x=ts, color=color, linestyle='--', alpha=0.6)
    plt.text(ts, offset + 5, label, rotation=90, fontsize=8, color=color)

plt.title("EEG During Oddball Task (Stimulus-Aligned)")
plt.xlabel("Time")
plt.ylabel("Normalized EEG (Vertically Offset)")
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()
