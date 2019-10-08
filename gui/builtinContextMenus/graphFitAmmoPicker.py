from gui.contextMenu import ContextMenuSingle


class GraphFitAmmoPicker(ContextMenuSingle):

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext != 'graphFitList':
            return False
        if mainItem is None or not mainItem.isFit:
            return False
        return True

    def getText(self, callingWindow, itmContext, mainItem):
        return 'Duplicate Fit with Ammo...'

    def activate(self, callingWindow, fullContext, mainItem, i):
        pass


GraphFitAmmoPicker.register()
