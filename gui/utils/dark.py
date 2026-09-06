import wx


def isDark():
    try:
        return wx.SystemSettings.GetAppearance().IsDark()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        return False
