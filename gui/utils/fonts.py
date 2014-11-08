'''
Font file to handle the differences in font calculations between
different wxPython versions
'''

import wx

if 'wxMSW' in wx.PlatformInfo and wx.VERSION < (2,9):
    SMALL  = (0,12)
    NORMAL = (0,14)
    BIG    = (0,15)
else:
    SMALL  = (0,10)
    NORMAL = (0,11)
    BIG    = (0,12)