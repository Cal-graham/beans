from flask import render_template
import random
import math
from threading import Thread
from time import sleep
if 1:
    #import smbus
    import RPi.GPIO as GPIO
    bus = smbus.SMBus(1)
    onRpi = 1
else:
    bus = None
    onRpi = 0


class SiteFrame:
    onRpi = onRpi
    bus = bus
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

    def init(self):
        if self.onRpi:
            GPIO.setmode(GPIO.BCM)
            for therm in self.pin:
                if therm[1]:
                    GPIO.setup(therm[0], GPIO.IN)
                else:
                    GPIO.setup(therm[0], GPIO.OUT)
        self.thermistor_thread = Thread(target=lambda: self.read_thermistors())
        self.thermistor_thread.start()

    def exit(self):
        if self.onRpi:
            GPIO.cleanup()
        self.run_threads = 0
        print('Exited')

    def read_thermistors(self):
        while self.run_threads:
            result = []
            for key in self.pin.keys():
                if self.onRpi:
                    result.append(self.therm_read(self.pin[key][0]))
                else:
                    result.append(random.randrange(0, 10, 1))
            for idx, reading in enumerate(result):
                self.current_read[idx] = self.current_read[idx] + (reading - 5)/10
            sleep(.5)

    def therm_read(self, chn):
        voltage = self.analog_read(chn) / 255.0 * 3.3
        ratio = 10 * voltage / (3.3 - voltage)
        kelvin = 1 / (1 / (273.15 + 25) + math.log(ratio / 10) / 3950.0)
        celsius = kelvin - 273.15
        return celsius

    def analog_read(self, chn):
        #value = self.bus.read_byte_data(self.address, self.cmd + chn)
        value = GPIO.input(chn)
        return value


