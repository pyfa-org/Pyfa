# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

# noinspection PyPackageRequirements
import wx


class PFListPane(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(1, 1),
                                   style=wx.TAB_TRAVERSAL)

        self._wList = []
        self._wCount = 0
        self.itemsHeight = 1

        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))

        self.SetVirtualSize((1, 1))
        self.SetScrollRate(0, 1)

        self.Bind(wx.EVT_SCROLLWIN_LINEUP, self.MScrollUp)
        self.Bind(wx.EVT_SCROLLWIN_LINEDOWN, self.MScrollDown)
        # self.Bind(wx.EVT_CHILD_FOCUS, self.OnChildFocus)
        # self.Bind(wx.EVT_LEFT_DOWN, self.ForceFocus)
        self.SetFocus()
        # self.Bind(wx.EVT_MOUSE_CAPTURE_CHANGED, self.ForceFocus)
        self.Bind(wx.EVT_SCROLLWIN_THUMBRELEASE, self.ForceFocus)

    def ForceFocus(self, event):
        if self.FindFocus() and self.FindFocus().Parent != self:
            self.SetFocus()
        event.Skip()

    def OnChildFocus(self, event):
        event.Skip()
        child = event.GetWindow()
        self.ScrollChildIntoView(child)

    def MScrollUp(self, event):

        posy = self.GetScrollPos(wx.VERTICAL)
        posy -= self.itemsHeight
        self.Scroll(0, posy)

        event.Skip()

    def MScrollDown(self, event):

        posy = self.GetScrollPos(wx.VERTICAL)
        posy += self.itemsHeight
        self.Scroll(0, posy)

        event.Skip()

    def ScrollChildIntoView(self, child):
        """
        Scrolls the panel such that the specified child window is in view.
        """
        sppu_x, sppu_y = self.GetScrollPixelsPerUnit()
        vs_x, vs_y = self.GetViewStart()
        cr = child.GetRect()
        clntsz = self.GetSize()
        new_vs_x, new_vs_y = -1, -1

        # is it before the left edge?
        if cr.x < 0 < sppu_x:
            new_vs_x = vs_x + (cr.x / sppu_x)

        # is it above the top?
        if cr.y < 0 < sppu_y:
            new_vs_y = vs_y + (cr.y / sppu_y)

        # For the right and bottom edges, scroll enough to show the
        # whole control if possible, but if not just scroll such that
        # the top/left edges are still visible

        # is it past the right edge ?
        if cr.right > clntsz.width and sppu_x > 0:
            diff = (cr.right - clntsz.width + 1) / sppu_x
            if cr.x - diff * sppu_x > 0:
                new_vs_x = vs_x + diff
            else:
                new_vs_x = vs_x + (cr.x / sppu_x)

        # is it below the bottom ?
        if cr.bottom > clntsz.height and sppu_y > 0:
            diff = (cr.bottom - clntsz.height + 1) / sppu_y
            if cr.y - diff * sppu_y > 0:
                new_vs_y = vs_y + diff
            else:
                new_vs_y = vs_y + (cr.y / sppu_y)

        # if we need to adjust
        if new_vs_x != -1 or new_vs_y != -1:
            self.Scroll(new_vs_x, new_vs_y)

    def AddWidget(self, widget):
        widget.Reparent(self)
        self._wList.append(widget)
        self._wCount += 1

    def GetWidgetList(self):
        return self._wList

    # Override this method if needed ( return False by default if we do not want to scroll to selected widget)
    def IsWidgetSelectedByContext(self, widget):
        return False

    def RefreshList(self, doRefresh=False, doFocus=False):
        maxy = 0

        selected = None
        for i in xrange(len(self._wList)):
            iwidth, iheight = self._wList[i].GetSize()
            xa, ya = self.CalcScrolledPosition((0, maxy))
            self._wList[i].SetPosition((xa, ya))
            if self.IsWidgetSelectedByContext(i):
                selected = self._wList[i]
            maxy += iheight

        self.SetVirtualSize((1, maxy))
        cwidth, cheight = self.GetVirtualSize()

        if selected:
            self.ScrollChildIntoView(selected)
            # selected.SetFocus()
        elif doFocus:
            self.SetFocus()

        for i in xrange(len(self._wList)):
            iwidth, iheight = self._wList[i].GetSize()
            self._wList[i].SetSize((cwidth, iheight))
            if doRefresh is True:
                self._wList[i].Refresh()
            self.itemsHeight = max(self.itemsHeight, iheight - 1)

    def RemoveWidget(self, child):
        child.Destroy()
        self._wList.remove(child)

    def RemoveAllChildren(self):
        for widget in self._wList:
            widget.Destroy()

        self._wList = []
