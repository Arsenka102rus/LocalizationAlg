import pyaudio

# Инициализация PyAudio
audio = pyaudio.PyAudio()

# Получение количества доступных устройств
device_count = audio.get_device_count()

print(f"Количество доступных аудио устройств: {device_count}")

# Перебор всех доступных устройств и вывод информации о них
for i in range(device_count):
    device_info = audio.get_device_info_by_index(i)
    if device_info['maxInputChannels'] > 0:  # Только устройства с входными каналами (микрофоны)
        print(f"Устройство {i}: {device_info['name']} - Входные каналы: {device_info['maxInputChannels']}")

# Закрытие PyAudio
audio.terminate()
