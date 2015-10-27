import wx

from gui.preferenceView import PreferenceView
from gui.bitmapLoader import BitmapLoader

import gui.mainFrame
import service

class PFCrestPref ( PreferenceView):
    title = "CREST"

    def populatePanel( self, panel ):

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = service.settings.CRESTSettings.getInstance()
        self.dirtySettings = False
        dlgWidth = panel.GetParent().GetParent().ClientSize.width
        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.stTitle = wx.StaticText( panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stTitle.Wrap( -1 )
        self.stTitle.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )

        mainSizer.Add( self.stTitle, 0, wx.ALL, 5 )

        self.m_staticline1 = wx.StaticLine( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        mainSizer.Add( self.m_staticline1, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )

        self.stInfo = wx.StaticText( panel, wx.ID_ANY, u"Please see the pyfa wiki on GitHub for information regarding these options.", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stInfo.Wrap(dlgWidth - 50)
        mainSizer.Add( self.stInfo, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )

        self.grantRadioBtn1 = wx.RadioButton( panel, wx.ID_ANY, u"Implicit Grant", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.grantRadioBtn1, 0, wx.ALL, 5 )

        self.grantRadioBtn2 = wx.RadioButton( panel, wx.ID_ANY, u"User-supplied details", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.grantRadioBtn2, 0, wx.ALL, 5 )

        proxyTitle = wx.StaticText( panel, wx.ID_ANY, "CREST client details", wx.DefaultPosition, wx.DefaultSize, 0 )
        proxyTitle.Wrap( -1 )
        proxyTitle.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )

        mainSizer.Add( proxyTitle, 0, wx.ALL, 5 )
        mainSizer.Add( wx.StaticLine( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL ), 0, wx.EXPAND, 5 )

        self.grantRadioBtn1.SetValue(self.settings.get('mode') == 0)
        self.grantRadioBtn2.SetValue(self.settings.get('mode') == 1)

        self.grantRadioBtn1.Bind(wx.EVT_RADIOBUTTON, self.OnRadioChange)
        self.grantRadioBtn2.Bind(wx.EVT_RADIOBUTTON, self.OnRadioChange)

        fgAddrSizer = wx.FlexGridSizer( 2, 2, 0, 0 )
        fgAddrSizer.AddGrowableCol( 1 )
        fgAddrSizer.SetFlexibleDirection( wx.BOTH )
        fgAddrSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.stSetID = wx.StaticText( panel, wx.ID_ANY, u"Client ID:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stSetID.Wrap( -1 )
        fgAddrSizer.Add( self.stSetID, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.inputClientID = wx.TextCtrl( panel, wx.ID_ANY, self.settings.get('clientID'), wx.DefaultPosition, wx.DefaultSize, 0 )

        fgAddrSizer.Add( self.inputClientID, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5 )

        self.stSetSecret = wx.StaticText( panel, wx.ID_ANY, u"Client Secret:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stSetSecret.Wrap( -1 )

        fgAddrSizer.Add( self.stSetSecret, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.inputClientSecret = wx.TextCtrl( panel, wx.ID_ANY, self.settings.get('clientSecret'), wx.DefaultPosition, wx.DefaultSize, 0 )

        fgAddrSizer.Add( self.inputClientSecret, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5 )

        self.btnApply = wx.Button( panel, wx.ID_ANY, u"Save Client Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btnApply.Bind(wx.EVT_BUTTON, self.OnBtnApply)

        mainSizer.Add( fgAddrSizer, 0, wx.EXPAND, 5)
        mainSizer.Add( self.btnApply, 0, wx.ALIGN_RIGHT, 5)

        self.ToggleProxySettings(self.settings.get('mode'))

        panel.SetSizer( mainSizer )
        panel.Layout()

    def OnRadioChange(self, event):
        self.settings.set('mode', 0 if self.grantRadioBtn1.Value else 1)
        self.ToggleProxySettings(self.settings.get('mode'))

    def OnBtnApply(self, event):
        self.settings.set('clientID', self.inputClientID.GetValue())
        self.settings.set('clientSecret', self.inputClientSecret.GetValue())
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
        return BitmapLoader.getBitmap("prefs_proxy", "gui")

PFCrestPref.register()
