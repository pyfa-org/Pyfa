def shorten(val, prec=4, lowest=0, highest=0):
    """
    Add suffix to value, transform value to match new suffix and round it.

    Keyword arguments:
    val -- value to process
    prec -- precision of final number (number of significant positions to show)
    lowest -- lowest order for suffixizing
    highest -- highest order for suffixizing

    Suffixes below lowest and above highest orders won't be used.
    """
    # Take numbers only matching/above lowest possible positive suffix
    if abs(val) >= 1000 and highest >= 3:
        suffixmap = {3 : "k", 6 : "M", 9 : "G"}
        # Start from highest possible suffix
        for key in sorted(suffixmap, reverse = True):
            # Find first suitable suffix and check if it's not above highest order
            if val >= 10**key and key <= highest:
                return u"{0}{1}".format(process(val/float(10**key), prec), suffixmap[key])
    # Take numbers between 0 and 1, and matching/below highest possible negative suffix
    elif abs(val) < 1 and val != 0 and lowest <= -3:
        suffixmap = {-6 : u'\u03bc', -3 : "m"}
        # Start from lowest possible suffix
        for key in sorted(suffixmap, reverse = False):
            # Check if mantissa with next suffix is in range [1, 1000)
            # Here we assume that each next order is greater than previous by 3
            if val < 10**(key+3) and key >= lowest:
                return u"{0}{1}".format(process(val/float(10**key), prec), suffixmap[key])
    # No suitable suffixes are found withing given order borders, or value
    # is already within [1, 1000) boundaries, just return rounded value with no suffix
    else:
        return u"{0}".format(process(val, prec))


def process(val, prec):
    """
    Round number.

    Keyword arguments:
    val -- value to round
    prec -- precision of final number (number of significant positions to show)

    Integer numbers are not rounded, only fractional part.
    """
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
