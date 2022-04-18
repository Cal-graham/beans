from time import time
import csv
import os
import numpy as np
from scipy import optimize as opt
from scipy import interpolate as interp

class Profiles:
    all_profiles = {}
    backup_profiles = {
        'pressure':{
                'grouphead': [[0,10,18,20,22,40,60],[1,4.5,6,7.5,9,7.5,4.5]]
                },
        'temperature':{
                'boiler': [[0,10,20,30,40,50,60],[100,100,100,100,100,100,100]],
                'grouphead': [[0,10,20,30,40,50,60],[60,60,60,60,60,60,60]]
        },
        'flow':{
                'grouphead': [[0,2,4,10,20,30,32,34,60],[0.1,2,4,4,4,4,2,0.1,0]]
        }
        }
    custom_profiles = {}
    pro_file = 'pro_file.csv'

    def __init__(self):
        if not os.path.isfile(self.pro_file):
            self.pro_file = 'Documents/git-repos/beans/app/pro_file.csv'
        if 1:
            with open(self.pro_file, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    profile = {}
                    profile['name'] = row.pop(0)
                    profile['graph'] = row.pop(0)
                    profile['source'] = row.pop(0)
                    x = []; y = []
                    while len(row)!= 0:
                        x.append(float(row.pop(0))); y.append(float(row.pop(0)))
                    profile['data'] = [x,y]
                    self.all_profiles[profile['name']] = profile
                    if 'base' in profile['name']:
                        self.set_base(profile['name'])
        #print(self.custom_profiles)

    def set_base(self, profile_name):
        if profile_name in self.all_profiles.keys():
            if self.all_profiles[profile_name]['graph'] not in self.custom_profiles.keys():
                self.custom_profiles[self.all_profiles[profile_name]['graph']] = {}
                self.backup_profiles[self.all_profiles[profile_name]['graph']] = {}
            self.custom_profiles[self.all_profiles[profile_name]['graph']][self.all_profiles[profile_name]['source']] = self.all_profiles[profile_name]['data']
            self.backup_profiles[self.all_profiles[profile_name]['graph']][self.all_profiles[profile_name]['source']] = self.all_profiles[profile_name]['data']
        else:
            return 0

    def save_current_profiles(self, name, graph):
        for source in self.custom_profiles[graph].keys():
            self.save_profile(f'{name}_{source}', graph, source, self.custom_profiles[graph][source][0], self.custom_profiles[graph][source][1])
        return 1

    def save_profile(self, name, graph, source, xdata, ydata):
        row = [name, graph, source]
        while len(xdata) != 0:
            row.append(xdata.pop(0))
            row.append(ydata.pop(0))
        with open(self.pro_file, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(row)
        profile = {}
        profile['name'] = row.pop(0)
        profile['graph'] = row.pop(0)
        profile['source'] = row.pop(0)
        x = []; y = []
        while len(row)!= 0:
            x.append(row.pop(0)); y.append(row.pop(0))
        profile['data'] = [x,y]
        self.all_profiles[profile['name']] = profile
        return 1

    def current_custom_profile(self, graph):
        results = []
        for source in self.custom_profiles[graph].keys():
                result = []
                for index in range(len(self.custom_profiles[graph][source][0])):
                    result.append({
                                'x': self.custom_profiles[graph][source][0][index],
                                'y': self.custom_profiles[graph][source][1][index]
                    })
                results.append(result)
        return results



'''    def check_start(func):
        def wrapper(self, gen, time_, type=None):
            if 'start_time' not in gen.keys():
                tmp = gen.copy()
                tmp['start_time'] = time()
                if type == None:
                    return func(self, tmp, time_)
                else:
                    return func(self, tmp, time_, type)
            elif (time_ - gen['start_time']) > 60 :
                return 0
            else:
                if type == None:
                    return func(self, gen, time_)
                else:
                    return func(self, gen, time_, type)
        return wrapper

    @check_start
    def custom_profile(self, gen, time_, type):
        for key in self.custom_profiles.keys():
            if key in type:
                for key_ in self.custom_profiles[key].keys():
                    if key_ in type:
                        return str(self.custom_profiles[key][f'func_{key_}'](time_ - gen['start_time']))

        return 0

    @check_start
    def constant_temperature_boiler(self, gen, time_):
        return 100

    @check_start
    def constant_temperature_grouphead(self, gen, time_):
        return 60

    @check_start
    def constant_temperature_grouphead_X(self, gen, time_):
        if 'constant_temperature_X' not in gen.keys():
            return constant_temperature(gen, time_)
        return gen['constant_temperature_X']

    @check_start
    def constant_pressure_grouphead(self, gen, time_):
        return 16

    @check_start
    def constant_flow_grouphead(self, gen, time_):
        return 8

    @check_start
    def light_roast_pressure_grouphead(self, gen, time_):
        if time_ - gen['start_time'] < 18:
            return ( 0.093*(time_ - gen['start_time']) )**4 + 1
        else:
            return ( -0.0023*( (time_ - gen['start_time']) - 18)**2 ) + 9

    @check_start
    def light_roast_flow_grouphead(self, gen, time_):
        if time_ - gen['start_time'] < 0.1:
            return 0
        elif time_ - gen['start_time'] < 18:
            return 8
        else:
            return np.exp(20 - (time_ - gen['start_time']))


'''
