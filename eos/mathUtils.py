#===============================================================================
# Copyright (C) 2010 Anton Vorobyov
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import decimal

def floorFloat(value):
    """Round float down to integer"""
    # We have to convert float to str to keep compatibility with
    # decimal module in python 2.6
    value = str(value)
    # Do the conversions for proper rounding down, avoiding float
    # representation errors
    result = int(decimal.Decimal(value).to_integral_value(rounding=decimal.ROUND_DOWN))
    return result
