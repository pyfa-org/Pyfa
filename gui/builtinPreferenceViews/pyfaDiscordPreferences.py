# noinspection PyPackageRequirements
import wx

from gui.preferenceView import PreferenceView
from gui.bitmap_loader import BitmapLoader

from service.discord import Discord, DiscordWebhookError
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

        self.stWebhookValidation = wx.StaticText(panel, wx.ID_ANY, _t("Webhook URL format is invalid."), wx.DefaultPosition, wx.DefaultSize, 0)
        self.stWebhookValidation.SetForegroundColour(wx.Colour(180, 40, 40))
        mainSizer.Add(self.stWebhookValidation, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)

        self.cbConfirmBeforeSend = wx.CheckBox(panel, wx.ID_ANY, _t("Confirm before sending fit to Discord"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.cbConfirmBeforeSend.SetValue(bool(self.settings.get('confirmBeforeSend')))
        self.cbConfirmBeforeSend.Bind(wx.EVT_CHECKBOX, self.OnConfirmBeforeSendChange)
        mainSizer.Add(self.cbConfirmBeforeSend, 0, wx.ALL | wx.EXPAND, 5)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btnTestWebhook = wx.Button(panel, wx.ID_ANY, _t("Test Webhook"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.btnTestWebhook.Bind(wx.EVT_BUTTON, self.OnTestWebhook)
        btnSizer.Add(self.btnTestWebhook, 0, wx.ALL, 5)
        mainSizer.Add(btnSizer, 0, wx.ALL | wx.EXPAND, 0)

        self.ToggleWebhookSettings(self.cbEnableDiscord.GetValue())
        self.UpdateWebhookValidationState()

        panel.SetSizer(mainSizer)
        panel.Layout()


    def OnCBEnableChange(self, event):
        self.settings.set('enableDiscord', self.cbEnableDiscord.GetValue())
        self.ToggleWebhookSettings(self.cbEnableDiscord.GetValue())
        self.UpdateWebhookValidationState()

    def OnWebhookUrlText(self, event):
        self.settings.set('webhookUrl', self.editWebhookURL.GetValue().strip())
        self.UpdateWebhookValidationState()

    def OnConfirmBeforeSendChange(self, event):
        self.settings.set('confirmBeforeSend', self.cbConfirmBeforeSend.GetValue())

    def ToggleWebhookSettings(self, enable):
        self.stWebhookURL.Enable(enable)
        self.editWebhookURL.Enable(enable)
        self.cbConfirmBeforeSend.Enable(enable)
        self.btnTestWebhook.Enable(enable)

    def UpdateWebhookValidationState(self):
        webhookValue = self.editWebhookURL.GetValue().strip()
        isValid = webhookValue == '' or Discord.isValidWebhookUrl(webhookValue)
        self.stWebhookValidation.Show(not isValid)
        canTest = self.cbEnableDiscord.GetValue() and Discord.isValidWebhookUrl(webhookValue)
        self.btnTestWebhook.Enable(canTest)

    def OnTestWebhook(self, event):
        try:
            Discord.getInstance().sendTestMessage()
        except DiscordWebhookError as e:
            wx.MessageBox(str(e), _t("Discord Webhook"), wx.OK | wx.ICON_ERROR)
            return

        wx.MessageBox(_t("Discord webhook test message sent successfully."), _t("Discord Webhook"), wx.OK | wx.ICON_INFORMATION)

    def getImage(self):
        return BitmapLoader.getBitmap("prefs_discord", "gui")


PFDiscordPref.register()

