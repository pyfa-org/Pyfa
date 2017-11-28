# noinspection PyPackageRequirements
import wx
import os

from gui.preferenceView import PreferenceView
from gui.bitmap_loader import BitmapLoader

import gui.mainFrame

from service.settings import HTMLExportSettings
import wx.lib.agw.hyperlink


class PFHTMLExportPref(PreferenceView):
    title = "HTML Export"
    desc = ("HTML Export (File > Export HTML) allows you to export your entire fitting "
            "database into an HTML file at the specified location. This file can be "
            "used to easily open your fits in a web-based fitting program")
    desc4 = ("Export Fittings in a minimal HTML Version, just containing the fittings links "
             "without any visual styling")

    def populatePanel(self, panel):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.HTMLExportSettings = HTMLExportSettings.getInstance()
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

        self.PathLinkCtrl = wx.lib.agw.hyperlink.HyperLinkCtrl(panel, wx.ID_ANY, self.HTMLExportSettings.getPath(),
                                             wx.DefaultPosition, wx.DefaultSize,
                                             URL='file:///{}'.format(self.HTMLExportSettings.getPath()),)
        mainSizer.Add(self.PathLinkCtrl, 0, wx.ALL | wx.EXPAND, 5)

        self.fileSelectDialog = wx.FileDialog(None, "Save Fitting As...",
                                              wildcard="EVE IGB HTML fitting file (*.html)|*.html", style=wx.FD_SAVE)
        self.fileSelectDialog.SetPath(self.HTMLExportSettings.getPath())
        self.fileSelectDialog.SetFilename(os.path.basename(self.HTMLExportSettings.getPath()))

        self.fileSelectButton = wx.Button(panel, -1, "Set export destination", pos=(0, 0))
        self.fileSelectButton.Bind(wx.EVT_BUTTON, self.selectHTMLExportFilePath)
        mainSizer.Add(self.fileSelectButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.stDesc4 = wx.StaticText(panel, wx.ID_ANY, self.desc4, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stDesc4.Wrap(dlgWidth - 50)
        mainSizer.Add(self.stDesc4, 0, wx.ALL, 5)

        self.exportMinimal = wx.CheckBox(panel, wx.ID_ANY, "Enable minimal format", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.exportMinimal.SetValue(self.HTMLExportSettings.getMinimalEnabled())
        self.exportMinimal.Bind(wx.EVT_CHECKBOX, self.OnMinimalEnabledChange)
        mainSizer.Add(self.exportMinimal, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(mainSizer)
        panel.Layout()

    def setPathLinkCtrlValues(self, path):
        self.PathLinkCtrl.SetLabel(self.HTMLExportSettings.getPath())
        self.PathLinkCtrl.SetURL('file:///{}'.format(self.HTMLExportSettings.getPath()))
        self.PathLinkCtrl.SetSize(wx.DefaultSize)
        self.PathLinkCtrl.Refresh()

    def selectHTMLExportFilePath(self, event):
        if self.fileSelectDialog.ShowModal() == wx.ID_OK:
            self.HTMLExportSettings.setPath(self.fileSelectDialog.GetPath())
            self.dirtySettings = True
            self.setPathLinkCtrlValues(self.HTMLExportSettings.getPath())

    def OnMinimalEnabledChange(self, event):
        self.HTMLExportSettings.setMinimalEnabled(self.exportMinimal.GetValue())

    def getImage(self):
        return BitmapLoader.getBitmap("prefs_html", "gui")


PFHTMLExportPref.register()
