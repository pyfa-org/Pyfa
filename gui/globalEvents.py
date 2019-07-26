# noinspection PyPackageRequirements
import wx.lib.newevent

FitChanged, FIT_CHANGED = wx.lib.newevent.NewEvent()
FitRemoved, FIT_REMOVED = wx.lib.newevent.NewEvent()
CharListUpdated, CHAR_LIST_UPDATED = wx.lib.newevent.NewEvent()
CharChanged, CHAR_CHANGED = wx.lib.newevent.NewEvent()
GraphOptionChanged, GRAPH_OPTION_CHANGED = wx.lib.newevent.NewEvent()
TargetProfileChanged, TARGET_PROFILE_CHANGED = wx.lib.newevent.NewEvent()
TargetProfileRemoved, TARGET_PROFILE_REMOVED = wx.lib.newevent.NewEvent()

SsoLoggingIn, EVT_SSO_LOGGING_IN = wx.lib.newevent.NewEvent()
SsoLogin, EVT_SSO_LOGIN = wx.lib.newevent.NewEvent()
SsoLogout, EVT_SSO_LOGOUT = wx.lib.newevent.NewEvent()
