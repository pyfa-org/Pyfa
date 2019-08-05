# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================


# In HSL format
BASE_COLORS = (
    (0 / 360.0, 1.0, 0.5, 'Red'),
    (120 / 360.0, 1.0, 0.5, 'Green'),
    (240 / 360.0, 1.0, 0.5, 'Blue'),
    (56 / 360.0, 1.0, 0.5, 'Yellow'),
    (180 / 360.0, 1.0, 0.5, 'Cyan'),
    (300 / 360.0, 1.0, 0.5, 'Magenta'),
    (40 / 360.0, 1.0, 0.5, 'Orange'),
    (275 / 360.0, 1.0, 0.5, 'Purple'))


def hsl_to_hsv(hsl):
    h, s, l = hsl
    s *= l if (l < 0.5) else (1 - l)
    l += s
    return (h, 2 * s / l, l)
