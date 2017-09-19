from gui.contextMenu import ContextMenu
import gui.mainFrame
import gui.globalEvents as GE
# noinspection PyPackageRequirements
import wx
from service.implantSet import ImplantSets as s_ImplantSets
from service.character import Character
from service.fit import Fit
from service.settings import ContextMenuSettings


class ImplantSets(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('implantSets'):
            return False

        sIS = s_ImplantSets.getInstance()
        implantSets = sIS.getImplantSetList()

        if len(implantSets) == 0:
            return False

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

        sIS = s_ImplantSets.getInstance()
        implantSets = sIS.getImplantSetList()

        self.context = context
        if len(selection) == 1:
            self.selection = selection[0]  # dirty hack here

        self.idmap = {}

        for set in implantSets:
            id = ContextMenu.nextID()
            mitem = wx.MenuItem(rootMenu, id, set.name)
            bindmenu.Bind(wx.EVT_MENU, self.handleSelection, mitem)
            self.idmap[id] = set
            m.AppendItem(mitem)

        return m

    def handleSelection(self, event):
        set = self.idmap.get(event.Id, None)

        if set is None:
            event.Skip()
            return

        if self.context == "implantEditor":
            # we are calling from character editor, the implant source is different
            sChar = Character.getInstance()
            char = self.selection.entityEditor.getActiveEntity()

            for implant in set.implants:
                sChar.addImplant(char.ID, implant.item.ID)

            wx.PostEvent(self.selection, GE.CharChanged())
        else:
            sFit = Fit.getInstance()
            fitID = self.mainFrame.getActiveFit()
            for implant in set.implants:
                sFit.addImplant(fitID, implant.item.ID, recalc=implant == set.implants[-1])

            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


ImplantSets.register()
