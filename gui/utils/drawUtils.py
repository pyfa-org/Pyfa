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

    mdc.SetBackground(wx.Brush(color))
    mdc.Clear()

    mdc.SelectObject(wx.NullBitmap)

    return canvas

def DrawGradientBar(width, height, gStart, gEnd, gMid = None):
    canvas = wx.EmptyBitmap(width,height)

    fillRatio = 4
    mdc = wx.MemoryDC()
    mdc.SelectObject(canvas)

    r = wx.Rect(0, 0, width, height)
    r.height = height / fillRatio

    if gMid is None:
        gMid = gStart

    mdc.GradientFillLinear(r, gStart, gEnd, wx.SOUTH)
    r.top = r.height
    r.height = height * (fillRatio - 1)/fillRatio + (1 if height % fillRatio != 0 else 0)

    mdc.GradientFillLinear(r, gMid, gEnd, wx.NORTH)

    mdc.SelectObject(wx.NullBitmap)

    return canvas


def GetPartialText(dc, text , maxWidth):
        ellipsis = "..."
        base_w, h = dc.GetTextExtent(ellipsis)

        lenText = len(text)
        drawntext = text
        w, dummy = dc.GetTextExtent(text)

        while lenText > 1:

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
