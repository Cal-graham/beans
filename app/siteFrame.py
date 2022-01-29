from time import sleep


if 1:
    import serial
    onRpi = 1
    arduino = 1
if 0:
    print('No GPIO import')
    arduino = 0
    onRpi = 0


class SiteFrame:
    onRpi = onRpi
    arduino = arduino
    current_read = []
    read_prev = [1, 1, 1, 1, 1, 1]
    if arduino:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.reset_input_buffer()
        if ser.in_waiting > 0:
            line = str(ser.readline())

    def init(self):
        pass

    def exit(self):
        pass

    def analog_read(self):
        if arduino:
            self.ser.reset_input_buffer()
            value = '0'
            read = []
            while value == '0':
                if self.ser.in_waiting > 0:
                    try:
                        value = str(self.ser.readline()).replace("b'", '').replace(",\\r\\n'", '')
                        read = [float(x) for x in value.split(',')]
                        if len(read) < 6:
                            value = '0'
                            read = []
                        for idx in range(0, 6):
                            if read[idx] > 1023:
                                value = '0'
                                read = []
                    except:
                        value = '0'
                sleep(0.05)
            self.read_prev = read
            return read
        else:
            return [1, 1, 1, 1, 1, 1]
