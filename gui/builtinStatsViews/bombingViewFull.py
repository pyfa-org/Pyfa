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

import gui.mainFrame
from gui.bitmap_loader import BitmapLoader
from gui.statsView import StatsView

_t = wx.GetTranslation


class BombingViewFull(StatsView):
    name = "bombingViewFull"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self._cachedValues = []
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def getHeaderText(self, fit):
        return _t("Bombing")

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent(text)
        return width

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()
        self.panel = contentPanel

        self.headerPanel = headerPanel

        # Display table
        sizerBombing = wx.FlexGridSizer(7, 5, 0, 0)
        for i in range(4):
            sizerBombing.AddGrowableCol(i + 1)
        contentSizer.Add(sizerBombing, 0, wx.EXPAND, 0)

        # Add an empty label, then the rest.
        sizerBombing.Add(wx.StaticText(contentPanel, wx.ID_ANY, ""), 0)
        toolTipText = {
            "em": _t("Electron Bomb"),
            "thermal": _t("Scorch Bomb"),
            "kinetic": _t("Concussion Bomb"),
            "explosive": _t("Shrapnel Bomb")
        }
        for damageType in ("em", "thermal", "kinetic", "explosive"):
            bitmap = BitmapLoader.getStaticBitmap("%s_big" % damageType, contentPanel, "gui")
            tooltip = wx.ToolTip(toolTipText[damageType])
            bitmap.SetToolTip(tooltip)
            sizerBombing.Add(bitmap, 0, wx.ALIGN_CENTER)

        for covertLevel in ("0", "1", "2", "3", "4", "5"):
            label = wx.StaticText(contentPanel, wx.ID_ANY, "%s" % covertLevel)
            tooltip = wx.ToolTip(_t("Covert Ops level"))
            label.SetToolTip(tooltip)
            sizerBombing.Add(label, 0, wx.ALIGN_CENTER)

            for damageType in ("em", "thermal", "kinetic", "explosive"):
                label = wx.StaticText(contentPanel, wx.ID_ANY, "0.0")
                setattr(self, "labelDamagetypeCovertlevel%s%s" % (damageType.capitalize(), covertLevel), label)
                sizerBombing.Add(label, 0, wx.ALIGN_CENTER)

    def refreshPanel(self, fit):
        # If we did anything interesting, we'd update our labels to reflect the new fit's stats here
        if fit is None:
            return

        bombDamage = 5800
        bombSigRadius = 400
        sigRadius = fit.ship.getModifiedItemAttr('signatureRadius')

        # get the raw values for all hp layers
        hullHP = fit.ship.getModifiedItemAttr('hp')
        armorHP = fit.ship.getModifiedItemAttr('armorHP')
        shieldHP = fit.ship.getModifiedItemAttr('shieldCapacity')

        # we calculate the total ehp for pure damage of all types based on raw hp and resonance (resonance= 1-resistance)
        emEhp = hullHP / fit.ship.getModifiedItemAttr('emDamageResonance') +\
                armorHP / fit.ship.getModifiedItemAttr('armorEmDamageResonance') +\
                shieldHP / fit.ship.getModifiedItemAttr('shieldEmDamageResonance')
        thermalEhp = hullHP / fit.ship.getModifiedItemAttr('thermalDamageResonance') +\
                armorHP / fit.ship.getModifiedItemAttr('armorThermalDamageResonance') +\
                shieldHP / fit.ship.getModifiedItemAttr('shieldThermalDamageResonance')
        kineticEhp = hullHP / fit.ship.getModifiedItemAttr('kineticDamageResonance') +\
                armorHP / fit.ship.getModifiedItemAttr('armorKineticDamageResonance') +\
                shieldHP / fit.ship.getModifiedItemAttr('shieldKineticDamageResonance')
        explosiveEhp = hullHP / fit.ship.getModifiedItemAttr('explosiveDamageResonance') +\
                armorHP / fit.ship.getModifiedItemAttr('armorExplosiveDamageResonance') +\
                shieldHP / fit.ship.getModifiedItemAttr('shieldExplosiveDamageResonance')

        # updates the labels for each combination of covert op level and damage type
        for covertLevel in ("0", "1", "2", "3", "4", "5"):
            modBombDamage = bombDamage * (1 + 0.05 * int(covertLevel))
            for damageType, ehp in (("em", emEhp), ("thermal", thermalEhp),
                                    ("kinetic", kineticEhp), ("explosive", explosiveEhp)):
                effectiveBombDamage = modBombDamage * min(bombSigRadius, sigRadius) / bombSigRadius
                label = getattr(self, "labelDamagetypeCovertlevel%s%s" % (damageType.capitalize(), covertLevel))
                label.SetLabel("{:.1f}".format(ehp / effectiveBombDamage))
                label.SetToolTip("Number of %s bombs to kill a %s using the respective "
                                 "bomber type with Covert Ops level %s" % (damageType, fit.name, covertLevel))

        self.panel.Layout()
        self.headerPanel.Layout()


BombingViewFull.register()
