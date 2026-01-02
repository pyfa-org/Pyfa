
from logbook import Logger
import wx

from service.settings import ThemeSettings

pyfalog = Logger(__name__)


def _isSystemDark():
    """Check if the operating system is in dark mode."""
    try:
        appearance = wx.SystemSettings.GetAppearance()
        return appearance.IsDark()
    except Exception:
        return False


def usePyfaDark():
    """
    Determine if the application should use Pyfa's custom dark colors.
    
    Theme behavior:
    - System Default:
        - macOS/Linux: Never use Pyfa Dark (use system colors)
        - Windows: Use Pyfa Dark if system is in dark mode
    - Light: Never use Pyfa Dark
    - Pyfa Dark: Always use Pyfa Dark
    
    Returns True if Pyfa's custom dark colors should be applied.
    """
    try:
        themeSettings = ThemeSettings.getInstance()
        mode = themeSettings.get('theme_mode')

        if mode == ThemeSettings.THEME_DARK:
            # "Pyfa Dark" selected - always use Pyfa dark colors
            return True
        elif mode == ThemeSettings.THEME_LIGHT:
            # "Light" selected - never use Pyfa dark colors
            return False
        else:  # THEME_SYSTEM - "System Default"
            # On Windows: use Pyfa Dark if system is dark
            # On macOS/Linux: never use Pyfa Dark (use system colors instead)
            if wx.Platform == '__WXMSW__':
                return _isSystemDark()
            else:
                return False
    except Exception:
        return False


def useSystemColors():
    """
    Determine if the application should use system default colors.
    
    This is True on macOS/Linux when "System Default" is selected,
    meaning we should not override any colors and let the OS handle theming.
    
    Returns True if system colors should be used without modification.
    """
    try:
        themeSettings = ThemeSettings.getInstance()
        mode = themeSettings.get('theme_mode')

        if mode == ThemeSettings.THEME_SYSTEM:
            # "System Default" on macOS/Linux means use system colors
            if wx.Platform != '__WXMSW__':
                return True
        return False
    except Exception:
        return False


# Keep isDark as an alias for backward compatibility
def isDark():
    """
    Backward compatibility alias for usePyfaDark().
    """
    return usePyfaDark()


def setWindowsDarkMode():
    """
    Enable dark mode for the entire application on Windows 10/11.
    This affects the menu bar, context menus, and other system UI elements.
    Must be called early in app initialization, before windows are created.
    """
    if not isDark():
        return
    
    if wx.Platform != "__WXMSW__":
        return
    
    try:
        import ctypes
        
        # SetPreferredAppMode constants
        # 0 = Default, 1 = AllowDark, 2 = ForceDark, 3 = ForceLight
        APPMODE_ALLOWDARK = 1
        APPMODE_FORCEDARK = 2
        
        # Try to load uxtheme ordinal 135 (SetPreferredAppMode) - Windows 10 1903+
        uxtheme = ctypes.windll.uxtheme
        
        # SetPreferredAppMode is ordinal 135
        try:
            SetPreferredAppMode = uxtheme[135]
            SetPreferredAppMode.argtypes = [ctypes.c_int]
            SetPreferredAppMode.restype = ctypes.c_int
            SetPreferredAppMode(APPMODE_FORCEDARK)
            pyfalog.debug("SetPreferredAppMode set to ForceDark")
        except Exception:
            # Try AllowDarkModeForApp (ordinal 135 on older builds, or different approach)
            try:
                AllowDarkModeForApp = uxtheme[135]
                AllowDarkModeForApp.argtypes = [ctypes.c_bool]
                AllowDarkModeForApp.restype = ctypes.c_bool
                AllowDarkModeForApp(True)
                pyfalog.debug("AllowDarkModeForApp enabled")
            except Exception:
                pass
        
        # FlushMenuThemes to apply immediately (ordinal 136)
        try:
            FlushMenuThemes = uxtheme[136]
            FlushMenuThemes()
            pyfalog.debug("FlushMenuThemes called")
        except Exception:
            pass
            
    except Exception as e:
        pyfalog.debug("Could not set Windows dark mode: {}", str(e))


def setDarkTitleBar(window):
    """
    Enable dark title bar on Windows 10/11 when in dark mode.
    This uses the Windows DWM API to set the immersive dark mode attribute.
    """
    if not isDark():
        return
    
    if wx.Platform != "__WXMSW__":
        return
    
    try:
        import ctypes
        
        # Get the window handle
        hwnd = window.GetHandle()
        
        # DWMWA_USE_IMMERSIVE_DARK_MODE = 20 (Windows 10 20H1+)
        # For older Windows 10 builds, it was 19
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        
        dwmapi = ctypes.windll.dwmapi
        
        # Try with attribute 20 first (newer Windows)
        value = ctypes.c_int(1)
        result = dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )
        
        # If that failed, try with attribute 19 (older Windows 10)
        if result != 0:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 19
            dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(value),
                ctypes.sizeof(value)
            )
        
        pyfalog.debug("Dark title bar enabled for window")
    except Exception as e:
        pyfalog.debug("Could not set dark title bar: {}", str(e))
