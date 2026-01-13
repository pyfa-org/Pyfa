"""
Centralized color definitions for Pyfa dark/light themes.
All UI components should import colors from here.

Color Logic:
- useSystemColors() True (macOS/Linux + System Default): Return wx.SystemSettings colors
- usePyfaDark() True (Pyfa Dark theme): Return Pyfa's custom dark colors
- Otherwise (Light theme): Return wx.SystemSettings colors
"""
import wx
from gui.utils.dark import usePyfaDark, useSystemColors


class Themes:
    """Provides theme-aware colors for the application."""

    # =========================================================================
    # Main Window Colors (override system colors for dark mode on Windows)
    # =========================================================================

    @staticmethod
    def windowBackground():
        """Main window/panel background"""
        if useSystemColors():
            return wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        if usePyfaDark():
            return wx.Colour(45, 45, 45)
        return wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)

    @staticmethod
    def buttonFace():
        """Button/toolbar background"""
        if useSystemColors():
            return wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
        if usePyfaDark():
            return wx.Colour(55, 55, 55)
        return wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)

    @staticmethod
    def text():
        """Standard text color"""
        if useSystemColors():
            return wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
        if usePyfaDark():
            return wx.Colour(220, 220, 220)
        return wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)

    @staticmethod
    def listBackground():
        """List/tree control background"""
        if useSystemColors():
            return wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX)
        if usePyfaDark():
            return wx.Colour(35, 35, 35)
        return wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX)

    # =========================================================================
    # Custom Pyfa Colors (dark/light variants)
    # =========================================================================

    @staticmethod
    def gaugeBackground():
        """Background color for gauge widgets - always dark grey (original Pyfa style)"""
        return wx.Colour(51, 51, 51)

    @staticmethod
    def errorBackground():
        """Background color for error states"""
        if useSystemColors():
            return wx.Colour(204, 51, 51)
        if usePyfaDark():
            return wx.Colour(70, 20, 20)
        return wx.Colour(204, 51, 51)

    @staticmethod
    def warningColor():
        """Warning/alert color"""
        if useSystemColors():
            return wx.Colour(204, 51, 51)
        if usePyfaDark():
            return wx.Colour(180, 80, 80)
        return wx.Colour(204, 51, 51)

    @staticmethod
    def inputBackground():
        """Background for editable input fields (TextCtrl, ComboBox, etc.)"""
        if useSystemColors():
            return wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        if usePyfaDark():
            return wx.Colour(50, 50, 50)
        return wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)

    @staticmethod
    def inputDisabledBackground():
        """Background for disabled/readonly input fields"""
        if useSystemColors():
            return wx.Colour(240, 240, 240)
        if usePyfaDark():
            return wx.Colour(45, 45, 45)
        return wx.Colour(240, 240, 240)

    @staticmethod
    def separatorColor():
        """Color for separators and dividers"""
        if useSystemColors():
            return wx.Colour(200, 200, 200)
        if usePyfaDark():
            return wx.Colour(80, 80, 80)
        return wx.Colour(200, 200, 200)

    @staticmethod
    def highlightBackground():
        """Background for highlighted/selected items"""
        if useSystemColors():
            return wx.Colour(220, 220, 240)
        if usePyfaDark():
            return wx.Colour(70, 70, 90)
        return wx.Colour(220, 220, 240)

    @staticmethod
    def styleInput(ctrl: wx.Control, disabled=False):
        """
        Apply theme colors to an input control (TextCtrl, Choice, ComboBox, etc.).
        Call this after creating the control.
        
        Note: On Windows with Pyfa Dark theme, native controls may not fully respect 
        SetBackgroundColour due to native theming. We disable the theme for this 
        control to allow custom background colors to work.
        
        When using system colors (macOS/Linux + System Default), we don't modify
        the control as the OS handles theming.
        """
        # When using system colors, let the OS handle everything
        if useSystemColors():
            return
        
        if disabled:
            bgColor = Themes.inputDisabledBackground()
        else:
            bgColor = Themes.inputBackground()
        
        fgColor = Themes.text()
        
        # On Windows, we need to disable the native theme to allow custom colors
        if wx.Platform == '__WXMSW__':
            try:
                import ctypes
                # SetWindowTheme with empty strings disables visual styles for the control
                uxtheme = ctypes.windll.uxtheme
                hwnd = ctrl.GetHandle()
                uxtheme.SetWindowTheme(hwnd, "", "")
            except Exception:
                pass
            
            # Also try the wx method
            if hasattr(ctrl, 'SetThemeEnabled'):
                ctrl.SetThemeEnabled(False)
        
        # Apply the colors
        ctrl.SetBackgroundColour(bgColor)
        ctrl.SetForegroundColour(fgColor)
        
        # For TextCtrl, we also need to set the default style for text
        if isinstance(ctrl, wx.TextCtrl):
            textAttr = wx.TextAttr(fgColor, bgColor)
            ctrl.SetDefaultStyle(textAttr)
        
        # Force a refresh to apply the new colors
        ctrl.Refresh()


# =============================================================================
# Themed Base Classes
# =============================================================================

class ThemedPanel(wx.Panel):
    """
    A wx.Panel that automatically applies theme-aware colors.
    Use this as a base class for panels that need dark mode support.
    
    By default uses buttonFace() for background. Override _getBackgroundColor()
    to use a different color (e.g., windowBackground()).
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._applyThemeColors()
    
    def _getBackgroundColor(self):
        """Override this to use a different background color."""
        return Themes.buttonFace()
    
    def _applyThemeColors(self):
        """Apply theme colors to this panel."""
        self.SetBackgroundColour(self._getBackgroundColor())
        self.SetForegroundColour(Themes.text())


class ThemedContentPanel(ThemedPanel):
    """A panel using windowBackground() - suitable for content areas."""
    
    def _getBackgroundColor(self):
        return Themes.windowBackground()


class ThemedListPanel(ThemedPanel):
    """A panel using listBackground() - suitable for list containers."""
    
    def _getBackgroundColor(self):
        return Themes.listBackground()


class ThemedFrame(wx.Frame):
    """
    A wx.Frame that automatically applies theme-aware colors and dark title bar.
    Use this as a base class for frames that need dark mode support.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._applyThemeColors()
    
    def _applyThemeColors(self):
        """Apply theme colors and dark title bar to this frame."""
        from gui.utils.dark import setDarkTitleBar
        self.SetBackgroundColour(Themes.buttonFace())
        self.SetForegroundColour(Themes.text())
        setDarkTitleBar(self)


class ThemedDialog(wx.Dialog):
    """
    A wx.Dialog that automatically applies theme-aware colors and dark title bar.
    Use this as a base class for dialogs that need dark mode support.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._applyThemeColors()
    
    def _applyThemeColors(self):
        """Apply theme colors and dark title bar to this dialog."""
        from gui.utils.dark import setDarkTitleBar
        self.SetBackgroundColour(Themes.buttonFace())
        self.SetForegroundColour(Themes.text())
        setDarkTitleBar(self)
