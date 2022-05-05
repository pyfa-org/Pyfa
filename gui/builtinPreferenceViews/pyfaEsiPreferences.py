# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui.bitmap_loader import BitmapLoader
from gui.preferenceView import PreferenceView
from service.settings import EsiSettings

# noinspection PyPackageRequirements
_t = wx.GetTranslation


class PFEsiPref(PreferenceView):

    def populatePanel(self, panel):
        self.title = _t("EVE SSO")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = EsiSettings.getInstance()
        self.dirtySettings = False
        dlgWidth = panel.GetParent().GetParent().ClientSize.width
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        mainSizer.Add(self.stTitle, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.stInfo = wx.StaticText(panel, wx.ID_ANY,
                                    _t("Please see the pyfa wiki on GitHub for information regarding these options."),
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.stInfo.Wrap(dlgWidth - 50)
        mainSizer.Add(self.stInfo, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.enforceJwtExpiration = wx.CheckBox(panel, wx.ID_ANY, _t("Enforce Token Expiration"), wx.DefaultPosition,
                                        wx.DefaultSize,
                                        0)
        self.enforceJwtExpiration.SetToolTip(wx.ToolTip(_t("This option is a workaround in case you cannot log into EVE SSO "
                                                       "due to 'Signature has expired' error")))
        mainSizer.Add(self.enforceJwtExpiration, 0, wx.ALL | wx.EXPAND, 5)

        rbSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rbMode = wx.RadioBox(panel, -1, _t("Login Authentication Method"), wx.DefaultPosition, wx.DefaultSize,
                                  [_t('Local Server'), _t('Manual')], 1, wx.RA_SPECIFY_COLS)
        self.rbMode.SetItemToolTip(0, _t("This option starts a local webserver that EVE SSO Server will call back to"
                                         " with information about the character login."))
        self.rbMode.SetItemToolTip(1, _t("This option prompts users to copy and paste information to allow for"
                                         " character login. Use this if having issues with the local server."))

        self.rbMode.SetSelection(self.settings.get('loginMode'))
        self.enforceJwtExpiration.SetValue(self.settings.get("enforceJwtExpiration" or True))

        rbSizer.Add(self.rbMode, 1, wx.TOP | wx.RIGHT, 5)

        self.rbMode.Bind(wx.EVT_RADIOBOX, self.OnModeChange)
        self.enforceJwtExpiration.Bind(wx.EVT_CHECKBOX, self.OnEnforceChange)
        mainSizer.Add(rbSizer, 1, wx.ALL | wx.EXPAND, 0)

        panel.SetSizer(mainSizer)
        panel.Layout()

    def OnTimeoutChange(self, event):
        self.settings.set('timeout', event.GetEventObject().GetValue())

    def OnModeChange(self, event):
        self.settings.set('loginMode', event.GetInt())

    def OnEnforceChange(self, event):
        self.settings.set('enforceJwtExpiration', self.enforceJwtExpiration.GetValue())
        event.Skip()

    def getImage(self):
        return BitmapLoader.getBitmap("eve", "gui")


PFEsiPref.register()
