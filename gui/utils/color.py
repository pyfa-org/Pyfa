# noinspection PyPackageRequirements
import wx


def Brighten(color, factor):
    """ Brightens a Color using a factor between 0 and 1"""
    r, g, b, a = color

    factor = min(max(factor, 0), 1)

    r += (255 - r) * factor
    b += (255 - b) * factor
    g += (255 - g) * factor

    return wx.Colour(r, g, b, a)


def Darken(color, factor):
    """ Darkens a Color using a factor between 0 and 1"""
    r, g, b, a = color

    factor = min(max(factor, 0), 1)
    factor = 1 - factor

    r *= factor
    g *= factor
    b *= factor

    r = min(max(r, 0), 255)
    b = min(max(b, 0), 255)
    g = min(max(g, 0), 255)

    return wx.Colour(r, g, b, a)


def _getBrightness(color):
    """
    Calculates brightness of color
    http://stackoverflow.com/a/596243/788054
    """
    r, g, b, a = color
    return 0.299 * r + 0.587 * g + 0.114 * b


def GetSuitable(color, factor: [0, 1]):
    """
    Calculates a suitable color based on original color (wx.Colour), its
    brightness, and a factor (darken/brighten by factor depending on
    calculated brightness)
    """

    brightness = _getBrightness(color)

    if brightness > 129:
        return Darken(color, factor)
    else:
        return Brighten(color, factor)


def CalculateTransition(s_color, e_color, delta):
    """
    Calculates the color between a given start and end color using a delta
    value between 0 and 1
    """

    sR, sG, sB, sA = s_color
    eR, eG, eB, eA = e_color

    tR = sR + (eR - sR) * delta
    tG = sG + (eG - sG) * delta
    tB = sB + (eB - sB) * delta

    return wx.Colour(tR, tG, tB, (sA + eA) / 2)
