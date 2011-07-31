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

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=None))

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