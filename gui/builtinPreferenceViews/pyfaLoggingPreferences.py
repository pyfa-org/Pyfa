import wx

from gui.preferenceView import PreferenceView
from gui.bitmapLoader import BitmapLoader

import gui.mainFrame
import service
import config


class PFGeneralPref ( PreferenceView):
    title = "Logging"

    def populatePanel( self, panel ):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.dirtySettings = False
        #self.openFitsSettings = service.SettingsProvider.getInstance().getSettings("pyfaPrevOpenFits", {"enabled": False, "pyfaOpenFits": []})

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.stTitle = wx.StaticText( panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stTitle.Wrap( -1 )
        self.stTitle.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        mainSizer.Add( self.stTitle, 0, wx.ALL, 5 )

        self.stSubTitle = wx.StaticText( panel, wx.ID_ANY, u"(Cannot be changed while Pyfa is running.)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stSubTitle.Wrap( -1 )
        self.stSubTitle.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
        mainSizer.Add( self.stSubTitle, 0, wx.ALL, 5 )

        self.m_staticline1 = wx.StaticLine( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        mainSizer.Add( self.m_staticline1, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )

        #Debug Logging
        self.cbdebugLogging = wx.CheckBox( panel, wx.ID_ANY, u"Debug Logging Enabled", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.cbdebugLogging, 0, wx.ALL|wx.EXPAND, 5 )


        defCharSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.cbdebugLogging.SetValue(config.debug)
        self.cbdebugLogging.Bind(wx.EVT_CHECKBOX, self.onCBdebugLogging)

        panel.SetSizer( mainSizer )
        panel.Layout()


    def onCBdebugLogging(self, event):
        # We don't want users to be able to actually change this,
        # so if they try and change it, set it back to the current setting
        self.cbdebugLogging.SetValue(config.debug)

        # In case we do, down there road, here's a bit of a start.
        '''
        if self.cbdebugLogging.GetValue() is True:
            self.cbdebugLogging.SetValue(False)
            config.Debug = self.cbdebugLogging.GetValue()
        else:
            self.cbdebugLogging.SetValue(True)
        config.Debug = self.cbdebugLogging.GetValue()
        '''

    def getImage(self):
        return BitmapLoader.getBitmap("prefs_settings", "gui")


PFGeneralPref.register()
