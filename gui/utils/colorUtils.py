import wx

#Brightens a color (wx.Colour), factor = [0,1]
def BrightenColor(color, factor):

    r,g,b = color
    a = color.Alpha()

    factor = min(max(factor, 0), 1)

    r+=(255-r)*factor
    b+=(255-b)*factor
    g+=(255-g)*factor

    return wx.Colour(r,g,b,a)

#Darkens a color (wx.Colour), factor = [0, 1]
def DarkenColor(color, factor):
    bkR ,bkG , bkB = color
    alpha = color.Alpha()
    factor = 1 - factor
    r = float(bkR * factor)
    g = float(bkG * factor)
    b = float(bkB * factor)

    r = min(max(r,0),255)
    b = min(max(b,0),255)
    g = min(max(g,0),255)

    return wx.Colour(r, g, b, alpha)

#Calculates the color between a given start and end colors, delta = [0,1]
#Colors are wx.Colour objects

def CalculateTransitionColor(startColor, endColor, delta):
    sR,sG,sB = startColor
    eR,eG,eB = endColor

    alphaS = startColor.Alpha()
    alphaE = endColor.Alpha()

    tR = sR + (eR - sR) *  delta
    tG = sG + (eG - sG) *  delta
    tB = sB + (eB - sB) *  delta

    return wx.Colour(tR, tG, tB, (alphaS + alphaE)/2)