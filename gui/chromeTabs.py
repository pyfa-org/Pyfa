# =============================================================================
# Copyright (C) 2010 Darriele
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
# noinspection PyPackageRequirements
import wx.lib.newevent
import gui.utils.colorUtils as colorUtils
import gui.utils.drawUtils as drawUtils
import gui.utils.fonts as fonts
from gui.bitmapLoader import BitmapLoader
from logbook import Logger
from service.fit import Fit

pyfalog = Logger(__name__)

_PageChanging, EVT_NOTEBOOK_PAGE_CHANGING = wx.lib.newevent.NewEvent()
_PageChanged, EVT_NOTEBOOK_PAGE_CHANGED = wx.lib.newevent.NewEvent()
_PageAdding, EVT_NOTEBOOK_PAGE_ADDING = wx.lib.newevent.NewEvent()
_PageClosing, EVT_NOTEBOOK_PAGE_CLOSING = wx.lib.newevent.NewEvent()
PageAdded, EVT_NOTEBOOK_PAGE_ADDED = wx.lib.newevent.NewEvent()
PageClosed, EVT_NOTEBOOK_PAGE_CLOSED = wx.lib.newevent.NewEvent()


class VetoAble(object):
    def __init__(self):
        self.__vetoed = False

    def Veto(self):
        self.__vetoed = True

    def isVetoed(self):
        return self.__vetoed


class NotebookTabChangeEvent(object):
    def __init__(self, old, new):
        self.__old = old
        self.__new = new

    def GetOldSelection(self):
        return self.__old

    def GetSelection(self):
        return self.__new

    OldSelection = property(GetOldSelection)
    Selection = property(GetSelection)


class PageChanging(_PageChanging, NotebookTabChangeEvent, VetoAble):
    def __init__(self, old, new):
        NotebookTabChangeEvent.__init__(self, old, new)
        _PageChanging.__init__(self)
        VetoAble.__init__(self)


class PageChanged(_PageChanged, NotebookTabChangeEvent):
    def __init__(self, old, new):
        NotebookTabChangeEvent.__init__(self, old, new)
        _PageChanged.__init__(self)


class PageClosing(_PageClosing, VetoAble):
    def __init__(self, i):
        self.__index = i
        _PageClosing.__init__(self)
        VetoAble.__init__(self)
        self.Selection = property(self.GetSelection)

    def GetSelection(self):
        return self.__index


class PageAdding(_PageAdding, VetoAble):
    def __init__(self):
        _PageAdding.__init__(self)
        VetoAble.__init__(self)


