import logging

import wx

from service.fit import Fit
from gui.bitmapLoader import BitmapLoader
from gui.preferenceView import PreferenceView

logger = logging.getLogger(__name__)


class PFFittingEnginePref(PreferenceView):
    title = "Fitting Engine"

    def __init__(self):
        self.dirtySettings = False

    def refreshPanel(self, fit):
        pass

    # noinspection PyAttributeOutsideInit
    def populatePanel(self, panel):
        # self.openFitsSettings = service.SettingsProvider.getInstance().getSettings("pyfaPrevOpenFits", {"enabled": False, "pyfaOpenFits": []})

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        mainSizer.Add(self.stTitle, 0, wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.cbGlobalForceReload = wx.CheckBox(panel, wx.ID_ANY, u"Factor in reload time when calculating capacitor usage, damage, and tank.",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbGlobalForceReload, 0, wx.ALL | wx.EXPAND, 5)

        # Future code once new cap sim is implemented
        '''
        self.cbGlobalForceReactivationTimer = wx.CheckBox( panel, wx.ID_ANY, u"Factor in reactivation timer", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.cbGlobalForceReactivationTimer, 0, wx.ALL|wx.EXPAND, 5 )

        text =  u"   Ignores reactivation timer when calculating capacitor usage,\n   damage, and tank."
        self.cbGlobalForceReactivationTimerText = wx.StaticText( panel, wx.ID_ANY, text, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cbGlobalForceReactivationTimerText.Wrap( -1 )
        self.cbGlobalForceReactivationTimerText.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
        mainSizer.Add( self.cbGlobalForceReactivationTimerText, 0, wx.ALL, 5 )
        '''

        # Future code for mining laser crystal
        '''
        self.cbGlobalMiningSpecialtyCrystal = wx.CheckBox( panel, wx.ID_ANY, u"Factor in reactivation timer", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.cbGlobalMiningSpecialtyCrystal, 0, wx.ALL|wx.EXPAND, 5 )

        text = u"   If enabled, displays the Specialty Crystal mining amount.\n   This is the amount mined when using crystals and mining the matching asteroid."
        self.cbGlobalMiningSpecialtyCrystalText = wx.StaticText( panel, wx.ID_ANY, text, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cbGlobalMiningSpecialtyCrystalText.Wrap( -1 )
        self.cbGlobalMiningSpecialtyCrystalText.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
        mainSizer.Add( self.cbGlobalMiningSpecialtyCrystalText, 0, wx.ALL, 5 )
        '''

        self.sFit = Fit.getInstance()

        self.cbGlobalForceReload.SetValue(self.sFit.serviceFittingOptions["useGlobalForceReload"])

        self.cbGlobalForceReload.Bind(wx.EVT_CHECKBOX, self.OnCBGlobalForceReloadStateChange)

        panel.SetSizer(mainSizer)
        panel.Layout()

    def OnCBGlobalForceReloadStateChange(self, event):
        self.sFit.serviceFittingOptions["useGlobalForceReload"] = self.cbGlobalForceReload.GetValue()

    def getImage(self):
        return BitmapLoader.getBitmap("settings_fitting", "gui")

    def OnWindowLeave(self, event):
        # We don't want to do anything when they leave,
        # but in the future we might.
        pass


PFFittingEnginePref.register()
