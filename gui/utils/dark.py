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
    """Whether pyfa should be drawing itself with dark colors.

    Used to pick between the light and dark color maps. wxMSW used to be
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

def themedColor(light, dark):
    return wx.Colour(*(dark if isDark() else light))


def warningTextColor():
    return themedColor((204, 51, 51), (255, 111, 111))


def errorTextColor():
    return themedColor((255, 0, 0), (255, 122, 122))


def highlightColor():
    return themedColor((255, 255, 0), (112, 96, 0))


def bindBackgroundToTheme(window, sysColor=wx.SYS_COLOUR_WINDOW):

    def apply():
        color = sysColor() if callable(sysColor) else wx.SystemSettings.GetColour(sysColor)
        window.SetBackgroundColour(color)

    def onSysColorChanged(event):
        apply()
        window.Refresh()
        event.Skip()

    apply()
    window.Bind(wx.EVT_SYS_COLOUR_CHANGED, onSysColorChanged)

def borderColor():
    return themedColor((64, 64, 64), (191, 191, 191))
