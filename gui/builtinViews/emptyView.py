import wx
import gui.globalEvents as GE
import gui.chromeTabs
import gui.mainFrame
import service
from gui import bitmapLoader

class BlankPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(0, 0))
        self.bkimg = bitmapLoader.getImage("pyfa_big", "icons")
        self.bkimg = self.bkimg.AdjustChannels(1,1,1,0.1)
        self.bkbmp = wx.BitmapFromImage(self.bkimg)

        self.showLogo = False

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.parent = parent

        self.parent.Bind(gui.chromeTabs.EVT_NOTEBOOK_PAGE_CHANGED, self.pageChanged)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBk)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_RIGHT_DCLICK, self.OnRightDClick)

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=None))

    def OnRightDClick(self, event):
        self.showLogo = False if self.showLogo else True
        self.Refresh()
        event.Skip()

    def OnSize(self, event):
        self.Refresh()
        event.Skip()

    def OnEraseBk(self, event):
        pass

    def OnPaint(self, event):
        rect = self.GetRect()

        windowColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        mdc = wx.BufferedPaintDC(self)
        mdc.SetBrush(wx.Brush(windowColor))
        mdc.Clear()
        x = (rect.width - self.bkbmp.GetWidth()) / 2
        y = (rect.height - self.bkbmp.GetHeight()) / 2
        if self.showLogo:
            mdc.DrawBitmap(self.bkbmp, x, y)

    def Destroy(self):
        self.parent.Unbind(gui.chromeTabs.EVT_NOTEBOOK_PAGE_CHANGED, handler=self.pageChanged)
        wx.Panel.Destroy(self)

    def pageChanged(self, event):
        if self.parent.IsActive(self):
            fitID = None
#            sFit = service.Fit.getInstance()
#            sFit.switchFit(fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

        event.Skip()