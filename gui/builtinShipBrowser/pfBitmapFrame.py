import wx


class PFBitmapFrame(wx.Frame):
    def __init__(self, parent, pos, bitmap):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=pos, size=wx.DefaultSize,
                          style=wx.NO_BORDER | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)
        img = bitmap.ConvertToImage()
        img = img.ConvertToGreyscale()
        bitmap = wx.BitmapFromImage(img)
        self.bitmap = bitmap
        self.SetSize((bitmap.GetWidth(), bitmap.GetHeight()))
        self.Bind(wx.EVT_PAINT, self.OnWindowPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnWindowEraseBk)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        self.timer = wx.Timer(self, wx.ID_ANY)
        self.direction = 1
        self.transp = 0
        self.SetSize((bitmap.GetWidth(), bitmap.GetHeight()))

        self.SetTransparent(0)
        self.Refresh()

    def OnTimer(self, event):
        self.transp += 20 * self.direction
        if self.transp > 200:
            self.transp = 200
            self.timer.Stop()
        if self.transp < 0:
            self.transp = 0
            self.timer.Stop()
            wx.Frame.Show(self, False)
            self.Destroy()
            return
        self.SetTransparent(self.transp)

    def Show(self, showWnd=True):
        if showWnd:
            wx.Frame.Show(self, showWnd)
            self.Parent.SetFocus()
            self.direction = 1
            self.timer.Start(5)
        else:
            self.direction = -1
            self.timer.Start(5)

    def OnWindowEraseBk(self, event):
        pass

    def OnWindowPaint(self, event):
        rect = self.GetRect()
        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)
        mdc.DrawBitmap(self.bitmap, 0, 0)
        mdc.SetPen(wx.Pen("#000000", width=1))
        mdc.SetBrush(wx.TRANSPARENT_BRUSH)
        mdc.DrawRectangle(0, 0, rect.width, rect.height)
