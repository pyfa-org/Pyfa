#===============================================================================
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
#===============================================================================

import wx
from gui.statsView import StatsView
from gui import builtinStatsViews
from gui import bitmapLoader
from gui import pygauge as PG
from util import formatAmount
import service
import gui.mainFrame

class ResistancesViewFull(StatsView):
    name = "resistancesViewFull"
    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self._cachedValues = []
        self._toggleEHP = 1

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def getHeaderText(self, fit):
        return "Resistances"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent( text )
        return width

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()
        self.panel = contentPanel

        self.headerPanel = headerPanel
        # Custom header  EHP
        headerContentSizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer = headerPanel.GetSizer()
        hsizer.Add(headerContentSizer,0,0,0)
        self.stEff = wx.StaticText(headerPanel, wx.ID_ANY, "( Effective HP: ")
        headerContentSizer.Add(self.stEff)
        headerPanel.GetParent().AddToggleItem(self.stEff)

        self.labelEhp = wx.StaticText(headerPanel, wx.ID_ANY, "0")
        headerContentSizer.Add(self.labelEhp, 0)
        headerPanel.GetParent().AddToggleItem(self.labelEhp)

        stCls = wx.StaticText(headerPanel, wx.ID_ANY, " )")

        headerPanel.GetParent().AddToggleItem( stCls )
        headerContentSizer.Add( stCls )
