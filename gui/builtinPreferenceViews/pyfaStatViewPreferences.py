import wx

from gui.preferenceView import PreferenceView
from gui.bitmapLoader import BitmapLoader

import gui.mainFrame
import service
from service.crest import CrestModes

from wx.lib.intctrl import IntCtrl

class PFStatViewPref ( PreferenceView):
    title = "Statistics Panel"

    def populatePanel( self, panel ):

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = service.settings.statViewSettings.getInstance()
        self.dirtySettings = False
        dlgWidth = panel.GetParent().GetParent().ClientSize.width
        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.stTitle = wx.StaticText( panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stTitle.Wrap( -1 )
        self.stTitle.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )

        mainSizer.Add( self.stTitle, 0, wx.ALL, 5 )

        # Row 1
        self.m_staticline1 = wx.StaticLine( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        mainSizer.Add( self.m_staticline1, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )

        rbSizerRow1 = wx.BoxSizer(wx.HORIZONTAL)

        self.rbMode = wx.RadioBox(panel, -1, "Resources", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        self.rbMode.SetSelection(self.settings.get('Resources'))
        rbSizerRow1.Add(self.rbMode, 1, wx.TOP | wx.RIGHT, 5 )
        self.rbMode.Bind(wx.EVT_RADIOBOX, self.OnModeChange)

        self.rbServer = wx.RadioBox(panel, -1, "Resistances", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        self.rbServer.SetSelection(self.settings.get('Resistances'))
        rbSizerRow1.Add(self.rbServer, 1, wx.ALL, 5 )
        self.rbServer.Bind(wx.EVT_RADIOBOX, self.OnServerChange)

        self.rbTankRecharge = wx.RadioBox(panel, -1, "Shield/Armor Regen", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        self.rbTankRecharge.SetSelection(self.settings.get('TankRecharge'))
        rbSizerRow1.Add(self.rbTankRecharge, 1, wx.ALL, 5 )
        self.rbServer.Bind(wx.EVT_RADIOBOX, self.OnServerChange)

        mainSizer.Add(rbSizerRow1, 1, wx.ALL|wx.EXPAND, 0)

        # Row 2
        self.m_staticline2 = wx.StaticLine( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        mainSizer.Add( self.m_staticline2, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )

        rbSizerRow2 = wx.BoxSizer(wx.HORIZONTAL)

        self.rbMode = wx.RadioBox(panel, -1, "Firepower", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        self.rbMode.SetSelection(self.settings.get('Firepower'))
        rbSizerRow2.Add(self.rbMode, 1, wx.TOP | wx.RIGHT, 5 )
        self.rbMode.Bind(wx.EVT_RADIOBOX, self.OnModeChange)

        self.rbServer = wx.RadioBox(panel, -1, "Capacitor", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        self.rbServer.SetSelection(self.settings.get('Capacitor'))
        rbSizerRow2.Add(self.rbServer, 1, wx.ALL, 5 )
        self.rbServer.Bind(wx.EVT_RADIOBOX, self.OnServerChange)

        self.rbTankRecharge = wx.RadioBox(panel, -1, "Misc", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        self.rbTankRecharge.SetSelection(self.settings.get('Misc'))
        rbSizerRow2.Add(self.rbTankRecharge, 1, wx.ALL, 5 )
        self.rbServer.Bind(wx.EVT_RADIOBOX, self.OnServerChange)

        mainSizer.Add(rbSizerRow2, 1, wx.ALL|wx.EXPAND, 0)

        # Row 3
        self.m_staticline3 = wx.StaticLine( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        mainSizer.Add( self.m_staticline3, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )

        rbSizerRow3 = wx.BoxSizer(wx.HORIZONTAL)

        self.rbMode = wx.RadioBox(panel, -1, "Price", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        self.rbMode.SetSelection(self.settings.get('Price'))
        rbSizerRow3.Add(self.rbMode, 1, wx.TOP | wx.RIGHT, 5 )
        self.rbMode.Bind(wx.EVT_RADIOBOX, self.OnModeChange)

        self.rbServer = wx.RadioBox(panel, -1, "Mining", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        self.rbServer.SetSelection(self.settings.get('Mining'))
        rbSizerRow3.Add(self.rbServer, 1, wx.ALL, 5 )
        self.rbServer.Bind(wx.EVT_RADIOBOX, self.OnServerChange)

        self.rbTankRecharge = wx.RadioBox(panel, -1, "???", wx.DefaultPosition, wx.DefaultSize, ['None', 'Minimal', 'Full'], 1, wx.RA_SPECIFY_COLS)
        self.rbTankRecharge.SetSelection(self.settings.get('Misc'))
        rbSizerRow3.Add(self.rbTankRecharge, 1, wx.ALL, 5 )
        self.rbServer.Bind(wx.EVT_RADIOBOX, self.OnServerChange)

        mainSizer.Add(rbSizerRow3, 1, wx.ALL|wx.EXPAND, 0)


        self.btnApply = wx.Button( panel, wx.ID_ANY, u"Save Client Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btnApply.Bind(wx.EVT_BUTTON, self.OnBtnApply)

        #mainSizer.Add( fgAddrSizer, 0, wx.EXPAND, 5)
        mainSizer.Add( self.btnApply, 0, wx.ALIGN_RIGHT, 5)

        #self.ToggleProxySettings(self.settings.get('mode'))


        panel.SetSizer( mainSizer )
        panel.Layout()

    def OnTimeoutChange(self, event):
        self.settings.set('timeout', event.GetEventObject().GetValue())

    def OnModeChange(self, event):
        self.settings.set('mode', event.GetInt())
        self.ToggleProxySettings(self.settings.get('mode'))
        service.Crest.restartService()

    def OnServerChange(self, event):
        self.settings.set('server', event.GetInt())
        service.Crest.restartService()

    def OnBtnApply(self, event):
        self.settings.set('clientID', self.inputClientID.GetValue().strip())
        self.settings.set('clientSecret', self.inputClientSecret.GetValue().strip())
        sCrest = service.Crest.getInstance()
        sCrest.delAllCharacters()

    def ToggleProxySettings(self, mode):
        if mode:
            self.stSetID.Enable()
            self.inputClientID.Enable()
            self.stSetSecret.Enable()
            self.inputClientSecret.Enable()
        else:
            self.stSetID.Disable()
            self.inputClientID.Disable()
            self.stSetSecret.Disable()
            self.inputClientSecret.Disable()

    def getImage(self):
        return BitmapLoader.getBitmap("eve", "gui")

PFStatViewPref.register()
