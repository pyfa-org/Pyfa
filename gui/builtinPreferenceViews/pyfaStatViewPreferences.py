# noinspection PyPackageRequirements
import wx

from gui.preferenceView import PreferenceView
from gui.bitmap_loader import BitmapLoader
from service.settings import StatViewSettings


class PFStatViewPref(PreferenceView):
    title = "Statistics Panel"

    def __init__(self):
        self.dirtySettings = False
        self.settings = StatViewSettings.getInstance()

    def refreshPanel(self, fit):
        pass

    # noinspection PyAttributeOutsideInit
    def populatePanel(self, panel):
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))

        mainSizer.Add(self.stTitle, 0, wx.ALL, 5)

        self.stSubTitle = wx.StaticText(panel, wx.ID_ANY,
                                        "Changes require restart of pyfa to take effect.",
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.stSubTitle.Wrap(-1)
        mainSizer.Add(self.stSubTitle, 0, wx.ALL, 3)

        # Row 1
        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.ALL, 5)

        rbSizerRow1 = wx.BoxSizer(wx.HORIZONTAL)

        self.rbResources = wx.RadioBox(panel, -1, "Resources", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        # Disable minimal as we don't have a view for this yet
        self.rbResources.EnableItem(1, False)
        self.rbResources.SetSelection(self.settings.get('resources'))
        rbSizerRow1.Add(self.rbResources, 1, wx.TOP | wx.RIGHT, 5)
        self.rbResources.Bind(wx.EVT_RADIOBOX, self.OnResourcesChange)

        self.rbResistances = wx.RadioBox(panel, -1, "Resistances", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        # Disable minimal as we don't have a view for this yet
        self.rbResistances.EnableItem(1, False)
        self.rbResistances.SetSelection(self.settings.get('resistances'))
        rbSizerRow1.Add(self.rbResistances, 1, wx.ALL, 5)
        self.rbResistances.Bind(wx.EVT_RADIOBOX, self.OnResistancesChange)

        self.rbRecharge = wx.RadioBox(panel, -1, "Shield/Armor Tank", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        # Disable minimal as we don't have a view for this yet
        self.rbRecharge.EnableItem(1, False)
        self.rbRecharge.SetSelection(self.settings.get('recharge'))
        rbSizerRow1.Add(self.rbRecharge, 1, wx.ALL, 5)
        self.rbRecharge.Bind(wx.EVT_RADIOBOX, self.OnRechargeChange)

        mainSizer.Add(rbSizerRow1, 1, wx.ALL | wx.EXPAND, 0)

        # Row 2
        rbSizerRow2 = wx.BoxSizer(wx.HORIZONTAL)

        self.rbFirepower = wx.RadioBox(panel, -1, "Firepower", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        # Disable minimal as we don't have a view for this yet
        self.rbFirepower.EnableItem(1, False)
        self.rbFirepower.SetSelection(self.settings.get('firepower'))
        rbSizerRow2.Add(self.rbFirepower, 1, wx.TOP | wx.RIGHT, 5)
        self.rbFirepower.Bind(wx.EVT_RADIOBOX, self.OnFirepowerChange)

        self.rbCapacitor = wx.RadioBox(panel, -1, "Capacitor", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        # Disable minimal as we don't have a view for this yet
        self.rbCapacitor.EnableItem(1, False)
        self.rbCapacitor.SetSelection(self.settings.get('capacitor'))
        rbSizerRow2.Add(self.rbCapacitor, 1, wx.ALL, 5)
        self.rbCapacitor.Bind(wx.EVT_RADIOBOX, self.OnCapacitorChange)

        self.rbMisc = wx.RadioBox(panel, -1, "Misc", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        # Disable full as we don't have a view for this yet
        self.rbMisc.EnableItem(2, False)
        self.rbMisc.SetSelection(self.settings.get('targetingMisc'))
        rbSizerRow2.Add(self.rbMisc, 1, wx.ALL, 5)
        self.rbMisc.Bind(wx.EVT_RADIOBOX, self.OnTargetingMiscChange)

        mainSizer.Add(rbSizerRow2, 1, wx.ALL | wx.EXPAND, 0)

        # Row 3
        rbSizerRow3 = wx.BoxSizer(wx.HORIZONTAL)

        self.rbPrice = wx.RadioBox(panel, -1, "Price", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        self.rbPrice.SetSelection(self.settings.get('price'))
        rbSizerRow3.Add(self.rbPrice, 1, wx.TOP | wx.RIGHT, 5)
        self.rbPrice.Bind(wx.EVT_RADIOBOX, self.OnPriceChange)

        self.rbOutgoing = wx.RadioBox(panel, -1, "Remote Reps", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        self.rbOutgoing.SetSelection(self.settings.get('outgoing'))
        rbSizerRow3.Add(self.rbOutgoing, 1, wx.TOP | wx.RIGHT, 5)
        self.rbOutgoing.Bind(wx.EVT_RADIOBOX, self.OnOutgoingChange)
        #  We don't have views for these.....yet
        '''
        self.rbMining = wx.RadioBox(panel, -1, "Mining", wx.DefaultPosition, wx.DefaultSize,
                                    ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        self.rbMining.SetSelection(self.settings.get('miningyield'))
        rbSizerRow3.Add(self.rbMining, 1, wx.ALL, 5)
        self.rbMining.Bind(wx.EVT_RADIOBOX, self.OnMiningYieldChange)

        self.rbDrones = wx.RadioBox(panel, -1, "Drones", wx.DefaultPosition, wx.DefaultSize,
                                    ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        self.rbDrones.SetSelection(self.settings.get('drones'))
        rbSizerRow3.Add(self.rbDrones, 1, wx.ALL, 5)
        self.rbDrones.Bind(wx.EVT_RADIOBOX, self.OnDroneChange)
        '''

        mainSizer.Add(rbSizerRow3, 1, wx.ALL | wx.EXPAND, 0)

        panel.SetSizer(mainSizer)
        panel.Layout()

    def OnResourcesChange(self, event):
        self.settings.set('resources', event.GetInt())

    def OnResistancesChange(self, event):
        self.settings.set('resistances', event.GetInt())

    def OnRechargeChange(self, event):
        self.settings.set('recharge', event.GetInt())

    def OnFirepowerChange(self, event):
        self.settings.set('firepower', event.GetInt())

    def OnCapacitorChange(self, event):
        self.settings.set('capacitor', event.GetInt())

    def OnTargetingMiscChange(self, event):
        self.settings.set('targetingMisc', event.GetInt())

    def OnPriceChange(self, event):
        self.settings.set('price', event.GetInt())

    def OnOutgoingChange(self, event):
        self.settings.set('outgoing', event.GetInt())

    def OnMiningYieldChange(self, event):
        self.settings.set('miningyield', event.GetInt())

    def OnDroneChange(self, event):
        self.settings.set('drones', event.GetInt())

    def getImage(self):
        return BitmapLoader.getBitmap("settings_stats", "gui")


PFStatViewPref.register()
