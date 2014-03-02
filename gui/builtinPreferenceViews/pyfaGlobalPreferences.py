import wx
import service
import urllib2

from gui.preferenceView import PreferenceView
from gui import bitmapLoader

import gui.mainFrame
import service
import gui.globalEvents as GE


class PFGlobalPref ( PreferenceView):
    title = "General Options"

    def populatePanel( self, panel ):
        charHelpText = '''Each fit has a character assigned to it, with different fits having different
character. Choose this option if you do not want to switch characters in between fits.'''
        dmgHelpText = '''Each fit has a damage profile character assigned to it, with different fits having different
profiles. Choose this option if you do not want to switch profiles in between fits.'''

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.dirtySettings = False

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.stTitle = wx.StaticText( panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stTitle.Wrap( -1 )
        self.stTitle.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )

        mainSizer.Add( self.stTitle, 0, wx.ALL, 5 )

        #self.m_staticline1 = wx.StaticLine( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        #mainSizer.Add( self.m_staticline1, 0, wx.EXPAND, 5 )

        self.cbGlobalChar = wx.CheckBox( panel, wx.ID_ANY, u"Use global character", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.cbGlobalChar, 0, wx.ALL|wx.EXPAND, 5 )

        self.cbGlobalDmgPattern = wx.CheckBox( panel, wx.ID_ANY, u"Use global damage pattern", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.cbGlobalDmgPattern, 0, wx.ALL|wx.EXPAND, 5 )

        self.cbGlobalForceReload = wx.CheckBox( panel, wx.ID_ANY, u"Factor in reload time", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.cbGlobalForceReload, 0, wx.ALL|wx.EXPAND, 5 )

        self.cbFitColorSlots = wx.CheckBox( panel, wx.ID_ANY, u"Color fitting view by slot", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.cbFitColorSlots, 0, wx.ALL|wx.EXPAND, 5 )

        # Needs to be implemented - save active fittings and reapply when starting pyfa
        #self.cbReopenFits = wx.CheckBox( panel, wx.ID_ANY, u"Reopen Fits", wx.DefaultPosition, wx.DefaultSize, 0 )
        #mainSizer.Add( self.cbReopenFits, 0, wx.ALL|wx.EXPAND, 5 )

        defCharSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.sFit = service.Fit.getInstance()
        useGlobalChar = self.sFit.serviceFittingOptions["useGlobalCharacter"]
        useGlobalDmgPattern = self.sFit.serviceFittingOptions["useGlobalDamagePattern"]
        useGlobalForceReload = self.sFit.serviceFittingOptions["useGlobalForceReload"]

        self.cbGlobalChar.SetValue(useGlobalChar)
        self.cbGlobalDmgPattern.SetValue(useGlobalDmgPattern)
        self.cbGlobalForceReload.SetValue(useGlobalForceReload)
        self.cbFitColorSlots.SetValue(self.sFit.serviceFittingOptions["colorFitBySlot"] or False)

        self.cbGlobalChar.Bind(wx.EVT_CHECKBOX, self.OnCBGlobalCharStateChange)
        self.cbGlobalDmgPattern.Bind(wx.EVT_CHECKBOX, self.OnCBGlobalDmgPatternStateChange)
        self.cbGlobalForceReload.Bind(wx.EVT_CHECKBOX, self.OnCBGlobalForceReloadStateChange)
        self.cbFitColorSlots.Bind(wx.EVT_CHECKBOX, self.onCBGlobalColorBySlot)

        panel.SetSizer( mainSizer )
        panel.Layout()

    def onCBGlobalColorBySlot(self, event):
        self.sFit.serviceFittingOptions["colorFitBySlot"] = self.cbFitColorSlots.GetValue()
        fitID = self.mainFrame.getActiveFit()
        self.sFit.refreshFit(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))
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
        return bitmapLoader.getBitmap("prefs_settings", "icons")

PFGlobalPref.register()