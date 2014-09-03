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
        name = pattern.name if pattern is not None else "No Profile"
        self.patternIds[id] = pattern
        if currBase:
            item = wx.MenuItem(menu, id, currBase)
        else:
            item = wx.MenuItem(menu, id, name)

        item.pattern = pattern
        return item

    def addSeperator(self, m, text):
        id = wx.NewId()
        m.Append(id, u'─ %s ─' % text)
        m.Enable(id, False)

    def getSubMenu(self, context, selection, menu, i):
        self.context = context
        menu.Bind(wx.EVT_MENU, self.handleResistSwitch)
        m = wx.Menu()
        m.Bind(wx.EVT_MENU, self.handleResistSwitch)
        self.patternIds = {}

        # @todo: this whole thing is a mess, please fix
        # Maybe look into processing resists into a dict and iterating through
        # dict to make submenus instead of this shitty logic
        items = []
        nameBase = None
        sub = None

        m.AppendItem(self.addPattern(m, None))  # Add reset
        m.AppendSeparator()
        for pattern  in self.patterns:
            start, end = pattern.name.find('['), pattern.name.find(']')
            if start is not -1 and end is not -1:
                currBase = pattern.name[start+1:end]
            else:
                currBase = None

            if nameBase is None or nameBase != currBase:
                sub = None
                base = pattern
                nameBase = currBase
                item = self.addPattern(m, pattern, currBase)
                items.append(item)
            else:
                if sub is None:
                    sub = wx.Menu()
                    sub.Bind(wx.EVT_MENU, self.handleResistSwitch)
                    item.SetSubMenu(sub)
                    sub.AppendItem(self.addPattern(sub, base))

                sub.AppendItem(self.addPattern(sub, pattern))
        for item in items:
            m.AppendItem(item)
        return m

TargetResists.register()
