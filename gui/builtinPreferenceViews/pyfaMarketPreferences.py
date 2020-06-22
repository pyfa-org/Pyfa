# noinspection PyPackageRequirements
import wx
from wx.lib.intctrl import IntCtrl

from gui.preferenceView import PreferenceView
from gui.bitmap_loader import BitmapLoader

import gui.mainFrame
import gui.globalEvents as GE
from service.settings import MarketPriceSettings
from service.fit import Fit
from service.price import Price

_t = wx.GetTranslation


class PFMarketPref(PreferenceView):

    def __init__(self):
        self.priceSettings = MarketPriceSettings.getInstance()

    def populatePanel(self, panel):
        self.title = _t("Market & Prices")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()

        helpCursor = wx.Cursor(wx.CURSOR_QUESTION_ARROW)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, _t("Market && Prices"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        mainSizer.Add(self.stTitle, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        delayTimer = wx.BoxSizer(wx.HORIZONTAL)
        self.stMarketDelay = wx.StaticText(panel, wx.ID_ANY, _t("Market Search Delay (ms):"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.stMarketDelay.Wrap(-1)
        if "wxGTK" not in wx.PlatformInfo:
            self.stMarketDelay.SetCursor(helpCursor)
        self.stMarketDelay.SetToolTip(wx.ToolTip(
                _t('The delay between a keystroke and the market search. Can help reduce lag when typing fast in the market search box.')))
        delayTimer.Add(self.stMarketDelay, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.intDelay = IntCtrl(panel, max=1000, limited=True)
        delayTimer.Add(self.intDelay, 0, wx.ALL, 5)
        mainSizer.Add(delayTimer, 0, wx.EXPAND | wx.TOP | wx.RIGHT, 10)
        self.intDelay.SetValue(self.sFit.serviceFittingOptions["marketSearchDelay"])
        self.intDelay.Bind(wx.lib.intctrl.EVT_INT, self.onMarketDelayChange)

        self.cbMarketShortcuts = wx.CheckBox(panel, wx.ID_ANY, _t("Show market shortcuts"), wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbMarketShortcuts, 0, wx.EXPAND | wx.TOP | wx.RIGHT, 10)
        self.cbMarketShortcuts.SetValue(self.sFit.serviceFittingOptions["showMarketShortcuts"] or False)
        self.cbMarketShortcuts.Bind(wx.EVT_CHECKBOX, self.onCBShowShortcuts)

        priceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.stDefaultSystem = wx.StaticText(panel, wx.ID_ANY, _t("Default Market Prices:"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.stDefaultSystem.Wrap(-1)
        priceSizer.Add(self.stDefaultSystem, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        if "wxGTK" not in wx.PlatformInfo:
            self.stDefaultSystem.SetCursor(helpCursor)
        self.stDefaultSystem.SetToolTip(wx.ToolTip(
                _t('The source you choose will be tried first, but subsequent sources will be used if the preferred source fails. '
                   'The system you choose will also be tried first, and if no data is available, global price will be used.')))
        self.chPriceSource = wx.Choice(panel, choices=sorted(Price.sources.keys()))
        self.chPriceSystem = wx.Choice(panel, choices=list(Price.systemsList.keys()))
        priceSizer.Add(self.chPriceSource, 1, wx.ALL | wx.EXPAND, 5)
        priceSizer.Add(self.chPriceSystem, 1, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(priceSizer, 0, wx.EXPAND | wx.TOP | wx.RIGHT, 10)
        self.chPriceSource.SetStringSelection(self.sFit.serviceFittingOptions["priceSource"])
        self.chPriceSource.Bind(wx.EVT_CHOICE, self.onPricesSourceSelection)
        self.chPriceSystem.SetStringSelection(self.sFit.serviceFittingOptions["priceSystem"])
        self.chPriceSystem.Bind(wx.EVT_CHOICE, self.onPriceSelection)

        self.tbTotalPriceBox = wx.StaticBoxSizer(wx.VERTICAL, panel, _t("Total Price Includes"))
        self.tbTotalPriceDrones = wx.CheckBox(panel, -1, _t("Drones"), wx.DefaultPosition, wx.DefaultSize, 1)
        self.tbTotalPriceDrones.SetValue(self.priceSettings.get("drones"))
        self.tbTotalPriceDrones.Bind(wx.EVT_CHECKBOX, self.OnTotalPriceDroneChange)
        self.tbTotalPriceBox.Add(self.tbTotalPriceDrones, 0, wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.tbTotalPriceCargo = wx.CheckBox(panel, -1, _t("Cargo"), wx.DefaultPosition, wx.DefaultSize, 1)
        self.tbTotalPriceCargo.SetValue(self.priceSettings.get("cargo"))
        self.tbTotalPriceCargo.Bind(wx.EVT_CHECKBOX, self.OnTotalPriceCargoChange)
        self.tbTotalPriceBox.Add(self.tbTotalPriceCargo, 0, wx.LEFT | wx.RIGHT, 5)
        self.tbTotalPriceCharacter = wx.CheckBox(panel, -1, _t("Implants && Boosters"), wx.DefaultPosition, wx.DefaultSize, 1)
        self.tbTotalPriceCharacter.SetValue(self.priceSettings.get("character"))
        self.tbTotalPriceCharacter.Bind(wx.EVT_CHECKBOX, self.OnTotalPriceCharacterChange)
        self.tbTotalPriceBox.Add(self.tbTotalPriceCharacter, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        mainSizer.Add(self.tbTotalPriceBox, 0, wx.EXPAND | wx.TOP | wx.RIGHT, 10)

        self.rbMarketSearch = wx.RadioBox(panel, -1, _t("Market Search && Recent Items"), wx.DefaultPosition, wx.DefaultSize,
                                          [_t("No changes to meta buttons"), _t("Enable all meta buttons for a duration of search / recents"),
                                           _t("Enable all meta buttons")], 1,
                                          wx.RA_SPECIFY_COLS)
        self.rbMarketSearch.SetSelection(self.priceSettings.get('marketMGSearchMode'))
        mainSizer.Add(self.rbMarketSearch, 0, wx.RIGHT | wx.TOP | wx.EXPAND, 10)
        self.rbMarketSearch.Bind(wx.EVT_RADIOBOX, self.OnMarketSearchChange)

        self.rbMarketEmpty = wx.RadioBox(panel, -1, _t("Market Group Selection"), wx.DefaultPosition, wx.DefaultSize,
                                         [_t("No changes to meta buttons"), _t("Enable all meta buttons")], 1, wx.RA_SPECIFY_COLS)
        self.rbMarketEmpty.SetSelection(self.priceSettings.get('marketMGMarketSelectMode'))
        mainSizer.Add(self.rbMarketEmpty, 0, wx.EXPAND | wx.TOP | wx.RIGHT, 10)
        self.rbMarketEmpty.Bind(wx.EVT_RADIOBOX, self.OnMarketGroupSelectionChange)

        self.rbMarketEmpty = wx.RadioBox(panel, -1, _t("Empty Market View"), wx.DefaultPosition, wx.DefaultSize,
                                         [_t("No changes to meta buttons"), _t("Enable leftmost available meta button"), _t("Enable all available meta buttons")], 1,
                                         wx.RA_SPECIFY_COLS)
        self.rbMarketEmpty.SetSelection(self.priceSettings.get('marketMGEmptyMode'))
        mainSizer.Add(self.rbMarketEmpty, 0, wx.EXPAND | wx.TOP | wx.RIGHT, 10)
        self.rbMarketEmpty.Bind(wx.EVT_RADIOBOX, self.OnMarketEmptyChange)

        self.rbMarketJump = wx.RadioBox(panel, -1, _t("Item Market Group Jump"), wx.DefaultPosition, wx.DefaultSize,
                                        [_t("No changes to meta buttons"), _t("Enable item's meta button"), _t("Enable item's meta button, disable others"),
                                         _t("Enable all meta buttons")], 1, wx.RA_SPECIFY_COLS)
        self.rbMarketJump.SetSelection(self.priceSettings.get('marketMGJumpMode'))
        mainSizer.Add(self.rbMarketJump, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, 10)
        self.rbMarketJump.Bind(wx.EVT_RADIOBOX, self.OnMarketJumpChange)

        panel.SetSizer(mainSizer)
        panel.Layout()

    def onMarketDelayChange(self, event):
        self.sFit.serviceFittingOptions["marketSearchDelay"] = self.intDelay.GetValue()
        event.Skip()

    def onCBShowShortcuts(self, event):
        self.sFit.serviceFittingOptions["showMarketShortcuts"] = self.cbMarketShortcuts.GetValue()

    def getImage(self):
        return BitmapLoader.getBitmap("settings_market", "gui")

    def onPriceSelection(self, event):
        system = self.chPriceSystem.GetString(self.chPriceSystem.GetSelection())
        self.sFit.serviceFittingOptions["priceSystem"] = system

        fitID = self.mainFrame.getActiveFit()

        self.sFit.refreshFit(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))
        event.Skip()

    def onPricesSourceSelection(self, event):
        source = self.chPriceSource.GetString(self.chPriceSource.GetSelection())
        self.sFit.serviceFittingOptions["priceSource"] = source

    def OnTotalPriceDroneChange(self, event):
        self.priceSettings.set('drones', event.GetInt())
        fitID = self.mainFrame.getActiveFit()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))

    def OnTotalPriceCargoChange(self, event):
        self.priceSettings.set('cargo', event.GetInt())
        fitID = self.mainFrame.getActiveFit()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))

    def OnTotalPriceCharacterChange(self, event):
        self.priceSettings.set('character', event.GetInt())
        fitID = self.mainFrame.getActiveFit()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))

    def OnMarketJumpChange(self, event):
        self.priceSettings.set('marketMGJumpMode', event.GetInt())

    def OnMarketEmptyChange(self, event):
        self.priceSettings.set('marketMGEmptyMode', event.GetInt())

    def OnMarketSearchChange(self, event):
        self.priceSettings.set('marketMGSearchMode', event.GetInt())

    def OnMarketGroupSelectionChange(self, event):
        self.priceSettings.set('marketMGMarketSelectMode', event.GetInt())


PFMarketPref.register()
