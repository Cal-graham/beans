from time import time


def check_start(func):
    def wrapper(gen, time_):
        if 'start_time' not in gen.keys():
            return func({'start_time': time()}, time_)
        else:
            return func(gen, time_)
    return wrapper


@check_start
def constant_temperature(gen, time_):
    return 60


@check_start
def constant_pressure(gen, time_):
    return 16


@check_start
def light_roast_pressure(gen, time_):
    if time_ - gen['start_time'] < 18:
        return ( 0.093*(time_ - gen['start_time']) )**4 + 1
    else:
        return ( -0.0023*( (time_ - gen['start_time']) - 18)**2 ) + 9
