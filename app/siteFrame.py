from time import sleep, time
import threading
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess


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
            self.limit_datapoints(2000)
            
        '''read = {}
        for idx in range(10):
            read = self.read_all_pins()
            for key in read.keys():
                if key in self.data.keys():
                    self.data[key].append(read[key])
                else:
                    self.data[key] = [read[key]]
        self.current_read = read 
        self.read_prev = read
        print(f'Initial Reading: {read}')
        while self.run_adc_thread:
            try:
                read = self.read_all_pins()
                for key in read.keys():
                    self.data[key].pop(0)
                    self.data[key].append(read[key])
                    self.read_avg[key] = np.average(self.data[key])
                    if np.abs(read[key] - self.read_prev[key]) > 5:
                        read[key] = self.read_prev[key]
                    elif np.abs(read[key] - self.read_avg[key]) > 20:    
                        read[key] = self.read_avg[key]
                self.current_read = read
                self.read_prev = self.current_read
            except Exception as e:
                print(e)'''
        
    def limit_datapoints(self, max):
        for key in self.pins.keys():
            if len(self.raw_data[key]) > max:
                del self.raw_data[key][0:len(self.raw_data[key])-max]; del self.time_data[key][0:len(self.raw_data[key])-max]
                
    def pull_readings(self, seconds):
        atime = seconds/len(self.pins.keys())
        for key in self.pins.keys():
            start = int(time())
            controller = self.adc[int(self.pins[key].split('.')[0])]
            pin = int(self.pins[key].split('.')[1])
            controller.start_adc(pin, gain=self.GAIN)
            while int(time()) - start < atime:
                self.raw_data[key].append(float(controller.get_last_result()/32767))
                self.time_data[key].append(float(time()%60))
            controller.stop_adc()
           
    def update_data(self):
        for key in self.pins.keys():
            if 'temp' in key:
                self.real_data[key] = self.convert_temp(self.raw_data[key].copy()); self.real_data[f'{key}_time'] = self.time_data[key].copy()
            if 'pressure' in key:
                self.real_data[key] = self.convert_pressure(self.raw_data[key].copy()); self.real_data[f'{key}_time'] = self.time_data[key].copy()
            else:
                self.real_data[key] = self.raw_data[key].copy(); self.real_data[f'{key}_time'] = self.time_data[key].copy()
   
    def smoothing(self):
        self.update_data()
        for key in self.pins.keys():
            self.filter_data[key] = lowess(self.real_data[key], self.real_data[f'{key}_time'], frac=0.4)
   
    def pull_points(self):
        self.smoothing()
        results = {}
        for key in self.pins.keys():
            results[key] = self.filter_data[key][-1]
        results['time'] = self.time_data['pressure_br']
        
    def read_all_pins(self):
        result = {}
        read = self.analog_read()
        for key in read.keys():
            if 'temp' in key:
                result[key] = self.convert_temp(read[key])
            elif 'pressure' in key:
                result[key] = self.convert_pressure(read[key])
            else:
                result[key] = read[key]
        return result
    
    def convert_temp(self, read):
        return 3950/np.log( np.divide( np.divide( np.multiply( np.add(read, -1), 10**4), (read) ), 10**5*np.exp(-3950/298) ) ) - 273  #Celsius

    def convert_pressure(self, read):
        return np.multiply( np.subtract( np.multiply(read, 4.092), 0.5), 50)   #psi
    
    def analog_read(self):
        result = {}
        self.atime = 0.05
        if onRpi:
            for key in self.pins1.keys():
                result[key] = self.averaged_read(self.adc1, self.pins1[key]) #np.average([self.adc1.read_adc(self.pins1[key], gain=self.GAIN)/32767 for x in range(10)])
            for key in self.pins2.keys():
                result[key] = self.averaged_read(self.adc2, self.pins2[key]) #np.average([self.adc2.read_adc(self.pins2[key], gain=self.GAIN)/32767 for x in range(10)])
            return result
        else:
            for key in self.pins1.keys():
                result[key] = np.random.rand(1)[0]
            for key in self.pins2.keys():
                result[key] = np.random.rand(1)[0]
            return result

    def averaged_read(adc, pin):
        start = time.time()
        adc.start_adc(pin, gain=self.GAIN)
        val = []
        while start - time.time() < self.atime:
            val.append(adc.get_last_result())
        print(val)
        adc.stop_adc()
        return np.average(val)
        
       
