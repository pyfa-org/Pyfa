# noinspection PyPackageRequirements
import wx
import math


def BrightenColor(color, factor):
    # Brightens a color (wx.Colour), factor = [0,1]

    r, g, b = color
    a = color.Alpha()

    factor = min(max(factor, 0), 1)

    r += (255 - r) * factor
    b += (255 - b) * factor
    g += (255 - g) * factor

    return wx.Colour(r, g, b, a)


def DarkenColor(color, factor):
    # Darkens a color (wx.Colour), factor = [0, 1]

    bkR, bkG, bkB = color

    alpha = color.Alpha()

    factor = min(max(factor, 0), 1)
    factor = 1 - factor

    r = float(bkR * factor)
    g = float(bkG * factor)
    b = float(bkB * factor)

    r = min(max(r, 0), 255)
    b = min(max(b, 0), 255)
    g = min(max(g, 0), 255)

    return wx.Colour(r, g, b, alpha)


def GetBrightnessO1(color):
    # Calculates the brightness of a color, different options

    r, g, b = color
    return 0.299 * r + 0.587 * g + 0.114 * b


def GetBrightnessO2(color):
    r, g, b = color
    return math.sqrt(0.241 * r * r + 0.691 * g * g + 0.068 * b * b)


def GetSuitableColor(color, factor):
    # Calculates a suitable color based on original color (wx.Colour), its brightness, a factor=[0,1] (darken/brighten by factor depending on calculated brightness)

    brightness = GetBrightnessO1(color)

    if brightness > 129:
        return DarkenColor(color, factor)
    else:
        return BrightenColor(color, factor)


def CalculateTransitionColor(startColor, endColor, delta):
    """
    Calculates the color between a given start and end colors, delta = [0,1]
    Colors are wx.Colour objects
    """

    sR, sG, sB = startColor
    eR, eG, eB = endColor

    alphaS = startColor.Alpha()
    alphaE = endColor.Alpha()

    tR = sR + (eR - sR) * delta
    tG = sG + (eG - sG) * delta
    tB = sB + (eB - sB) * delta

    return wx.Colour(tR, tG, tB, (alphaS + alphaE) / 2)
