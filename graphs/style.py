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

# noinspection PyPackageRequirements
import wx

from service.const import GraphColor, GraphLightness, GraphLineStyle

ColorData = namedtuple('ColorData', ('hsl', 'name', 'iconName'))
LightnessData = namedtuple('LightnessData', ('name', 'iconName', 'func'))
_t = wx.GetTranslation


class LineStyleData:

    def __init__(self, name, iconNamePrefix, mplSpec):
        self.name = name
        self._iconNamePrefix = iconNamePrefix
        self.mplSpec = mplSpec

    @property
    def iconName(self):
        # Get lightness out of RGB color, see following link for math:
        # https://www.niwa.nu/2013/05/math-behind-colorspace-conversions-rgb-hsl/
        r, g, b, a = (c / 255 for c in wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        l = (max(r, g, b) + min (r, g, b)) / 2
        suffix = '_black' if l > 0.3 else '_white'
        return '{}{}'.format(self._iconNamePrefix, suffix)


# In HSL format
BASE_COLORS = OrderedDict([
    (GraphColor.red, ColorData((0 / 360.0, 1.0, 0.5), _t('Red'), 'color_red')),
    (GraphColor.green, ColorData((120 / 360.0, 1.0, 0.5), _t('Green'), 'color_green')),
    (GraphColor.blue, ColorData((240 / 360.0, 1.0, 0.5), _t('Blue'), 'color_blue')),
    (GraphColor.orange, ColorData((40 / 360.0, 1.0, 0.5), _t('Orange'), 'color_orange')),
    (GraphColor.magenta, ColorData((300 / 360.0, 1.0, 0.5), _t('Magenta'), 'color_magenta')),
    (GraphColor.cyan, ColorData((180 / 360.0, 1.0, 0.5), _t('Cyan'), 'color_cyan')),
    (GraphColor.purple, ColorData((275 / 360.0, 1.0, 0.5), _t('Purple'), 'color_purple')),
    (GraphColor.yellow, ColorData((56 / 360.0, 1.0, 0.5), _t('Yellow'), 'color_yellow'))])


def hsl_to_hsv(hsl):
    h, s, l = hsl
    s *= l if (l < 0.5) else (1 - l)
    l += s
    return (h, 2 * s / l, l)


def darken(hsl):
    h, s, l = hsl
    return h, s * 0.5, l * 0.7


def brighten(hsl):
    h, s, l = hsl
    return h, s * 0.5, l + (1 - l) * 0.5


LIGHTNESSES = OrderedDict([
    (GraphLightness.normal, LightnessData(_t('Normal'), 'lightness_normal', lambda hsl: hsl)),
    (GraphLightness.dark, LightnessData(_t('Dark'), 'lightness_dark', darken)),
    (GraphLightness.bright, LightnessData(_t('Bright'), 'lightness_bright', brighten))])


STYLES = OrderedDict([
    (GraphLineStyle.solid, LineStyleData(_t('Solid'), 'style_solid', 'solid')),
    (GraphLineStyle.dashed, LineStyleData(_t('Dashed'), 'style_dashed', (0, (5, 1)))),
    (GraphLineStyle.dotted, LineStyleData(_t('Dotted'), 'style_dotted', (0, (1, 1)))),
    (GraphLineStyle.dashdotted, LineStyleData(_t('Dash-dotted'), 'style_dashdot', (0, (3, 1, 1, 1))))])
