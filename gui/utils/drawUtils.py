import wx
import gui.utils.colorUtils as colorUtils


def RenderGradientBar(windowColor, width, height, sFactor, eFactor, mFactor = None):

    if sFactor == 0 and eFactor == 0 and mFactor == None:
        return DrawFilledBitmap(width,height, windowColor)

    gStart = colorUtils.GetSuitableColor(windowColor, sFactor)

    if mFactor:
        gMid = colorUtils.GetSuitableColor(windowColor, mFactor)
    else:
         gMid = None

    gEnd = colorUtils.GetSuitableColor(windowColor, eFactor)

    return DrawGradientBar(width, height, gStart, gEnd, gMid)


def DrawFilledBitmap(width, height, color):
    canvas = wx.EmptyBitmap(width,height)

    mdc = wx.MemoryDC()
    mdc.SelectObject(canvas)

    mdc.SetBrush(wx.Brush(color))
    mdc.Clear()

    mdc.SelectObject(wx.NullBitmap)

    return canvas

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