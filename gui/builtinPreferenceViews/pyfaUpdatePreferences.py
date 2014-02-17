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
to receive notifications for.
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
        
        self.suppressAll = wx.CheckBox( panel, wx.ID_ANY, u"Don't check for updates", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.suppressPrerelease = wx.CheckBox( panel, wx.ID_ANY, u"Suppress pre-release notifications", wx.DefaultPosition, wx.DefaultSize, 0 )

        mainSizer.Add( self.suppressAll, 0, wx.ALL|wx.EXPAND, 5 )
        mainSizer.Add( self.suppressPrerelease, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.suppressAll.Bind(wx.EVT_CHECKBOX, self.OnSuppressAllStateChange)
        self.suppressPrerelease.Bind(wx.EVT_CHECKBOX, self.OnPrereleaseStateChange)
        
        self.suppressAll.SetValue(self.UpdateSettings.get('all'))
        self.suppressPrerelease.SetValue(self.UpdateSettings.get('prerelease'))
        
        if (self.UpdateSettings.get('version')):
            self.versionSizer = wx.BoxSizer( wx.VERTICAL )

            
            self.versionTitle = wx.StaticText( panel, wx.ID_ANY, "Suppressing "+self.UpdateSettings.get('version')+" Notifications", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.versionTitle.Wrap( -1 )
            self.versionTitle.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
            
            self.versionInfo = '''
There is a release available which you have chosen to suppress. 
You can choose to reset notification suppression for this release, 
or download the new release from GitHub.
'''

            self.versionSizer.AddSpacer( ( 5, 5), 0, wx.EXPAND, 5 )

            self.versionSizer.Add( wx.StaticLine( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL ), 0, wx.EXPAND, 5 )
            self.versionSizer.AddSpacer( ( 5, 5), 0, wx.EXPAND, 5 )

            self.versionSizer.Add( self.versionTitle, 0, wx.EXPAND, 5 )
            self.versionDesc = wx.StaticText( panel, wx.ID_ANY, self.versionInfo, wx.DefaultPosition, wx.DefaultSize, 0 )
            self.versionSizer.Add( self.versionDesc, 0, wx.ALL, 5 )

            actionSizer = wx.BoxSizer( wx.HORIZONTAL )
            resetSizer = wx.BoxSizer( wx.VERTICAL )
            
            self.downloadButton = wx.Button( panel, wx.ID_ANY, "Download", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.downloadButton.Bind(wx.EVT_BUTTON, self.OnDownload)
            resetSizer.Add( self.downloadButton, 0, wx.ALL, 5 )
            actionSizer.Add( resetSizer, 1, wx.EXPAND, 5 )

            self.resetButton = wx.Button( panel, wx.ID_ANY, "Reset Suppression", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.resetButton.Bind(wx.EVT_BUTTON, self.ResetSuppression)
            actionSizer.Add( self.resetButton, 0, wx.ALL, 5 )
            self.versionSizer.Add( actionSizer, 0, wx.EXPAND, 5 )
            mainSizer.Add( self.versionSizer, 0, wx.EXPAND, 5 )
            
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

    def OnPrereleaseStateChange(self, event):
        self.UpdateSettings.set('prerelease', self.suppressPrerelease.IsChecked())

    def ResetSuppression(self, event):
        self.UpdateSettings.set('version', None)

        # Todo: Find a way to hide the entire panel in one go
        self.versionSizer.Hide(True)
        self.versionTitle.Hide()
        self.versionDesc.Hide()
        self.downloadButton.Hide()
        self.resetButton.Hide()
        self.resetButton.Hide()
        
    def OnDownload(self, event):
        wx.LaunchDefaultBrowser('https://github.com/DarkFenX/Pyfa/releases/tag/'+self.UpdateSettings.get('version'))
    
    def getImage(self):
        return bitmapLoader.getBitmap("pyfa64", "icons")

PFUpdatePref.register()