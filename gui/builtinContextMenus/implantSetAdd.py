# noinspection PyPackageRequirements
import wx

import gui.fitCommands as cmd
import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.character import Character
from service.implantSet import ImplantSets as s_ImplantSets


class AddImplantSet(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):

        sIS = s_ImplantSets.getInstance()
        implantSets = sIS.getImplantSetList()

        if len(implantSets) == 0:
            return False
        return srcContext in ("implantView", "implantEditor")

    def getText(self, callingWindow, itmContext):
        return "Add Implant Set"

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        m = wx.Menu()
        bindmenu = rootMenu if "wxMSW" in wx.PlatformInfo else m

        sIS = s_ImplantSets.getInstance()
        implantSets = sIS.getImplantSetList()

        self.context = context
        self.callingWindow = callingWindow

        self.idmap = {}

        for set in sorted(implantSets, key=lambda i: i.name):
            id = ContextMenuUnconditional.nextID()
            mitem = wx.MenuItem(rootMenu, id, set.name)
            bindmenu.Bind(wx.EVT_MENU, self.handleSelection, mitem)
            self.idmap[id] = set
            m.Append(mitem)

        return m

    def handleSelection(self, event):
        set = self.idmap.get(event.Id, None)

        if set is None:
            event.Skip()
            return

        if self.context == "implantEditor":
            charEditor = self.callingWindow.Parent.Parent
            # we are calling from character editor, the implant source is different
            sChar = Character.getInstance()
            char = charEditor.entityEditor.getActiveEntity()

            for implant in set.implants:
                sChar.addImplant(char.ID, implant.item.ID)

            wx.PostEvent(charEditor, GE.CharChanged())
        else:
            self.mainFrame.command.Submit(cmd.GuiAddImplantSetCommand(
                fitID=self.mainFrame.getActiveFit(),
                itemIDs=[i.itemID for i in set.implants]))


AddImplantSet.register()
