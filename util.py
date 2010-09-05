def shorten(val, prec=4, lowest=0, highest=0):
    if abs(val) >= 1000 and highest >= 3:
        suffixmap = {3 : "k", 6 : "M", 9 : "G"}
        for key in sorted(suffixmap, reverse = True):
            if val >= 10**key and key <= highest:
                return u"{0}{1}".format(process(val/float(10**key), prec), suffixmap[key])
    elif abs(val) < 1 and val != 0 and lowest <= -3:
        suffixmap = {-6 : u'\u03bc', -3 : "m"}
        for key in sorted(suffixmap, reverse = False):
            if val < 10**(key+3) and key >= lowest:
                return u"{0}{1}".format(process(val/float(10**key), prec), suffixmap[key])
    else:
        return u"{0}".format(process(val, prec))


def process(val, prec):
    # Check if we have no integer and some fraction after bunch of zeroes,
    # counting these zeros in process
    shiftFraction, integersNumber = 0, 0
    if int(val) == 0 and val != 0:
        while val < 0.1**(shiftFraction+1):
            shiftFraction += 1
    else:
        while abs(val) >= 10**(integersNumber):
            integersNumber +=1
    # We want to show at least (prec) significant numbers in any cases
    roundFactor = prec + shiftFraction - integersNumber
    # But we don't want to round integers
    if roundFactor < 0: roundFactor = 0
    val = round(val, roundFactor)
    # Strip trailing zero for integers and convert to string
    result = str(val)[-2:] == '.0' and str(val)[:-2] or str(val)
    return result
