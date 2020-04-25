import math


def roundToPrec(val, prec, nsValue=None):
    """
    nsValue: custom value which should be used to determine normalization shift
    """
    # We're not rounding integers anyway
    # Also make sure that we do not ask to calculate logarithm of zero
    if int(val) == val:
        return int(val)
    roundFactor = int(prec - math.floor(math.log10(abs(val if nsValue is None else nsValue))) - 1)
    # But we don't want to round integers
    if roundFactor < 0:
        roundFactor = 0
    # Do actual rounding
    val = round(val, roundFactor)
    # Make sure numbers with .0 part designating float don't get through
    if int(val) == val:
        val = int(val)
    return val


def roundDec(val, prec):
    if int(val) == val:
        return int(val)
    return round(val, prec)
