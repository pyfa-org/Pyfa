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

# noinspection PyPackageRequirements
import wx

from eos.saveddata.mode import Mode
from eos.utils.float import floatUnerr
from gui.bitmap_loader import BitmapLoader
from gui.utils.numberFormatter import formatAmount
from gui.viewColumn import ViewColumn
from service.attribute import Attribute
from service.fit import Fit


regenGroups = (
    'Capacitor Battery', 'Structure Capacitor Battery',
    'Capacitor Power Relay', 'Structure Capacitor Power Relay',
    'Capacitor Recharger', 'Power Diagnostic System', 'Capacitor Flux Coil',
    'Rig Core', 'Shield Power Relay')


class CapacitorUse(ViewColumn):

    name = 'Capacitor Usage'

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)

        self.mask = wx.LIST_MASK_IMAGE

        Attribute.getInstance().getAttributeInfo('capacitorNeed')
        self.imageId = fittingView.imageList.GetImageIndex('capacitorRecharge_small', 'gui')
        self.bitmap = BitmapLoader.getBitmap('capacitorRecharge_small', 'gui')

    def getText(self, mod):
        if isinstance(mod, Mode):
            return ''
        fit = Fit.getInstance().getFit(self.fittingView.getActiveFit())
        if fit is None:
            return ''
        capUse = mod.capUse
        # Do not show cap diff numbers
        if mod.item is not None and mod.item.group.name in regenGroups:
            capRegenDiff = fit.getCapRegenGainFromMod(mod)
        else:
            capRegenDiff = 0
        capDiff = floatUnerr(capRegenDiff - capUse)
        if capDiff:
            return formatAmount(capDiff, 3, 0, 3, forceSign=True)
        else:
            return ''

    def getImageId(self, mod):
        return -1

    def getToolTip(self, mod):
        if isinstance(mod, Mode):
            return ''
        if mod.item is not None and mod.item.group.name in regenGroups:
            return 'Effect on peak capacitor regeneration'
        if mod.capUse:
            return 'Capacitor usage'
        return ''


CapacitorUse.register()
