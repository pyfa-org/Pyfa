from gui.builtinShipBrowser.pfListPane import PFListPane
import gui.mainFrame
import gui.utils.animUtils as animUtils


class PFWidgetsContainer(PFListPane):
    def __init__(self, parent):
        PFListPane.__init__(self, parent)

        self.anim = animUtils.LoadAnimation(self, label="", size=(100, 12))
        self.anim.Stop()
        self.anim.Show(False)

    def ShowLoading(self, mode=True):
        if mode:
            aweight, aheight = self.anim.GetSize()
            cweight, cheight = self.GetSize()
            ax = (cweight - aweight) / 2
            ay = (cheight - aheight) / 2
            self.anim.SetPosition((ax, ay))
            self.anim.Show()
            self.anim.Play()
        else:
            self.anim.Stop()
            self.anim.Show(False)

    def IsWidgetSelectedByContext(self, widget):
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        stage = self.Parent.GetActiveStage()
        fit = mainFrame.getActiveFit()
        if stage == 3 or stage == 4:
            if self._wList[widget].GetType() == 3:
                if fit == self._wList[widget].fitID:
                    return True
        return False
