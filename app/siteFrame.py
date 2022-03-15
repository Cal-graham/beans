from time import sleep
import threading
import numpy as np

if 1:
    import Adafruit_ADS1x15
    onRpi = 1
if 0:
    onRpi = 0


class SiteFrame:
    onRpi = onRpi
    data = {}
    run_adc_thread = 0
    adc_thread = None
    adc1 = None
    adc2 = None
    current_read = {}
    read_prev = {}
    read_avg = {}
    pins2 = {
        'pressure_br': 0,
        'temp_gh': 1,
        'temp_br': 2,
        'gh4': 3
    }
    pins1 = {
        'br1': 0,
        'br2': 1,
        'br3': 2,
        'br4': 3
    }

    def __init__(self):
        if onRpi:
            self.adc1 = Adafruit_ADS1x15.ADS1115()
            self.adc2 = Adafruit_ADS1x15.ADS1115(address=0x49)
            self.GAIN = 1; print('Site Frame Initialized')
        if self.run_adc_thread == 0:
            self.run_adc_thread = 1
            self.adc_thread = threading.Thread(target=lambda: self.comms())
            self.adc_thread.start()
        else:
            pass

    def exit(self):
        self.run_adc_thread = 0
        self.adc_thread.join()
        pass

    def comms(self):
        read = {}
        for idx in range(10):
            read = self.read_all_pins(); #print(read)
            for key in read.keys():
                if key in self.data.keys():
                    self.data[key].append(read[key])
                else:
                    self.data[key] = [read[key]]
        self.current_read = read; self.read_prev = read;
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
                print(e)
                
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
        return 3950/np.log( ((1-read)*10**4/(read))/(10**5*np.exp(-3950/298)) ) - 273  #Celsius

    def convert_pressure(self, read):
        return (read*4.092 - 0.5)*50   #psi
    
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
            val.append(adc.get_last_result)
        print(val)
        adc.stop_adc()
        return np.average(val)
        
       
