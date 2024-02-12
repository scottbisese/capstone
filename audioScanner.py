import pyaudio
import numpy as np
import socket

# Setup socket
host = '192.168.1.12'  # Server computer's IP address
port = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Initialize PyAudio
p = pyaudio.PyAudio()

# List all audio devices and print them
def list_devices():
    print("Available audio devices:")
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print(f"{i}: {dev['name']}")

list_devices()

# Set this based on the output from list_devices
apollo_index = 2  # Assuming Apollo Twin's index is 2

# Constants for the audio stream
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Sample rate
CHUNK = 1024  # Number of audio samples per frame

if apollo_index is None:
    print("Please set the 'apollo_index' variable to the index of your Apollo Twin device.")
else:
    # Open stream using the Apollo Twin
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=apollo_index)  # Use Apollo Twin for input

    print("Listening with Apollo Twin...")

    counter = 0
    try:
        while True:
            # Capture data
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            
            # Perform FFT and find peak frequency
            spectrum = np.fft.rfft(audio_data)
            freq_magnitude = np.abs(spectrum)
            peak_freq_index = np.argmax(freq_magnitude[1:]) + 1  # Ignore DC component
            true_peak_freq = peak_freq_index * RATE / CHUNK
            
            print(f"Peak Frequency: {true_peak_freq} Hz")
            
            # Send the peak frequency value as a string only when counter is even
            if counter % 2 == 0:
                client_socket.sendall(str(true_peak_freq).encode('utf-8'))
            counter += 1

    except KeyboardInterrupt:
        print("\nStopping")
    finally:
        # Cleanup
        stream.stop_stream()
        stream.close()
        p.terminate()
        client_socket.close()
