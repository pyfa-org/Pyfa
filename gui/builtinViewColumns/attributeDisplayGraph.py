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
import gui.mainFrame
from eos.saveddata.fit import Fit
from eos.utils.spoolSupport import SpoolOptions, SpoolType
from gui.bitmap_loader import BitmapLoader
from gui.viewColumn import ViewColumn
from gui.utils.numberFormatter import formatAmount


class GraphColumn(ViewColumn, metaclass=ABCMeta):

    def __init__(self, fittingView, iconID, formatSpec=(3, 0, 3)):
        ViewColumn.__init__(self, fittingView)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.imageId = fittingView.imageList.GetImageIndex(iconID, 'icons')
        self.bitmap = BitmapLoader.getBitmap(iconID, 'icons')
        self.mask = wx.LIST_MASK_TEXT
        self.formatSpec = formatSpec

    @abstractmethod
    def _getValue(self, fit):
        raise NotImplementedError

    def getText(self, stuff):
        if isinstance(stuff, Fit):
            val, unit = self._getValue(stuff)
            if val is None:
                return ''
            return formatAmount(val, *self.formatSpec, unitName=unit)
        return ''

    @abstractmethod
    def _getFitTooltip(self):
        raise NotImplementedError

    def getToolTip(self, stuff):
        if isinstance(stuff, Fit):
            return self._getFitTooltip()
        return ''

class DpsColumn(GraphColumn):

    name = 'Dps'

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1432, (3, 0, 0))

    def _getValue(self, fit):
        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
        return fit.getTotalDps(spoolOptions=SpoolOptions(SpoolType.SCALE, defaultSpoolValue, False)).total, None

    def _getFitTooltip(self):
        return 'Declared DPS'


DpsColumn.register()


class VolleyColumn(GraphColumn):

    name = 'Volley'

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1397, (3, 0, 0))

    def _getValue(self, fit):
        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
        return fit.getTotalVolley(spoolOptions=SpoolOptions(SpoolType.SCALE, defaultSpoolValue, False)).total, None

    def _getFitTooltip(self):
        return 'Declared volley'


VolleyColumn.register()


class SpeedColumn(GraphColumn):

    name = 'Speed'

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1389)

    def _getValue(self, fit):
        return fit.ship.getModifiedItemAttr('maxVelocity'), 'm/s'

    def _getFitTooltip(self):
        return 'Ship maximum speed'


SpeedColumn.register()


class RadiusColumn(GraphColumn):

    name = 'Radius'

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 3266)

    def _getValue(self, fit):
        return fit.ship.getModifiedItemAttr('radius'), 'm'

    def _getFitTooltip(self):
        return 'Ship radius'


RadiusColumn.register()


class SignatureRadiusColumn(GraphColumn):

    name = 'SigRadius'

    def __init__(self, fittingView, params):
        super().__init__(fittingView, 1390)

    def _getValue(self, fit):
        return fit.ship.getModifiedItemAttr('signatureRadius'), 'm'

    def _getFitTooltip(self):
        return 'Ship signature radius'


SignatureRadiusColumn.register()
