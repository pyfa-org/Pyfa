# noinspection PyPackageRequirements
import wx
import gui.utils.colorUtils as colorUtils


def RenderGradientBar(windowColor, width, height, sFactor, eFactor, mFactor=None, fillRatio=2):
    if sFactor == 0 and eFactor == 0 and mFactor is None:
        return DrawFilledBitmap(width, height, windowColor)

    gStart = colorUtils.GetSuitableColor(windowColor, sFactor)

    if mFactor:
        gMid = colorUtils.GetSuitableColor(windowColor, mFactor)
    else:
        gMid = colorUtils.GetSuitableColor(windowColor, sFactor + (eFactor - sFactor) / 2)

    gEnd = colorUtils.GetSuitableColor(windowColor, eFactor)

    return DrawGradientBar(width, height, gStart, gEnd, gMid, fillRatio)


def DrawFilledBitmap(width, height, color):
    canvas = wx.EmptyBitmap(width, height)

    mdc = wx.MemoryDC()
    mdc.SelectObject(canvas)

    mdc.SetBackground(wx.Brush(color))
    mdc.Clear()

    mdc.SelectObject(wx.NullBitmap)

    return canvas


# noinspection PyPropertyAccess
def DrawGradientBar(width, height, gStart, gEnd, gMid=None, fillRatio=4):
    # we need to have dimensions to draw
    # assert width > 0 and height > 0
    canvas = wx.EmptyBitmap(width, height)

    mdc = wx.MemoryDC()
    mdc.SelectObject(canvas)

    r = wx.Rect(0, 0, width, height)
    r.height = height / fillRatio

    if gMid is None:
        gMid = gStart

    mdc.GradientFillLinear(r, gStart, gMid, wx.SOUTH)
    r.top = r.height
    r.height = height * (fillRatio - 1) / fillRatio + (1 if height % fillRatio != 0 else 0)

    mdc.GradientFillLinear(r, gMid, gEnd, wx.SOUTH)

    mdc.SelectObject(wx.NullBitmap)

    return canvas


def GetPartialText(dc, text, maxWidth, defEllipsis="..."):
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


def GetRoundBitmap(w, h, r):
    maskColor = wx.Color(0, 0, 0)
    shownColor = wx.Color(5, 5, 5)
    b = wx.EmptyBitmap(w, h)
    dc = wx.MemoryDC(b)
    dc.SetBrush(wx.Brush(maskColor))
    dc.DrawRectangle(0, 0, w, h)
    dc.SetBrush(wx.Brush(shownColor))
    dc.SetPen(wx.Pen(shownColor))
    dc.DrawRoundedRectangle(0, 0, w, h, r)
    dc.SelectObject(wx.NullBitmap)
    b.SetMaskColour(maskColor)
    return b


def GetRoundShape(w, h, r):
    return wx.RegionFromBitmap(GetRoundBitmap(w, h, r))


def CreateDropShadowBitmap(bitmap, opacity):
    img = wx.ImageFromBitmap(bitmap)
    img = img.AdjustChannels(0, 0, 0, opacity)
    return wx.BitmapFromImage(img)
