import wx
from gui_service.character import Character
from gui_service.implantSet import ImplantSets as ImplantSet

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenu
from gui_service.fit import Fit


class ImplantSets(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        return srcContext in ("implantView", "implantEditor")

    def getText(self, itmContext, selection):
        return "Add Implant Set"

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        """
        A note on the selection here: Most context menus act on a fit, so it's easy enough to get the active fit from
        the MainFrame instance. There's never been a reason to get info from another window, so there's not common
        way of doing this. However, we use this context menu within the Character Editor to apply implant sets to a
        character, so we need to access the character editor.

        It is for these reasons that I hijack the selection parameter when calling the menu and pass a pointer to the
        Character Editor. This way we can use it to get current editing character ID and apply the implants.

        It would probably be better to have a function on the MainFrame to get the currently open Character Editor (as
        we do with the item stats window). Eventually... Until then, this long ass note will remain to remind me why
        stupid shit like this is even happening.
        """

        m = wx.Menu()
        bindmenu = rootMenu if "wxMSW" in wx.PlatformInfo else m

        sIS = ImplantSet.getInstance()
        implantSets = sIS.getImplantSetList()

        self.context = context
        if len(selection) == 1:
            self.selection = selection[0]  # dirty hack here

        self.idmap = {}

        for implantSet in implantSets:
            id_ = ContextMenu.nextID()
            mitem = wx.MenuItem(rootMenu, id_, implantSet.name)
            bindmenu.Bind(wx.EVT_MENU, self.handleSelection, mitem)
            self.idmap[id_] = implantSet
            m.AppendItem(mitem)

        return m

    def handleSelection(self, event):
        implant_set = self.idmap.get(event.Id, None)

        if implant_set is None:
            event.Skip()
            return

        if self.context == "implantEditor":
            # we are calling from character editor, the implant source is different
            sChar = Character.getInstance()
            charID = self.selection.getActiveCharacter()

            for implant in implant_set.implants:
                sChar.addImplant(charID, implant.item.ID)

            wx.PostEvent(self.selection, GE.CharChanged())
        else:
            sFit = Fit.getInstance()
            fitID = self.mainFrame.getActiveFit()
            for implant in implant_set.implants:
                sFit.addImplant(fitID, implant.item.ID, recalc=implant == implant_set.implants[-1])

            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


ImplantSets.register()
