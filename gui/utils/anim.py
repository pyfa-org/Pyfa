# noinspection PyPackageRequirements
import wx
import gui.utils.color as colorUtils


class LoadAnimation(wx.Window):
    def __init__(self, parent, id=wx.ID_ANY, label="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.Window.__init__(self, parent, id, pos=pos, size=size, style=style)

        self.label = label

        self.animTimerId = wx.NewId()
        self.animTimer = wx.Timer(self, self.animTimerId)
        self.animTimerPeriod = 50

        self.animCount = 0
        self.animDir = 1
        self.bars = 10
        self.padding = 2

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.animTimer.Start(self.animTimerPeriod)

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

    def Play(self):
        if self.animTimer.IsRunning():
            self.animTimer.Stop()
        self.animCount = 0
        self.animTimer.Start(self.animTimerPeriod)

    def Stop(self):
        if self.animTimer.IsRunning():
            self.animTimer.Stop()

    def OnTimer(self, event):
        self.animCount += self.animDir

        if self.animCount >= self.bars:
            self.animCount = self.bars - 1
            self.animDir = -1

        if self.animCount < 0:
            self.animCount = 0
            self.animDir = 1

        self.Refresh()

    def OnEraseBackground(self, event):
        pass

    def OnPaint(self, event):
        rect = self.GetClientRect()
        dc = wx.AutoBufferedPaintDC(self)
        windowColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        dc.SetBackground(wx.Brush(windowColor))
        dc.Clear()

        barColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
        shadeColor = colorUtils.GetSuitable(barColor, 0.75)

        barWidth = rect.width / self.bars
        barHeight = rect.height - self.padding * 2

        x = self.padding

        for bar in range(self.bars):
            if bar != self.animCount:
                dc.SetPen(wx.Pen(shadeColor))
                dc.SetBrush(wx.Brush(shadeColor))
                bh = barHeight
                y = self.padding
            else:
                barColor = colorUtils.GetSuitable(barColor, float(self.animCount / 2) / 10)
                dc.SetPen(wx.Pen(barColor))
                dc.SetBrush(wx.Brush(barColor))
                bh = rect.height
                y = 0

            dc.DrawRectangle(x, y, barWidth, bh)
            x += barWidth

        textColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
        dc.SetTextForeground(textColor)
        dc.DrawLabel(self.label, rect, wx.ALIGN_CENTER)


class WaitDialog(wx.Dialog):
    def __init__(self, parent, title="Processing"):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=title, size=(300, 30),
                           style=wx.NO_BORDER)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.progress = LoadAnimation(self, label=title, size=(300, 30))
        mainSizer.Add(self.progress, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(mainSizer)
        self.Layout()
        self.CenterOnParent()
