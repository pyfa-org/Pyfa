# coding: utf-8

import wx
from logbook import Logger

pyfalog = Logger(__name__)


class PFStaticText(wx.Panel):
    def __init__(self, parent, label=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=parent.GetSize())
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, wx.ID_ANY, label, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE)
        text.Wrap(-1)
        mainSizer.Add(text, 1, wx.ALL, 10)
        self.SetSizer(mainSizer)
        self.Layout()

    @staticmethod
    def GetType():
        return -1
