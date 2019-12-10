# noinspection PyPackageRequirements
import wx

from gui.contextMenu import ContextMenuUnconditional
from service.implantSet import ImplantSets as s_ImplantSets


class ImplantSetAdd(ContextMenuUnconditional):

    def display(self, callingWindow, srcContext):

        sIS = s_ImplantSets.getInstance()
        implantSets = sIS.getImplantSetList()

        if len(implantSets) == 0:
            return False

        return srcContext in ("implantSetAdd", "implantEditor")

    def getText(self, callingWindow, itmContext):
        return "Add As New Implant Set"

    def activate(self, callingWindow, fullContext, i):
        sIS = s_ImplantSets.getInstance()
        implantSets = sIS.getImplantSetList()
        callingWindow.mainFrame.OnShowImplantSetEditor(None, implantSets)


ImplantSetAdd.register()
