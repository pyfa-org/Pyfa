import ctypes

import wx

from logbook import Logger

from service.settings import ThemeSettings


pyfalog = Logger(__name__)

WM_THEMECHANGED = 0x031A


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
            flags = wx.App.DarkMode_Always if theme == ThemeSettings.DARK else wx.App.DarkMode_Auto
            if not app.MSWEnableDarkMode(flags):
                pyfalog.info('wx could not enable dark mode, it needs Windows 10 20H1 or later')
        result = app.SetAppearance(appearance)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        pyfalog.warning('Could not apply theme: {0}', e)
        return False

    if result == wx.App.AppearanceResult.CannotChange:
        pyfalog.info('Appearance can no longer be changed, pyfa has to be restarted to apply it')
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


def bindNativeTheme(window):
    """Keep a native wxMSW control's visual style in step with the theme.

    Windows draws parts of native controls itself, off the window's visual style rather than off
    any color we set. wxWindowMSW::MSWGetDarkModeSupport() asks for the Explorer style, and no
    control overrides that, so in dark mode the tree still gets the light style, whose expander
    glyph for an opened item is nearly black and vanishes against the dark background. Asking for
    the dark variant of the same style gets the light glyphs (and dark scrollbars) instead. The
    style is only available from Windows 10, and elsewhere this does nothing.
    """
    if 'wxMSW' not in wx.PlatformInfo:
        return

    def apply():
        handle = window.GetHandle()
        if not handle:
            return
        theme = 'DarkMode_Explorer' if isDark() else 'Explorer'
        try:
            result = ctypes.WinDLL('uxtheme').SetWindowTheme(
                ctypes.c_void_p(handle), ctypes.c_wchar_p(theme), None)
            if result:
                pyfalog.warning('Requesting the {0} visual style failed with 0x{1:08x}', theme, result & 0xffffffff)
                return
            # native controls hold on to the style they opened and only pick up a new one when
            # they are told it changed, which is what wx does after setting a theme itself
            ctypes.WinDLL('user32').SendMessageW(ctypes.c_void_p(handle), WM_THEMECHANGED, 0, 0)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            pyfalog.warning('Could not apply the {0} visual style: {1}', theme, e)

    def onSysColorChanged(event):
        # wx puts the light style back when the mode changes, so ours has to go on after it
        apply()
        window.Refresh()
        event.Skip()

    apply()
    window.Bind(wx.EVT_SYS_COLOUR_CHANGED, onSysColorChanged)
