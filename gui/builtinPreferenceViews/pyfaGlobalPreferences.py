import wx
import service

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

        panel.SetSizer( mainSizer )
        panel.Layout()

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