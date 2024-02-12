# capstone
### 2/11/2024

## so what you need is

### 1. clone the rpi-rgb-matrix library from github.com/hzeller

### 2. move s2l.py into the rpi-rgb-matrix/bindings/python/samples/ folder and run it from terminal/command line with "sudo python3 test6.py --led-cols=64 --led-rows=32 --led-gpio-mapping=adafruit-hat --led-slowdown-gpi=3" (if on raspberry pi 4 you need the led slowdown flag and 3 as a value)

### 3. brew install supercollider on the not pi computer

### 4. run polyphony.scd once you plug in your midi device

### 5. find the ip address of your pi on your network by running "ip addr show" in the CLI/terminal  should be to the right of inet under wlan0.

### 6. enter ip address in fftSender.py code, in s2l it will be 0.0.0.0 and the same port.

### 7. run the receiving s2l.py code first and it will say 'server is listening on 0.0.0.0:12345'

### 8. make sure the polyphony.scd is running on supercollider and then...

### 9. run 