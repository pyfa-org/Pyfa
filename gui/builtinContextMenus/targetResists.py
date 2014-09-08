# -*- coding: utf-8 -*-

from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
import gui.globalEvents as GE
import wx
from gui import bitmapLoader

class TargetResists(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        if self.mainFrame.getActiveFit() is None or srcContext not in ("firepowerViewFull",):
            return False

        sTR = service.TargetResists.getInstance()
        self.patterns = sTR.getTargetResistsList()
        self.patterns.sort( key=lambda p: (p.name in ["None"], p.name) )

        return len(self.patterns) > 0

    def getText(self, itmContext, selection):
        return "Target Resists"

    def activate(self, fullContext, selection, i):
        pass

    def handleResistSwitch(self, event):
        pattern = self.patternIds.get(event.Id, False)
        if pattern is False:
            event.Skip()
            return

        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.setTargetResists(fitID, pattern)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def addPattern(self, menu, pattern, currBase = None):
        id = wx.NewId()
        name = getattr(pattern, "_name", pattern.name) if pattern is not None else "No Profile"

        self.patternIds[id] = pattern
        item = wx.MenuItem(menu, id, name)
        # set pattern attr to menu item
        item.pattern = pattern

        # determine active pattern
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        f = sFit.getFit(fitID)
        tr = f.targetResists

        if tr == pattern:
            bitmap = bitmapLoader.getBitmap("state_active_small", "icons")
            item.SetBitmap(bitmap)
        return item

    def addSeperator(self, m, text):
        id = wx.NewId()
        m.Append(id, u'─ %s ─' % text)
        m.Enable(id, False)

    def getSubMenu(self, context, selection, menu, i, id):
        self.context = context
        menu.Bind(wx.EVT_MENU, self.handleResistSwitch)
        m = wx.Menu()
        m.Bind(wx.EVT_MENU, self.handleResistSwitch)
        self.patternIds = {}

        self.subMenus = {}
        self.singles  = []

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

        m.AppendItem(self.addPattern(m, None))  # Add reset
        m.AppendSeparator()

        # Single items, no parent
        for pattern in self.singles:
            m.AppendItem(self.addPattern(m, pattern))

        # Items that have a parent
        for menuName, patterns in self.subMenus.items():
            # Create parent item for root menu that is simply name of parent
            item = wx.MenuItem(menu, wx.NewId(), menuName)

            # Create menu for child items
            sub = wx.Menu()
            sub.Bind(wx.EVT_MENU, self.handleResistSwitch)

            # Apply child menu to parent item
            item.SetSubMenu(sub)

            # Append child items to child menu
            for pattern in patterns:
                sub.AppendItem(self.addPattern(sub, pattern))
            m.AppendItem(item)  #finally, append parent item to root menu

        return m

TargetResists.register()
