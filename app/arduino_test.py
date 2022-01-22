from time import sleep
import serial


def run():
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    while True:
        ser.reset_input_buffer(); sleep(0.1)
        value = 0
        while value == 0:
            if ser.in_waiting > 0:
                ser.readline(); value = ser.readline()
                print(value)
        sleep(1)


if __name__ == "__main__":
    run()

