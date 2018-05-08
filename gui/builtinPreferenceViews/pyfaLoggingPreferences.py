import wx

from gui.preferenceView import PreferenceView
from gui.bitmap_loader import BitmapLoader
import config
from logbook import Logger

pyfalog = Logger(__name__)


def OnDumpLogs(event):
    pyfalog.critical("Dump log button was pressed. Writing all logs to log file.")


class PFGeneralPref(PreferenceView):
    title = "Logging"

    def populatePanel(self, panel):
        self.dirtySettings = False

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        mainSizer.Add(self.stTitle, 0, wx.ALL, 5)

        self.stSubTitle = wx.StaticText(panel, wx.ID_ANY, "(Cannot be changed while pyfa is running. Set via command line switches.)",
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.stSubTitle.Wrap(-1)
        mainSizer.Add(self.stSubTitle, 0, wx.ALL, 3)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        # Database path
        self.stLogPath = wx.StaticText(panel, wx.ID_ANY, "Log file location:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stLogPath.Wrap(-1)
        mainSizer.Add(self.stLogPath, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.inputLogPath = wx.TextCtrl(panel, wx.ID_ANY, config.logPath, wx.DefaultPosition, wx.DefaultSize, 0)
        self.inputLogPath.SetEditable(False)
        self.inputLogPath.SetBackgroundColour((200, 200, 200))
        mainSizer.Add(self.inputLogPath, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        import requests
        self.certPath = wx.StaticText(panel, wx.ID_ANY, "Cert Path:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.certPath .Wrap(-1)
        mainSizer.Add(self.certPath, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.certPathCtrl = wx.TextCtrl(panel, wx.ID_ANY, requests.certs.where(), wx.DefaultPosition, wx.DefaultSize, 0)
        self.certPathCtrl.SetEditable(False)
        self.certPathCtrl.SetBackgroundColour((200, 200, 200))
        mainSizer.Add(self.certPathCtrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        # Debug Logging
        self.cbdebugLogging = wx.CheckBox(panel, wx.ID_ANY, "Debug Logging Enabled", wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbdebugLogging, 0, wx.ALL | wx.EXPAND, 5)

        self.stDumpLogs = wx.StaticText(panel, wx.ID_ANY, "Pressing this button will cause all logs in memory to write to the log file:",
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.stDumpLogs, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.btnDumpLogs = wx.Button(panel, wx.ID_ANY, "Dump All Logs", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btnDumpLogs.Bind(wx.EVT_BUTTON, OnDumpLogs)
        mainSizer.Add(self.btnDumpLogs, 0, wx.ALIGN_LEFT, 5)

        self.cbdebugLogging.SetValue(config.debug)
        self.cbdebugLogging.Bind(wx.EVT_CHECKBOX, self.onCBdebugLogging)

        panel.SetSizer(mainSizer)
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
        return BitmapLoader.getBitmap("settings_log", "gui")


PFGeneralPref.register()
