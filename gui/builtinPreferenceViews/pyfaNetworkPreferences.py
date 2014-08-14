import wx

from gui.preferenceView import PreferenceView
from gui import bitmapLoader

import gui.mainFrame
import service

class PFNetworkPref ( PreferenceView):
    title = "Network"

    def populatePanel( self, panel ):

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.networkSettings = service.settings.NetworkSettings.getInstance()
        self.dirtySettings = False

        self.nMode = self.networkSettings.getMode()
        self.nAddr = self.networkSettings.getAddress()
        self.nPort = self.networkSettings.getPort()
        self.nType = self.networkSettings.getType()

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.stTitle = wx.StaticText( panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stTitle.Wrap( -1 )
        self.stTitle.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )

        mainSizer.Add( self.stTitle, 0, wx.ALL, 5 )

        self.m_staticline1 = wx.StaticLine( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        mainSizer.Add( self.m_staticline1, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )

        ptypeSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.stPType = wx.StaticText( panel, wx.ID_ANY, u"Mode:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stPType.Wrap( -1 )
        ptypeSizer.Add( self.stPType, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.chProxyTypeChoices = [ u"No proxy", u"Auto-detected proxy settings", u"Manual proxy settings" ]
        self.chProxyType = wx.Choice( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.chProxyTypeChoices, 0 )


        self.chProxyType.SetSelection( self.nMode )

        ptypeSizer.Add( self.chProxyType, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        mainSizer.Add( ptypeSizer, 0, wx.EXPAND, 5 )

        fgAddrSizer = wx.FlexGridSizer( 2, 2, 0, 0 )
        fgAddrSizer.AddGrowableCol( 1 )
        fgAddrSizer.SetFlexibleDirection( wx.BOTH )
        fgAddrSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )


        self.stPSetAddr = wx.StaticText( panel, wx.ID_ANY, u"Addr:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stPSetAddr.Wrap( -1 )
        fgAddrSizer.Add( self.stPSetAddr, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.editProxySettingsAddr = wx.TextCtrl( panel, wx.ID_ANY, self.nAddr, wx.DefaultPosition, wx.DefaultSize, 0 )

        fgAddrSizer.Add( self.editProxySettingsAddr, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5 )

        self.stPSetPort = wx.StaticText( panel, wx.ID_ANY, u"Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stPSetPort.Wrap( -1 )

        fgAddrSizer.Add( self.stPSetPort, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.editProxySettingsPort = wx.TextCtrl( panel, wx.ID_ANY, self.nPort, wx.DefaultPosition, wx.DefaultSize, 0 )

        fgAddrSizer.Add( self.editProxySettingsPort, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5 )

        mainSizer.Add( fgAddrSizer, 0, wx.EXPAND, 5)

        self.stPSAutoDetected = wx.StaticText( panel, wx.ID_ANY, u"Auto-detected: ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stPSAutoDetected.Wrap( -1 )
        mainSizer.Add( self.stPSAutoDetected, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        btnSizer = wx.BoxSizer( wx.HORIZONTAL )
        btnSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )

        self.btnApply = wx.Button( panel, wx.ID_ANY, u"Apply", wx.DefaultPosition, wx.DefaultSize, 0 )

        btnSizer.Add( self.btnApply, 0, wx.ALL, 5 )

        mainSizer.Add(btnSizer, 0, wx.EXPAND,5)

        proxy = self.networkSettings.autodetect()

        if proxy is not None:
            addr,port  =  proxy
            txt = addr + ":" + str(port)
        else:
            txt = "None"

        self.stPSAutoDetected.SetLabel("Auto-detected: " + txt)
        self.stPSAutoDetected.Disable()

        self.chProxyType.Bind(wx.EVT_CHOICE, self.OnCHProxyTypeSelect)
        self.editProxySettingsAddr.Bind(wx.EVT_TEXT, self.OnEditPSAddrText)
        self.editProxySettingsPort.Bind(wx.EVT_TEXT, self.OnEditPSPortText)


        self.btnApply.Bind(wx.EVT_BUTTON, self.OnBtnApply)

        self.UpdateApplyButtonState()

        if self.nMode is not 2:
            self.ToggleProxySettings(False)
        else:
            self.ToggleProxySettings(True)

        panel.SetSizer( mainSizer )
        panel.Layout()

    def OnEditPSAddrText(self, event):
        self.nAddr = self.editProxySettingsAddr.GetValue()
        self.dirtySettings = True
        self.UpdateApplyButtonState()

    def OnEditPSPortText(self, event):
        self.nPort = self.editProxySettingsPort.GetValue()
        self.dirtySettings = True
        self.UpdateApplyButtonState()

    def OnBtnApply(self, event):
        self.dirtySettings = False
        self.UpdateApplyButtonState()
        self.SaveSettings()

    def SaveSettings(self):
        self.networkSettings.setMode(self.nMode)
        self.networkSettings.setAddress(self.nAddr)
        self.networkSettings.setPort(self.nPort)
        self.networkSettings.setType(self.nType)

    def UpdateApplyButtonState(self):
        if self.dirtySettings:
            self.btnApply.Enable()
        else:
            self.btnApply.Disable()

    def OnCHProxyTypeSelect(self, event):
        choice = self.chProxyType.GetSelection()

        self.nMode = choice
        self.dirtySettings = True

        self.UpdateApplyButtonState()

        if choice is not 2:
            self.ToggleProxySettings(False)
        else:
            self.ToggleProxySettings(True)

    def ToggleProxySettings(self, mode):
        if mode:
            self.stPSetAddr.Enable()
            self.editProxySettingsAddr.Enable()
            self.stPSetPort.Enable()
            self.editProxySettingsPort.Enable()
        else:
            self.stPSetAddr.Disable()
            self.editProxySettingsAddr.Disable()
            self.stPSetPort.Disable()
            self.editProxySettingsPort.Disable()

    def getImage(self):
        return bitmapLoader.getBitmap("prefs_proxy", "icons")

PFNetworkPref.register()
