# noinspection PyPackageRequirements
import wx.lib.newevent

FitRenamed, FIT_RENAMED = wx.lib.newevent.NewEvent()
FitChanged, FIT_CHANGED = wx.lib.newevent.NewEvent()
FitRemoved, FIT_REMOVED = wx.lib.newevent.NewEvent()
FitNotesChanged, FIT_NOTES_CHANGED = wx.lib.newevent.NewEvent()
CharListUpdated, CHAR_LIST_UPDATED = wx.lib.newevent.NewEvent()
CharChanged, CHAR_CHANGED = wx.lib.newevent.NewEvent()
GraphOptionChanged, GRAPH_OPTION_CHANGED = wx.lib.newevent.NewEvent()
TargetProfileRenamed, TARGET_PROFILE_RENAMED = wx.lib.newevent.NewEvent()
TargetProfileChanged, TARGET_PROFILE_CHANGED = wx.lib.newevent.NewEvent()
TargetProfileRemoved, TARGET_PROFILE_REMOVED = wx.lib.newevent.NewEvent()
# For events when item is actually replaced under the hood,
# but from user's perspective it's supposed to change/mutate
ItemChangedInplace, ITEM_CHANGED_INPLACE = wx.lib.newevent.NewEvent()

EffectiveHpToggled, EFFECTIVE_HP_TOGGLED = wx.lib.newevent.NewEvent()

SsoLoggingIn, EVT_SSO_LOGGING_IN = wx.lib.newevent.NewEvent()
SsoLogin, EVT_SSO_LOGIN = wx.lib.newevent.NewEvent()
SsoLogout, EVT_SSO_LOGOUT = wx.lib.newevent.NewEvent()
