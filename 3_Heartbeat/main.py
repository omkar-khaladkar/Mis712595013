import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Load audio file
fs, data = wavfile.read("heartbeat11.wav")

# Convert to mono if stereo
if data.ndim > 1:
    data = data[:, 0]

# Normalize
data = data / np.max(np.abs(data))

# Time axis
time = np.arange(len(data)) / fs

# --- Schmitt Trigger Beat Detection ---
high_thresh = 0.4
low_thresh = 0.1
beat_indices = []
state = 0  # 0 = waiting, 1 = detected

for i in range(len(data)):
    if state == 0 and data[i] > high_thresh:
        beat_indices.append(i)
        state = 1
    elif state == 1 and data[i] < low_thresh:
        state = 0

# Convert beat indices to time
beat_times = np.array(beat_indices) / fs

# --- Calculations ---
total_beats = len(beat_times)
duration_sec = len(data) / fs
beats_per_min = (total_beats / duration_sec) * 60

# Beats per 10 seconds
beats_per_10sec = []
for i in range(0, int(duration_sec), 10):
    count = np.sum((beat_times >= i) & (beat_times < i + 10))
    beats_per_10sec.append(count)

# --- Output ---
print(f"Total Beats: {total_beats}")
print(f"Duration (sec): {duration_sec:.2f}")
print(f"Beats per Minute (BPM): {beats_per_min:.2f}")
print("Beats per 10 seconds:", beats_per_10sec)

# --- Plot waveform with detected beats ---
plt.figure(figsize=(12, 4))
plt.plot(time, data, label="Heartbeat Signal")
plt.plot(beat_times, data[beat_indices], 'ro', label="Detected Beats")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.title("Heartbeat Detection using Schmitt Trigger")
plt.legend()
plt.tight_layout()
plt.show()
