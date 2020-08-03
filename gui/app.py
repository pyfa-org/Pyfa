import wx
import config
import os
import sys
from logbook import Logger
pyfalog = Logger(__name__)
from service.settings import LocaleSettings


class PyfaApp(wx.App):
    def OnInit(self):
        """
        Do application initialization work, e.g. define application globals.
        """

        # Name for my application.
        self.appName = "pyfa"

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