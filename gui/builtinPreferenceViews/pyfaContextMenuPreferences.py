import wx

from gui.preferenceView import PreferenceView
from gui.bitmap_loader import BitmapLoader
import gui.mainFrame
from service.settings import ContextMenuSettings

_t = wx.GetTranslation


class PFContextMenuPref(PreferenceView):

    def populatePanel(self, panel):
        self.title = _t("Context Menus")
        self.settings = ContextMenuSettings.getInstance()
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.dirtySettings = False
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        mainSizer.Add(self.stTitle, 0, wx.EXPAND | wx.ALL, 5)

        self.stSubTitle = wx.StaticText(
                panel, wx.ID_ANY,
                _t('Disabling context menus can improve responsiveness.\n'
                   'You can hold {} key + right-click to show all menu items regardless of these settings.').format(
                        'Command' if 'wxMac' in wx.PlatformInfo else 'Control'),
                wx.DefaultPosition, wx.DefaultSize, 0)
        self.stSubTitle.Wrap(-1)
        mainSizer.Add(self.stSubTitle, 0, wx.ALL, 5)

        # Row 1
        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.ALL, 5)

        rbSizerRow1 = wx.BoxSizer(wx.HORIZONTAL)

        self.rbBox1 = wx.RadioBox(panel, -1, _t("Set as Damage Pattern"), wx.DefaultPosition, wx.DefaultSize, [_t('Disabled'), _t('Enabled')], 1, wx.RA_SPECIFY_COLS)
        self.rbBox1.SetSelection(self.settings.get('ammoPattern'))
        rbSizerRow1.Add(self.rbBox1, 1, wx.ALL, 5)
        self.rbBox1.Bind(wx.EVT_RADIOBOX, self.OnSetting1Change)

        self.rbBox2 = wx.RadioBox(panel, -1, _t("Change Skills"), wx.DefaultPosition, wx.DefaultSize, [_t('Disabled'), _t('Enabled')], 1, wx.RA_SPECIFY_COLS)
        self.rbBox2.SetSelection(self.settings.get('changeAffectingSkills'))
        rbSizerRow1.Add(self.rbBox2, 1, wx.ALL, 5)
        self.rbBox2.Bind(wx.EVT_RADIOBOX, self.OnSetting2Change)

        self.rbBox3 = wx.RadioBox(panel, -1, _t("Variations"), wx.DefaultPosition, wx.DefaultSize, [_t('Disabled'), _t('Enabled')], 1, wx.RA_SPECIFY_COLS)
        self.rbBox3.SetSelection(self.settings.get('metaSwap'))
        rbSizerRow1.Add(self.rbBox3, 1, wx.ALL, 5)
        self.rbBox3.Bind(wx.EVT_RADIOBOX, self.OnSetting3Change)

        mainSizer.Add(rbSizerRow1, 1, wx.ALL | wx.EXPAND, 0)

        # Row 2
        rbSizerRow2 = wx.BoxSizer(wx.HORIZONTAL)

        self.rbBox4 = wx.RadioBox(panel, -1, _t("Project onto Fit"), wx.DefaultPosition, wx.DefaultSize, [_t('Disabled'), _t('Enabled')], 1, wx.RA_SPECIFY_COLS)
        self.rbBox4.SetSelection(self.settings.get('project'))
        rbSizerRow2.Add(self.rbBox4, 1, wx.ALL, 5)
        self.rbBox4.Bind(wx.EVT_RADIOBOX, self.OnSetting4Change)

        self.rbBox5 = wx.RadioBox(panel, -1, _t("Fill with module"), wx.DefaultPosition, wx.DefaultSize, [_t('Disabled'), _t('Enabled')], 1, wx.RA_SPECIFY_COLS)
        self.rbBox5.SetSelection(self.settings.get('moduleFill'))
        rbSizerRow2.Add(self.rbBox5, 1, wx.ALL, 5)
        self.rbBox5.Bind(wx.EVT_RADIOBOX, self.OnSetting5Change)

        mainSizer.Add(rbSizerRow2, 1, wx.ALL | wx.EXPAND, 0)

        # Row 3
        rbSizerRow3 = wx.BoxSizer(wx.HORIZONTAL)

        self.rbBox6 = wx.RadioBox(panel, -1, _t("Spoolup"), wx.DefaultPosition, wx.DefaultSize, [_t('Disabled'), _t('Enabled')], 1, wx.RA_SPECIFY_COLS)
        self.rbBox6.SetSelection(self.settings.get('spoolup'))
        rbSizerRow3.Add(self.rbBox6, 1, wx.ALL, 5)
        self.rbBox6.Bind(wx.EVT_RADIOBOX, self.OnSetting6Change)

        self.rbBox7 = wx.RadioBox(panel, -1, _t("Additions Panel Copy/Paste"), wx.DefaultPosition, wx.DefaultSize, [_t('Disabled'), _t('Enabled')], 1,
                                  wx.RA_SPECIFY_COLS)
        self.rbBox7.SetSelection(self.settings.get('additionsCopyPaste'))
        rbSizerRow3.Add(self.rbBox7, 1, wx.ALL, 5)
        self.rbBox7.Bind(wx.EVT_RADIOBOX, self.OnSetting7Change)

        mainSizer.Add(rbSizerRow3, 1, wx.ALL | wx.EXPAND, 0)

        panel.SetSizer(mainSizer)
        panel.Layout()

    def OnSetting1Change(self, event):
        self.settings.set('ammoPattern', event.GetInt())

    def OnSetting2Change(self, event):
        self.settings.set('changeAffectingSkills', event.GetInt())

    def OnSetting3Change(self, event):
        self.settings.set('metaSwap', event.GetInt())

    def OnSetting4Change(self, event):
        self.settings.set('project', event.GetInt())

    def OnSetting5Change(self, event):
        self.settings.set('moduleFill', event.GetInt())

    def OnSetting6Change(self, event):
        self.settings.set('spoolup', event.GetInt())

    def OnSetting7Change(self, event):
        self.settings.set('additionsCopyPaste', event.GetInt())

    def getImage(self):
        return BitmapLoader.getBitmap("settings_menu", "gui")


PFContextMenuPref.register()
