# noinspection PyPackageRequirements
import wx

from gui.preferenceView import PreferenceView
from gui.bitmap_loader import BitmapLoader
from service.settings import UpdateSettings


class PFUpdatePref(PreferenceView):
    title = "Updates"
    desc = ("Pyfa can automatically check and notify you of new releases. "
            "This feature is toggled in the Network settings. "
            "Here, you may allow pre-release notifications and view "
            "suppressed release notifications, if any.")

    def populatePanel(self, panel):
        self.UpdateSettings = UpdateSettings.getInstance()
        self.dirtySettings = False

        dlgWidth = panel.GetParent().GetParent().ClientSize.width

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        mainSizer.Add(self.stTitle, 0, wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.stDesc = wx.StaticText(panel, wx.ID_ANY, self.desc, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stDesc.Wrap(dlgWidth - 50)
        mainSizer.Add(self.stDesc, 0, wx.ALL, 5)

        self.suppressPrerelease = wx.CheckBox(panel, wx.ID_ANY, "Allow pre-release notifications", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.suppressPrerelease.Bind(wx.EVT_CHECKBOX, self.OnPrereleaseStateChange)
        self.suppressPrerelease.SetValue(not self.UpdateSettings.get('prerelease'))

        mainSizer.Add(self.suppressPrerelease, 0, wx.ALL | wx.EXPAND, 5)

        if self.UpdateSettings.get('version'):
            self.versionSizer = wx.BoxSizer(wx.VERTICAL)

            self.versionTitle = wx.StaticText(panel, wx.ID_ANY, "Suppressing {0} Notifications".format(
                    self.UpdateSettings.get('version')), wx.DefaultPosition, wx.DefaultSize, 0)
            self.versionTitle.Wrap(-1)
            self.versionTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))

            self.versionInfo = ("There is a release available which you have chosen to suppress. "
                                "You can choose to reset notification suppression for this release, "
                                "or download the new release from GitHub.")

            self.versionSizer.AddStretchSpacer()

            self.versionSizer.Add(wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL),
                                  0, wx.EXPAND, 5)
            self.versionSizer.AddStretchSpacer()

            self.versionSizer.Add(self.versionTitle, 0, wx.EXPAND, 5)
            self.versionDesc = wx.StaticText(panel, wx.ID_ANY, self.versionInfo, wx.DefaultPosition, wx.DefaultSize, 0)
            self.versionDesc.Wrap(dlgWidth - 50)
            self.versionSizer.Add(self.versionDesc, 0, wx.ALL, 5)

            actionSizer = wx.BoxSizer(wx.HORIZONTAL)
            resetSizer = wx.BoxSizer(wx.VERTICAL)

            self.downloadButton = wx.Button(panel, wx.ID_ANY, "Download", wx.DefaultPosition, wx.DefaultSize, 0)
            self.downloadButton.Bind(wx.EVT_BUTTON, self.OnDownload)
            resetSizer.Add(self.downloadButton, 0, wx.ALL, 5)
            actionSizer.Add(resetSizer, 1, wx.EXPAND, 5)

            self.resetButton = wx.Button(panel, wx.ID_ANY, "Reset Suppression", wx.DefaultPosition, wx.DefaultSize, 0)
            self.resetButton.Bind(wx.EVT_BUTTON, self.ResetSuppression)
            actionSizer.Add(self.resetButton, 0, wx.ALL, 5)
            self.versionSizer.Add(actionSizer, 0, wx.EXPAND, 5)
            mainSizer.Add(self.versionSizer, 0, wx.EXPAND, 5)

        panel.SetSizer(mainSizer)
        panel.Layout()

    def OnPrereleaseStateChange(self, event):
        self.UpdateSettings.set('prerelease', not self.suppressPrerelease.IsChecked())

    def ResetSuppression(self, event):
        self.UpdateSettings.set('version', None)

        # Todo: Find a way to hide the entire panel in one go
        self.versionSizer.Hide(True)
        self.versionTitle.Hide()
        self.versionDesc.Hide()
        self.downloadButton.Hide()
        self.resetButton.Hide()
        self.resetButton.Hide()

    def OnDownload(self, event):
        wx.LaunchDefaultBrowser('https://github.com/pyfa-org/Pyfa/releases/tag/' + self.UpdateSettings.get('version'))

    def getImage(self):
        return BitmapLoader.getBitmap("prefs_update", "gui")


PFUpdatePref.register()
