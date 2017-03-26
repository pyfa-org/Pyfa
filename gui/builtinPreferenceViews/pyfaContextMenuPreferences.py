import wx

from gui.preferenceView import PreferenceView
from gui.bitmapLoader import BitmapLoader
import gui.mainFrame
from service.settings import ContextMenuSettings


class PFContextMenuPref(PreferenceView):
    title = "Context Menu Panel"

    def populatePanel(self, panel):
        self.settings = ContextMenuSettings.getInstance()
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.dirtySettings = False
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))

        mainSizer.Add(self.stTitle, 0, wx.ALL, 5)

        self.stSubTitle = wx.StaticText(panel, wx.ID_ANY,
                                        u"Disabling context menus can improve responsiveness.",
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.stSubTitle.Wrap(-1)
        mainSizer.Add(self.stSubTitle, 0, wx.ALL, 5)

        # Row 1
        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.ALL, 5)

        rbSizerRow1 = wx.BoxSizer(wx.HORIZONTAL)

        self.rbBox1 = wx.RadioBox(panel, -1, "Set as Damage Pattern", wx.DefaultPosition, wx.DefaultSize, ['Disabled', 'Enabled'], 1, wx.RA_SPECIFY_COLS)
        self.rbBox1.SetSelection(self.settings.get('ammoPattern'))
        rbSizerRow1.Add(self.rbBox1, 1, wx.TOP | wx.RIGHT, 5)
        self.rbBox1.Bind(wx.EVT_RADIOBOX, self.OnSetting1Change)

        self.rbBox2 = wx.RadioBox(panel, -1, "Change Skills", wx.DefaultPosition, wx.DefaultSize, ['Disabled', 'Enabled'], 1, wx.RA_SPECIFY_COLS)
        self.rbBox2.SetSelection(self.settings.get('changeAffectingSkills'))
        rbSizerRow1.Add(self.rbBox2, 1, wx.ALL, 5)
        self.rbBox2.Bind(wx.EVT_RADIOBOX, self.OnSetting2Change)

        self.rbBox3 = wx.RadioBox(panel, -1, "Factor in Reload Time", wx.DefaultPosition, wx.DefaultSize, ['Disabled', 'Enabled'], 1, wx.RA_SPECIFY_COLS)
        self.rbBox3.SetSelection(self.settings.get('factorReload'))
        rbSizerRow1.Add(self.rbBox3, 1, wx.ALL, 5)
        self.rbBox3.Bind(wx.EVT_RADIOBOX, self.OnSetting3Change)

        mainSizer.Add(rbSizerRow1, 1, wx.ALL | wx.EXPAND, 0)

        # Row 2
        rbSizerRow2 = wx.BoxSizer(wx.HORIZONTAL)

        self.rbBox4 = wx.RadioBox(panel, -1, "Variations", wx.DefaultPosition, wx.DefaultSize, ['Disabled', 'Enabled'], 1, wx.RA_SPECIFY_COLS)
        self.rbBox4.SetSelection(self.settings.get('metaSwap'))
        rbSizerRow2.Add(self.rbBox4, 1, wx.TOP | wx.RIGHT, 5)
        self.rbBox4.Bind(wx.EVT_RADIOBOX, self.OnSetting4Change)

        '''
        self.rbBox5 = wx.RadioBox(panel, -1, "Charge", wx.DefaultPosition, wx.DefaultSize, ['Disabled', 'Enabled'], 1, wx.RA_SPECIFY_COLS)
        self.rbBox5.SetSelection(self.settings.get('moduleAmmoPicker'))
        rbSizerRow2.Add(self.rbBox5, 1, wx.ALL, 5)
        self.rbBox5.Bind(wx.EVT_RADIOBOX, self.OnSetting5Change)
        '''

        self.rbBox6 = wx.RadioBox(panel, -1, "Charge (All)", wx.DefaultPosition, wx.DefaultSize, ['Disabled', 'Enabled'], 1, wx.RA_SPECIFY_COLS)
        self.rbBox6.SetSelection(self.settings.get('moduleGlobalAmmoPicker'))
        rbSizerRow2.Add(self.rbBox6, 1, wx.ALL, 5)
        self.rbBox6.Bind(wx.EVT_RADIOBOX, self.OnSetting6Change)

        mainSizer.Add(rbSizerRow2, 1, wx.ALL | wx.EXPAND, 0)

        # Row 3
        rbSizerRow3 = wx.BoxSizer(wx.HORIZONTAL)

        self.rbBox7 = wx.RadioBox(panel, -1, "Project onto Fit", wx.DefaultPosition, wx.DefaultSize, ['Disabled', 'Enabled'], 1, wx.RA_SPECIFY_COLS)
        self.rbBox7.SetSelection(self.settings.get('project'))
        rbSizerRow3.Add(self.rbBox7, 1, wx.TOP | wx.RIGHT, 5)
        self.rbBox7.Bind(wx.EVT_RADIOBOX, self.OnSetting7Change)

        mainSizer.Add(rbSizerRow3, 1, wx.ALL | wx.EXPAND, 0)

        panel.SetSizer(mainSizer)
        panel.Layout()

    def OnSetting1Change(self, event):
        self.settings.set('ammoPattern', event.GetInt())

    def OnSetting2Change(self, event):
        self.settings.set('changeAffectingSkills', event.GetInt())

    def OnSetting3Change(self, event):
        self.settings.set('factorReload', event.GetInt())

    def OnSetting4Change(self, event):
        self.settings.set('metaSwap', event.GetInt())

    def OnSetting5Change(self, event):
        self.settings.set('moduleAmmoPicker', event.GetInt())

    def OnSetting6Change(self, event):
        self.settings.set('moduleGlobalAmmoPicker', event.GetInt())

    def OnSetting7Change(self, event):
        self.settings.set('project', event.GetInt())

    def getImage(self):
        return BitmapLoader.getBitmap("settings_menu", "gui")


PFContextMenuPref.register()
