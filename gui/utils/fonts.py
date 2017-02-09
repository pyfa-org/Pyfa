"""
Font file to handle the differences in font calculations between
different wxPython versions
"""

# noinspection PyPackageRequirements
import wx

if 'wxMac' in wx.PlatformInfo:
    sizes = (10, 11, 12)
else:
    sizes = (7, 8, 9)

SMALL, NORMAL, BIG = sizes
