import socket
from samplebase import SampleBase
import re

def nm_to_rgb(wavelength):
    gamma = 0.8
    intensity_max = 255
    factor = 0
    red = green = blue = 0

    if 380 <= wavelength < 440:
        red = -(wavelength - 440) / (440 - 380)
        green = 0.0
        blue = 1.0
    elif 440 <= wavelength < 490:
        red = 0.0
        green = (wavelength - 440) / (490 - 440)
        blue = 1.0
    elif 490 <= wavelength < 510:
        red = 0.0
        green = 1.0
        blue = -(wavelength - 510) / (510 - 490)
    elif 510 <= wavelength < 580:
        red = (wavelength - 510) / (580 - 510)
        green = 1.0
        blue = 0.0
    elif 580 <= wavelength < 645:
        red = 1.0
        green = -(wavelength - 645) / (645 - 580)
        blue = 0.0
    elif 645 <= wavelength <= 780:
        red = 1.0
        green = 0.0
        blue = 0.0

    if 380 <= wavelength < 420:
        factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
    elif 420 <= wavelength <= 700:
        factor = 1.0
    elif 700 < wavelength <= 780:
        factor = 0.3 + 0.7 * (780 - wavelength) / (80)
    
    if red != 0:
        red = round(intensity_max * ((red * factor) ** gamma))
    if green != 0:
        green = round(intensity_max * ((green * factor) ** gamma))
    if blue != 0:
        blue = round(intensity_max * ((blue * factor) ** gamma))

    return red, green, blue

class FrequencyToColorServer(SampleBase):
    def __init__(self, *args, **kwargs):
        super(FrequencyToColorServer, self).__init__(*args, **kwargs)
        self.server_socket = None
        self.conn = None

    def setup_server(self):
        host = '0.0.0.0'
        port = 12345
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        print(f"Server is listening on {host}:{port}")
        self.conn, addr = self.server_socket.accept()
        print(f"Connected by {addr}")

    def run(self):
        self.setup_server()
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        try:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break

                # Attempt to decode and split the received data into individual frequency values
                data_str = data.decode('utf-8')
                frequency_str_list = re.findall(r'\d+\.\d+', data_str)  # Find all floating-point numbers in the string

                for freq_str in frequency_str_list:
                    try:
                        peak_frequency = float(freq_str)
                        print(f"Received Peak Frequency: {peak_frequency} Hz")
                        wavelength = 380 + (peak_frequency - 20) * (780 - 380) / (1000 - 20)
                        rgb_value = nm_to_rgb(wavelength)
                        print("RGB:", rgb_value)
                        self.offscreen_canvas.Fill(rgb_value[0], rgb_value[1], rgb_value[2])
                        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
                    except ValueError as e:
                        print(f"Error converting '{freq_str}' to float: {e}")
                        # Optionally log the error or take other corrective action here

        except KeyboardInterrupt:
            print("\nServer stopping")
        finally:
            self.conn.close()
            self.server_socket.close()

# Main function
if __name__ == "__main__":
    frequency_to_color_server = FrequencyToColorServer()
    if (not frequency_to_color_server.process()):
        frequency_to_color_server.print_help()