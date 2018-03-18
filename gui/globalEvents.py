# noinspection PyPackageRequirements
import wx.lib.newevent

FitChanged, FIT_CHANGED = wx.lib.newevent.NewEvent()
CharListUpdated, CHAR_LIST_UPDATED = wx.lib.newevent.NewEvent()
CharChanged, CHAR_CHANGED = wx.lib.newevent.NewEvent()

SsoLoggingIn, EVT_SSO_LOGGING_IN = wx.lib.newevent.NewEvent()
SsoLogin, EVT_SSO_LOGIN = wx.lib.newevent.NewEvent()
SsoLogout, EVT_SSO_LOGOUT = wx.lib.newevent.NewEvent()
