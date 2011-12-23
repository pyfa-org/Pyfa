import wx
import service
import urllib2

from gui.preferenceView import PreferenceView
from gui import bitmapLoader

import gui.mainFrame
import service
import gui.globalEvents as GE


class PFGlobalPref ( PreferenceView):
    title = "Pyfa Global Options"

    def populatePanel( self, panel ):

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.proxySettings = service.settings.ProxySettings.getInstance()
        self.dirtySettings = False

        self.nMode = self.proxySettings.getMode()
        self.nAddr = self.proxySettings.getAddress()
        self.nPort = self.proxySettings.getPort()
        self.nType = self.proxySettings.getType()


        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.stTitle = wx.StaticText( panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stTitle.Wrap( -1 )
        self.stTitle.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )

        mainSizer.Add( self.stTitle, 0, wx.ALL, 5 )

#        self.m_staticline1 = wx.StaticLine( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
#        mainSizer.Add( self.m_staticline1, 0, wx.EXPAND, 5 )

        self.cbGlobalChar = wx.CheckBox( panel, wx.ID_ANY, u"Use global character", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.cbGlobalChar, 0, wx.ALL|wx.EXPAND, 5 )

        self.cbGlobalDmgPattern = wx.CheckBox( panel, wx.ID_ANY, u"Use global damage pattern", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.cbGlobalDmgPattern, 0, wx.ALL|wx.EXPAND, 5 )

        self.cbGlobalForceReload = wx.CheckBox( panel, wx.ID_ANY, u"Factor in reload time", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.cbGlobalForceReload, 0, wx.ALL|wx.EXPAND, 5 )

        defCharSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.stDefChar = wx.StaticText( panel, wx.ID_ANY, u"Default character:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stDefChar.Wrap( -1 )
        defCharSizer.Add( self.stDefChar, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        chDefaultCharChoices = []
        self.chDefaultChar = wx.Choice( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chDefaultCharChoices, 0 )
        self.chDefaultChar.SetSelection( 0 )
        defCharSizer.Add( self.chDefaultChar, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        mainSizer.Add( defCharSizer, 0, wx.EXPAND, 5 )


        self.m_staticline2 = wx.StaticLine( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        mainSizer.Add( self.m_staticline2, 0, wx.EXPAND, 5 )

        self.stPTitle = wx.StaticText( panel, wx.ID_ANY, "Proxy settings", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stPTitle.Wrap( -1 )
        self.stPTitle.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )

        mainSizer.Add( self.stPTitle, 0, wx.ALL, 5 )


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

        proxy = None
        proxAddr = proxPort = ""
        proxydict = urllib2.ProxyHandler().proxies
        txt = "Auto-detected: "

        validPrefixes = ("https", "http")

        for prefix in validPrefixes:
            if not prefix in proxydict:
                continue
            proxyline = proxydict[prefix]
            proto = "{0}://".format(prefix)
            if proxyline[:len(proto)] == proto:
                proxyline = proxyline[len(proto):]
            proxAddr, proxPort = proxyline.split(":")
            proxPort = int(proxPort.rstrip("/"))
            proxy = (proxAddr, proxPort)
            break

        if len(proxAddr) == 0:
            txt += "None"
        else:
            txt += proto + proxAddr + ":" + str(proxPort)

        self.stPSAutoDetected.SetLabel(txt)
        self.stPSAutoDetected.Disable()

        cChar = service.Character.getInstance()
        charList = cChar.getCharacterList()

        for id, name, active in charList:
            self.chDefaultChar.Append(name, id)

        self.chDefaultChar.SetSelection(0)

        self.sFit = service.Fit.getInstance()
        useGlobalChar = self.sFit.serviceFittingOptions["useGlobalCharacter"]
        useGlobalDmgPattern = self.sFit.serviceFittingOptions["useGlobalDamagePattern"]
        useGlobalForceReload = self.sFit.serviceFittingOptions["useGlobalForceReload"]

        self.cbGlobalChar.SetValue(useGlobalChar)
        self.cbGlobalDmgPattern.SetValue(useGlobalDmgPattern)
        self.cbGlobalForceReload.SetValue(useGlobalForceReload)

        self.cbGlobalChar.Bind(wx.EVT_CHECKBOX, self.OnCBGlobalCharStateChange)
        self.cbGlobalDmgPattern.Bind(wx.EVT_CHECKBOX, self.OnCBGlobalDmgPatternStateChange)
        self.cbGlobalForceReload.Bind(wx.EVT_CHECKBOX, self.OnCBGlobalForceReloadStateChange)

        self.chDefaultChar.Disable()
        self.chDefaultChar.Show(False)
        self.stDefChar.Show(False)

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
        self.proxySettings.setMode(self.nMode)
        self.proxySettings.setAddress(self.nAddr)
        self.proxySettings.setPort(self.nPort)
        self.proxySettings.setType(self.nType)

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

    def OnCBProxySettingsStateChange(self, event):
        self.ToggleProxySettings(self.cbProxySettings.GetValue())
        event.Skip()

    def OnCBGlobalForceReloadStateChange(self, event):
        self.sFit.serviceFittingOptions["useGlobalForceReload"] = self.cbGlobalForceReload.GetValue()
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

    def getImage(self):
        return bitmapLoader.getBitmap("pyfa64", "icons")

PFGlobalPref.register()