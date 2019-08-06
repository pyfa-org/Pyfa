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


from collections import OrderedDict

from service.const import Color


# In HSL format
BASE_COLORS = OrderedDict([
    (Color.red, ((0 / 360.0, 1.0, 0.5), 'color_red')),
    (Color.green, ((120 / 360.0, 1.0, 0.5), 'color_green')),
    (Color.blue, ((240 / 360.0, 1.0, 0.5), 'color_blue')),
    (Color.yellow, ((56 / 360.0, 1.0, 0.5), 'color_yellow')),
    (Color.cyan, ((180 / 360.0, 1.0, 0.5), 'color_cyan')),
    (Color.magenta, ((300 / 360.0, 1.0, 0.5), 'color_magenta')),
    (Color.orange, ((40 / 360.0, 1.0, 0.5), 'color_orange')),
    (Color.purple, ((275 / 360.0, 1.0, 0.5), 'color_purple'))])


def hsl_to_hsv(hsl):
    h, s, l = hsl
    s *= l if (l < 0.5) else (1 - l)
    l += s
    return (h, 2 * s / l, l)
