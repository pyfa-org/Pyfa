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
        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.stTitle = wx.StaticText( panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stTitle.Wrap( -1 )
        self.stTitle.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )

        mainSizer.Add( self.stTitle, 0, wx.ALL, 5 )

        self.m_staticline1 = wx.StaticLine( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        mainSizer.Add( self.m_staticline1, 0, wx.EXPAND, 5 )

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


#        self.cbProxySettings = wx.CheckBox( panel, wx.ID_ANY, u"Manual proxy settings", wx.DefaultPosition, wx.DefaultSize, 0 )
#        mainSizer.Add( self.cbProxySettings, 0, wx.ALL, 5 )

        ptypeSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.stPType = wx.StaticText( panel, wx.ID_ANY, u"Mode:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stPType.Wrap( -1 )
        ptypeSizer.Add( self.stPType, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.chProxyTypeChoices = [ u"No proxy settings", u"Auto-detected proxy settings", u"Manual proxy settings" ]
        self.chProxyType = wx.Choice( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.chProxyTypeChoices, 0 )
        self.chProxyType.SetSelection( 0 )

        ptypeSizer.Add( self.chProxyType, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        mainSizer.Add( ptypeSizer, 0, wx.EXPAND, 5 )

        fgAddrSizer = wx.FlexGridSizer( 2, 2, 0, 0 )
        fgAddrSizer.SetFlexibleDirection( wx.BOTH )
        fgAddrSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )


        self.stPSetAddr = wx.StaticText( panel, wx.ID_ANY, u"Addr:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stPSetAddr.Wrap( -1 )
        fgAddrSizer.Add( self.stPSetAddr, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.editProxySettingsAddr = wx.TextCtrl( panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )

        fgAddrSizer.Add( self.editProxySettingsAddr, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.stPSetPort = wx.StaticText( panel, wx.ID_ANY, u"Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stPSetPort.Wrap( -1 )

        fgAddrSizer.Add( self.stPSetPort, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.editProxySettingsPort = wx.TextCtrl( panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )

        fgAddrSizer.Add( self.editProxySettingsPort, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        mainSizer.Add( fgAddrSizer, 0, wx.EXPAND, 5)

        self.stPSAutoDetected = wx.StaticText( panel, wx.ID_ANY, u"Auto-detected: ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stPSAutoDetected.Wrap( -1 )
        mainSizer.Add( self.stPSAutoDetected, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        ps = urllib2.ProxyHandler().proxies
        txt = "Auto-detected: "

        for type in ps:
            txt += ps[type]
            txt += "  "

        if len(ps) == 0:
            txt += "None"

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

#        self.cbProxySettings.Bind(wx.EVT_CHECKBOX, self.OnCBProxySettingsStateChange)
        self.chDefaultChar.Disable()
        self.chDefaultChar.Show(False)
        self.stDefChar.Show(False)

#        self.ToggleProxySettings(self.cbProxySettings.GetValue())

        panel.SetSizer( mainSizer )
        panel.Layout()

    def ToggleProxySettings(self, mode):
        if mode:
            self.chProxyType.Enable()
            self.editProxySettings.Enable()
        else:
            self.chProxyType.Disable()
            self.editProxySettings.Disable()

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