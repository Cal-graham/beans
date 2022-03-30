from time import time


def check_start(func):
    def wrapper(gen):
        if 'start_time' not in gen.keys():
            return func({'start_time': time()})
        else:
            return func(gen)
    return wrapper


@check_start
def constant_temperature(gen):
    return 60


@check_start
def constant_pressure(gen):
    return 16


@check_start
def light_roast_pressure(gen):
    if time() - gen['start_time'] < 18:
        return ( 0.093*(time() - gen['start_time']) )**4 + 1
    else:
        return ( -0.0023*( (time() - gen['start_time']) - 18)**2 ) + 9