class PFNotebook(wx.Panel):
    def __init__(self, parent, canAdd=True):
        """
        Instance of Pyfa Notebook. Initializes general layout, includes methods
        for setting current page, replacing pages, etc

        parent - wx parent element
        canAdd - True if tabs be deleted and added, passed directly to
                 PFTabsContainer
        """

        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(-1, -1))

        self.pages = []
        self.activePage = None

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        tabsSizer = wx.BoxSizer(wx.VERTICAL)
        self.tabsContainer = PFTabsContainer(self, canAdd=canAdd)
        tabsSizer.Add(self.tabsContainer, 0, wx.EXPAND)

        style = wx.DOUBLE_BORDER if 'wxMSW' in wx.PlatformInfo else wx.SIMPLE_BORDER

        contentSizer = wx.BoxSizer(wx.VERTICAL)
        self.pageContainer = wx.Panel(self, style=style)
        self.pageContainer.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        contentSizer.Add(self.pageContainer, 1, wx.EXPAND, 5)

        mainSizer.Add(tabsSizer, 0, wx.EXPAND, 5)
        mainSizer.Add(contentSizer, 1, wx.EXPAND | wx.BOTTOM, 2)

        self.SetSizer(mainSizer)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Layout()

    def GetPage(self, i):
        return self.pages[i]

    def SetPage(self, i, page):
        if i >= len(self.pages) or i is None or page is None:
            return

        oldPage = self.pages[i]
        self.pages[i] = page
        if oldPage == self.activePage:
            oldPage.Destroy()
            self.activePage = page
        else:
            oldPage.Destroy()

        page.Reparent(self.pageContainer)

        if self.activePage == page:
            self.ShowActive()

    @staticmethod
    def GetBorders():
        """Gets border widths to better determine page size in ShowActive()"""

        bx = wx.SystemSettings_GetMetric(wx.SYS_BORDER_X)
        by = wx.SystemSettings_GetMetric(wx.SYS_BORDER_Y)

        if bx < 0:
            bx = 1
        if by < 0:
            by = 1

        return bx, by

    def ReplaceActivePage(self, page):
        self.SetPage(self.GetSelection(), page)

    def GetSelectedPage(self):
        return self.activePage

    def GetPageIndex(self, page):
        return self.pages.index(page) if page in self.pages else None

    def GetSelection(self):
        return self.GetPageIndex(self.activePage)

    def GetCurrentPage(self):
        return self.activePage

    def GetPageCount(self):
        return len(self.pages)

    def NextPage(self):
        """Used with keyboard shortcut for next page navigation"""
        cpage = self.GetSelection()

        if cpage is None:
            return

        if cpage < self.GetPageCount() - 1:
            self.SetSelection(cpage + 1)
            npage = cpage + 1
        else:
            self.SetSelection(0)
            npage = 0

        wx.PostEvent(self, PageChanged(cpage, npage))

    def PrevPage(self):
        """Used with keyboard shortcut for previous page navigation"""
        cpage = self.GetSelection()

        if cpage is None:
            return

        if cpage > 0:
            self.SetSelection(cpage - 1)
            npage = cpage - 1
        else:
            self.SetSelection(self.GetPageCount() - 1)
            npage = self.GetPageCount() - 1

        wx.PostEvent(self, PageChanged(cpage, npage))

    def AddPage(self, tabWnd=None, tabTitle="Empty Tab", tabImage=None, showClose=True):
        if self.activePage:
            self.activePage.Hide()

        if not tabWnd:
            tabWnd = wx.Panel(self)

        tabWnd.Reparent(self.pageContainer)

        self.pageContainer.Layout()

        self.pages.append(tabWnd)
        self.tabsContainer.AddTab(tabTitle, tabImage, showClose)

        self.activePage = tabWnd
        self.ShowActive(True)

    def DisablePage(self, page, toggle):
        idx = self.GetPageIndex(page)

        if toggle and page == self.activePage:
            try:
                # Set page to the first non-disabled page
                self.SetSelection(next(i for i, _ in enumerate(self.pages) if not self.tabsContainer.tabs[i].disabled))
            except StopIteration:
                self.SetSelection(0)

        self.tabsContainer.DisableTab(idx, toggle)

    def SetSelection(self, page):
        oldsel = self.GetSelection()
        if oldsel != page:
            self.activePage.Hide()
            self.activePage = self.pages[page]
            self.tabsContainer.SetSelected(page)
            self.ShowActive()

    def DeletePage(self, n, internal=False):
        """
        Deletes page.

        n -- index of page to be deleted
        internal -- True if we're deleting the page from the PFTabsContainer
        """
        page = self.pages[n]
        self.pages.remove(page)
        page.Destroy()

        if not internal:
            # If we're not deleting from the tab, delete the tab
            # (deleting from the tab automatically deletes itself)
            self.tabsContainer.DeleteTab(n, True)

        sel = self.tabsContainer.GetSelected()
        if sel is not None:
            self.activePage = self.pages[sel]
            self.ShowActive()
            wx.PostEvent(self, PageChanged(-1, sel))
        else:
            self.activePage = None

    def SwitchPages(self, src, dest):
        self.pages[src], self.pages[dest] = self.pages[dest], self.pages[src]

    def ShowActive(self, resizeOnly=False):
        """
        Sets the size of the page and shows. The sizing logic adjusts for some
        minor sizing errors (scrollbars going beyond bounds)

        resizeOnly -- if we are not interested in showing the page, only setting
                      the size

        @todo: is resizeOnly still needed? Was introduced with 8b8b97 in mid 2011
        to fix a resizing bug with blank pages, cannot reproduce 13Sept2014
        """

        ww, wh = self.pageContainer.GetSize()
        bx, by = self.GetBorders()
        ww -= bx * 4
        wh -= by * 4
        self.activePage.SetSize((max(ww, -1), max(wh, -1)))
        self.activePage.SetPosition((0, 0))

        if not resizeOnly:
            self.activePage.Show()

        self.Layout()

    def IsActive(self, page):
        return self.activePage == page

    def SetPageTitle(self, i, text, refresh=True):
        tab = self.tabsContainer.tabs[i]
        tab.text = text
        if refresh:
            self.tabsContainer.AdjustTabsSize()
            self.Refresh()

    def SetPageIcon(self, i, icon, refresh=True):
        tab = self.tabsContainer.tabs[i]
        tab.tabImg = icon
        if refresh:
            self.tabsContainer.AdjustTabsSize()
            self.Refresh()

    def SetPageTextIcon(self, i, text=wx.EmptyString, icon=None):
        self.SetPageTitle(i, text, False)
        self.SetPageIcon(i, icon, False)
        self.tabsContainer.AdjustTabsSize()
        self.Refresh()

    def Refresh(self):
        self.tabsContainer.Refresh()

    def OnSize(self, event):
        w, h = self.GetSize()
        self.tabsContainer.SetSize((w, -1))
        self.tabsContainer.UpdateSize()
        self.tabsContainer.Refresh()
        self.Layout()

        if self.activePage:
            self.ShowActive()
        event.Skip()


