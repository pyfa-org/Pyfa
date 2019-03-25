# noinspection PyPackageRequirements
import wx
from wx.lib.intctrl import IntCtrl

from gui.preferenceView import PreferenceView
from gui.bitmap_loader import BitmapLoader

import gui.mainFrame
import gui.globalEvents as GE
from service.settings import PriceMenuSettings
from service.fit import Fit
from service.price import Price


class PFMarketPref(PreferenceView):
    title = "Market & Prices"

    def __init__(self):
        self.dirtySettings = False
        self.priceSettings = PriceMenuSettings.getInstance()

    def populatePanel(self, panel):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.dirtySettings = False

        helpCursor = wx.Cursor(wx.CURSOR_QUESTION_ARROW)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))

        mainSizer.Add(self.stTitle, 0, wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.cbMarketShortcuts = wx.CheckBox(panel, wx.ID_ANY, "Show market shortcuts", wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbMarketShortcuts, 0, wx.ALL | wx.EXPAND, 5)

        priceSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.stDefaultSystem = wx.StaticText(panel, wx.ID_ANY, "Default Market Prices:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stDefaultSystem.Wrap(-1)
        priceSizer.Add(self.stDefaultSystem, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.stDefaultSystem.SetCursor(helpCursor)
        self.stDefaultSystem.SetToolTip(wx.ToolTip(
            'The source you choose will be tried first, but subsequent sources will be used if the preferred source fails. '
            'The system you choose will also be tried first, and if no data is available, global price will be used.'))

        self.chPriceSource = wx.Choice(panel, choices=sorted(Price.sources.keys()))
        self.chPriceSystem = wx.Choice(panel, choices=list(Price.systemsList.keys()))
        priceSizer.Add(self.chPriceSource, 1, wx.ALL | wx.EXPAND, 5)
        priceSizer.Add(self.chPriceSystem, 1, wx.ALL | wx.EXPAND, 5)

        mainSizer.Add(priceSizer, 0, wx.ALL | wx.EXPAND, 0)

        delayTimer = wx.BoxSizer(wx.HORIZONTAL)

        self.stMarketDelay = wx.StaticText(panel, wx.ID_ANY, "Market Search Delay (ms):", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stMarketDelay.Wrap(-1)
        self.stMarketDelay.SetCursor(helpCursor)
        self.stMarketDelay.SetToolTip(
            wx.ToolTip('The delay between a keystroke and the market search. Can help reduce lag when typing fast in the market search box.'))

        delayTimer.Add(self.stMarketDelay, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.intDelay = IntCtrl(panel, max=1000, limited=True)
        delayTimer.Add(self.intDelay, 0, wx.ALL, 5)

        mainSizer.Add(delayTimer, 0, wx.ALL | wx.EXPAND, 0)

        self.sFit = Fit.getInstance()

        self.cbMarketShortcuts.SetValue(self.sFit.serviceFittingOptions["showMarketShortcuts"] or False)
        self.chPriceSource.SetStringSelection(self.sFit.serviceFittingOptions["priceSource"])
        self.chPriceSystem.SetStringSelection(self.sFit.serviceFittingOptions["priceSystem"])
        self.intDelay.SetValue(self.sFit.serviceFittingOptions["marketSearchDelay"])

        self.cbMarketShortcuts.Bind(wx.EVT_CHECKBOX, self.onCBShowShortcuts)
        self.chPriceSource.Bind(wx.EVT_CHOICE, self.onPricesSourceSelection)
        self.chPriceSystem.Bind(wx.EVT_CHOICE, self.onPriceSelection)
        self.intDelay.Bind(wx.lib.intctrl.EVT_INT, self.onMarketDelayChange)

        self.tbTotalPriceBox = wx.StaticBoxSizer(wx.VERTICAL, panel, "Total Price Includes")
        self.tbTotalPriceShip = wx.CheckBox(panel, -1, "Ship", wx.DefaultPosition, wx.DefaultSize, 1)
        self.tbTotalPriceShip.SetValue(self.priceSettings.get("ship"))
        self.tbTotalPriceShip.Bind(wx.EVT_CHECKBOX, self.OnTotalPriceShipChange)
        self.tbTotalPriceBox.Add(self.tbTotalPriceShip)
        self.tbTotalPriceModules = wx.CheckBox(panel, -1, "Modules", wx.DefaultPosition, wx.DefaultSize, 1)
        self.tbTotalPriceModules.SetValue(self.priceSettings.get("modules"))
        self.tbTotalPriceModules.Bind(wx.EVT_CHECKBOX, self.OnTotalPriceModulesChange)
        self.tbTotalPriceBox.Add(self.tbTotalPriceModules)
        self.tbTotalPriceDrones = wx.CheckBox(panel, -1, "Drones", wx.DefaultPosition, wx.DefaultSize, 1)
        self.tbTotalPriceDrones.SetValue(self.priceSettings.get("drones"))
        self.tbTotalPriceDrones.Bind(wx.EVT_CHECKBOX, self.OnTotalPriceDroneChange)
        self.tbTotalPriceBox.Add(self.tbTotalPriceDrones)
        self.tbTotalPriceCargo = wx.CheckBox(panel, -1, "Cargo", wx.DefaultPosition, wx.DefaultSize, 1)
        self.tbTotalPriceCargo.SetValue(self.priceSettings.get("cargo"))
        self.tbTotalPriceCargo.Bind(wx.EVT_CHECKBOX, self.OnTotalPriceCargoChange)
        self.tbTotalPriceBox.Add(self.tbTotalPriceCargo)
        self.tbTotalPriceCharacter = wx.CheckBox(panel, -1, "Implants && Boosters", wx.DefaultPosition, wx.DefaultSize, 1)
        self.tbTotalPriceCharacter.SetValue(self.priceSettings.get("character"))
        self.tbTotalPriceCharacter.Bind(wx.EVT_CHECKBOX, self.OnTotalPriceCharacterChange)
        self.tbTotalPriceBox.Add(self.tbTotalPriceCharacter)
        mainSizer.Add(self.tbTotalPriceBox, 1, wx.TOP | wx.RIGHT, 5)

        panel.SetSizer(mainSizer)
        panel.Layout()

    def onMarketDelayChange(self, event):
        self.sFit.serviceFittingOptions["marketSearchDelay"] = self.intDelay.GetValue()
        event.Skip()

    def onCBShowShortcuts(self, event):
        self.sFit.serviceFittingOptions["showMarketShortcuts"] = self.cbMarketShortcuts.GetValue()

    def getImage(self):
        return BitmapLoader.getBitmap("prefs_settings", "gui")

    def onPriceSelection(self, event):
        system = self.chPriceSystem.GetString(self.chPriceSystem.GetSelection())
        self.sFit.serviceFittingOptions["priceSystem"] = system

        fitID = self.mainFrame.getActiveFit()

        self.sFit.refreshFit(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))
        event.Skip()

    def onPricesSourceSelection(self, event):
        source = self.chPriceSource.GetString(self.chPriceSource.GetSelection())
        self.sFit.serviceFittingOptions["priceSource"] = source

    def OnTotalPriceShipChange(self, event):
        self.priceSettings.set('ship', event.GetInt())
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.mainFrame.getActiveFit()))

    def OnTotalPriceModulesChange(self, event):
        self.priceSettings.set('modules', event.GetInt())
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.mainFrame.getActiveFit()))

    def OnTotalPriceDroneChange(self, event):
        self.priceSettings.set('drones', event.GetInt())
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.mainFrame.getActiveFit()))

    def OnTotalPriceCargoChange(self, event):
        self.priceSettings.set('cargo', event.GetInt())
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.mainFrame.getActiveFit()))

    def OnTotalPriceCharacterChange(self, event):
        self.priceSettings.set('character', event.GetInt())
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.mainFrame.getActiveFit()))


PFMarketPref.register()
