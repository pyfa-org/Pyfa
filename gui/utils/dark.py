import wx

from logbook import Logger

from service.settings import ThemeSettings


pyfalog = Logger(__name__)


def systemIsDark():
    """Whether the desktop itself is currently using a dark appearance."""
    try:
        return wx.SystemSettings.GetAppearance().IsDark()
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception:
        return False


def isDark():
    """Whether pyfa should be drawing itself with dark colours.

    Used to pick between the light and dark colour maps. wxMSW used to be
    excluded here because wxWidgets 3.2 could not do dark mode on Windows at
    all; 3.3 can, so the platform is no longer special-cased.
    """
    theme = ThemeSettings.getInstance().get('theme')
    if theme == ThemeSettings.DARK:
        return True
    if theme == ThemeSettings.BRIGHT:
        return False
    return systemIsDark()


def applyTheme(app=None):
    """Push the configured theme onto wx so native controls follow it too.

    Returns True if wx accepted the change. On MSW dark mode is opt-in and
    upstream considers it experimental, so it has to be enabled explicitly
    before requesting a dark appearance.
    """
    app = app or wx.GetApp()
    if app is None:
        return False

    theme = ThemeSettings.getInstance().get('theme')
    appearance = {
        ThemeSettings.SYSTEM: wx.App.Appearance.System,
        ThemeSettings.DARK: wx.App.Appearance.Dark,
    }.get(theme, wx.App.Appearance.Light)

    try:
        if 'wxMSW' in wx.PlatformInfo and theme != ThemeSettings.BRIGHT:
            app.MSWEnableDarkMode()
        result = app.SetAppearance(appearance)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        pyfalog.warning('Could not apply theme: {0}', e)
        return False

    if result != wx.App.AppearanceResult.Ok:
        pyfalog.info('wx did not apply the requested appearance (result {0})', int(result))
        return False
    return True