class PFTabRenderer(object):
    def __init__(self, size=(36, 24), text=wx.EmptyString, img=None, inclination=6, closeButton=True):
        """
        Renders a new tab

        text -- tab label
        img -- wxImage of tab icon
        inclination -- does not seem to affect class, maybe used to be a variable
                       for custom drawn tab inclinations before there were bitmaps?
        closeButton -- True if tab can be closed
        """
        # tab left/right zones inclination
        self.ctabLeft = BitmapLoader.getImage("ctableft", "gui")
        self.ctabMiddle = BitmapLoader.getImage("ctabmiddle", "gui")
        self.ctabRight = BitmapLoader.getImage("ctabright", "gui")
        self.ctabClose = BitmapLoader.getImage("ctabclose", "gui")

        self.leftWidth = self.ctabLeft.GetWidth()
        self.rightWidth = self.ctabRight.GetWidth()
        self.middleWidth = self.ctabMiddle.GetWidth()
        self.closeBtnWidth = self.ctabClose.GetWidth()

        width, height = size
        if width < self.leftWidth + self.rightWidth + self.middleWidth:
            width = self.leftWidth + self.rightWidth + self.middleWidth
        if height < self.ctabMiddle.GetHeight():
            height = self.ctabMiddle.GetHeight()

        self.inclination = inclination
        self.text = text
        self.disabled = False
        self.tabSize = (width, height)
        self.closeButton = closeButton
        self.selected = False
        self.closeBtnHovering = False
        self.tabBitmap = None
        self.tabBackBitmap = None
        self.cbSize = 5
        self.padding = 4
        self.font = wx.Font(fonts.NORMAL, wx.SWISS, wx.NORMAL, wx.NORMAL, False)

        self.tabImg = img
        self.position = (0, 0)  # Not used internally for rendering - helper for tab container
        self.InitTab()

    def SetPosition(self, position):
        self.position = position

    def GetPosition(self):
        return self.position

    def GetSize(self):
        return self.tabSize

    def SetSize(self, size):
        w, h = size
        if w < self.leftWidth + self.rightWidth + self.middleWidth:
            w = self.leftWidth + self.rightWidth + self.middleWidth
        if h < self.ctabMiddle.GetHeight():
            h = self.ctabMiddle.GetHeight()

        self.tabSize = (w, h)
        self.InitTab()

    def SetSelected(self, sel=True):
        self.selected = sel
        self.InitTab()

    def GetSelected(self):
        return self.selected

    def IsSelected(self):
        return self.selected

    def ShowCloseButtonHovering(self, hover=True):
        if self.closeBtnHovering != hover:
            self.closeBtnHovering = hover
            self._Render()

    def GetCloseButtonHoverStatus(self):
        return self.closeBtnHovering

    def GetTabRegion(self):
        nregion = self.CopyRegion(self.tabRegion)
        nregion.SubtractRegion(self.closeBtnRegion) if self.closeButton else self.tabRegion
        return nregion

    def GetCloseButtonRegion(self):
        return self.CopyRegion(self.closeBtnRegion)

    def GetMinSize(self):
        ebmp = wx.EmptyBitmap(1, 1)
        mdc = wx.MemoryDC()
        mdc.SelectObject(ebmp)
        mdc.SetFont(self.font)
        textSizeX, textSizeY = mdc.GetTextExtent(self.text)
        totalSize = self.leftWidth + self.rightWidth + textSizeX + self.closeBtnWidth / 2 + 16 + self.padding * 2
        mdc.SelectObject(wx.NullBitmap)
        return totalSize, self.tabHeight

    def SetTabImage(self, img):
        self.tabImg = img

    @staticmethod
    def CopyRegion(region):
        rect = region.GetBox()

        newRegion = wx.Region(rect.X, rect.Y, rect.Width, rect.Height)
        newRegion.IntersectRegion(region)

        return newRegion

    def InitTab(self):
        self.tabWidth, self.tabHeight = self.tabSize

        self.contentWidth = self.tabWidth - self.leftWidth - self.rightWidth
        self.tabRegion = None
        self.closeBtnRegion = None

        self.InitColors()
        self.InitBitmaps()

        self.ComposeTabBack()
        self.InitTabRegions()
        self._Render()

    def InitBitmaps(self):
        """
        Creates bitmap for tab

        Takes the bitmaps already set and replaces a known color (black) with
        the needed color, while also considering selected state. Color dependant
        on platform -- see InitColors().
        """
        if self.selected:
            tr, tg, tb = self.selectedColor
        else:
            tr, tg, tb = self.inactiveColor

        ctabLeft = self.ctabLeft.Copy()
        ctabRight = self.ctabRight.Copy()
        ctabMiddle = self.ctabMiddle.Copy()

        ctabLeft.Replace(0, 0, 0, tr, tg, tb)
        ctabRight.Replace(0, 0, 0, tr, tg, tb)
        ctabMiddle.Replace(0, 0, 0, tr, tg, tb)

        self.ctabLeftBmp = wx.BitmapFromImage(ctabLeft)
        self.ctabRightBmp = wx.BitmapFromImage(ctabRight)
        self.ctabMiddleBmp = wx.BitmapFromImage(ctabMiddle)
        self.ctabCloseBmp = wx.BitmapFromImage(self.ctabClose)

    def ComposeTabBack(self):
        """
        Creates the tab background bitmap based upon calculated dimension values
        and modified bitmaps via InitBitmaps()
        """
        bkbmp = wx.EmptyBitmap(self.tabWidth, self.tabHeight)

        mdc = wx.MemoryDC()
        mdc.SelectObject(bkbmp)

        # mdc.SetBackground(wx.Brush((0x12, 0x23, 0x32)))
        mdc.Clear()

        mdc.DrawBitmap(self.ctabLeftBmp, 0, 0)  # set the left bitmap

        # convert middle bitmap and scale to tab width
        cm = self.ctabMiddleBmp.ConvertToImage()
        mimg = cm.Scale(self.contentWidth, self.ctabMiddle.GetHeight(), wx.IMAGE_QUALITY_NORMAL)
        mbmp = wx.BitmapFromImage(mimg)
        mdc.DrawBitmap(mbmp, self.leftWidth, 0)  # set middle bitmap, offset by left

        # set right bitmap offset by left + middle
        mdc.DrawBitmap(self.ctabRightBmp, self.contentWidth + self.leftWidth, 0)

        mdc.SelectObject(wx.NullBitmap)

        # bkbmp.SetMaskColour((0x12, 0x23, 0x32))

        if self.tabBackBitmap:
            del self.tabBackBitmap

        self.tabBackBitmap = bkbmp

    def InitTabRegions(self):
        """
        Initializes regions for tab, which makes it easier to determine if
        given coordinates are incluced in a region
        """
        self.tabRegion = wx.RegionFromBitmap(self.tabBackBitmap)
        self.closeBtnRegion = wx.RegionFromBitmap(self.ctabCloseBmp)
        self.closeBtnRegion.Offset(
                self.contentWidth + self.leftWidth - self.ctabCloseBmp.GetWidth() / 2,
                (self.tabHeight - self.ctabCloseBmp.GetHeight()) / 2
        )

    def InitColors(self):
        """Determines colors used for tab, based on system settings"""
        self.tabColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE)
        self.inactiveColor = colorUtils.GetSuitableColor(self.tabColor, 0.25)
        self.selectedColor = colorUtils.GetSuitableColor(self.tabColor, 0.10)

    def Render(self):
        return self.tabBitmap

    def _Render(self):
        """Renders the tab, complete with the icon, text, and close button"""
        if self.tabBitmap:
            del self.tabBitmap

        height = self.tabHeight

        # rect = wx.Rect(0, 0, self.tabWidth, self.tabHeight)

        canvas = wx.EmptyBitmap(self.tabWidth, self.tabHeight, 24)

        mdc = wx.MemoryDC()

        mdc.SelectObject(canvas)
        # mdc.SetBackground(wx.Brush ((0x12,0x23,0x32)))
        mdc.Clear()

        # r = copy.copy(rect)
        # r.top = r.left = 0
        # r.height = height
        mdc.DrawBitmap(self.tabBackBitmap, 0, 0, True)

        if self.tabImg:
            bmp = wx.BitmapFromImage(self.tabImg.ConvertToGreyscale() if self.disabled else self.tabImg)
            if self.contentWidth > 16:  # @todo: is this conditional relevant anymore?
                # Draw tab icon
                mdc.DrawBitmap(bmp, self.leftWidth + self.padding - bmp.GetWidth() / 2, (height - bmp.GetHeight()) / 2)
            textStart = self.leftWidth + self.padding + bmp.GetWidth() / 2
        else:
            textStart = self.leftWidth

        mdc.SetFont(self.font)

        maxsize = self.tabWidth - textStart - self.rightWidth - self.padding * 4
        color = self.selectedColor if self.selected else self.inactiveColor

        mdc.SetTextForeground(colorUtils.GetSuitableColor(color, 1))

        text = drawUtils.GetPartialText(mdc, self.text, maxsize, "")
        tx, ty = mdc.GetTextExtent(text)
        mdc.DrawText(text, textStart + self.padding, height / 2 - ty / 2)

        if self.closeButton:
            if self.closeBtnHovering:
                cbmp = self.ctabCloseBmp
            else:
                cimg = self.ctabCloseBmp.ConvertToImage()
                cimg = cimg.AdjustChannels(0.7, 0.7, 0.7, 0.3)
                cbmp = wx.BitmapFromImage(cimg)

            mdc.DrawBitmap(
                    cbmp,
                    self.contentWidth + self.leftWidth - self.ctabCloseBmp.GetWidth() / 2,
                    (height - self.ctabCloseBmp.GetHeight()) / 2,
            )

        mdc.SelectObject(wx.NullBitmap)

        canvas.SetMaskColour((0x12, 0x23, 0x32))
        img = canvas.ConvertToImage()

        if not img.HasAlpha():
            img.InitAlpha()

        bmp = wx.BitmapFromImage(img)
        self.tabBitmap = bmp

    def __repr__(self):
        return "PFTabRenderer(text={}, disabled={}) at {}".format(
                self.text, self.disabled, hex(id(self))
        )


