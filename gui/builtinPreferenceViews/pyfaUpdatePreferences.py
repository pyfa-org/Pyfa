import wx
import service
import os

from gui.preferenceView import PreferenceView
from gui import bitmapLoader

import service
import gui.globalEvents as GE


class PFUpdatePref (PreferenceView):
    title = "Pyfa Update Options"
    desc  = """
Pyfa can automatically check and notify you of new releases. 
These options will allow you to choose what kind of updates, if any, you wish 
to receive notifications for
"""

    def populatePanel( self, panel ):
        self.UpdateSettings = service.settings.UpdateSettings.getInstance()
        self.dirtySettings = False

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.stTitle = wx.StaticText( panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stTitle.Wrap( -1 )
        self.stTitle.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        mainSizer.Add( self.stTitle, 0, wx.ALL, 5 )
        
        self.stDesc = wx.StaticText( panel, wx.ID_ANY, self.desc, wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.stDesc, 0, wx.ALL, 5 )
        
        self.suppressAll = wx.CheckBox( panel, wx.ID_ANY, u"Suppress all update notifications", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.suppressPrerelease = wx.CheckBox( panel, wx.ID_ANY, u"Suppress only pre-release notifications", wx.DefaultPosition, wx.DefaultSize, 0 )
        
        mainSizer.Add( self.suppressAll, 0, wx.ALL|wx.EXPAND, 5 )
        mainSizer.Add( self.suppressPrerelease, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.suppressAll.Bind(wx.EVT_CHECKBOX, self.OnSuppressAllStateChange)
        
        self.ToggleSuppressAll(self.suppressAll.IsChecked())
        
        panel.SetSizer( mainSizer )
        panel.Layout()

    def ToggleSuppressAll(self, bool):
        ''' Toggles other inputs on/off depending on value of SuppressAll '''
        if bool:
            self.suppressPrerelease.Disable()
        else:
            self.suppressPrerelease.Enable()

    def OnSuppressAllStateChange(self, event):
        self.UpdateSettings.set('all', self.suppressAll.IsChecked())
        self.ToggleSuppressAll(self.suppressAll.IsChecked())

    def getImage(self):
        return bitmapLoader.getBitmap("pyfa64", "icons")

PFUpdatePref.register()