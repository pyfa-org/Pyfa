import wx
import gui.mainFrame
import webbrowser
import gui.globalEvents as GE
import config
import time

from service.settings import EsiSettings

_t = wx.GetTranslation


class SsoLogin(wx.Dialog):

    def __init__(self, server: config.ApiServer, start_local_server=True):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        from service.esi import Esi
        super().__init__(
                self.mainFrame, id=wx.ID_ANY, title=_t("SSO Login"), style=wx.DEFAULT_DIALOG_STYLE,
                size=wx.Size(450, 240) if "wxGTK" in wx.PlatformInfo else wx.Size(400, 240))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        if start_local_server:
            text = wx.StaticText(self, wx.ID_ANY, _t("Waiting for character login through EVE Single Sign-On."))
            bSizer1.Add(text, 0, wx.ALL | wx.EXPAND, 10)
            bSizer1.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.EXPAND, 15)
            text = wx.StaticText(self, wx.ID_ANY, _t("If auto-login fails, copy and paste the token provided by pyfa.io"))
            bSizer1.Add(text, 0, wx.ALL | wx.EXPAND, 10)
        elif server.name == "Serenity":
            text = wx.StaticText(self, wx.ID_ANY, _t("Please copy and paste the url when your authorization is completed"))
            bSizer1.Add(text, 0, wx.ALL | wx.EXPAND, 10)

        else:
            text = wx.StaticText(self, wx.ID_ANY, _t("Please copy and paste the token provided by pyfa.io"))
            bSizer1.Add(text, 0, wx.ALL | wx.EXPAND, 10)

        self.ssoInfoCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, (-1, -1), style=wx.TE_MULTILINE)
        self.ssoInfoCtrl.SetFont(wx.Font(8, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL))
        self.ssoInfoCtrl.Layout()
        self.ssoInfoCtrl.Bind(wx.EVT_TEXT, self.OnTextEnter)

        bSizer1.Add(self.ssoInfoCtrl, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)

        self.Esisettings = EsiSettings.getInstance()

        bSizer3 = wx.BoxSizer(wx.VERTICAL)
        bSizer3.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.BOTTOM | wx.EXPAND, 10)

        bSizer3.Add(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL), 0, wx.EXPAND)
        bSizer1.Add(bSizer3, 0, wx.ALL | wx.EXPAND, 10)

        self.SetSizer(bSizer1)
        self.Center()
        self.sEsi = Esi.getInstance()

        serverAddr = self.sEsi.startServer(0) if start_local_server else None
        uri = self.sEsi.get_login_uri(serverAddr)

        if server.name == "Serenity":
            webbrowser.open(config.SSO_LOGOFF_SERENITY)
            time.sleep(1)

        self.okBtn = self.FindWindow(wx.ID_OK)
        self.okBtn.Enable(False)
        # Ensure we clean up once they hit the "OK" button
        self.okBtn.Bind(wx.EVT_BUTTON, self.OnDestroy)

        webbrowser.open(uri)

        self.mainFrame.Bind(GE.EVT_SSO_LOGIN, self.OnLogin)
        # Ensure we clean up if ESC is pressed
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)

    def OnTextEnter(self, event):
        t = event.String.strip()
        if t == "":
            self.okBtn.Enable(False)
        else:
            self.okBtn.Enable(True)
        event.Skip()

    def OnLogin(self, event):
        # This would normally happen if it was logged in via server auto-login. In this case, the modal is done, we effectively want to cancel out
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def OnDestroy(self, event):
        # Clean up by unbinding some events and stopping the server
        self.mainFrame.Unbind(GE.EVT_SSO_LOGIN, handler=self.OnLogin)
        if self:
            self.Unbind(wx.EVT_WINDOW_DESTROY, handler=self.OnDestroy)
        self.sEsi.stopServer()
        event.Skip()
