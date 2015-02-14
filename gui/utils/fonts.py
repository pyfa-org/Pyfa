import wx

if 'wxMac' in wx.PlatformInfo:
    sizes = (10, 11, 12)
else:
    sizes = (7, 8, 9)

SMALL, NORMAL, BIG = sizes
