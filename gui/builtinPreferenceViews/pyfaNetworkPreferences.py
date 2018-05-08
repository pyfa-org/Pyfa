# noinspection PyPackageRequirements
import wx

from gui.preferenceView import PreferenceView
from gui.bitmap_loader import BitmapLoader

import gui.mainFrame
from service.settings import NetworkSettings
from service.network import Network


class PFNetworkPref(PreferenceView):
    title = "Network"

    def populatePanel(self, panel):

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = NetworkSettings.getInstance()
        self.network = Network.getInstance()
        self.dirtySettings = False

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))

        mainSizer.Add(self.stTitle, 0, wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.cbEnableNetwork = wx.CheckBox(panel, wx.ID_ANY, "Enable Network", wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbEnableNetwork, 0, wx.ALL | wx.EXPAND, 5)

        subSizer = wx.BoxSizer(wx.VERTICAL)
        self.cbEve = wx.CheckBox(panel, wx.ID_ANY, "EVE Servers (API && CREST import)", wx.DefaultPosition,
                                 wx.DefaultSize, 0)
        subSizer.Add(self.cbEve, 0, wx.ALL | wx.EXPAND, 5)

        self.cbPricing = wx.CheckBox(panel, wx.ID_ANY, "Pricing updates", wx.DefaultPosition, wx.DefaultSize, 0)
        subSizer.Add(self.cbPricing, 0, wx.ALL | wx.EXPAND, 5)

        self.cbPyfaUpdate = wx.CheckBox(panel, wx.ID_ANY, "Pyfa Update checks", wx.DefaultPosition, wx.DefaultSize, 0)
        subSizer.Add(self.cbPyfaUpdate, 0, wx.ALL | wx.EXPAND, 5)

        mainSizer.Add(subSizer, 0, wx.LEFT | wx.EXPAND, 30)

        proxyTitle = wx.StaticText(panel, wx.ID_ANY, "Proxy settings", wx.DefaultPosition, wx.DefaultSize, 0)
        proxyTitle.Wrap(-1)
        proxyTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))

        mainSizer.Add(proxyTitle, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL), 0,
                      wx.EXPAND, 5)

        self.cbEnableNetwork.SetValue(self.settings.isEnabled(self.network.ENABLED))
        self.cbEve.SetValue(self.settings.isEnabled(self.network.EVE))
        self.cbPricing.SetValue(self.settings.isEnabled(self.network.PRICES))
        self.cbPyfaUpdate.SetValue(self.settings.isEnabled(self.network.UPDATE))

        self.cbEnableNetwork.Bind(wx.EVT_CHECKBOX, self.OnCBEnableChange)
        self.cbEve.Bind(wx.EVT_CHECKBOX, self.OnCBEveChange)
        self.cbPricing.Bind(wx.EVT_CHECKBOX, self.OnCBPricingChange)
        self.cbPyfaUpdate.Bind(wx.EVT_CHECKBOX, self.OnCBUpdateChange)

        self.toggleNetworks(self.cbEnableNetwork.GetValue())

        # ---------------
        # Proxy
        # ---------------

        self.nMode = self.settings.getMode()
        self.nAddr = self.settings.getAddress()
        self.nPort = self.settings.getPort()
        self.nType = self.settings.getType()
        self.nAuth = self.settings.getProxyAuthDetails()  # tuple of (login, password)
        if self.nAuth is None:
            self.nAuth = ("", "")  # we don't want None here, it should be a tuple

        ptypeSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.stPType = wx.StaticText(panel, wx.ID_ANY, "Mode:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stPType.Wrap(-1)
        ptypeSizer.Add(self.stPType, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.chProxyTypeChoices = ["No proxy", "Auto-detected proxy settings", "Manual proxy settings"]
        self.chProxyType = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.chProxyTypeChoices, 0)

        self.chProxyType.SetSelection(self.nMode)

        ptypeSizer.Add(self.chProxyType, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        mainSizer.Add(ptypeSizer, 0, wx.EXPAND, 5)

        fgAddrSizer = wx.FlexGridSizer(2, 2, 0, 0)
        fgAddrSizer.AddGrowableCol(1)
        fgAddrSizer.SetFlexibleDirection(wx.BOTH)
        fgAddrSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.stPSetAddr = wx.StaticText(panel, wx.ID_ANY, "Addr:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stPSetAddr.Wrap(-1)
        fgAddrSizer.Add(self.stPSetAddr, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.editProxySettingsAddr = wx.TextCtrl(panel, wx.ID_ANY, self.nAddr, wx.DefaultPosition, wx.DefaultSize, 0)

        fgAddrSizer.Add(self.editProxySettingsAddr, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.stPSetPort = wx.StaticText(panel, wx.ID_ANY, "Port:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stPSetPort.Wrap(-1)

        fgAddrSizer.Add(self.stPSetPort, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.editProxySettingsPort = wx.TextCtrl(panel, wx.ID_ANY, self.nPort, wx.DefaultPosition, wx.DefaultSize, 0)

        fgAddrSizer.Add(self.editProxySettingsPort, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        mainSizer.Add(fgAddrSizer, 0, wx.EXPAND, 5)

        # proxy auth information: login and pass
        self.stPSetLogin = wx.StaticText(panel, wx.ID_ANY, "Username:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stPSetLogin.Wrap(-1)
        self.editProxySettingsLogin = wx.TextCtrl(panel, wx.ID_ANY, self.nAuth[0], wx.DefaultPosition, wx.DefaultSize,
                                                   0)
        self.stPSetPassword = wx.StaticText(panel, wx.ID_ANY, "Password:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stPSetPassword.Wrap(-1)
        self.editProxySettingsPassword = wx.TextCtrl(panel, wx.ID_ANY, self.nAuth[1], wx.DefaultPosition,
                                                      wx.DefaultSize, wx.TE_PASSWORD)
        pAuthSizer = wx.BoxSizer(wx.HORIZONTAL)
        pAuthSizer.Add(self.stPSetLogin, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        pAuthSizer.Add(self.editProxySettingsLogin, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        pAuthSizer.Add(self.stPSetPassword, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        pAuthSizer.Add(self.editProxySettingsPassword, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        mainSizer.Add(pAuthSizer, 0, wx.EXPAND, 5)

        self.stPSAutoDetected = wx.StaticText(panel, wx.ID_ANY, "Auto-detected: ", wx.DefaultPosition, wx.DefaultSize,
                                               0)
        self.stPSAutoDetected.Wrap(-1)
        mainSizer.Add(self.stPSAutoDetected, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.AddStretchSpacer()

        self.btnApply = wx.Button(panel, wx.ID_ANY, "Apply Proxy Settings", wx.DefaultPosition, wx.DefaultSize, 0)

        btnSizer.Add(self.btnApply, 0, wx.ALL, 5)

        mainSizer.Add(btnSizer, 0, wx.EXPAND, 5)

        proxy = self.settings.autodetect()

        if proxy is not None:
             addr, port = proxy
             txt = addr + ":" + str(port)
        else:
             txt = "None"

        self.stPSAutoDetected.SetLabel("Auto-detected: " + txt)
        self.stPSAutoDetected.Disable()

        self.chProxyType.Bind(wx.EVT_CHOICE, self.OnCHProxyTypeSelect)
        self.editProxySettingsAddr.Bind(wx.EVT_TEXT, self.OnEditPSAddrText)
        self.editProxySettingsPort.Bind(wx.EVT_TEXT, self.OnEditPSPortText)
        self.editProxySettingsLogin.Bind(wx.EVT_TEXT, self.OnEditPSLoginText)
        self.editProxySettingsPassword.Bind(wx.EVT_TEXT, self.OnEditPSPasswordText)

        self.btnApply.Bind(wx.EVT_BUTTON, self.OnBtnApply)

        self.UpdateApplyButtonState()

        if self.nMode is not NetworkSettings.PROXY_MODE_MANUAL:  # == 2
            self.ToggleProxySettings(False)
        else:
            self.ToggleProxySettings(True)

        panel.SetSizer(mainSizer)
        panel.Layout()

    def toggleNetworks(self, toggle):
        self.cbEve.Enable(toggle)
        self.cbPricing.Enable(toggle)
        self.cbPyfaUpdate.Enable(toggle)

    def OnCBEnableChange(self, event):
        self.settings.toggleAccess(self.network.ENABLED, self.cbEnableNetwork.GetValue())
        self.toggleNetworks(self.cbEnableNetwork.GetValue())

    def OnCBUpdateChange(self, event):
        self.settings.toggleAccess(self.network.UPDATE, self.cbPyfaUpdate.GetValue())

    def OnCBPricingChange(self, event):
        self.settings.toggleAccess(self.network.PRICES, self.cbPricing.GetValue())

    def OnCBEveChange(self, event):
        self.settings.toggleAccess(self.network.EVE, self.cbEve.GetValue())

    def OnEditPSAddrText(self, event):
        self.nAddr = self.editProxySettingsAddr.GetValue()
        self.dirtySettings = True
        self.UpdateApplyButtonState()

    def OnEditPSPortText(self, event):
        self.nPort = self.editProxySettingsPort.GetValue()
        self.dirtySettings = True
        self.UpdateApplyButtonState()

    def OnEditPSLoginText(self, event):
        self.nAuth = (self.editProxySettingsLogin.GetValue(), self.nAuth[1])
        self.dirtySettings = True
        self.UpdateApplyButtonState()

    def OnEditPSPasswordText(self, event):
        self.nAuth = (self.nAuth[0], self.editProxySettingsPassword.GetValue())
        self.dirtySettings = True
        self.UpdateApplyButtonState()

    def OnBtnApply(self, event):
        self.dirtySettings = False
        self.UpdateApplyButtonState()
        self.SaveSettings()

    def SaveSettings(self):
        self.settings.setMode(self.nMode)
        self.settings.setAddress(self.nAddr)
        self.settings.setPort(self.nPort)
        self.settings.setType(self.nType)
        self.settings.setProxyAuthDetails(self.nAuth[0], self.nAuth[1])

    def UpdateApplyButtonState(self):
        if self.dirtySettings:
            self.btnApply.Enable()
        else:
            self.btnApply.Disable()

    def OnCHProxyTypeSelect(self, event):
        choice = self.chProxyType.GetSelection()

        self.nMode = choice
        self.dirtySettings = True

        self.UpdateApplyButtonState()

        if choice is not NetworkSettings.PROXY_MODE_MANUAL:
            self.ToggleProxySettings(False)
        else:
            self.ToggleProxySettings(True)

    def ToggleProxySettings(self, mode):
        if mode:
            self.stPSetAddr.Enable()
            self.editProxySettingsAddr.Enable()
            self.stPSetPort.Enable()
            self.editProxySettingsPort.Enable()
            self.stPSetLogin.Enable()
            self.stPSetPassword.Enable()
            self.editProxySettingsLogin.Enable()
            self.editProxySettingsPassword.Enable()
        else:
            self.stPSetAddr.Disable()
            self.editProxySettingsAddr.Disable()
            self.stPSetPort.Disable()
            self.editProxySettingsPort.Disable()
            self.stPSetLogin.Disable()
            self.stPSetPassword.Disable()
            self.editProxySettingsLogin.Disable()
            self.editProxySettingsPassword.Disable()

    def getImage(self):
        return BitmapLoader.getBitmap("prefs_proxy", "gui")


PFNetworkPref.register()
