import wx

def DrawGradientBar(width, height, gStart, gEnd, gMid = None):
    canvas = wx.EmptyBitmap(width,height)

    mdc = wx.MemoryDC()
    mdc.SelectObject(canvas)

    r = wx.Rect(0, 0, width, height)
    r.height = r.height / 2

    if gMid is None:
        gMid = gStart

    mdc.GradientFillLinear(r, gStart, gEnd, wx.SOUTH)
    r.top = r.height
    mdc.GradientFillLinear(r, gMid, gEnd, wx.NORTH)

    mdc.SelectObject(wx.NullBitmap)

    return canvas