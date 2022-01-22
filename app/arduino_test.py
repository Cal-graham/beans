from time import sleep
import serial


ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
while True:
    ser.reset_input_buffer()
    value = 0
    while value == 0:
        if ser.in_waiting > 0:
            value = ser.readline().decode('utf-8').rstrip()
            print(value)
    sleep(1)




