from time import sleep, time
from copy import deepcopy
import threading
import numpy as np
import requests


if 1:
    import Adafruit_ADS1x15
    onRpi = 1
if 0:
    onRpi = 0


class SiteFrame:
    onRpi = onRpi
    reading_limit = 50
    raw_data = {}
    real_data = {}
    time_data = {}
    filter_data = {}
    run_adc_thread = 0
    run_smoothing_thread = 0
    last_pressure_alert = 0
    adc_thread = None
    smoothing_thread = None
    adc = []
    pins = {
        'pressure_boiler': '1.0',
        'temperature_grouphead': '1.1',
        'temperature_boiler': '1.2',
        'flow_grouphead': '1.3'
    }

    def __init__(self):
        if onRpi:
            self.adc.append(Adafruit_ADS1x15.ADS1115())
            self.adc.append(Adafruit_ADS1x15.ADS1115(address=0x49))
            self.GAIN = 1
            print('Site Frame Initializing...')
            for key in self.pins.keys():
                self.raw_data[key] = []
                self.real_data[key] = []
                self.filter_data[key] = []
                self.time_data[key] = []
        if self.run_adc_thread == 0:
            self.run_adc_thread = 1
            self.adc_thread = threading.Thread(target=lambda: self.comms())
            self.adc_thread.start()
        if self.run_smoothing_thread == 0:
            self.run_smoothing_thread = 1
            self.smoothing_thread = threading.Thread(target=lambda: self.smooth())
            self.smoothing_thread.start()
        sleep(1)
        print('Initialized')

    def exit(self):
        self.run_adc_thread = 0
        self.adc_thread.join()
        pass

    def comms(self):
        self.pull_readings(4)
        while self.run_adc_thread:
            self.pull_readings(0.1)
            #print('readings:',len(self.raw_data['temp_br']))
            self.limit_datapoints(self.reading_limit)

    def limit_datapoints(self, max):
        for key in self.pins.keys():
            while len(self.raw_data[key]) > max:
                self.raw_data[key].pop(0)
                self.time_data[key].pop(0)

    def pull_readings(self, seconds):
        atime = seconds/len(self.pins.keys())
        for key in self.pins.keys():
            controller = self.adc[int(self.pins[key].split('.')[0])]
            pin = int(self.pins[key].split('.')[1])
            controller.start_adc(pin, gain=self.GAIN) #; count = 0
            start = time()
            while time() - start < atime:
                self.raw_data[key].append(float(controller.get_last_result()/32767))
                self.time_data[key].append(float(time()%60)) #; count = count + 1
            controller.stop_adc() #; print('Updated ', key, count)

    def smooth(self):
        while self.run_smoothing_thread:
            self.update_data()
            for key in self.pins.keys():
                self.filter_data[key] = np.average(self.real_data[key])
                if 'pressure' in key:
                    if self.filter_data[key] > 20:
                        self.pressure_alert()

    def update_data(self):
        for key in self.pins.keys():
            if 'temp' in key:
                self.real_data[key] = self.convert_temp(self.raw_data[key][0:self.reading_limit].copy())
                self.real_data[f'{key}_time'] = self.time_data[key][0:self.reading_limit].copy()
            elif 'pressure' in key:
                self.real_data[key] = self.convert_pressure(self.raw_data[key][0:self.reading_limit].copy())
                self.real_data[f'{key}_time'] = self.time_data[key][0:self.reading_limit].copy()
            else:
                self.real_data[key] = self.raw_data[key][0:self.reading_limit].copy()
                self.real_data[f'{key}_time'] = self.time_data[key][0:self.reading_limit].copy()

    def smooth_data(self):
        for key in self.pins.keys():
            weight = np.exp(np.linspace(0, 1, 100))
            self.filter_data[key] = np.sum( np.multiply(self.real_data[key], weight) ) / np.sum( weight )

    def pull_points(self):
        self.update_data()
        self.smooth_data()
        results = {}
        for key in self.pins.keys():
            results[key] = self.filter_data[key]
        return results

    def convert_temp(self, read):
        result = []
        for value in read:
            result.append(3950/np.log( ((1-value)*10**4/value)/(10**5*np.exp(-3950/298)) ) - 273 - 2)
        return result

    def convert_pressure(self, read):
        result = []
        for value in read:
            result.append((value*4.092 - 0.5)*50)
        return result
    
    def pressure_alert(self):
        if time() - self.last_pressure_alert > 5*60:
            self.notify('ALERT - High Pressure'); self.last_pressure_alert = time()

    def notify(self, message):
        requests.post(
            'https://maker.ifttt.com/trigger/notification/with/key/fEcmU_SfuJkXpOY0Ty4fYVzFsEg0L1UP8X8364OZ12q', 
                      json={"value1":message,"value2":"none","value3":"none"})
    
