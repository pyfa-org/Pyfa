import wx
import gui.mainFrame
import webbrowser
import gui.globalEvents as GE


class SsoLogin(wx.Dialog):

    def __init__(self):
        mainFrame = gui.mainFrame.MainFrame.getInstance()

        wx.Dialog.__init__(self, mainFrame, id=wx.ID_ANY, title="SSO Login", size=wx.Size(400, 240))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        text = wx.StaticText(self, wx.ID_ANY, "Copy and paste the block of text provided by pyfa.io, then click OK")
        bSizer1.Add(text, 0, wx.ALL | wx.EXPAND, 10)

        self.ssoInfoCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, (-1, -1), style=wx.TE_MULTILINE)
        self.ssoInfoCtrl.SetFont(wx.Font(8, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL))
        self.ssoInfoCtrl.Layout()

        bSizer1.Add(self.ssoInfoCtrl, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)
        bSizer3.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.BOTTOM | wx.EXPAND, 10)

        bSizer3.Add(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL), 0, wx.EXPAND)
        bSizer1.Add(bSizer3, 0, wx.ALL | wx.EXPAND, 10)

        self.SetSizer(bSizer1)
        self.Center()

        mainFrame.Bind(GE.EVT_SSO_LOGIN, self.OnLogin)

        from service.esi import Esi

        self.sEsi = Esi.getInstance()
        uri = self.sEsi.getLoginURI(None)
        webbrowser.open(uri)

    def OnLogin(self, event):
        self.Close()
        event.Skip()


class SsoLoginServer(wx.Dialog):
    def __init__(self, port):
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        wx.Dialog.__init__(self, mainFrame, id=wx.ID_ANY, title="SSO Login", size=(-1, -1))

        from service.esi import Esi

        self.sEsi = Esi.getInstance()
        serverAddr = self.sEsi.startServer(port)

        uri = self.sEsi.getLoginURI(serverAddr)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        mainFrame.Bind(GE.EVT_SSO_LOGIN, self.OnLogin)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        text = wx.StaticText(self, wx.ID_ANY, "Waiting for character login through EVE Single Sign-On.")
        bSizer1.Add(text, 0, wx.ALL | wx.EXPAND, 10)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)
        bSizer3.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.BOTTOM | wx.EXPAND, 10)

        bSizer3.Add(self.CreateStdDialogButtonSizer(wx.CANCEL), 0, wx.EXPAND)
        bSizer1.Add(bSizer3, 0, wx.BOTTOM | wx.RIGHT | wx.LEFT | wx.EXPAND, 10)

        self.SetSizer(bSizer1)
        self.Fit()
        self.Center()

        webbrowser.open(uri)

    def OnLogin(self, event):
        self.Close()
        event.Skip()

    def OnClose(self, event):
        self.sEsi.stopServer()
        event.Skip()
