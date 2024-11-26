import pyroadacoustics as pyroad

import numpy as np
import scipy.signal
from scipy.io import wavfile
import matplotlib.pyplot as plt

# Sampling Frequency
fs = 8000

# Atmospheric Parameters
T = 20
p = 1
h_rel = 50

env = pyroad.Environment(fs = fs, temperature = T, pressure = p, rel_humidity = h_rel)

# Define source signal
t = np.arange(0,5,1/fs)

# 1. Sinusoidal Signal
f = 2000
src_signal = np.sin(2 * np.pi * f * t)

env.add_source(position = np.array([3,20,1]), signal=src_signal, trajectory_points=np.array([[3,20,1], [3,-20,1]]), source_velocity=np.array([5]))


# Add microphone array
mic_array = np.array([[0,0,1], [0,0.5,1]])
env.add_microphone_array(mic_array)

# Add noise signal

# 1. Default white noise
env.set_background_noise(SNR = 0)

interp_method = "Allpass"
include_reflection = True
include_air_absorption = True

env.set_simulation_params(interp_method, include_reflection, include_air_absorption)

# Run simulation
signal = env.simulate()

# Compute spectrogram of received signal
ff, tt, Sxx = scipy.signal.spectrogram(signal[0], fs = fs)

# Plots
fig, axs = plt.subplots(1,2, figsize = (15,5))

# Waveform Received Signal
axs[0].plot(np.arange(len(signal[0]))/fs, signal[0])
axs[0].set_title('Received Signal')
axs[0].set_xlabel('Time [s]')

# Spectrogram Received Signal
axs[1].pcolormesh(tt, ff, Sxx, shading='auto', vmax = 0.0004, rasterized=True)
axs[1].set_title('Spectrogram Received Signal')
axs[1].set_xlabel('Time [s]')
axs[1].set_ylabel('Frequency [Hz]')

# Save Audio File

# Limit loudness
signal[0] = signal[0] / max(abs(signal[0]))

wavfile.write('demo_audio.wav', fs, signal[0])