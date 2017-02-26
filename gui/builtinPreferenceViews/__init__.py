# noinspection PyPackageRequirements
import wx

__all__ = [
    "pyfaGeneralPreferences",
    "pyfaHTMLExportPreferences",
    "pyfaUpdatePreferences",
    "pyfaNetworkPreferences",
    "pyfaDatabasePreferences",
    "pyfaLoggingPreferences",
    "pyfaEnginePreferences",
    "pyfaStatViewPreferences",
]

if 'wxMac' not in wx.PlatformInfo or ('wxMac' in wx.PlatformInfo and wx.VERSION >= (3, 0)):
    __all__.append("pyfaCrestPreferences")
