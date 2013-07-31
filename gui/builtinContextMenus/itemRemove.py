from gui.contextMenu import ContextMenu
import gui.mainFrame

class ItemRemove(ContextMenu):
    def __init__(self, parent):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.parent = parent

    def display(self, srcContext, selection):
        return srcContext in ("fittingModule", "droneItem", "implantItem", "boosterItem")

    def getText(self, itmContext, selection):
        return "Remove {0}".format(itmContext if itmContext is not None else "Item")

    def activate(self, fullContext, selection, i):
        srcContext = fullContext[0]
        if srcContext == "fittingModule":
            for module in selection:
                if module is not None: self.parent.removeModule(module)
        elif srcContext == "droneItem":
            for drone in selection:
                if drone is not None: self.parent.removeDrone(drone)
        elif srcContext == "implantItem":
            for implant in selection:
                if implant is not None: self.parent.removeImplant(implant)
        elif srcContext == "boosterItem":
            for booster in selection:
                if booster is not None: self.parent.removeBooster(booster)


ItemRemove.register()
