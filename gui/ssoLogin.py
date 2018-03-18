import wx

class SsoLogin(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="SSO Login", size=wx.Size(400, 240))

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
