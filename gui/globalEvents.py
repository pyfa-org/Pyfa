# noinspection PyPackageRequirements
from wx.lib.newevent import NewEvent

FitRenamed, FIT_RENAMED = NewEvent()
FitChanged, FIT_CHANGED = NewEvent()
FitRemoved, FIT_REMOVED = NewEvent()
FitNotesChanged, FIT_NOTES_CHANGED = NewEvent()
CharListUpdated, CHAR_LIST_UPDATED = NewEvent()
CharChanged, CHAR_CHANGED = NewEvent()
GraphOptionChanged, GRAPH_OPTION_CHANGED = NewEvent()
TargetProfileRenamed, TARGET_PROFILE_RENAMED = NewEvent()
TargetProfileChanged, TARGET_PROFILE_CHANGED = NewEvent()
TargetProfileRemoved, TARGET_PROFILE_REMOVED = NewEvent()
# For events when item is actually replaced under the hood,
# but from user's perspective it's supposed to change/mutate
ItemChangedInplace, ITEM_CHANGED_INPLACE = NewEvent()

EffectiveHpToggled, EFFECTIVE_HP_TOGGLED = NewEvent()

SsoLoggingIn, EVT_SSO_LOGGING_IN = NewEvent()
SsoLogin, EVT_SSO_LOGIN = NewEvent()
SsoLogout, EVT_SSO_LOGOUT = NewEvent()
