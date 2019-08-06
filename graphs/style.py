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


from collections import OrderedDict, namedtuple

from service.const import GraphColor, GraphLightness


ColorData = namedtuple('ColorData', ('hsl', 'name', 'iconName'))
LightnessData = namedtuple('LightnessData', ('name', 'iconName', 'func'))


# In HSL format
BASE_COLORS = OrderedDict([
    (GraphColor.red, ColorData((0 / 360.0, 1.0, 0.5), 'Red', 'color_red')),
    (GraphColor.green, ColorData((120 / 360.0, 1.0, 0.5), 'Green', 'color_green')),
    (GraphColor.blue, ColorData((240 / 360.0, 1.0, 0.5), 'Blue', 'color_blue')),
    (GraphColor.yellow, ColorData((56 / 360.0, 1.0, 0.5), 'Yellow', 'color_yellow')),
    (GraphColor.cyan, ColorData((180 / 360.0, 1.0, 0.5), 'Cyan', 'color_cyan')),
    (GraphColor.magenta, ColorData((300 / 360.0, 1.0, 0.5), 'Magenta', 'color_magenta')),
    (GraphColor.orange, ColorData((40 / 360.0, 1.0, 0.5), 'Orange', 'color_orange')),
    (GraphColor.purple, ColorData((275 / 360.0, 1.0, 0.5), 'Purple', 'color_purple'))])


def hsl_to_hsv(hsl):
    h, s, l = hsl
    s *= l if (l < 0.5) else (1 - l)
    l += s
    return (h, 2 * s / l, l)


def darken(hsl):
    h, s, l = hsl
    return h, s * 0.7, l * 0.7


def brighten(hsl):
    h, s, l = hsl
    return h, s * 0.7, l + (1 - l) * 0.4


LIGHTNESSES = OrderedDict([
    (GraphLightness.normal, LightnessData('Normal', 'lightness_normal', lambda hsl: hsl)),
    (GraphLightness.dark, LightnessData('Dark', 'lightness_dark', darken)),
    (GraphLightness.bright, LightnessData('Bright', 'lightness_bright', brighten))])
