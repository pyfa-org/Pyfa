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

from abc import ABCMeta, abstractmethod

# noinspection PyPackageRequirements
import wx

import eos.config
from eos.saveddata.fit import Fit
from eos.saveddata.targetProfile import TargetProfile
from eos.utils.spoolSupport import SpoolOptions, SpoolType
from graphs.wrapper import BaseWrapper
from gui.bitmap_loader import BitmapLoader
from gui.utils.numberFormatter import formatAmount
from gui.viewColumn import ViewColumn


class GraphColumn(ViewColumn, metaclass=ABCMeta):

    proportionWidth = 2
    stickPrefixToValue = False

    def __init__(self, fittingView, iconID, formatSpec=(3, 0, 3)):
        ViewColumn.__init__(self, fittingView)
        self.imageId = fittingView.imageList.GetImageIndex(iconID, 'icons')
        self.bitmap = BitmapLoader.getBitmap(iconID, 'icons')
        self.mask = wx.LIST_MASK_TEXT
        self.formatSpec = formatSpec

    @abstractmethod
    def _getValue(self, fit):
        raise NotImplementedError

    def getText(self, stuff):
        if isinstance(stuff, BaseWrapper):
            stuff = stuff.item
        if isinstance(stuff, (Fit, TargetProfile)):
            val, unit = self._getValue(stuff)
            if val is None:
                return ''
            # Stick to value - 25k GJ
            if self.stickPrefixToValue:
                return '{} {}'.format(formatAmount(val, *self.formatSpec), unit)
            # Stick to unit - 25 km
            else:
                return formatAmount(val, *self.formatSpec, unitName=unit)
        return ''

    @abstractmethod
    def _getFitTooltip(self):
        raise NotImplementedError

    def getToolTip(self, stuff):
        if isinstance(stuff, BaseWrapper):
            stuff = stuff.item
        if isinstance(stuff, (Fit, TargetProfile)):
            return self._getFitTooltip()
        return ''


class DpsColumn(GraphColumn):

    name = 'Dps'

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1432, (3, 0, 0))

    def _getValue(self, fit):
        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
        return fit.getTotalDps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpoolValue, False)).total, None

    def _getFitTooltip(self):
        return 'Declared DPS'


DpsColumn.register()


class VolleyColumn(GraphColumn):

    name = 'Volley'

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1397, (3, 0, 0))

    def _getValue(self, fit):
        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
        return fit.getTotalVolley(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpoolValue, False)).total, None

    def _getFitTooltip(self):
        return 'Declared volley'


VolleyColumn.register()


class SpeedColumn(GraphColumn):

    name = 'Speed'

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1389)

    def _getValue(self, stuff):
        if isinstance(stuff, Fit):
            speed = stuff.ship.getModifiedItemAttr('maxVelocity')
        elif isinstance(stuff, TargetProfile):
            speed = stuff.maxVelocity
        else:
            speed = 0
        return speed, 'm/s'

    def _getFitTooltip(self):
        return 'Maximum speed'


SpeedColumn.register()


class AgilityColumn(GraphColumn):

    name = 'Agility'

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1401, (3, 0, 0))

    def _getValue(self, fit):
        return fit.alignTime, None

    def _getFitTooltip(self):
        return 'Agility factor'


AgilityColumn.register()


class RadiusColumn(GraphColumn):

    name = 'Radius'

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 3266)

    def _getValue(self, stuff):
        if isinstance(stuff, Fit):
            radius = stuff.ship.getModifiedItemAttr('radius')
        elif isinstance(stuff, TargetProfile):
            radius = stuff.radius
        else:
            radius = 0
        return radius, 'm'

    def _getFitTooltip(self):
        return 'Radius'


RadiusColumn.register()