class PFAddRenderer(object):
    def __init__(self):
        """Renders the add tab button"""
        self.addImg = BitmapLoader.getImage("ctabadd", "gui")
        self.width = self.addImg.GetWidth()
        self.height = self.addImg.GetHeight()

        self.region = None
        self.tbmp = wx.BitmapFromImage(self.addImg)
        self.addBitmap = None

        self.position = (0, 0)
        self.highlighted = False

        self.InitRenderer()

    def GetPosition(self):
        return self.position

    def SetPosition(self, pos):
        self.position = pos

    def GetSize(self):
        return self.width, self.height

    def GetHeight(self):
        return self.height

    def GetWidth(self):
        return self.width

    def InitRenderer(self):
        self.region = self.CreateRegion()
        self._Render()

    def CreateRegion(self):
        region = wx.RegionFromBitmap(self.tbmp)
        return region

    @staticmethod
    def CopyRegion(region):
        rect = region.GetBox()

        newRegion = wx.Region(rect.X, rect.Y, rect.Width, rect.Height)
        newRegion.IntersectRegion(region)

        return newRegion

    def GetRegion(self):
        return self.CopyRegion(self.region)

    def Highlight(self, highlight=False):
        self.highlighted = highlight
        self._Render()

    def IsHighlighted(self):
        return self.highlighted

    def Render(self):
        return self.addBitmap

    def _Render(self):
        if self.addBitmap:
            del self.addBitmap

        alpha = 1 if self.highlighted else 0.3

        img = self.addImg.AdjustChannels(1, 1, 1, alpha)
        bbmp = wx.BitmapFromImage(img)
        self.addBitmap = bbmp


