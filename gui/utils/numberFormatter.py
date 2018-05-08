import math


def formatAmount(val, prec=3, lowest=0, highest=0, currency=False, forceSign=False):
    """
    Add suffix to value, transform value to match new suffix and round it.

    Keyword arguments:
    val -- value to process
    prec -- precision of final number (number of significant positions to show)
    lowest -- lowest order for suffixizing for numbers 0 < |num| < 1
    highest -- highest order for suffixizing for numbers |num| > 1
    currency -- if currency, billion suffix will be B instead of G
    forceSign -- if True, positive numbers are signed too
    """
    if val is None:
        return ""
    # Define suffix maps
    posSuffixMap = {3: "k", 6: "M", 9: "B" if currency is True else "G"}
    negSuffixMap = {-6: '\u03bc', -3: "m"}
    # Define tuple of the map keys
    # As we're going to go from the biggest order of abs(key), sort
    # them differently due to one set of values being negative
    # and other positive
    posOrders = tuple(sorted(iter(posSuffixMap.keys()), reverse=True))
    negOrders = tuple(sorted(iter(negSuffixMap.keys()), reverse=False))
    # Find the least abs(key)
    posLowest = min(posOrders)
    negHighest = max(negOrders)
    # By default, mantissa takes just value and no suffix
    mantissa, suffix = val, ""
    # Positive suffixes
    if abs(val) > 1 and highest >= posLowest:
        # Start from highest possible suffix
        for key in posOrders:
            # Find first suitable suffix and check if it's not above highest order
            if abs(val) >= 10 ** key and key <= highest:
                mantissa, suffix = val / float(10 ** key), posSuffixMap[key]
                # Do additional step to eliminate results like 999999 => 1000k
                # If we're already using our greatest order, we can't do anything useful
                if posOrders.index(key) == 0:
                    break
                else:
                    # Get order greater than current
                    prevKey = posOrders[posOrders.index(key) - 1]
                    # Check if the key to which we potentially can change is greater
                    # than our highest boundary
                    if prevKey > highest:
                        # If it is, bail - we already have acceptable results
                        break
                    # Find multiplier to get from one order to another
                    orderDiff = 10 ** (prevKey - key)
                    # If rounded mantissa according to our specifications is greater than
                    # or equal to multiplier
                    if roundToPrec(mantissa, prec) >= orderDiff:
                        # Divide mantissa and use suffix of greater order
                        mantissa, suffix = mantissa / orderDiff, posSuffixMap[prevKey]
                    # Otherwise consider current results as acceptable
                    break
    # Take numbers between 0 and 1, and matching/below highest possible negative suffix
    elif abs(val) < 1 and val != 0 and lowest <= negHighest:
        # Start from lowest possible suffix
        for key in negOrders:
            # Get next order
            try:
                nextKey = negOrders[negOrders.index(key) + 1]
            except IndexError:
                nextKey = 0
            # Check if mantissa with next suffix is in range [1, 1000)
            if abs(val) < 10 ** nextKey and key >= lowest:
                mantissa, suffix = val / float(10 ** key), negSuffixMap[key]
                # Do additional step to eliminate results like 0.9999 => 1000m
                # Check if the key we're potentially switching to is greater than our
                # upper boundary
                if nextKey > highest:
                    # If it is, leave loop with results we already have
                    break
                # Find the multiplier between current and next order
                orderDiff = 10 ** (nextKey - key)
                # If rounded mantissa according to our specifications is greater than
                # or equal to multiplier
                if roundToPrec(mantissa, prec) >= orderDiff:
                    # Divide mantissa and use suffix of greater order
                    # Use special handling of zero key as it's not on the map
                    mantissa, suffix = mantissa / orderDiff, posSuffixMap[nextKey] if nextKey != 0 else ""
                # Otherwise consider current results as acceptable
                break
    # Round mantissa according to our prec variable
    mantissa = roundToPrec(mantissa, prec)
    sign = "+" if forceSign is True and mantissa > 0 else ""
    # Round mantissa and add suffix
    result = "{0}{1}{2}".format(sign, mantissa, suffix)
    return result


def roundToPrec(val, prec):
    # We're not rounding integers anyway
    # Also make sure that we do not ask to calculate logarithm of zero
    if int(val) == val:
        return int(val)
    # Find round factor, taking into consideration that we want to keep at least prec
    # positions for fractions with zero integer part (e.g. 0.0000354 for prec=3)
    roundFactor = int(prec - math.ceil(math.log10(abs(val))))
    # But we don't want to round integers
    if roundFactor < 0:
        roundFactor = 0
    # Do actual rounding
    val = round(val, roundFactor)
    # Make sure numbers with .0 part designating float don't get through
    if int(val) == val:
        val = int(val)
    return val
