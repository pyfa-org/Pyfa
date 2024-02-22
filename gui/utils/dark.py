import wx


def isDark():
    if 'wxMSW' in wx.PlatformInfo:
        return False
    try:
        return wx.SystemSettings.GetAppearance().IsDark()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        return False
