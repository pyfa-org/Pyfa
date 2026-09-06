import wx
import config
import os
import sys
from logbook import Logger
pyfalog = Logger(__name__)
from service.settings import LocaleSettings, ThemeSettings


class PyfaApp(wx.App):
    def OnInit(self):
        """
        Do application initialization work, e.g. define application globals.
        """

        # Name for my application.
        self.appName = "pyfa"

        # Windows can only apply appearance before any windows exist.
        self.ApplyAppearance()

        #------------

        # # Simplified init method.
        # self.DoConfig()
        # self.Init() # InspectionMixin
        # # work around for Python stealing "_".
        # sys.displayhook = _displayHook
        #
        # #------------


        # Return locale folder.
        localeDir = os.path.join(config.pyfaPath, "locale")

        # Set language stuff and update to last used language.
        self.locale = None
        wx.Locale.AddCatalogLookupPathPrefix(localeDir)
        # Set language stuff and update to last used language.
        self.UpdateLanguage(config.language)

        return True

    #-----------------------------------------------------------------------

    def UpdateLanguage(self, lang=None):
        """
        Update the language to the requested one.

        Make *sure* any existing locale is deleted before the new
        one is created. The old C++ object needs to be deleted
        before the new one is created, and if we just assign a new
        instance to the old Python variable, the old C++ locale will
        not be destroyed soon enough, likely causing a crash.

        :param string `lang`: one of the supported language codes.
        """

        # Language domain.
        langDomain = config.CATALOG

        # If an unsupported language is requested default to English.

        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale

        # Create a locale object for this language.
        langInfo = wx.Locale.FindLanguageInfo(lang)
        if langInfo is not None:
            pyfalog.debug("Setting language to: " + lang)
            self.locale = wx.Locale(langInfo.Language)
            if self.locale.IsOk():
                success = self.locale.AddCatalog(langDomain)
                if not success:
                    print("Langauage catalog not successfully loaded")

        else:
            pyfalog.debug("Cannot find langauge: " + lang)
            self.locale = wx.Locale(wx.Locale.FindLanguageInfo(LocaleSettings.defaults['locale']).Language)

    def ApplyAppearance(self):
        try:
            appearance_map = {
                ThemeSettings.SYSTEM: wx.App.Appearance.System,
                ThemeSettings.LIGHT: wx.App.Appearance.Light,
                ThemeSettings.DARK: wx.App.Appearance.Dark,
            }
        except AttributeError:
            pyfalog.debug("wx.App.Appearance is not available; skipping theme setup")
            return

        mode = ThemeSettings.getInstance().get('appearance')
        target = appearance_map.get(mode, wx.App.Appearance.System)
        try:
            result = self.SetAppearance(target)
            pyfalog.info("Set appearance to {0} (result {1})", mode, result)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            pyfalog.warning("Failed to set application appearance: {0}", e)