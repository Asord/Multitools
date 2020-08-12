from .Color import *

def linearDistribution(start, stop, counter, modulus, clockwise):
    if clockwise:
        return [(start + (stop - start) / counter * pos) % modulus for pos in range(counter)]
    else:
        return [(start - (start - stop) / counter * pos) % modulus for pos in range(counter)]

def curvedDistribution(counter, clockwise, red=100, green=100, blue=100):
    if red+green+blue == 300:
        rem = counter % 3
        
        lr = linearDistribution(0  , 120, int(red   / 300 * counter) ,360 ,clockwise) 
        lg = linearDistribution(120, 240, int(green / 300 * counter) ,360 ,clockwise) 
        lb = linearDistribution(240, 360, int(blue  / 300 * counter) ,360 ,clockwise)
        
        total = lr + lg + lb
        total += [359 for _ in range( counter-len(total) )]
        
        
        return total
    else:
        return linearDistribution(0,359,counter,360,clockwise)


def hsv_generator(start, stop, cnt, clockwise, coefs):
    _colors = []

    start_hue, start_sat, start_val = start
    stop_hue , stop_sat , stop_val  = stop

    if clockwise:
        if stop_hue < start_hue: stop_hue += 360.0
    else:
        if stop_hue > start_hue: start_hue += 360.0

    hue        = linearDistribution(start_hue, stop_hue, cnt, 360.0, clockwise)
    saturation = linearDistribution(start_sat, stop_sat, cnt, 1.1, clockwise)
    value      = linearDistribution(start_val, stop_val, cnt, 1.1, clockwise)

    for i in range(cnt):
        _colors.append(Color().fromHSV(hue[i], saturation[i], value[i]).enhance(coefs))

    return _colors

def hsv_generatorT(start=(0.0, 1.0, 1.0), stop=(360.0, 1.0, 1.0), cnt=21, clockwise=True, coefs=RatioAdjustment()):
    hsv = hsv_generator(start, stop, cnt, clockwise, coefs)
    return [e for e in hsv]

def hsv_generatorTT(start=(0.0, 1.0, 1.0), stop=(360.0, 1.0, 1.0), cnt=21, clockwise=True, coefs=RatioAdjustment()):
    hsv = hsv_generator(start, stop, cnt, clockwise, coefs)
    return [[e] for e in hsv]