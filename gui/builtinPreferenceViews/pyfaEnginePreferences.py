import logging

import wx

from service.fit import Fit
from gui.bitmap_loader import BitmapLoader
from gui.preferenceView import PreferenceView
from service.settings import EOSSettings

logger = logging.getLogger(__name__)


class PFFittingEnginePref(PreferenceView):
    title = "Fitting Engine"

    def __init__(self):
        self.dirtySettings = False

    def refreshPanel(self, fit):
        pass

    # noinspection PyAttributeOutsideInit
    def populatePanel(self, panel):

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        helpCursor = wx.Cursor(wx.CURSOR_QUESTION_ARROW)

        self.engine_settings = EOSSettings.getInstance()

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        mainSizer.Add(self.stTitle, 0, wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.cbGlobalForceReload = wx.CheckBox(panel, wx.ID_ANY, "Factor in reload time when calculating capacitor usage, damage, and tank.",
                                               wx.DefaultPosition, wx.DefaultSize, 0)

        mainSizer.Add(self.cbGlobalForceReload, 0, wx.ALL | wx.EXPAND, 5)

        self.cbStrictSkillLevels = wx.CheckBox(panel, wx.ID_ANY,
                                               "Enforce strict skill level requirements",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.cbStrictSkillLevels.SetCursor(helpCursor)
        self.cbStrictSkillLevels.SetToolTip(wx.ToolTip(
            'When enabled, skills will check their dependencies\' requirements when their levels change and reset ' +
            'skills that no longer meet the requirement.\neg: Setting Drones from level V to IV will reset the Heavy ' +
            'Drone Operation skill, as that requires Drones V'))

        mainSizer.Add(self.cbStrictSkillLevels, 0, wx.ALL | wx.EXPAND, 5)

        self.cbUniversalAdaptiveArmorHardener = wx.CheckBox(panel, wx.ID_ANY,
                                                            "When damage profile is Uniform, set Reactive Armor " +
                                                            "Hardener to match (old behavior).",
                                                            wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbUniversalAdaptiveArmorHardener, 0, wx.ALL | wx.EXPAND, 5)

        # Future code once new cap sim is implemented
        '''
        self.cbGlobalForceReactivationTimer = wx.CheckBox( panel, wx.ID_ANY, u"Factor in reactivation timer", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.cbGlobalForceReactivationTimer, 0, wx.ALL|wx.EXPAND, 5 )

        text =  u"   Ignores reactivation timer when calculating capacitor usage,\n   damage, and tank."
        self.cbGlobalForceReactivationTimerText = wx.StaticText( panel, wx.ID_ANY, text, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cbGlobalForceReactivationTimerText.Wrap( -1 )
        self.cbGlobalForceReactivationTimerText.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
        mainSizer.Add( self.cbGlobalForceReactivationTimerText, 0, wx.ALL, 5 )
        '''

        # Future code for mining laser crystal
        '''
        self.cbGlobalMiningSpecialtyCrystal = wx.CheckBox( panel, wx.ID_ANY, u"Factor in reactivation timer", wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.cbGlobalMiningSpecialtyCrystal, 0, wx.ALL|wx.EXPAND, 5 )

        text = u"   If enabled, displays the Specialty Crystal mining amount.\n   This is the amount mined when using crystals and mining the matching asteroid."
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

        self.cbUniversalAdaptiveArmorHardener.SetValue(self.engine_settings.get("useStaticAdaptiveArmorHardener"))
        self.cbUniversalAdaptiveArmorHardener.Bind(wx.EVT_CHECKBOX, self.OnCBUniversalAdaptiveArmorHardenerChange)

        panel.SetSizer(mainSizer)
        panel.Layout()

    def OnCBGlobalForceReloadStateChange(self, event):
        self.sFit.serviceFittingOptions["useGlobalForceReload"] = self.cbGlobalForceReload.GetValue()

    def OnCBStrictSkillLevelsChange(self, event):
        self.engine_settings.set("strictSkillLevels", self.cbStrictSkillLevels.GetValue())

    def OnCBUniversalAdaptiveArmorHardenerChange(self, event):
        self.engine_settings.set("useStaticAdaptiveArmorHardener", self.cbUniversalAdaptiveArmorHardener.GetValue())

    def getImage(self):
        return BitmapLoader.getBitmap("settings_fitting", "gui")

    def OnWindowLeave(self, event):
        # We don't want to do anything when they leave,
        # but in the future we might.
        pass


PFFittingEnginePref.register()
