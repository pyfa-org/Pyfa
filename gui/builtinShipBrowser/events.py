# noinspection PyPackageRequirements
import wx.lib.newevent

FitRenamed, EVT_FIT_RENAMED = wx.lib.newevent.NewEvent()
FitSelected, EVT_FIT_SELECTED = wx.lib.newevent.NewEvent()
FitRemoved, EVT_FIT_REMOVED = wx.lib.newevent.NewEvent()

BoosterListUpdated, BOOSTER_LIST_UPDATED = wx.lib.newevent.NewEvent()

Stage1Selected, EVT_SB_STAGE1_SEL = wx.lib.newevent.NewEvent()
Stage2Selected, EVT_SB_STAGE2_SEL = wx.lib.newevent.NewEvent()
Stage3Selected, EVT_SB_STAGE3_SEL = wx.lib.newevent.NewEvent()
SearchSelected, EVT_SB_SEARCH_SEL = wx.lib.newevent.NewEvent()
ImportSelected, EVT_SB_IMPORT_SEL = wx.lib.newevent.NewEvent()
