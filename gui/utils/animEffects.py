import math


def OUT_CIRC(t, b, c, d):
    t = float(t)
    b = float(b)
    c = float(c)
    d = float(d)

    t = t / d - 1

    return c * math.sqrt(1 - t * t) + b


def OUT_QUART(t, b, c, d):
    t = float(t)
    b = float(b)
    c = float(c)
    d = float(d)

    t = t / d - 1

    return -c * (t * t * t * t - 1) + b


def INOUT_CIRC(t, b, c, d):
    t = float(t)
    b = float(b)
    c = float(c)
    d = float(d)
    t1 = t / (d / 2)

    if (t / (d / 2)) < 1:
        return -c / 2 * (math.sqrt(1 - (t / (d / 2)) ** 2) - 1) + b
    else:
        return c / 2 * (math.sqrt(1 - (t1 - 2) ** 2) + 1) + b


def IN_CUBIC(t, b, c, d):
    t = float(t)
    b = float(b)
    c = float(c)
    d = float(d)

    t /= d

    return c * t * t * t + b


def OUT_QUAD(t, b, c, d):
    t = float(t)
    b = float(b)
    c = float(c)
    d = float(d)

    t /= d

    return -c * t * (t - 2) + b


def OUT_BOUNCE(t, b, c, d):
    t = float(t)
    b = float(b)
    c = float(c)
    d = float(d)

    t /= d

    if t < (1 / 2.75):
        return c * (7.5625 * t * t) + b
    elif t < (2 / 2.75):
        t -= (1.5 / 2.75)
        return c * (7.5625 * t * t + .75) + b
    elif t < (2.5 / 2.75):
        t -= (2.25 / 2.75)
        return c * (7.5625 * t * t + .9375) + b
    else:
        t -= (2.625 / 2.75)
        return c * (7.5625 * t * t + .984375) + b


def INOUT_EXP(t, b, c, d):
    t = float(t)
    b = float(b)
    c = float(c)
    d = float(d)

    t1 = t / (d / 2)

    if t == 0:
        return b
    elif t == d:
        return b + c
    elif t1 < 1:
        return c / 2 * math.pow(2, 10 * (t1 - 1)) + b - c * 0.0005
    else:
        return c / 2 * 1.0005 * (-math.pow(2, -10 * (t1 - 1)) + 2) + b
