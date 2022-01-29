from time import sleep
import threading
import numpy as np


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
    data = []
    numthreads = 0
    run_thread = 0
    thread = None
    current_read = []
    read_prev = []
    read_avg = []
    if arduino:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.reset_input_buffer()
        if ser.in_waiting > 0:
            line = str(ser.readline())

    def init(self):
        if self.run_thread == 0:
            self.run_thread = 1
            self.thread = threading.Thread(target=lambda: self.comms())
            self.thread.start()
        else:
            pass

    def exit(self):
        self.run_thread = 0
        self.thread.join()
        pass

    def comms(self):
        self.numthreads += 1
        read = []
        for idx in range(10):
            read = self.analog_read()
            self.data.append(read)
        self.read_avg = list(np.mean(self.data, 1))
        self.read_prev = self.read_avg
        print(f'Starting mean values: {self.read_avg}')
        while self.run_thread:
            try:
                self.current_read = self.analog_read()
                for idx in range(0,len(self.current_read)):
                    if np.abs(self.current_read[idx] - self.read_avg[idx]) > 200:
                        self.current_read[idx] = self.read_avg[idx]
                    else:
                        pass #print('within range')
                    if np.abs(self.current_read[idx] - self.read_prev[idx]) > 20:
                        self.current_read[idx] = self.read_avg[idx]
                #print(self.current_read, self.read_avg, self.read_prev)
                self.data.append(self.current_read)
                self.data.pop(0)
                self.read_prev = self.current_read
                if len(self.data) != 1:
                    temp = list(np.mean(np.array(self.data), 0))
                    self.read_avg = temp #; print(self.numthreads)
                else:
                    pass #print(len(self.data))
            except Exception as e:
                print(e); print(len(self.data))
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
                sleep(0.1)
            #self.read_prev = read
            return read
        else:
            return list(np.random.rand(6))
