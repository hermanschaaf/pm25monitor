import serial
import time
import os
from Adafruit_IO import Client

ser = serial.Serial('/dev/ttyUSB0')

ADAFRUIT_KEY = os.environ.get("ADAFRUIT_KEY")
ADAFRUIT_SECRET = os.environ.get("ADAFRUIT_SECRET")

aio = Client(ADAFRUIT_KEY, ADAFRUIT_SECRET) if ADAFRUIT_KEY else None 

i = 0
while True:
    data = []
    ser.reset_input_buffer()
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)

    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10

    print(f"PM2.5: {pmtwofive}   PM10: {pmten}")

    if aio and i % 10 == 0:
        aio.send('pmtwofive', pmtwofive)
        aio.send('pmten', pmten)

    i += 1
    time.sleep(1)