class SignatureRadiusColumn(GraphColumn):

    name = 'SigRadius'

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1390)

    def _getValue(self, stuff):
        if isinstance(stuff, Fit):
            sigRadius = stuff.ship.getModifiedItemAttr('signatureRadius')
        elif isinstance(stuff, TargetProfile):
            sigRadius = stuff.signatureRadius
        else:
            sigRadius = 0
        return sigRadius, 'm'

    def _getFitTooltip(self):
        return 'Signature radius'


SignatureRadiusColumn.register()


class ShieldAmountColumn(GraphColumn):

    name = 'ShieldAmount'
    stickPrefixToValue = True

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1384)

    def _getValue(self, fit):
        return fit.ship.getModifiedItemAttr('shieldCapacity'), 'HP'

    def _getFitTooltip(self):
        return 'Maximum shield amount'


ShieldAmountColumn.register()


class ShieldTimeColumn(GraphColumn):

    name = 'ShieldTime'

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1392, (3, 0, 0))

    def _getValue(self, fit):
        return fit.ship.getModifiedItemAttr('shieldRechargeRate') / 1000, 's'

    def _getFitTooltip(self):
        return 'Time to regenerate shield from 0% to 98.7%'


ShieldTimeColumn.register()


class CapAmountColumn(GraphColumn):

    name = 'CapAmount'
    stickPrefixToValue = True

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1668)

    def _getValue(self, fit):
        return fit.ship.getModifiedItemAttr('capacitorCapacity'), 'GJ'

    def _getFitTooltip(self):
        return 'Maximum capacitor amount'


CapAmountColumn.register()


class CapTimeColumn(GraphColumn):

    name = 'CapTime'

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1392, (3, 0, 0))

    def _getValue(self, fit):
        return fit.ship.getModifiedItemAttr('rechargeRate') / 1000, 's'

    def _getFitTooltip(self):
        return 'Time to regenerate capacitor from 0% to 98.7%'


CapTimeColumn.register()


class WarpSpeedColumn(GraphColumn):

    name = 'WarpSpeed'

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1389, (3, 0, 0))

    def _getValue(self, fit):
        return fit.warpSpeed, 'AU/s'

    def _getFitTooltip(self):
        return 'Warp speed'


WarpSpeedColumn.register()


class WarpDistanceColumn(GraphColumn):

    name = 'WarpDistance'

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1391, (3, 0, 0))

    def _getValue(self, fit):
        return fit.maxWarpDistance, 'AU'

    def _getFitTooltip(self):
        return 'Maximum warp distance'


WarpDistanceColumn.register()


class ScanResolutionColumn(GraphColumn):

    name = 'ScanResolution'
    stickPrefixToValue = True

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 74)

    def _getValue(self, fit):
        return fit.ship.getModifiedItemAttr('scanResolution'), 'mm'

    def _getFitTooltip(self):
        return 'Scan Resolution'


ScanResolutionColumn.register()


class ShieldRRColumn(GraphColumn):

    name = 'ShieldRR'
    stickPrefixToValue = True

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1384, (3, 0, 3))

    def _getValue(self, fit):
        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
        return fit.getRemoteReps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpoolValue, False)).shield, 'HP/s'

    def _getFitTooltip(self):
        return 'Declared shield repair speed'


ShieldRRColumn.register()


class ArmorRRColumn(GraphColumn):

    name = 'ArmorRR'
    stickPrefixToValue = True

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 80, (3, 0, 3))

    def _getValue(self, fit):
        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
        return fit.getRemoteReps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpoolValue, False)).armor, 'HP/s'

    def _getFitTooltip(self):
        return 'Declared armor repair speed'


ArmorRRColumn.register()


class HullRRColumn(GraphColumn):

    name = 'HullRR'
    stickPrefixToValue = True

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 67, (3, 0, 3))

    def _getValue(self, fit):
        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
        return fit.getRemoteReps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpoolValue, False)).hull, 'HP/s'

    def _getFitTooltip(self):
        return 'Declared hull repair speed'


HullRRColumn.register()