class PFTabsContainer(wx.Panel):
    def __init__(self, parent, pos=(0, 0), size=(100, 22), id=wx.ID_ANY, canAdd=True):
        """
        Defines the tab container. Handles functions such as tab selection and
        dragging, and defines minimum width of tabs (all tabs are of equal width,
        which is determined via widest tab). Also handles the tab preview, if any.
        """

        wx.Panel.__init__(self, parent, id, pos, size)
        if wx.VERSION >= (3, 0):
            self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self.tabs = []
        width, height = size
        self.width = width
        self.height = height
        self.containerHeight = height
        self.startDrag = False
        self.dragging = False
        self.sFit = Fit.getInstance()
        self.efxBmp = None

        self.inclination = 7
        if canAdd:
            self.reserved = 48
        else:
            self.reserved = self.inclination * 4

        self.dragTrail = 3  # pixel distance to drag before we actually start dragging
        self.dragx = 0
        self.dragy = 0
        self.draggedTab = None
        self.dragTrigger = self.dragTrail

        self.showAddButton = canAdd

        self.tabContainerWidth = width - self.reserved
        self.tabMinWidth = width
        self.tabShadow = None

        self.addButton = PFAddRenderer()
        self.addBitmap = self.addButton.Render()

        self.previewTimer = None
        self.previewTimerID = wx.ID_ANY
        self.previewWnd = None
        self.previewBmp = None
        self.previewPos = None
        self.previewTab = None

        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMiddleUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SYS_COLOUR_CHANGED, self.OnSysColourChanged)
        self.tabShadow = PFTabRenderer((self.tabMinWidth, self.height + 1), inclination=self.inclination)

    def OnSysColourChanged(self, event):
        for tab in self.tabs:
            tab.InitTab()
        self.Refresh()

    def OnSize(self, event):
        self.UpdateSize()
        event.Skip()

    def UpdateSize(self):
        width, _ = self.GetSize()
        if width != self.width:
            self.width = width
            self.tabContainerWidth = self.width - self.reserved
            self.AdjustTabsSize()

    def OnLeftDown(self, event):
        """Determines what happens when user left clicks (down)"""
        mposx, mposy = event.GetPosition()
        if not self.startDrag:
            tab = self.FindTabAtPos(mposx, mposy)
            if tab:
                self.CheckTabSelected(tab, mposx, mposy)
                if self.showAddButton:
                    # If we can add tabs, we can drag them. Set flag
                    self.startDrag = True
                    tx, ty = tab.GetPosition()
                    self.dragx = mposx - tx
                    self.dragy = self.containerHeight - self.height
                self.Refresh()

            self.draggedTab = tab

    def OnLeftUp(self, event):
        """Determines what happens when user left clicks (up)"""
        mposx, mposy = event.GetPosition()
        if self.startDrag and self.dragging:
            self.dragging = False
            self.startDrag = False
            self.draggedTab = None
            self.dragTrigger = self.dragTrail
            self.UpdateTabsPosition()
            self.Refresh()
            if self.HasCapture():
                self.ReleaseMouse()

            return

        if self.startDrag:
            self.startDrag = False
            self.dragTrigger = self.dragTrail

        # Checks if we selected the add button and, if True, returns
        if self.CheckAddButton(mposx, mposy):
            return

        # If there are no tabs, don't waste time
        if self.GetTabsCount() == 0:
            return

        # Gets selected tab (was set when user down clicked)
        selTab = self.GetSelectedTab()

        # Check if we selected close button for selected tab
        if self.CheckTabClose(selTab, mposx, mposy):
            return

        # Check if we selected close button for all others
        for tab in self.tabs:
            if self.CheckTabClose(tab, mposx, mposy):
                return

    def OnMiddleUp(self, event):
        mposx, mposy = event.GetPosition()

        tab = self.FindTabAtPos(mposx, mposy)

        if tab is None or not tab.closeButton:  # if not able to close, return False
            return False

        index = self.tabs.index(tab)
        ev = PageClosing(index)
        wx.PostEvent(self.Parent, ev)
        if ev.isVetoed():
            return False

        index = self.GetTabIndex(tab)
        self.DeleteTab(index)
        wx.PostEvent(self.Parent, PageClosed(index=index))
        sel = self.GetSelected()

        if sel is not None:
            wx.PostEvent(self.Parent, PageChanged(-1, sel))

    def GetSelectedTab(self):
        for tab in self.tabs:
            if tab.GetSelected():
                return tab
        return None

    def GetSelected(self):
        for tab in self.tabs:
            if tab.GetSelected():
                return self.tabs.index(tab)
        return None

    def SetSelected(self, tabIndex):
        oldSelTab = self.GetSelectedTab()
        oldSelTab.SetSelected(False)
        self.tabs[tabIndex].SetSelected(True)
        self.Refresh()

    def CheckTabSelected(self, tab, x, y):
        """
        Selects the tab at x, y. If the tab at x, y is already selected, simply
        return true. Otherwise, perform TabHitTest and set tab at position to
        selected
        """
        oldSelTab = self.GetSelectedTab()
        if oldSelTab == tab:
            return True

        if self.TabHitTest(tab, x, y):
            if tab.disabled:
                return
            tab.SetSelected(True)
            oldSelTab.SetSelected(False)

            ev = PageChanging(self.tabs.index(oldSelTab), self.tabs.index(tab))
            wx.PostEvent(self.Parent, ev)

            if ev.isVetoed():
                return False

            self.Refresh()
            selTab = self.tabs.index(tab)
            self.Parent.SetSelection(selTab)

            wx.PostEvent(self.Parent, PageChanged(self.tabs.index(oldSelTab), self.tabs.index(tab)))

            return True

        return False

    def CheckTabClose(self, tab, x, y):
        """Determines if close button was selected for the given tab."""
        if not tab.closeButton:  # if not able to close, return False
            return False

        closeBtnReg = tab.GetCloseButtonRegion()
        tabPosX, tabPosY = tab.GetPosition()
        closeBtnReg.Offset(tabPosX, tabPosY)

        if closeBtnReg.Contains(x, y):
            index = self.tabs.index(tab)
            ev = PageClosing(index)
            wx.PostEvent(self.Parent, ev)
            if ev.isVetoed():
                return False

            index = self.GetTabIndex(tab)
            self.DeleteTab(index)
            wx.PostEvent(self.Parent, PageClosed(index=index))
            sel = self.GetSelected()

            if sel is not None:
                wx.PostEvent(self.Parent, PageChanged(-1, sel))

            return True
        return False

    def CheckAddButton(self, x, y):
        """Determines if add button was selected."""
        if not self.showAddButton:  # if not able to add, return False
            return

        reg = self.addButton.GetRegion()
        ax, ay = self.addButton.GetPosition()
        reg.Offset(ax, ay)

        if reg.Contains(x, y):
            ev = PageAdding()
            wx.PostEvent(self.Parent, ev)
            if ev.isVetoed():
                return False

            self.Parent.AddPage()
            wx.PostEvent(self.Parent, PageAdded())
            return True

    def CheckCloseButtons(self, x, y):
        """
        Checks if mouse pos at x, y is over a close button. If so, set the
        close hovering flag for that tab
        """
        dirty = False
        # @todo: maybe change to for...else
        for tab in self.tabs:
            closeBtnReg = tab.GetCloseButtonRegion()
            tabPos = tab.GetPosition()
            tabPosX, tabPosY = tabPos
            closeBtnReg.Offset(tabPosX, tabPosY)

            if closeBtnReg.Contains(x, y):
                if not tab.GetCloseButtonHoverStatus():
                    tab.ShowCloseButtonHovering(True)
                    dirty = True
            else:
                if tab.GetCloseButtonHoverStatus():
                    tab.ShowCloseButtonHovering(False)
                    dirty = True
        if dirty:
            self.Refresh()

    def FindTabAtPos(self, x, y):
        if self.GetTabsCount() == 0:
            return None

        selTab = self.GetSelectedTab()
        if self.TabHitTest(selTab, x, y):
            return selTab

        for tab in self.tabs:
            if self.TabHitTest(tab, x, y):
                return tab
        return None

    @staticmethod
    def TabHitTest(tab, x, y):
        tabRegion = tab.GetTabRegion()
        tabPos = tab.GetPosition()
        tabPosX, tabPosY = tabPos
        tabRegion.Offset(tabPosX, tabPosY)

        if tabRegion.Contains(x, y):
            return True

        return False

    def GetTabAtLeft(self, tabIndex):
        return self.tabs[tabIndex - 1] if tabIndex > 0 else None

    def GetTabAtRight(self, tabIndex):
        return self.tabs[tabIndex + 1] if tabIndex < self.GetTabsCount() - 1 else None

    def SwitchTabs(self, src, dest, draggedTab=None):
        self.tabs[src], self.tabs[dest] = self.tabs[dest], self.tabs[src]
        self.UpdateTabsPosition(draggedTab)
        self.Parent.SwitchPages(src, dest)
        self.Refresh()

    def GetTabIndex(self, tab):
        return self.tabs.index(tab)

    def OnMotion(self, event):
        """
        Determines what happens when the mouse moves. This handles primarily
        dragging (region tab can be dragged) as well as checking if we are over
        an actionable button.
        """
        mposx, mposy = event.GetPosition()

        if self.startDrag:
            if not self.dragging:
                if self.dragTrigger < 0:
                    self.dragging = True
                    self.dragTrigger = self.dragTrail
                    self.CaptureMouse()
                else:
                    self.dragTrigger -= 1
            if self.dragging:
                dtx = mposx - self.dragx
                w, h = self.draggedTab.GetSize()

                if dtx < 0:
                    dtx = 0
                if dtx + w > self.tabContainerWidth + self.inclination * 2:
                    dtx = self.tabContainerWidth - w + self.inclination * 2
                self.draggedTab.SetPosition((dtx, self.dragy))

                index = self.GetTabIndex(self.draggedTab)

                leftTab = self.GetTabAtLeft(index)
                rightTab = self.GetTabAtRight(index)

                if leftTab:
                    lw, lh = leftTab.GetSize()
                    lx, ly = leftTab.GetPosition()

                    if lx + lw / 2 - self.inclination * 2 > dtx:
                        self.SwitchTabs(index - 1, index, self.draggedTab)
                        return

                if rightTab:
                    rw, rh = rightTab.GetSize()
                    rx, ry = rightTab.GetPosition()

                    if rx + rw / 2 + self.inclination * 2 < dtx + w:
                        self.SwitchTabs(index + 1, index, self.draggedTab)
                        return
                self.UpdateTabsPosition(self.draggedTab)
                self.Refresh()
                return
            return

        self.CheckCloseButtons(mposx, mposy)
        self.CheckAddHighlighted(mposx, mposy)
        self.CheckTabPreview(mposx, mposy)

        event.Skip()

    def CheckTabPreview(self, mposx, mposy):
        """
        Checks to see if we have a tab preview and sets up the timer for it
        to display
        """
        if not self.sFit.serviceFittingOptions["showTooltip"] or False:
            return

        if self.previewTimer:
            if self.previewTimer.IsRunning():
                if self.previewWnd:
                    self.previewTimer.Stop()
                return

        if self.previewWnd:
            self.previewWnd.Show(False)
            del self.previewWnd
            self.previewWnd = None

        for tab in self.tabs:
            if not tab.GetSelected():
                if self.TabHitTest(tab, mposx, mposy):
                    try:
                        page = self.Parent.GetPage(self.GetTabIndex(tab))
                        if hasattr(page, "Snapshot"):
                            if not self.previewTimer:
                                self.previewTimer = wx.Timer(self, self.previewTimerID)

                            self.previewTab = tab
                            self.previewTimer.Start(500, True)
                            break
                    except Exception as e:
                        pyfalog.critical("Exception caught in CheckTabPreview.")
                        pyfalog.critical(e)

    def CheckAddHighlighted(self, x, y):
        """
        Checks to see if x, y are in add button region, and sets the highlight
        flag
        """
        if not self.showAddButton:
            return

        reg = self.addButton.GetRegion()
        ax, ay = self.addButton.GetPosition()
        reg.Offset(ax, ay)

        if reg.Contains(x, y):
            if not self.addButton.IsHighlighted():
                self.addButton.Highlight(True)
                self.Refresh()
        else:
            if self.addButton.IsHighlighted():
                self.addButton.Highlight(False)
                self.Refresh()

    def OnPaint(self, event):
        if "wxGTK" in wx.PlatformInfo:
            mdc = wx.AutoBufferedPaintDC(self)
        else:
            mdc = wx.BufferedPaintDC(self)

        if 'wxMac' in wx.PlatformInfo and wx.VERSION < (3, 0):
            color = wx.Colour(0, 0, 0)
            brush = wx.Brush(color)

            # noinspection PyPackageRequirements,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
            from Carbon.Appearance import kThemeBrushDialogBackgroundActive
            # noinspection PyUnresolvedReferences
            brush.MacSetTheme(kThemeBrushDialogBackgroundActive)
        else:
            color = wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE)
            brush = wx.Brush(color)

        if "wxGTK" not in wx.PlatformInfo:
            mdc.SetBackground(brush)
            mdc.Clear()

        selected = None

        tabsWidth = 0

        for tab in self.tabs:
            tabsWidth += tab.tabWidth - self.inclination * 2

        if self.showAddButton:
            ax, ay = self.addButton.GetPosition()
            mdc.DrawBitmap(self.addButton.Render(), ax, ay, True)

        for i in range(len(self.tabs) - 1, -1, -1):
            tab = self.tabs[i]
            posx, posy = tab.GetPosition()

            if not tab.IsSelected():
                mdc.DrawBitmap(self.efxBmp, posx, posy, True)
                bmp = tab.Render()
                img = bmp.ConvertToImage()
                img = img.AdjustChannels(1, 1, 1, 0.85)
                bmp = wx.BitmapFromImage(img)
                mdc.DrawBitmap(bmp, posx, posy, True)

            else:
                selected = tab

        if selected:
            posx, posy = selected.GetPosition()
            mdc.DrawBitmap(self.efxBmp, posx, posy, True)

            bmp = selected.Render()

            if self.dragging:
                img = bmp.ConvertToImage()
                img = img.AdjustChannels(1.2, 1.2, 1.2, 0.7)
                bmp = wx.BitmapFromImage(img)

            mdc.DrawBitmap(bmp, posx, posy, True)

    def OnErase(self, event):
        pass

    def UpdateTabFX(self):
        w, h = self.tabShadow.GetSize()
        if self.efxBmp is None or w != self.tabMinWidth:
            self.tabShadow.SetSize((self.tabMinWidth, self.height + 1))
            fxBmp = self.tabShadow.Render()

            simg = fxBmp.ConvertToImage()
            if not simg.HasAlpha():
                simg.InitAlpha()
            simg = simg.Blur(2)
            simg = simg.AdjustChannels(0.3, 0.3, 0.3, 0.35)

            self.efxBmp = wx.BitmapFromImage(simg)

    def AddTab(self, title=wx.EmptyString, img=None, showClose=False):
        self.ClearTabsSelected()

        tabRenderer = PFTabRenderer((120, self.height), title, img, self.inclination, closeButton=showClose)
        tabRenderer.SetSelected(True)

        self.tabs.append(tabRenderer)
        self.AdjustTabsSize()
        self.Refresh()

    def ClearTabsSelected(self):
        for tab in self.tabs:
            tab.SetSelected(False)

    def DisableTab(self, tab, disabled=True):
        tabRenderer = self.tabs[tab]
        tabRenderer.disabled = disabled

        self.AdjustTabsSize()
        self.Refresh()

    def DeleteTab(self, tab, external=False):
        tabRenderer = self.tabs[tab]
        wasSelected = tabRenderer.GetSelected()
        self.tabs.remove(tabRenderer)

        if tabRenderer:
            del tabRenderer

        if wasSelected and self.GetTabsCount() > 0:
            if tab > self.GetTabsCount() - 1:
                self.tabs[self.GetTabsCount() - 1].SetSelected(True)
            else:
                self.tabs[tab].SetSelected(True)

        if not external:
            self.Parent.DeletePage(tab, True)

        self.AdjustTabsSize()
        self.Refresh()

    def GetTabsCount(self):
        return len(self.tabs)

    def AdjustTabsSize(self):
        tabMinWidth = 9000000  # Really, it should be over 9000
        tabMaxWidth = 0
        for tab in self.tabs:
            mw, mh = tab.GetMinSize()
            if tabMinWidth > mw:
                tabMinWidth = mw
            if tabMaxWidth < mw:
                tabMaxWidth = mw
        if tabMaxWidth < 100:
            tabMaxWidth = 100
        if self.GetTabsCount() > 0:
            if (self.GetTabsCount()) * (tabMaxWidth - self.inclination * 2) > self.tabContainerWidth:
                self.tabMinWidth = float(self.tabContainerWidth) / float(self.GetTabsCount()) + self.inclination * 2
            else:
                self.tabMinWidth = tabMaxWidth

        if self.tabMinWidth < 1:
            self.tabMinWidth = 1
        for tab in self.tabs:
            tab.GetSize()
            tab.SetSize((self.tabMinWidth, self.height))

        if self.GetTabsCount() > 0:
            self.UpdateTabFX()

        self.UpdateTabsPosition()

    def UpdateTabsPosition(self, skipTab=None):
        tabsWidth = 0
        for tab in self.tabs:
            tabsWidth += tab.tabWidth - self.inclination * 2

        pos = tabsWidth
        selected = None
        selpos = None
        for i in range(len(self.tabs) - 1, -1, -1):
            tab = self.tabs[i]
            width = tab.tabWidth - self.inclination * 2
            pos -= width
            if not tab.IsSelected():
                tab.SetPosition((pos, self.containerHeight - self.height))
            else:
                selected = tab
                selpos = pos
        if selected is not skipTab:
            selected.SetPosition((selpos, self.containerHeight - self.height))
        self.addButton.SetPosition(
            (
                round(tabsWidth) + self.inclination * 2,
                self.containerHeight - self.height / 2 - self.addButton.GetHeight() / 3
            )
        )

    def OnLeaveWindow(self, event):

        if self.startDrag and not self.dragging:
            self.dragging = False
            self.startDrag = False
            self.draggedTab = None
            self.dragTrigger = self.dragTrail
            if self.HasCapture():
                self.ReleaseMouse()

        if self.previewWnd:
            self.previewWnd.Show(False)
            del self.previewWnd
            self.previewWnd = None
        event.Skip()

    def OnTimer(self, event):
        mposx, mposy = wx.GetMousePosition()
        cposx, cposy = self.ScreenToClient((mposx, mposy))
        if self.FindTabAtPos(cposx, cposy) == self.previewTab:
            if not self.previewTab.GetSelected():
                page = self.Parent.GetPage(self.GetTabIndex(self.previewTab))
                if page.Snapshot():
                    self.previewWnd = PFNotebookPagePreview(
                        self,
                        (mposx + 3, mposy + 3),
                        page.Snapshot(),
                        self.previewTab.text
                    )
                    self.previewWnd.Show()

        event.Skip()


