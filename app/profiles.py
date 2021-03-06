from time import time
import numpy as np


def check_start(func):
    def wrapper(gen, time_):
        if 'start_time' not in gen.keys():
            tmp = gen.copy()
            tmp['start_time'] = time()
            return func(tmp, time_)
        elif (time_ - gen['start_time']) > 60 :
            return 0
        else:
            return func(gen, time_)
    return wrapper


@check_start
def constant_temperature(gen, time_):
    return 60


@check_start
def constant_temperature_X(gen, time_):
    if 'constant_temperature_X' not in gen.keys():
        return constant_temperature(gen, time_)
    return gen['constant_temperature_X']


@check_start
def constant_pressure(gen, time_):
    return 16


@check_start
def constant_flow(gen, time_):
    return 8


@check_start
def light_roast_pressure(gen, time_):
    if time_ - gen['start_time'] < 18:
        return ( 0.093*(time_ - gen['start_time']) )**4 + 1
    else:
        return ( -0.0023*( (time_ - gen['start_time']) - 18)**2 ) + 9


@check_start
def light_roast_flow(gen, time_):
    if time_ - gen['start_time'] < 0.1:
        return 0
    elif time_ - gen['start_time'] < 18:
        return 8
    else:
        return np.exp(20 - (time_ - gen['start_time']))


