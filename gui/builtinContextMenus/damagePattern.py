from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
import gui.globalEvents as GE
import wx
from gui import bitmapLoader

class DamagePattern(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        return srcContext in ("resistancesViewFull",) and self.mainFrame.getActiveFit() is not None

    def getText(self, itmContext, selection):
        sDP = service.DamagePattern.getInstance()
        self.patterns = sDP.getDamagePatternList()
        self.patterns.sort( key=lambda p: (p.name not in ["Uniform",
                                                "Selected Ammo"], p.name) )

        self.patternIds = {}
        self.subMenus = {}
        self.singles =  []

        # iterate and separate damage patterns based on "[Parent] Child"
        for pattern in self.patterns:
            start, end = pattern.name.find('['), pattern.name.find(']')
            if start is not -1 and end is not -1:
                currBase = pattern.name[start+1:end]
                # set helper attr
                setattr(pattern, "_name", pattern.name[end+1:].strip())
                if currBase not in self.subMenus:
                    self.subMenus[currBase] = []
                self.subMenus[currBase].append(pattern)
            else:
                self.singles.append(pattern)

        # return list of names, with singles first followed by submenu names
        self.m = map(lambda p: p.name, self.singles) + self.subMenus.keys()
        return self.m

    def handlePatternSwitch(self, event):
        pattern = self.patternIds.get(event.Id, False)
        if pattern is False:
            event.Skip()
            return

        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.setDamagePattern(fitID, pattern)
        setattr(self.mainFrame,"_activeDmgPattern", pattern)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def addPattern(self, menu, pattern):
        id = wx.NewId()
        name = getattr(pattern, "_name", pattern.name) if pattern is not None else "No Profile"

        self.patternIds[id] = pattern
        item = wx.MenuItem(menu, id, name)
        menu.Bind(wx.EVT_MENU, self.handlePatternSwitch, item)

        # set pattern attr to menu item
        item.pattern = pattern

        # determine active pattern
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        f = sFit.getFit(fitID)
        dp = f.damagePattern

        if dp == pattern:
            bitmap = bitmapLoader.getBitmap("state_active_small", "icons")
            item.SetBitmap(bitmap)
        return item

    def getSubMenu(self, context, selection, menu, i, id):
        menu.Bind(wx.EVT_MENU, self.handlePatternSwitch)  # this bit is required for some reason

        if self.m[i] not in self.subMenus:
            # if we're trying to get submenu to something that shouldn't have one,
            # redirect event of the item to handlePatternSwitch and put pattern in
            # our patternIds mapping, then return None for no submenu
            self.patternIds[id] = self.singles[i]
            menu.Bind(wx.EVT_MENU, self.handlePatternSwitch, id=id)
            return None

        sub = wx.Menu()
        sub.Bind(wx.EVT_MENU, self.handlePatternSwitch)

        # Items that have a parent
        for pattern in self.subMenus[self.m[i]]:
            sub.AppendItem(self.addPattern(sub, pattern))

        return sub

DamagePattern.register()
