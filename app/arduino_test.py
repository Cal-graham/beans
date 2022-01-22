from time import sleep
import serial


def run():
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    while True:
        ser.reset_input_buffer();
        value = '0'
        while value == '0':
            if ser.in_waiting > 0:
                ser.readline()
                try:
                    value = str(ser.readline()).replace("b'", '').replace(",\\r\\n'", '')
                    print(value)
                    print(value.split(','))
                except:
                    print("comms error")
                    value = '0'; sleep(1)
        sleep(1)


if __name__ == "__main__":
    run()

