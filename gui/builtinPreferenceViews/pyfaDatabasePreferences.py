import wx

from gui.preferenceView import PreferenceView
from gui.bitmapLoader import BitmapLoader

import gui.mainFrame
import service
import config

import logging

logger = logging.getLogger(__name__)

from eos.db.saveddata.loadDefaultDatabaseValues import DefaultDatabaseValues


class PFGeneralPref ( PreferenceView):
    title = "Database"

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

        #Save in Root
        self.cbsaveInRoot = wx.CheckBox( panel, wx.ID_ANY, u"Using Executable Path for Saved Fit Database and Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.cbsaveInRoot, 0, wx.ALL|wx.EXPAND, 5 )

        #Database path
        self.stSetUserPath = wx.StaticText( panel, wx.ID_ANY, u"Pyfa User Path:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stSetUserPath.Wrap( -1 )
        mainSizer.Add( self.stSetUserPath, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        self.inputUserPath = wx.TextCtrl(panel, wx.ID_ANY, config.savePath, wx.DefaultPosition, wx.DefaultSize, 0)
        self.inputUserPath.SetEditable(False)
        self.inputUserPath.SetBackgroundColour((200, 200, 200))
        mainSizer.Add(self.inputUserPath, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        #Save DB
        self.stFitDB = wx.StaticText( panel, wx.ID_ANY, u"Fitting Database:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stFitDB.Wrap( -1 )
        mainSizer.Add( self.stFitDB, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.inputFitDB = wx.TextCtrl(panel, wx.ID_ANY, config.saveDB, wx.DefaultPosition, wx.DefaultSize, 0)
        self.inputFitDB.SetEditable(False)
        self.inputFitDB.SetBackgroundColour((200, 200, 200))
        mainSizer.Add(self.inputFitDB, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        #Game Data DB
        self.stGameDB = wx.StaticText( panel, wx.ID_ANY, u"Game Database:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stGameDB.Wrap( -1 )
        mainSizer.Add( self.stGameDB, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.inputGameDB = wx.TextCtrl(panel, wx.ID_ANY, config.gameDB, wx.DefaultPosition, wx.DefaultSize, 0)
        self.inputGameDB.SetEditable(False)
        self.inputGameDB.SetBackgroundColour((200, 200, 200))
        mainSizer.Add(self.inputGameDB, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)


        defCharSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.cbsaveInRoot.SetValue(config.saveInRoot)
        self.cbsaveInRoot.Bind(wx.EVT_CHECKBOX, self.onCBsaveInRoot)

        self.inputUserPath.Bind(wx.EVT_LEAVE_WINDOW, self.OnWindowLeave)
        self.inputFitDB.Bind(wx.EVT_LEAVE_WINDOW, self.OnWindowLeave)
        self.inputGameDB.Bind(wx.EVT_LEAVE_WINDOW, self.OnWindowLeave)

        panel.SetSizer( mainSizer )
        panel.Layout()


    def onCBsaveInRoot(self, event):
        # We don't want users to be able to actually change this,
        # so if they try and change it, set it back to the current setting
        self.cbsaveInRoot.SetValue(config.saveInRoot)

        # If we ever enable it might need this.
        '''
        config.saveInRoot = self.cbsaveInRoot.GetValue()
        '''

    def getImage(self):
        return BitmapLoader.getBitmap("prefs_settings", "gui")

    def OnWindowLeave(self, event):
        # We don't want to do anything when they leave,
        # but in the future we'd want to make sure settings
        # changed get saved.
        pass

        '''
        #Set database path
        config.defPaths(self.inputFitDBPath.GetValue())

        logger.debug("Running database import")
        if self.cbimportDefaults is True:
            # Import default database values
            # Import values that must exist otherwise Pyfa breaks
            DefaultDatabaseValues.importRequiredDefaults()
            # Import default values for damage profiles
            DefaultDatabaseValues.importDamageProfileDefaults()
            # Import default values for target resist profiles
            DefaultDatabaseValues.importResistProfileDefaults()
        '''

PFGeneralPref.register()
