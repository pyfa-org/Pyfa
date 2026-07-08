# noinspection PyPackageRequirements
import wx

from gui.preferenceView import PreferenceView
from gui.bitmap_loader import BitmapLoader

from service.settings import DiscordSettings

_t = wx.GetTranslation


class PFDiscordPref(PreferenceView):

    def populatePanel(self, panel):
        self.title = _t("Discord")
        self.settings = DiscordSettings.getInstance()

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        dlgWidth = panel.GetParent().GetParent().ClientSize.width

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        mainSizer.Add(self.stTitle, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        desc = _t("Enable or disable Discord integration features in pyfa.")
        self.stDesc = wx.StaticText(panel, wx.ID_ANY, desc, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stDesc.Wrap(dlgWidth - 50)
        mainSizer.Add(self.stDesc, 0, wx.ALL, 5)

        self.cbEnableDiscord = wx.CheckBox(panel, wx.ID_ANY, _t("Enable Discord Integration"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.cbEnableDiscord.SetValue(bool(self.settings.get('enableDiscord')))
        self.cbEnableDiscord.Bind(wx.EVT_CHECKBOX, self.OnCBEnableChange)
        mainSizer.Add(self.cbEnableDiscord, 0, wx.ALL | wx.EXPAND, 5)

        webhookSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.stWebhookURL = wx.StaticText(panel, wx.ID_ANY, _t("Webhook URL:"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.stWebhookURL.Wrap(-1)
        webhookSizer.Add(self.stWebhookURL, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        webhookValue = self.settings.get('webhookUrl') or ""
        self.editWebhookURL = wx.TextCtrl(panel, wx.ID_ANY, webhookValue, wx.DefaultPosition, wx.DefaultSize, 0)
        self.editWebhookURL.Bind(wx.EVT_TEXT, self.OnWebhookUrlText)
        webhookSizer.Add(self.editWebhookURL, 1, wx.ALL | wx.EXPAND, 5)

        mainSizer.Add(webhookSizer, 0, wx.ALL | wx.EXPAND, 0)

        self.ToggleWebhookSettings(self.cbEnableDiscord.GetValue())

        panel.SetSizer(mainSizer)
        panel.Layout()


    def OnCBEnableChange(self, event):
        self.settings.set('enableDiscord', self.cbEnableDiscord.GetValue())
        self.ToggleWebhookSettings(self.cbEnableDiscord.GetValue())

    def OnWebhookUrlText(self, event):
        self.settings.set('webhookUrl', self.editWebhookURL.GetValue().strip())

    def ToggleWebhookSettings(self, enable):
        self.stWebhookURL.Enable(enable)
        self.editWebhookURL.Enable(enable)

    def getImage(self):
        return BitmapLoader.getBitmap("prefs_discord", "gui")


PFDiscordPref.register()

