# noinspection PyPackageRequirements
import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.bitmap_loader import BitmapLoader
from gui.preferenceView import PreferenceView
from service.fit import Fit
from service.settings import SettingsProvider, LocaleSettings
import eos.config
import wx.lib.agw.hyperlink as hl


_t = wx.GetTranslation


class PFGeneralPref(PreferenceView):

    def populatePanel(self, panel):
        self.title = _t("General")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.dirtySettings = False
        self.openFitsSettings = SettingsProvider.getInstance().getSettings("pyfaPrevOpenFits",
                                                                           {"enabled": False, "pyfaOpenFits": []})
        self.localeSettings = LocaleSettings.getInstance()
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        mainSizer.Add(self.stTitle, 0, wx.EXPAND | wx.ALL, 5)

        helpCursor = wx.Cursor(wx.CURSOR_QUESTION_ARROW)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        langBox = wx.StaticBoxSizer(wx.VERTICAL, panel, _t("Language (requires restart)"))
        mainSizer.Add(langBox, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, 10)

        langSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.langChoices = sorted([langInfo for lang, langInfo in LocaleSettings.supported_langauges().items()], key=lambda x: x.Description)
        pyfaLangsEnabled = bool(self.langChoices)

        if pyfaLangsEnabled:
            self.stLangLabel = wx.StaticText(panel, wx.ID_ANY, _t("pyfa:"), wx.DefaultPosition, wx.DefaultSize, 0)
            self.stLangLabel.Wrap(-1)
            langSizer.Add(self.stLangLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

            def langDisplay(langInfo):
                progress = self.localeSettings.get_progress(langInfo.CanonicalName)
                progress_display = (" ({}%)".format(progress['translated_progress']) if progress is not None else "")
                return langInfo.Description + progress_display

            self.chLang = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [langDisplay(x) for x in self.langChoices], 0)
            self.chLang.Bind(wx.EVT_CHOICE, self.onLangSelection)

            selectedIndex = self.langChoices.index(next((x for x in self.langChoices if x.CanonicalName == self.localeSettings.get('locale')), None))
            self.chLang.SetSelection(selectedIndex)

            langSizer.Add(self.chLang, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            langBox.Add(langSizer)
            langBox.Add(hl.HyperLinkCtrl(panel, -1,
                                         _t("Interested in helping with translations?"),
                                         URL="https://github.com/pyfa-org/Pyfa/blob/master/locale/README.md"
                                         ), 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 15)
        else:
            self.stLangLabel = wx.StaticText(panel, wx.ID_ANY, _t("Pyfa language selection disabled. Please check if .mo files have been generated.\nRefer to locale/README.md for info."), wx.DefaultPosition, wx.DefaultSize, 0)
            self.stLangLabel.Wrap(-1)
            langSizer.Add(self.stLangLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            langBox.Add(langSizer)

        eosLangSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.stEosLangLabel = wx.StaticText(panel, wx.ID_ANY, _t("EVE Data:"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.stEosLangLabel.Wrap(-1)
        eosLangSizer.Add(self.stEosLangLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.eosLangChoices = [(LocaleSettings.defaults['eos_locale'], LocaleSettings.defaults['eos_locale'])] + \
                              sorted([(wx.Locale.FindLanguageInfo(x).Description, x) for x in eos.config.translation_mapping.keys()], key=lambda x: x[0])

        self.chEosLang = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [x[0] for x in self.eosLangChoices], 0)
        self.chEosLang.Bind(wx.EVT_CHOICE, self.onEosLangSelection)

        selectedIndex = self.eosLangChoices.index(
            next((x for x in self.eosLangChoices if x[1] == self.localeSettings.get('eos_locale')), None))
        self.chEosLang.SetSelection(selectedIndex)

        eosLangSizer.Add(self.chEosLang, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        langBox.Add(eosLangSizer)
        langBox.Add(wx.StaticText(panel, wx.ID_ANY,
                                  _t("Auto will use the same language pyfa uses if available, otherwise English"),
                                  wx.DefaultPosition,
                                  wx.DefaultSize, 0), 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 15)

        self.cbGlobalChar = wx.CheckBox(panel, wx.ID_ANY, _t("Use global character"), wx.DefaultPosition, wx.DefaultSize,
                                        0)
        mainSizer.Add(self.cbGlobalChar, 0, wx.ALL | wx.EXPAND, 5)

        self.cbDefaultCharImplants = wx.CheckBox(panel, wx.ID_ANY, _t("Use character implants by default for new fits"),
                                                 wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbDefaultCharImplants, 0, wx.ALL | wx.EXPAND, 5)

        self.cbGlobalDmgPattern = wx.CheckBox(panel, wx.ID_ANY, _t("Use global damage pattern"), wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        mainSizer.Add(self.cbGlobalDmgPattern, 0, wx.ALL | wx.EXPAND, 5)

        self.cbCompactSkills = wx.CheckBox(panel, wx.ID_ANY, _t("Compact skills needed tooltip"), wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        mainSizer.Add(self.cbCompactSkills, 0, wx.ALL | wx.EXPAND, 5)

        self.cbFitColorSlots = wx.CheckBox(panel, wx.ID_ANY, _t("Color fitting view by slot"), wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        mainSizer.Add(self.cbFitColorSlots, 0, wx.ALL | wx.EXPAND, 5)

        self.cbReopenFits = wx.CheckBox(panel, wx.ID_ANY, _t("Reopen previous fits on startup"), wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        mainSizer.Add(self.cbReopenFits, 0, wx.ALL | wx.EXPAND, 5)

        self.cbRackSlots = wx.CheckBox(panel, wx.ID_ANY, _t("Separate Racks"), wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbRackSlots, 0, wx.ALL | wx.EXPAND, 5)

        labelSizer = wx.BoxSizer(wx.VERTICAL)
        self.cbRackLabels = wx.CheckBox(panel, wx.ID_ANY, _t("Show Rack Labels"), wx.DefaultPosition, wx.DefaultSize, 0)
        labelSizer.Add(self.cbRackLabels, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(labelSizer, 0, wx.LEFT | wx.EXPAND, 30)

        self.cbShowTooltip = wx.CheckBox(panel, wx.ID_ANY, _t("Show fitting tab tooltips"), wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbShowTooltip, 0, wx.ALL | wx.EXPAND, 5)

        self.cbGaugeAnimation = wx.CheckBox(panel, wx.ID_ANY, _t("Animate gauges"), wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbGaugeAnimation, 0, wx.ALL | wx.EXPAND, 5)

        self.cbOpenFitInNew = wx.CheckBox(panel, wx.ID_ANY, _t("Open fittings in a new page by default"),
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbOpenFitInNew, 0, wx.ALL | wx.EXPAND, 5)

        self.cbShowShipBrowserTooltip = wx.CheckBox(panel, wx.ID_ANY, _t("Show ship browser tooltip"),
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbShowShipBrowserTooltip, 0, wx.ALL | wx.EXPAND, 5)

        self.cbReloadAll = wx.CheckBox(panel, wx.ID_ANY, _t("Change charge in all modules of the same type"),
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        if "wxGTK" not in wx.PlatformInfo:
            self.cbReloadAll.SetCursor(helpCursor)
        self.cbReloadAll.SetToolTip(wx.ToolTip(
                _t('When disabled, reloads charges just in selected modules. Action can be reversed by holding Ctrl or Alt key while changing charge.')))
        mainSizer.Add(self.cbReloadAll, 0, wx.ALL | wx.EXPAND, 5)

        self.cbExpMutants = wx.CheckBox(panel, wx.ID_ANY, _t("Include more information in names of mutated items"),
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        if "wxGTK" not in wx.PlatformInfo:
            self.cbExpMutants.SetCursor(helpCursor)
        self.cbExpMutants.SetToolTip(wx.ToolTip(
                _t('Use short mutaplasmid name and base item name instead of actual item name. Works if EVE data language is set to English.')))
        mainSizer.Add(self.cbExpMutants, 0, wx.ALL | wx.EXPAND, 5)

        self.rbAddLabels = wx.RadioBox(panel, -1, _t("Extra info in Additions panel tab names"), wx.DefaultPosition, wx.DefaultSize,
                                       [_t("None"), _t("Quantity of active items"), _t("Quantity of all items")], 1, wx.RA_SPECIFY_COLS)
        mainSizer.Add(self.rbAddLabels, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, 10)
        self.rbAddLabels.Bind(wx.EVT_RADIOBOX, self.OnAddLabelsChange)

        self.sFit = Fit.getInstance()

        self.cbGlobalChar.SetValue(self.sFit.serviceFittingOptions["useGlobalCharacter"])
        self.cbDefaultCharImplants.SetValue(self.sFit.serviceFittingOptions["useCharacterImplantsByDefault"])
        self.cbGlobalDmgPattern.SetValue(self.sFit.serviceFittingOptions["useGlobalDamagePattern"])
        self.cbFitColorSlots.SetValue(self.sFit.serviceFittingOptions["colorFitBySlot"] or False)
        self.cbRackSlots.SetValue(self.sFit.serviceFittingOptions["rackSlots"] or False)
        self.cbRackLabels.SetValue(self.sFit.serviceFittingOptions["rackLabels"] or False)
        self.cbCompactSkills.SetValue(self.sFit.serviceFittingOptions["compactSkills"] or False)
        self.cbReopenFits.SetValue(self.openFitsSettings["enabled"])
        self.cbShowTooltip.SetValue(self.sFit.serviceFittingOptions["showTooltip"] or False)
        self.cbGaugeAnimation.SetValue(self.sFit.serviceFittingOptions["enableGaugeAnimation"])
        self.cbOpenFitInNew.SetValue(self.sFit.serviceFittingOptions["openFitInNew"])
        self.cbShowShipBrowserTooltip.SetValue(self.sFit.serviceFittingOptions["showShipBrowserTooltip"])
        self.cbReloadAll.SetValue(self.sFit.serviceFittingOptions["ammoChangeAll"])
        self.cbExpMutants.SetValue(self.sFit.serviceFittingOptions["expandedMutantNames"])
        self.rbAddLabels.SetSelection(self.sFit.serviceFittingOptions["additionsLabels"])

        self.cbGlobalChar.Bind(wx.EVT_CHECKBOX, self.OnCBGlobalCharStateChange)
        self.cbDefaultCharImplants.Bind(wx.EVT_CHECKBOX, self.OnCBDefaultCharImplantsStateChange)
        self.cbGlobalDmgPattern.Bind(wx.EVT_CHECKBOX, self.OnCBGlobalDmgPatternStateChange)
        self.cbFitColorSlots.Bind(wx.EVT_CHECKBOX, self.onCBGlobalColorBySlot)
        self.cbRackSlots.Bind(wx.EVT_CHECKBOX, self.onCBGlobalRackSlots)
        self.cbRackLabels.Bind(wx.EVT_CHECKBOX, self.onCBGlobalRackLabels)
        self.cbCompactSkills.Bind(wx.EVT_CHECKBOX, self.onCBCompactSkills)
        self.cbReopenFits.Bind(wx.EVT_CHECKBOX, self.onCBReopenFits)
        self.cbShowTooltip.Bind(wx.EVT_CHECKBOX, self.onCBShowTooltip)
        self.cbGaugeAnimation.Bind(wx.EVT_CHECKBOX, self.onCBGaugeAnimation)
        self.cbOpenFitInNew.Bind(wx.EVT_CHECKBOX, self.onCBOpenFitInNew)
        self.cbShowShipBrowserTooltip.Bind(wx.EVT_CHECKBOX, self.onCBShowShipBrowserTooltip)
        self.cbReloadAll.Bind(wx.EVT_CHECKBOX, self.onCBReloadAll)
        self.cbExpMutants.Bind(wx.EVT_CHECKBOX, self.onCBExpMutants)

        self.cbRackLabels.Enable(self.sFit.serviceFittingOptions["rackSlots"] or False)

        panel.SetSizer(mainSizer)
        panel.Layout()

    def onLangSelection(self, event):
        selection = self.chLang.GetSelection()
        locale = self.langChoices[selection]
        self.localeSettings.set('locale', locale.CanonicalName)

    def onEosLangSelection(self, event):
        selection = self.chEosLang.GetSelection()
        locale = self.eosLangChoices[selection]
        self.localeSettings.set('eos_locale', locale[1])

    def onCBGlobalColorBySlot(self, event):
        # todo: maybe create a SettingChanged event that we can fire, and have other things hook into, instead of having the preference panel itself handle the
        # updating of things related to settings.
        self.sFit.serviceFittingOptions["colorFitBySlot"] = self.cbFitColorSlots.GetValue()
        fitID = self.mainFrame.getActiveFit()
        self.sFit.refreshFit(fitID)

        iView = self.mainFrame.marketBrowser.itemView
        if iView.active:
            iView.update(iView.active)

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))
        event.Skip()

    def onCBGlobalRackSlots(self, event):
        self.sFit.serviceFittingOptions["rackSlots"] = self.cbRackSlots.GetValue()
        self.cbRackLabels.Enable(self.cbRackSlots.GetValue())
        fitID = self.mainFrame.getActiveFit()
        self.sFit.refreshFit(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))
        event.Skip()

    def onCBGlobalRackLabels(self, event):
        self.sFit.serviceFittingOptions["rackLabels"] = self.cbRackLabels.GetValue()
        fitID = self.mainFrame.getActiveFit()
        self.sFit.refreshFit(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))
        event.Skip()

    def OnCBGlobalCharStateChange(self, event):
        self.sFit.serviceFittingOptions["useGlobalCharacter"] = self.cbGlobalChar.GetValue()
        event.Skip()

    def OnCBDefaultCharImplantsStateChange(self, event):
        self.sFit.serviceFittingOptions["useCharacterImplantsByDefault"] = self.cbDefaultCharImplants.GetValue()
        event.Skip()

    def OnCBGlobalDmgPatternStateChange(self, event):
        self.sFit.serviceFittingOptions["useGlobalDamagePattern"] = self.cbGlobalDmgPattern.GetValue()
        event.Skip()

    def onCBCompactSkills(self, event):
        self.sFit.serviceFittingOptions["compactSkills"] = self.cbCompactSkills.GetValue()
        fitID = self.mainFrame.getActiveFit()
        self.sFit.refreshFit(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))
        event.Skip()

    def onCBReopenFits(self, event):
        self.openFitsSettings["enabled"] = self.cbReopenFits.GetValue()

    def onCBShowTooltip(self, event):
        self.sFit.serviceFittingOptions["showTooltip"] = self.cbShowTooltip.GetValue()

    def onCBGaugeAnimation(self, event):
        self.sFit.serviceFittingOptions["enableGaugeAnimation"] = self.cbGaugeAnimation.GetValue()

    def onCBOpenFitInNew(self, event):
        self.sFit.serviceFittingOptions["openFitInNew"] = self.cbOpenFitInNew.GetValue()

    def onCBShowShipBrowserTooltip(self, event):
        self.sFit.serviceFittingOptions["showShipBrowserTooltip"] = self.cbShowShipBrowserTooltip.GetValue()

    def onCBReloadAll(self, event):
        self.sFit.serviceFittingOptions["ammoChangeAll"] = self.cbReloadAll.GetValue()

    def onCBExpMutants(self, event):
        self.sFit.serviceFittingOptions["expandedMutantNames"] = self.cbExpMutants.GetValue()
        fitID = self.mainFrame.getActiveFit()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))

    def OnAddLabelsChange(self, event):
        self.sFit.serviceFittingOptions["additionsLabels"] = event.GetInt()
        fitID = self.mainFrame.getActiveFit()
        self.sFit.refreshFit(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))
        event.Skip()

    def getImage(self):
        return BitmapLoader.getBitmap("prefs_settings", "gui")


PFGeneralPref.register()
