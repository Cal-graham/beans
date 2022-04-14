from time import time
import numpy as np
from scipy import optimize as opt
from scipy import interpolate as interp

class Profiles:

    custom_profiles = {
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



    def gen_custom_profile_functions(self):
        graphs = [key for key in self.custom_profiles.keys()]
        for graph in graphs:
            sources = [key for key in self.custom_profiles[graph].keys() if 'func' not in key]
            for source in sources:
                        x = self.custom_profiles[graph][source][0]
                        y = self.custom_profiles[graph][source][1]; #print(x, y)
                        weights = []
                        for val in x:
                            if val < 30:
                                weights.append(0.5*((val/30)))
                            else:
                                weights.append(0.5*(np.abs(60-val)/30))
                        self.custom_profiles[graph][f'func_{source}'] = interp.LSQUnivariateSpline(x, y, [18, 22], k=2) #interp.UnivariateSpline(x, y, w=weights, s=0.25) #interp1d(x, y, kind='cubic', bounds_error=False, fill_value=0)
                        #opt.curve_fit(fit_func, x, y)
                        #self.custom_profiles[graph][f'func_{source}'] = fit_func.copy()


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

    def check_start(func):
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


