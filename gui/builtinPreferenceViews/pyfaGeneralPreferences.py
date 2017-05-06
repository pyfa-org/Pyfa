# noinspection PyPackageRequirements
import wx
from wx.lib.intctrl import IntCtrl

from gui.preferenceView import PreferenceView
from gui.bitmapLoader import BitmapLoader

import gui.mainFrame
import gui.globalEvents as GE
from service.settings import SettingsProvider
from service.fit import Fit
from service.price import Price


class PFGeneralPref(PreferenceView):
    title = "General"

    def populatePanel(self, panel):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.dirtySettings = False
        self.openFitsSettings = SettingsProvider.getInstance().getSettings("pyfaPrevOpenFits",
                                                                           {"enabled": False, "pyfaOpenFits": []})

        helpCursor = wx.StockCursor(wx.CURSOR_QUESTION_ARROW)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))

        mainSizer.Add(self.stTitle, 0, wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.cbGlobalChar = wx.CheckBox(panel, wx.ID_ANY, u"Use global character", wx.DefaultPosition, wx.DefaultSize,
                                        0)
        mainSizer.Add(self.cbGlobalChar, 0, wx.ALL | wx.EXPAND, 5)

        self.cbGlobalDmgPattern = wx.CheckBox(panel, wx.ID_ANY, u"Use global damage pattern", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        mainSizer.Add(self.cbGlobalDmgPattern, 0, wx.ALL | wx.EXPAND, 5)

        self.cbCompactSkills = wx.CheckBox(panel, wx.ID_ANY, u"Compact skills needed tooltip", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        mainSizer.Add(self.cbCompactSkills, 0, wx.ALL | wx.EXPAND, 5)

        self.cbFitColorSlots = wx.CheckBox(panel, wx.ID_ANY, u"Color fitting view by slot", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        mainSizer.Add(self.cbFitColorSlots, 0, wx.ALL | wx.EXPAND, 5)

        self.cbReopenFits = wx.CheckBox(panel, wx.ID_ANY, u"Reopen previous fits on startup", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        mainSizer.Add(self.cbReopenFits, 0, wx.ALL | wx.EXPAND, 5)

        self.cbRackSlots = wx.CheckBox(panel, wx.ID_ANY, u"Separate Racks", wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbRackSlots, 0, wx.ALL | wx.EXPAND, 5)

        labelSizer = wx.BoxSizer(wx.VERTICAL)
        self.cbRackLabels = wx.CheckBox(panel, wx.ID_ANY, u"Show Rack Labels", wx.DefaultPosition, wx.DefaultSize, 0)
        labelSizer.Add(self.cbRackLabels, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(labelSizer, 0, wx.LEFT | wx.EXPAND, 30)

        self.cbShowTooltip = wx.CheckBox(panel, wx.ID_ANY, u"Show tab tooltips", wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbShowTooltip, 0, wx.ALL | wx.EXPAND, 5)

        self.cbMarketShortcuts = wx.CheckBox(panel, wx.ID_ANY, u"Show market shortcuts", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        mainSizer.Add(self.cbMarketShortcuts, 0, wx.ALL | wx.EXPAND, 5)

        self.cbGaugeAnimation = wx.CheckBox(panel, wx.ID_ANY, u"Animate gauges", wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbGaugeAnimation, 0, wx.ALL | wx.EXPAND, 5)

        self.cbExportCharges = wx.CheckBox(panel, wx.ID_ANY, u"Export loaded charges", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        mainSizer.Add(self.cbExportCharges, 0, wx.ALL | wx.EXPAND, 5)

        self.cbOpenFitInNew = wx.CheckBox(panel, wx.ID_ANY, u"Open fittings in a new page by default",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbOpenFitInNew, 0, wx.ALL | wx.EXPAND, 5)

        self.cbShowShipBrowserTooltip = wx.CheckBox(panel, wx.ID_ANY, u"Show ship browser tooltip",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbShowShipBrowserTooltip, 0, wx.ALL | wx.EXPAND, 5)

        priceSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.stDefaultSystem = wx.StaticText(panel, wx.ID_ANY, u"Default Market Prices:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stDefaultSystem.Wrap(-1)
        priceSizer.Add(self.stDefaultSystem, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.chPriceSystem = wx.Choice(panel, choices=Price.systemsList.keys())
        priceSizer.Add(self.chPriceSystem, 1, wx.ALL | wx.EXPAND, 5)

        mainSizer.Add(priceSizer, 0, wx.ALL | wx.EXPAND, 0)

        delayTimer = wx.BoxSizer(wx.HORIZONTAL)

        self.stMarketDelay = wx.StaticText(panel, wx.ID_ANY, u"Market Search Delay (ms):", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stMarketDelay.Wrap(-1)
        self.stMarketDelay.SetCursor(helpCursor)
        self.stMarketDelay.SetToolTip(
            wx.ToolTip('The delay between a keystroke and the market search. Can help reduce lag when typing fast in the market search box.'))

        delayTimer.Add(self.stMarketDelay, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.intDelay = IntCtrl(panel, max=1000, limited=True)
        delayTimer.Add(self.intDelay, 0, wx.ALL, 5)

        mainSizer.Add(delayTimer, 0, wx.ALL | wx.EXPAND, 0)

        self.sFit = Fit.getInstance()

        self.cbGlobalChar.SetValue(self.sFit.serviceFittingOptions["useGlobalCharacter"])
        self.cbGlobalDmgPattern.SetValue(self.sFit.serviceFittingOptions["useGlobalDamagePattern"])
        self.cbFitColorSlots.SetValue(self.sFit.serviceFittingOptions["colorFitBySlot"] or False)
        self.cbRackSlots.SetValue(self.sFit.serviceFittingOptions["rackSlots"] or False)
        self.cbRackLabels.SetValue(self.sFit.serviceFittingOptions["rackLabels"] or False)
        self.cbCompactSkills.SetValue(self.sFit.serviceFittingOptions["compactSkills"] or False)
        self.cbReopenFits.SetValue(self.openFitsSettings["enabled"])
        self.cbShowTooltip.SetValue(self.sFit.serviceFittingOptions["showTooltip"] or False)
        self.cbMarketShortcuts.SetValue(self.sFit.serviceFittingOptions["showMarketShortcuts"] or False)
        self.cbGaugeAnimation.SetValue(self.sFit.serviceFittingOptions["enableGaugeAnimation"])
        self.cbExportCharges.SetValue(self.sFit.serviceFittingOptions["exportCharges"])
        self.cbOpenFitInNew.SetValue(self.sFit.serviceFittingOptions["openFitInNew"])
        self.chPriceSystem.SetStringSelection(self.sFit.serviceFittingOptions["priceSystem"])
        self.cbShowShipBrowserTooltip.SetValue(self.sFit.serviceFittingOptions["showShipBrowserTooltip"])
        self.intDelay.SetValue(self.sFit.serviceFittingOptions["marketSearchDelay"])

        self.cbGlobalChar.Bind(wx.EVT_CHECKBOX, self.OnCBGlobalCharStateChange)
        self.cbGlobalDmgPattern.Bind(wx.EVT_CHECKBOX, self.OnCBGlobalDmgPatternStateChange)
        self.cbFitColorSlots.Bind(wx.EVT_CHECKBOX, self.onCBGlobalColorBySlot)
        self.cbRackSlots.Bind(wx.EVT_CHECKBOX, self.onCBGlobalRackSlots)
        self.cbRackLabels.Bind(wx.EVT_CHECKBOX, self.onCBGlobalRackLabels)
        self.cbCompactSkills.Bind(wx.EVT_CHECKBOX, self.onCBCompactSkills)
        self.cbReopenFits.Bind(wx.EVT_CHECKBOX, self.onCBReopenFits)
        self.cbShowTooltip.Bind(wx.EVT_CHECKBOX, self.onCBShowTooltip)
        self.cbMarketShortcuts.Bind(wx.EVT_CHECKBOX, self.onCBShowShortcuts)
        self.cbGaugeAnimation.Bind(wx.EVT_CHECKBOX, self.onCBGaugeAnimation)
        self.cbExportCharges.Bind(wx.EVT_CHECKBOX, self.onCBExportCharges)
        self.cbOpenFitInNew.Bind(wx.EVT_CHECKBOX, self.onCBOpenFitInNew)
        self.chPriceSystem.Bind(wx.EVT_CHOICE, self.onPriceSelection)
        self.cbShowShipBrowserTooltip.Bind(wx.EVT_CHECKBOX, self.onCBShowShipBrowserTooltip)
        self.intDelay.Bind(wx.lib.intctrl.EVT_INT, self.onMarketDelayChange)

        self.cbRackLabels.Enable(self.sFit.serviceFittingOptions["rackSlots"] or False)

        panel.SetSizer(mainSizer)
        panel.Layout()

    def onMarketDelayChange(self, event):
        self.sFit.serviceFittingOptions["marketSearchDelay"] = self.intDelay.GetValue()
        event.Skip()

    def onCBGlobalColorBySlot(self, event):
        self.sFit.serviceFittingOptions["colorFitBySlot"] = self.cbFitColorSlots.GetValue()
        fitID = self.mainFrame.getActiveFit()
        self.sFit.refreshFit(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))
        event.Skip()

    def onCBGlobalRackSlots(self, event):
        self.sFit.serviceFittingOptions["rackSlots"] = self.cbRackSlots.GetValue()
        self.cbRackLabels.Enable(self.cbRackSlots.GetValue())
        fitID = self.mainFrame.getActiveFit()
        self.sFit.refreshFit(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))
        event.Skip()

    def onCBGlobalRackLabels(self, event):
        self.sFit.serviceFittingOptions["rackLabels"] = self.cbRackLabels.GetValue()
        fitID = self.mainFrame.getActiveFit()
        self.sFit.refreshFit(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))
        event.Skip()

    def OnCBGlobalCharStateChange(self, event):
        self.sFit.serviceFittingOptions["useGlobalCharacter"] = self.cbGlobalChar.GetValue()
        event.Skip()

    def OnCBGlobalDmgPatternStateChange(self, event):
        self.sFit.serviceFittingOptions["useGlobalDamagePattern"] = self.cbGlobalDmgPattern.GetValue()
        event.Skip()

    def onCBCompactSkills(self, event):
        self.sFit.serviceFittingOptions["compactSkills"] = self.cbCompactSkills.GetValue()
        fitID = self.mainFrame.getActiveFit()
        self.sFit.refreshFit(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))
        event.Skip()

    def onCBReopenFits(self, event):
        self.openFitsSettings["enabled"] = self.cbReopenFits.GetValue()

    def onCBShowTooltip(self, event):
        self.sFit.serviceFittingOptions["showTooltip"] = self.cbShowTooltip.GetValue()

    def onCBShowShortcuts(self, event):
        self.sFit.serviceFittingOptions["showMarketShortcuts"] = self.cbMarketShortcuts.GetValue()

    def onCBGaugeAnimation(self, event):
        self.sFit.serviceFittingOptions["enableGaugeAnimation"] = self.cbGaugeAnimation.GetValue()

    def onCBExportCharges(self, event):
        self.sFit.serviceFittingOptions["exportCharges"] = self.cbExportCharges.GetValue()

    def onCBOpenFitInNew(self, event):
        self.sFit.serviceFittingOptions["openFitInNew"] = self.cbOpenFitInNew.GetValue()

    def onCBShowShipBrowserTooltip(self, event):
        self.sFit.serviceFittingOptions["showShipBrowserTooltip"] = self.cbShowShipBrowserTooltip.GetValue()

    def getImage(self):
        return BitmapLoader.getBitmap("prefs_settings", "gui")

    def onPriceSelection(self, event):
        system = self.chPriceSystem.GetString(self.chPriceSystem.GetSelection())
        self.sFit.serviceFittingOptions["priceSystem"] = system

        fitID = self.mainFrame.getActiveFit()

        self.sFit.refreshFit(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))
        event.Skip()


PFGeneralPref.register()
