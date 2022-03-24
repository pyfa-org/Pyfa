import logging

import wx

from service.fit import Fit
from gui.bitmap_loader import BitmapLoader
import gui.globalEvents as GE
from gui.preferenceView import PreferenceView
from service.settings import EOSSettings
import gui.mainFrame
from wx.lib.intctrl import IntCtrl

logger = logging.getLogger(__name__)

_t = wx.GetTranslation


class PFFittingEnginePref(PreferenceView):
    def __init__(self):
        self.dirtySettings = False

    def refreshPanel(self, fit):
        pass

    # noinspection PyAttributeOutsideInit
    def populatePanel(self, panel):
        self.title = _t("Fitting Engine")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        helpCursor = wx.Cursor(wx.CURSOR_QUESTION_ARROW)

        self.engine_settings = EOSSettings.getInstance()

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        mainSizer.Add(self.stTitle, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.cbGlobalForceReload = wx.CheckBox(panel, wx.ID_ANY, _t("Factor in reload time when calculating capacitor usage, damage, and tank."),
                                               wx.DefaultPosition, wx.DefaultSize, 0)

        mainSizer.Add(self.cbGlobalForceReload, 0, wx.ALL | wx.EXPAND, 5)

        self.cbStrictSkillLevels = wx.CheckBox(panel, wx.ID_ANY,
                                               _t("Enforce strict skill level requirements"),
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.cbStrictSkillLevels.SetCursor(helpCursor)
        self.cbStrictSkillLevels.SetToolTip(wx.ToolTip(
                _t('When enabled, skills will check their dependencies\' requirements when their levels change and reset '
                   'skills that no longer meet the requirement.\neg: Setting Drones from level V to IV will reset the Heavy '
                   'Drone Operation skill, as that requires Drones V')))

        mainSizer.Add(self.cbStrictSkillLevels, 0, wx.ALL | wx.EXPAND, 5)

        spoolup_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.spool_up_label = wx.StaticText(panel, wx.ID_ANY, _t("Global Default Spoolup Percentage:"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.spool_up_label.Wrap(-1)
        self.spool_up_label.SetCursor(helpCursor)
        self.spool_up_label.SetToolTip(
                wx.ToolTip(_t('The amount of spoolup to use by default on module which support it. Can be changed on a per-module basis')))

        spoolup_sizer.Add(self.spool_up_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.spoolup_value = IntCtrl(panel, min=0, max=100, limited=True)
        spoolup_sizer.Add(self.spoolup_value, 0, wx.ALL, 5)

        mainSizer.Add(spoolup_sizer, 0, wx.ALL | wx.EXPAND, 0)

        # Future code once new cap sim is implemented
        '''
        self.cbGlobalForceReactivationTimer = wx.CheckBox( panel, wx.ID_ANY, "Factor in reactivation timer", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.cbGlobalForceReactivationTimer, 0, wx.ALL|wx.EXPAND, 5 )

        text =  "   Ignores reactivation timer when calculating capacitor usage,\n   damage, and tank."
        self.cbGlobalForceReactivationTimerText = wx.StaticText( panel, wx.ID_ANY, text, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cbGlobalForceReactivationTimerText.Wrap( -1 )
        self.cbGlobalForceReactivationTimerText.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
        mainSizer.Add( self.cbGlobalForceReactivationTimerText, 0, wx.ALL, 5 )
        '''

        # Future code for mining laser crystal
        '''
        self.cbGlobalMiningSpecialtyCrystal = wx.CheckBox( panel, wx.ID_ANY, "Factor in reactivation timer", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.cbGlobalMiningSpecialtyCrystal, 0, wx.ALL|wx.EXPAND, 5 )

        text = "   If enabled, displays the Specialty Crystal mining amount.\n   This is the amount mined when using crystals and mining the matching asteroid."
        self.cbGlobalMiningSpecialtyCrystalText = wx.StaticText( panel, wx.ID_ANY, text, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cbGlobalMiningSpecialtyCrystalText.Wrap( -1 )
        self.cbGlobalMiningSpecialtyCrystalText.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
        mainSizer.Add( self.cbGlobalMiningSpecialtyCrystalText, 0, wx.ALL, 5 )
        '''

        self.sFit = Fit.getInstance()

        self.cbGlobalForceReload.SetValue(self.sFit.serviceFittingOptions["useGlobalForceReload"])
        self.cbGlobalForceReload.Bind(wx.EVT_CHECKBOX, self.OnCBGlobalForceReloadStateChange)

        self.cbStrictSkillLevels.SetValue(self.engine_settings.get("strictSkillLevels"))
        self.cbStrictSkillLevels.Bind(wx.EVT_CHECKBOX, self.OnCBStrictSkillLevelsChange)

        self.spoolup_value.SetValue(int(self.engine_settings.get("globalDefaultSpoolupPercentage") * 100))
        self.spoolup_value.Bind(wx.lib.intctrl.EVT_INT, self.OnSpoolupChange)

        panel.SetSizer(mainSizer)
        panel.Layout()

    def OnSpoolupChange(self, event):
        self.engine_settings.set("globalDefaultSpoolupPercentage", self.spoolup_value.GetValue() / 100)

    def OnCBGlobalForceReloadStateChange(self, event):
        fitIDs = self.sFit.toggleFactorReload(value=bool(self.cbGlobalForceReload.GetValue()))
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=tuple(fitIDs)))

    def OnCBStrictSkillLevelsChange(self, event):
        self.engine_settings.set("strictSkillLevels", self.cbStrictSkillLevels.GetValue())


    def getImage(self):
        return BitmapLoader.getBitmap("settings_fitting", "gui")

    def OnWindowLeave(self, event):
        # We don't want to do anything when they leave,
        # but in the future we might.
        pass


PFFittingEnginePref.register()
