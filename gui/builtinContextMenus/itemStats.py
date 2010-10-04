from gui.contextMenu import ContextMenu

class ItemStats(ContextMenu):
    def __init__(self):
        pass

    def display(self, context):
        return True

    def getText(self, context):
        return "Item stats"

    def activate(self, context):
        pass

ItemStats.register()