# noinspection PyPackageRequirements
import wx

from gui.preferenceView import PreferenceView
from gui.bitmap_loader import BitmapLoader

import gui.mainFrame

from service.settings import EsiSettings

# noinspection PyPackageRequirements
from wx.lib.intctrl import IntCtrl

from service.esi import Esi


class PFEsiPref(PreferenceView):
    title = "EVE SSO"

    def populatePanel(self, panel):

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = EsiSettings.getInstance()
        self.dirtySettings = False
        dlgWidth = panel.GetParent().GetParent().ClientSize.width
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))

        mainSizer.Add(self.stTitle, 0, wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.stInfo = wx.StaticText(panel, wx.ID_ANY,
                                    "Please see the pyfa wiki on GitHub for information regarding these options.",
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.stInfo.Wrap(dlgWidth - 50)
        mainSizer.Add(self.stInfo, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        rbSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rbMode = wx.RadioBox(panel, -1, "Login Authentication Method", wx.DefaultPosition, wx.DefaultSize,
                                  ['Local Server', 'Manual'], 1, wx.RA_SPECIFY_COLS)
        self.rbMode.SetItemToolTip(0, "This options starts a local webserver that the web application will call back to with information about the character login.")
        self.rbMode.SetItemToolTip(1, "This option prompts users to copy and paste information from the web application to allow for character login. Use this if having issues with the local server.")
        # self.rbServer = wx.RadioBox(panel, -1, "Server", wx.DefaultPosition, wx.DefaultSize,
        #                             ['Tranquility', 'Singularity'], 1, wx.RA_SPECIFY_COLS)

        self.rbMode.SetSelection(self.settings.get('loginMode'))
        # self.rbServer.SetSelection(self.settings.get('server'))

        rbSizer.Add(self.rbMode, 1, wx.TOP | wx.RIGHT, 5)
        # rbSizer.Add(self.rbServer, 1, wx.ALL, 5)

        self.rbMode.Bind(wx.EVT_RADIOBOX, self.OnModeChange)
        # self.rbServer.Bind(wx.EVT_RADIOBOX, self.OnServerChange)

        mainSizer.Add(rbSizer, 1, wx.ALL | wx.EXPAND, 0)

        timeoutSizer = wx.BoxSizer(wx.HORIZONTAL)

        # self.stTimout = wx.StaticText(panel, wx.ID_ANY, "Timeout (seconds):", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.stTimout.Wrap(-1)
        #
        # timeoutSizer.Add(self.stTimout, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # self.intTimeout = IntCtrl(panel, max=300000, limited=True, value=self.settings.get('timeout'))
        # timeoutSizer.Add(self.intTimeout, 0, wx.ALL, 5)
        # self.intTimeout.Bind(wx.lib.intctrl.EVT_INT, self.OnTimeoutChange)
        #
        # mainSizer.Add(timeoutSizer, 0, wx.ALL | wx.EXPAND, 0)

        # detailsTitle = wx.StaticText(panel, wx.ID_ANY, "CREST client details", wx.DefaultPosition, wx.DefaultSize, 0)
        # detailsTitle.Wrap(-1)
        # detailsTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        #
        # mainSizer.Add(detailsTitle, 0, wx.ALL, 5)
        # mainSizer.Add(wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL), 0,
        #               wx.EXPAND, 5)

        # fgAddrSizer = wx.FlexGridSizer(2, 2, 0, 0)
        # fgAddrSizer.AddGrowableCol(1)
        # fgAddrSizer.SetFlexibleDirection(wx.BOTH)
        # fgAddrSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        #
        # self.stSetID = wx.StaticText(panel, wx.ID_ANY, "Client ID:", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.stSetID.Wrap(-1)
        # fgAddrSizer.Add(self.stSetID, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        #
        # self.inputClientID = wx.TextCtrl(panel, wx.ID_ANY, self.settings.get('clientID'), wx.DefaultPosition,
        #                                  wx.DefaultSize, 0)
        #
        # fgAddrSizer.Add(self.inputClientID, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)
        #
        # self.stSetSecret = wx.StaticText(panel, wx.ID_ANY, "Client Secret:", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.stSetSecret.Wrap(-1)
        #
        # fgAddrSizer.Add(self.stSetSecret, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        #
        # self.inputClientSecret = wx.TextCtrl(panel, wx.ID_ANY, self.settings.get('clientSecret'), wx.DefaultPosition,
        #                                      wx.DefaultSize, 0)
        #
        # fgAddrSizer.Add(self.inputClientSecret, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)
        #
        # self.btnApply = wx.Button(panel, wx.ID_ANY, "Save Client Settings", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.btnApply.Bind(wx.EVT_BUTTON, self.OnBtnApply)
        #
        # mainSizer.Add(fgAddrSizer, 0, wx.EXPAND, 5)
        # mainSizer.Add(self.btnApply, 0, wx.ALIGN_RIGHT, 5)

        # self.ToggleProxySettings(self.settings.get('loginMode'))

        panel.SetSizer(mainSizer)
        panel.Layout()

    def OnTimeoutChange(self, event):
        self.settings.set('timeout', event.GetEventObject().GetValue())

    def OnModeChange(self, event):
        self.settings.set('loginMode', event.GetInt())

    def OnServerChange(self, event):
        self.settings.set('server', event.GetInt())

    def OnBtnApply(self, event):
        self.settings.set('clientID', self.inputClientID.GetValue().strip())
        self.settings.set('clientSecret', self.inputClientSecret.GetValue().strip())
        sEsi = Esi.getInstance()
        sEsi.delAllCharacters()

    def getImage(self):
        return BitmapLoader.getBitmap("eve", "gui")


PFEsiPref.register()