class PFNotebookPagePreview(wx.Frame):
    def __init__(self, parent, pos, bitmap, title):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=wx.EmptyString,
            pos=pos,
            size=wx.DefaultSize,
            style=wx.NO_BORDER | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP
        )

        self.title = title
        self.bitmap = bitmap
        self.SetSize((bitmap.GetWidth(), bitmap.GetHeight()))
        self.Bind(wx.EVT_PAINT, self.OnWindowPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnWindowEraseBk)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        self.timer = wx.Timer(self, wx.ID_ANY)
        self.timerSleep = None
        self.timerSleepId = wx.NewId()
        self.direction = 1
        self.padding = 15
        self.transp = 0

        hfont = wx.Font(fonts.NORMAL, wx.SWISS, wx.NORMAL, wx.NORMAL, False)
        self.SetFont(hfont)

        tx, ty = self.GetTextExtent(self.title)
        tx += self.padding * 2

        if bitmap.GetWidth() < tx:
            width = tx
        else:
            width = bitmap.GetWidth()

        self.SetSize((width, bitmap.GetHeight() + 16))

        self.SetTransparent(0)
        self.Refresh()

    def OnTimer(self, event):
        self.transp += 20 * self.direction

        if self.transp > 220:
            self.transp = 220
            self.timer.Stop()

        if self.transp < 0:
            self.transp = 0
            self.timer.Stop()
            wx.Frame.Show(self, False)
            self.Destroy()
            return
        self.SetTransparent(self.transp)

    def RaiseParent(self):
        wnd = self
        lastwnd = None
        while wnd is not None:
            lastwnd = wnd
            wnd = wnd.Parent
        if lastwnd:
            lastwnd.Raise()

    def Show(self, showWnd=True):
        if showWnd:
            wx.Frame.Show(self, showWnd)
            self.RaiseParent()
            self.direction = 1
            self.timer.Start(10)
        else:
            self.direction = -1
            self.timer.Start(10)

    def OnWindowEraseBk(self, event):
        pass

    def OnWindowPaint(self, event):
        rect = self.GetRect()
        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)
        color = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        mdc.SetBackground(wx.Brush(color))
        mdc.Clear()

        font = wx.Font(fonts.NORMAL, wx.SWISS, wx.NORMAL, wx.NORMAL, False)
        mdc.SetFont(font)

        x, y = mdc.GetTextExtent(self.title)

        mdc.SetBrush(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT)))
        mdc.DrawRectangle(0, 0, rect.width, 16)

        mdc.SetTextForeground(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))

        mdc.DrawText(self.title, (rect.width - x) / 2, (16 - y) / 2)

        mdc.DrawBitmap(self.bitmap, 0, 16)

        mdc.SetPen(wx.Pen("#000000", width=1))
        mdc.SetBrush(wx.TRANSPARENT_BRUSH)

        mdc.DrawRectangle(0, 16, rect.width, rect.height - 16)
