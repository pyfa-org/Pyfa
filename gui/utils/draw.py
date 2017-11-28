# noinspection PyPackageRequirements
import wx
from . import color


def RenderGradientBar(windowColor, width, height, sFactor, eFactor, mFactor=None , fillRatio=2):

    if sFactor == 0 and eFactor == 0 and mFactor is None:
        return DrawFilledBitmap(width, height, windowColor)

    gStart = color.GetSuitable(windowColor, sFactor)

    if mFactor:
        gMid = color.GetSuitable(windowColor, mFactor)
    else:
        gMid = color.GetSuitable(windowColor, sFactor + (eFactor - sFactor) / 2)

    gEnd = color.GetSuitable(windowColor, eFactor)

    return DrawGradientBar(width, height, gStart, gEnd, gMid, fillRatio)


def DrawFilledBitmap(width, height, color):
    canvas = wx.Bitmap(width, height)

    mdc = wx.MemoryDC()
    mdc.SelectObject(canvas)

    mdc.SetBackground(wx.Brush(color))
    mdc.Clear()

    mdc.SelectObject(wx.NullBitmap)

    return canvas


def DrawGradientBar(width, height, gStart, gEnd, gMid=None, fillRatio=4):
    canvas = wx.Bitmap(width, height)

    mdc = wx.MemoryDC()
    mdc.SelectObject(canvas)

    r = wx.Rect(0, 0, width, height)
    r.SetHeight(height / fillRatio)

    if gMid is None:
        gMid = gStart

    mdc.GradientFillLinear(r, gStart, gMid, wx.SOUTH)
    r.SetTop(r.GetHeight())
    r.SetHeight(height * (fillRatio - 1) / fillRatio + (1 if height % fillRatio != 0 else 0))

    mdc.GradientFillLinear(r, gMid, gEnd, wx.SOUTH)

    mdc.SelectObject(wx.NullBitmap)

    return canvas


def GetPartialText(dc, text , maxWidth, defEllipsis="..."):
        ellipsis = defEllipsis
        base_w, h = dc.GetTextExtent(ellipsis)

        lenText = len(text)
        drawntext = text
        w, dummy = dc.GetTextExtent(text)

        while lenText > 0:

            if w + base_w <= maxWidth:
                break

            w_c, h_c = dc.GetTextExtent(drawntext[-1])
            drawntext = drawntext[0:-1]
            lenText -= 1
            w -= w_c

        while len(ellipsis) > 0 and w + base_w > maxWidth:
            ellipsis = ellipsis[0:-1]
            base_w, h = dc.GetTextExtent(ellipsis)
        if len(text) > lenText:
            return drawntext + ellipsis
        else:
            return text


def CreateDropShadowBitmap(bitmap, opacity):
    img = bitmap.ConvertToImage()
    img = img.AdjustChannels(0, 0, 0, opacity)
    return wx.Bitmap(img)
