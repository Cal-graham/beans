from time import sleep, time
from copy import deepcopy
import threading
import numpy as np


if 1:
    import Adafruit_ADS1x15
    onRpi = 1
if 0:
    onRpi = 0


class SiteFrame:
    onRpi = onRpi
    raw_data = {}
    real_data = {}
    time_data = {}
    filter_data = {}
    run_adc_thread = 0
    adc_thread = None
    adc = []
    current_read = {}
    read_prev = {}
    read_avg = {}
    pins = {
        'pressure_br': '1.0',
        'temp_gh': '1.1',
        'temp_br': '1.2',
        #'gh4': 3
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
            sleep(5)
            print('Initialized')
        else:
            pass

    def exit(self):
        self.run_adc_thread = 0
        self.adc_thread.join()
        pass

    def comms(self):
        self.pull_readings(4)
        while self.run_adc_thread:
            self.pull_readings(0.5)
            print('readings:',len(self.raw_data['temp_br'])); self.limit_datapoints(200)

    def limit_datapoints(self, max):
        for key in self.pins.keys():
            while len(self.raw_data[key]) > max:
                self.raw_data[key].pop(0)
                self.time_data[key].pop(0)

    def pull_readings(self, seconds):
        atime = seconds/len(self.pins.keys()); # print('read data')
        for key in self.pins.keys():
            start = int(time())
            controller = self.adc[int(self.pins[key].split('.')[0])]
            pin = int(self.pins[key].split('.')[1])
            controller.start_adc(pin, gain=self.GAIN) #; loop = 0
            while time() - start < atime:
                self.raw_data[key].append(float(controller.get_last_result()/32767))
                self.time_data[key].append(float(time()%60)) # ; loop = loop + 1; print('Loops:', loop)
            controller.stop_adc()

    def update_data(self):
        for key in self.pins.keys():
            if 'temp' in key:
                self.real_data[key] = self.convert_temp(self.raw_data[key].copy())
                self.real_data[f'{key}_time'] = self.time_data[key][0:len(self.real_data[key])].copy()
            elif 'pressure' in key:
                self.real_data[key] = self.convert_pressure(self.raw_data[key].copy())
                self.real_data[f'{key}_time'] = self.time_data[key][0:len(self.real_data[key])].copy()
            else:
                self.real_data[key] = self.raw_data[key].copy()
                self.real_data[f'{key}_time'] = self.time_data[key][0:len(self.real_data[key])].copy()

    def smoothing(self):
        self.update_data()
        for key in self.pins.keys():
            '''ind = 0
            weight = []
            for value in self.real_data[f'{key}_time']:
                if value >= self.real_data[f'{key}_time'][0] and ind == 0:
                    weight.append((value - self.real_data[f'{key}_time'][0])/60)
                else:
                    weight.append((value - self.real_data[f'{key}_time'][0] + 60)/60)
                    ind = 1'''
            #print(self.raw_data['temp_br'][-1], self.real_data['temp_br'][-1], np.sum(weight))
            self.filter_data[key] = np.average(self.real_data[key]) #np.sum( np.multiply(self.real_data[key], weight) ) / np.sum( weight )
            #self.filter_data[key] = lowess(self.real_data[key], self.real_data[f'{key}_time'], frac=0.4)

    def pull_points(self):
        self.smoothing(); # print('smoothed data')
        results = {}
        for key in self.pins.keys():
            results[key] = self.filter_data[key] #list(self.filter_data[key][-1])[0]
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