#        headerContentSizer.Add(wx.StaticLine(headerPanel, wx.ID_ANY), 1, wx.ALIGN_CENTER)

        # Display table
        col = 0
        row = 0
        sizerResistances = wx.GridBagSizer(0, 0)
        contentSizer.Add( sizerResistances, 0, wx.EXPAND , 0)

        for i in xrange(6):
            sizerResistances.AddGrowableCol(i + 1)

        # Add an empty label, then the rest.
        sizerResistances.Add(wx.StaticText(contentPanel, wx.ID_ANY), wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ))
        col+=1
        toolTipText = {"em" : "EM", "thermal" : "Thermal", "kinetic" : "Kinetic", "explosive" : "Explosive"}
        for damageType in ("em", "thermal", "kinetic", "explosive"):
            bitmap = bitmapLoader.getStaticBitmap("%s_big" % damageType, contentPanel, "icons")
            tooltip = wx.ToolTip(toolTipText[damageType])
            bitmap.SetToolTip(tooltip)
            sizerResistances.Add(bitmap, wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER)
            col+=1
        self.stEHPs = wx.StaticText(contentPanel, wx.ID_ANY, "EHP", style = wx.DOUBLE_BORDER)
        self.stEHPs.SetToolTip(wx.ToolTip("Click to toggle between effective HP and raw HP"))

        self.stEHPs.Bind(wx.EVT_LEFT_UP, self.toggleEHP)


        sizerResistances.Add(self.stEHPs, wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER)
        col=0
        row+=1

        gaugeColours=( ((38,133,198),(52,86,98)), ((198,38,38),(83,65,67)), ((163,163,163),(74,90,93)), ((198,133,38),(81,83,67)) )

        toolTipText = {"shield" : "Shield", "armor" : "Armor", "hull" : "Hull", "damagePattern" : "Damage Pattern"}
        for tankType in ("shield", "armor", "hull", "separator", "damagePattern"):
            if tankType != "separator":
                bitmap = bitmapLoader.getStaticBitmap("%s_big" % tankType, contentPanel, "icons")
                tooltip = wx.ToolTip(toolTipText[tankType])
                bitmap.SetToolTip(tooltip)
                sizerResistances.Add(bitmap, wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER)
                col+=1

            else:
                sizerResistances.Add(wx.StaticLine(contentPanel, wx.ID_ANY), wx.GBPosition( row, col ), wx.GBSpan( 1, 6 ), wx.EXPAND|wx.ALIGN_CENTER)
                row+=1
                col=0

                continue
            currGColour=0

            for damageType in ("em", "thermal", "kinetic", "explosive"):

                box = wx.BoxSizer(wx.HORIZONTAL)
                sizerResistances.Add(box, wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER)


                #Fancy gauges addon

                pgColour= gaugeColours[currGColour]
                fc = pgColour[0]
                bc = pgColour[1]
                currGColour+=1

                lbl = PG.PyGauge(contentPanel, wx.ID_ANY, 100)
                lbl.SetMinSize((48, 16))
                lbl.SetBackgroundColour(wx.Colour(bc[0],bc[1],bc[2]))
                lbl.SetBarColour(wx.Colour(fc[0],fc[1],fc[2]))
                lbl.SetBarGradient()
                lbl.SetFractionDigits(1)

                setattr(self, "gaugeResistance%s%s" % (tankType.capitalize(), damageType.capitalize()), lbl)
                box.Add(lbl, 0, wx.ALIGN_CENTER)

                col+=1
            box = wx.BoxSizer(wx.VERTICAL)
            box.SetMinSize(wx.Size(self.getTextExtentW("WWWWk"), -1))

            lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0" if tankType != "damagePattern" else "")
            box.Add(lbl, 0, wx.ALIGN_CENTER)

            setattr(self, "labelResistance%sEhp" % tankType.capitalize(), lbl)
            sizerResistances.Add(box, wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER)
            row+=1
            col=0

    def toggleEHP(self,event):



        self._toggleEHP *= -1
        self.refreshPanel(self._currentFit)


    def refreshPanel(self, fit):
        #If we did anything intresting, we'd update our labels to reflect the new fit's stats here
        self._currentFit = fit
        sDP = service.DamagePattern.getInstance()
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        if self._toggleEHP == 1:
            activeDmgPattern = getattr(self.mainFrame,"_activeDmgPattern", sDP.getDamagePattern("Uniform"))

            sFit.setDamagePattern(fitID, activeDmgPattern)
            self.stEHPs.SetLabel("EHP")
        else:
            sFit.setDamagePattern(fitID, None)
            self.stEHPs.SetLabel("HP")
        self.stEHPs.SetToolTip(wx.ToolTip("Click to toggle between effective HP and raw HP"))


        for tankType in ("shield", "armor", "hull"):
            for damageType in ("em", "thermal", "kinetic", "explosive"):
                if fit is not None:
                    resonanceType = tankType if tankType != "hull" else ""
                    resonance = "%s%sDamageResonance" % (resonanceType, damageType.capitalize())
                    resonance = resonance[0].lower() + resonance[1:]
                    resonance = (1 - fit.ship.getModifiedItemAttr(resonance)) * 100
                else:
                    resonance = 0

                lbl = getattr(self, "gaugeResistance%s%s" % (tankType.capitalize(), damageType.capitalize()))

                lbl.SetValue(resonance)

        ehp = fit.ehp if fit is not None else None
        total = 0
        for tankType in ("shield", "armor", "hull"):
            lbl = getattr(self, "labelResistance%sEhp" % tankType.capitalize())
            if ehp is not None:
                total += ehp[tankType]
                lbl.SetLabel(formatAmount(ehp[tankType], 3, 0, 9))
                lbl.SetToolTip(wx.ToolTip("%s: %d" % (tankType.capitalize(), ehp[tankType])))
            else:
                lbl.SetLabel("0")


        self.labelEhp.SetLabel("%s" % formatAmount(total, 3, 0, 9))
        if self._toggleEHP == 1:
            self.stEff.SetLabel("( Effective HP: ")
            self.labelEhp.SetToolTip(wx.ToolTip("Effective: %d HP" % total))
        else:
            self.stEff.SetLabel("( Raw HP: ")
            self.labelEhp.SetToolTip(wx.ToolTip("Raw: %d HP" % total))


        damagePattern = fit.damagePattern if fit is not None else None
        total = sum((damagePattern.emAmount, damagePattern.thermalAmount,
                    damagePattern.kineticAmount, damagePattern.explosiveAmount)) if damagePattern is not None else 0

        for damageType in ("em", "thermal", "kinetic", "explosive"):
            lbl = getattr(self, "gaugeResistanceDamagepattern%s" % damageType.capitalize())

            if damagePattern is not None:
                lbl.SetValueRange(getattr(damagePattern, "%sAmount" % damageType), total)
            else:
                lbl.SetValue(0)

        self.panel.Layout()
        self.headerPanel.Layout()

ResistancesViewFull.register()

