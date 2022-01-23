import random
from threading import Thread
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
    address = 0x48
    cmd = 0x40
    data = {}
    thermistor_thread = None
    run_threads = 1
    current_read = [0, 0, 0, 0]
    pin = {
        'therm1': [ 4, 1, 'gpHd1'],    #
        'therm2': [17, 1, 'gpHd2'],
        'therm3': [18, 1, 'bolr1'],
        'therm4': [27, 1, 'bolr2']
    }
    if arduino:
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        ser.reset_input_buffer()
        if ser.in_waiting > 0:
            line = str(ser.readline())
            #print(line)

    def init(self):
        #if self.onRpi:
        #    GPIO.setmode(GPIO.BCM)
        #    for therm in self.pin:
        #        if therm[1]:
        #            GPIO.setup(therm[0], GPIO.IN)
        #        else:
        #            GPIO.setup(therm[0], GPIO.OUT)
        #self.thermistor_thread = Thread(target=lambda: self.read_thermistors())
        #self.thermistor_thread.start()

    def exit(self):
        if self.onRpi:
            pass#GPIO.cleanup()
        self.run_threads = 0
        print('Exited')

    def read_thermistors(self):
        while self.run_threads:
            if self.onRpi and self.arduino:
                self.current_read = self.analog_read()
            else:
                self.current_read = []
                for x in range(6):
                    self.current_read.append(random.randrange(0, 10, 1))
            sleep(.05)

    def analog_read(self):
        avg = [0,0,0,0,0,0]
        iters = 5
        for average in range(iters):
            self.ser.reset_input_buffer()
            value = '0'
            while value == '0':
                results = []
                if self.ser.in_waiting > 0:
                    try:
                        self.ser.readline()
                        value = str(self.ser.readline()).replace("b'", '').replace(",\\r\\n'", '')
                        results= [float(x) for x in value.split(',')]
                        if len(results) < 6:
                            value = '0'
                        for idx in range(0,6):
                            if results[idx] > 1023:
                                value = '0'
                                break
                        avg = [avg[x] + results[x] for x in range(len(results))]
                    except:
                        #print("comms error")
                        value = '0'
                return [avg[idx]/iters for idx in range(len(avg))]

