import numpy as np
import pyaudio
from scipy.signal import correlate
import librosa


def load_audiofile(file_path):
    signal, samplerate = librosa.load(file_path, sr=None, mono=False)
    return signal, samplerate


def find_loudest_signal(signals):
    # rms = np.sqrt(np.mean(signal**2))
    max_rms_values = [np.max(librosa.feature.rms(y=signal, frame_length=1024, hop_length=512)) for signal in signals]

    return np.argmax(max_rms_values) + 1


def calculate_earliest_signal(signals, samplerates):
    delays = [0]
    for i in range(1, len(signals)):
        if isinstance(samplerates, list):
            samplerate = samplerates[i]
        else:
            samplerate = samplerates

        len_diff = len(signals[0]) - len(signals[i])

        if len_diff > 0:
            signals[i] = np.pad(signals[i], (0, len_diff), 'constant')
        elif len_diff < 0:
            signals[0] = np.pad(signals[0], (0, -len_diff), 'constant')

        correlation = correlate(signals[0], signals[i], mode='full')

        delay_samples = np.argmax(correlation) - len(signals[0]) + 1

        delays.append(delay_samples / samplerate)

    return np.argmax(delays) + 1

mic_positions = np.array([
    [1, 0],
    [0.5, np.sqrt(3)/2],
    [-0.5, np.sqrt(3)/2],
    [-1, 0],
    [-0.5, -np.sqrt(3)/2],
    [0.5, -np.sqrt(3)/2]
])

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# audio = pyaudio.PyAudio()

# stream = audio.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK,
#                     stream_callback=process_audio)
#
# stream.start_stream()
#
# try:
#     while stream.is_active():
#         pass
# except KeyboardInterrupt:
#     stream.stop_stream()
#     stream.close()
#     audio.terminate()



# print("Выберите режим работы программы:"
#       "В реальном времени (По-умолчанию)"
#       "Работа с аудио-файлами")

file = load_audiofile('sounds/A1_CH_25_20.wav')

print(f"{find_loudest_signal(file[0])} сигнал/канал громче всех")
print(f"{calculate_earliest_signal(file[0], file[1])} сигнал пришёл раньше всех")