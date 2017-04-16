# noinspection PyPackageRequirements
import wx


def toClipboard(text):
    clip = wx.TheClipboard
    clip.Open()
    data = wx.TextDataObject(text)
    clip.SetData(data)
    clip.Close()


def fromClipboard():
    clip = wx.TheClipboard
    clip.Open()
    data = wx.TextDataObject("")
    if clip.GetData(data):
        clip.Close()
        return data.GetText()
    else:
        clip.Close()
        return None
