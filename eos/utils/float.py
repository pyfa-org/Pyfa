"""
Sometimes use of floats may lead to undesirable results, e.g.
  int(2.3 / 0.1) = 22.
We cannot afford to use different number representations (e.g. representations
provided by decimal or fraction modules), thus consequences are worked around by
this module.
"""

import math
import sys


# As we will be rounding numbers after operations (which introduce higher error
# than base float representation error), we need to keep less significant
# numbers than for single float number w/o operations
keepDigits = int(sys.float_info.dig / 2)


def floatUnerr(value):
    """Round possible float number error, killing some precision in process."""
    if value in (0, math.inf):
        return value
    # Find round factor, taking into consideration that we want to keep at least
    # predefined amount of significant digits
    roundFactor = int(keepDigits - math.ceil(math.log10(abs(value))))
    return round(value, roundFactor)
