#!/usr/bin/env python

# --------------------------------------------------------------------------------- #
# Pyfa's custom Notebook core python IMPLEMENTATION
#
# Darriele (homeworld using gmail point com) - 10/27/2010
# Updated: 11/11/2010
#
# --------------------------------------------------------------------------------- #

import wx
import copy
import time
from gui import bitmapLoader

_PageChanging, EVT_NOTEBOOK_PAGE_CHANGING = wx.lib.newevent.NewEvent()
_PageChanged, EVT_NOTEBOOK_PAGE_CHANGED = wx.lib.newevent.NewEvent()
_PageAdding, EVT_NOTEBOOK_PAGE_ADDING = wx.lib.newevent.NewEvent()
_PageClosing, EVT_NOTEBOOK_PAGE_CLOSING = wx.lib.newevent.NewEvent()
PageAdded, EVT_NOTEBOOK_PAGE_ADDED = wx.lib.newevent.NewEvent()
PageClosed, EVT_NOTEBOOK_PAGE_CLOSED = wx.lib.newevent.NewEvent()

class VetoAble():
    def __init__(self):
        self.__vetoed = False

    def Veto(self):
        self.__vetoed = True

    def isVetoed(self):
        return self.__vetoed

class NotebookTabChangeEvent():

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
    def __init__(self, parent, canAdd = True):
        wx.Panel.__init__(self, parent, wx.ID_ANY,size = (-1,-1))

        self.pages = []
        self.activePage = None

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        tabsSizer = wx.BoxSizer( wx.VERTICAL )

        self.tabsContainer = PFTabsContainer(self, canAdd = canAdd)
        tabsSizer.Add( self.tabsContainer, 0, wx.EXPAND )

        mainSizer.Add( tabsSizer, 0, wx.EXPAND, 5 )

        contentSizer = wx.BoxSizer( wx.VERTICAL )
        if 'wxMSW' in wx.PlatformInfo:
            style = wx.DOUBLE_BORDER
        else:
            style = wx.SIMPLE_BORDER
        self.pageContainer = wx.Panel(self, style = style)
        self.pageContainer.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        contentSizer.Add( self.pageContainer, 1, wx.EXPAND, 5 )

        mainSizer.Add( contentSizer, 1, wx.EXPAND | wx.BOTTOM, 2 )

        self.SetSizer( mainSizer )
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


    def GetBorders(self):
        bx = wx.SystemSettings_GetMetric(wx.SYS_BORDER_X)
        by = wx.SystemSettings_GetMetric(wx.SYS_BORDER_Y)
        if bx<0:
            bx = 1
        if by<0:
            by = 1
        return (bx,by)

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

    def AddPage(self, tabWnd = None, tabTitle ="Empty Tab", tabImage = None, showClose = True):
        if self.activePage:
            self.activePage.Hide()
        if not tabWnd:
            tabWnd = wx.Panel(self)
        tabWnd.Reparent(self.pageContainer)
        self.pageContainer.Layout()

        self.pages.append(tabWnd)
        self.tabsContainer.AddTab(tabTitle, tabImage, showClose)

        self.activePage = tabWnd


    def SetSelection(self, page):
        oldsel = self.GetSelection()
        if oldsel != page:
            self.activePage.Hide()
            self.activePage = self.pages[page]
            self.tabsContainer.SetSelected(page)
            self.ShowActive()

    def DeletePage(self, n, internal = False):
        page = self.pages[n]

        self.pages.remove(page)
        page.Hide()
        page.Destroy()

        if not internal:
            self.tabsContainer.DeleteTab(n, True)

        sel = self.tabsContainer.GetSelected()
        if sel is not None:
            self.activePage = self.pages[sel]
            self.ShowActive()
        else:
            self.activePage = None


    def SwitchPages(self, src, dest, internal = False):
        self.pages[src], self.pages[dest] = self.pages[dest], self.pages[src]

    def ShowActive(self):
        size = self.pageContainer.GetSize()
        bx, by = self.GetBorders()
        ww,wh = size
        ww -= bx * 4 if 'wxGTK' in wx.PlatformInfo else 6
        wh -= by * 4 if 'wxGTK' in wx.PlatformInfo else 6
        self.activePage.SetSize((ww,wh))
        self.activePage.SetPosition((bx,by))
        self.activePage.Show()
        self.Layout()


    def IsActive(self, page):
        return self.activePage == page

    def SetPageText(self, i, text, refresh=True):
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
        self.SetPageText(i, text, False)
        self.SetPageIcon(i, icon, False)
        self.tabsContainer.AdjustTabsSize()
        self.Refresh()

    def Refresh(self):
        self.tabsContainer.Refresh()

    def OnSize(self, event):
        w,h= self.GetSize()
        self.tabsContainer.SetSize((w, -1))
        self.tabsContainer.UpdateSize()
        self.tabsContainer.Refresh()
        self.Layout()

        if self.activePage:
            self.ShowActive()
        event.Skip()

class PFTabRenderer:
    def __init__(self, size = (36,24), text = wx.EmptyString, img = None, inclination = 6 , closeButton = True, fontSize = 14):

        # tab left/right zones inclination
        self.ctabLeft = bitmapLoader.getImage("ctableft", "icons")
        self.ctabMiddle = bitmapLoader.getImage("ctabmiddle", "icons")
        self.ctabRight = bitmapLoader.getImage("ctabright", "icons")
        self.ctabClose = bitmapLoader.getImage("ctabclose", "icons")

        self.leftWidth = self.ctabLeft.GetWidth()
        self.rightWidth = self.ctabRight.GetWidth()
        self.middleWidth = self.ctabMiddle.GetWidth()
        self.closeBtnWidth  = self.ctabClose.GetWidth()

        width, height = size
        if width < self.leftWidth + self.rightWidth + self.middleWidth:
            width = self.leftWidth + self.rightWidth + self.middleWidth
        if height < self.ctabMiddle.GetHeight():
            height = self.ctabMiddle.GetHeight()

        self.inclination = inclination
        self.text = text
        self.tabSize = (width, height)
        self.closeButton = closeButton
        self.fontSize = fontSize
        self.selected = False
        self.closeBtnHovering = False
        self.tabBitmap = None
        self.tabBackBitmap = None
        self.cbSize = 5
        self.padding = 4
        self.font = wx.FontFromPixelSize((0, self.fontSize), wx.SWISS, wx.NORMAL, wx.NORMAL, False)

        self.tabImg = img
        self.position = (0, 0) # Not used internaly for rendering - helper for tab container
        self.InitTab()

    def SetPosition(self, position):
        self.position = position

    def GetPosition(self):
        return self.position

    def GetSize(self):
        return self.tabSize

    def SetSize(self, size):
        otw,oth = self.tabSize
        w,h = size
        if w< self.leftWidth + self.rightWidth + self.middleWidth:
            w = self.leftWidth + self.rightWidth + self.middleWidth
        if h < self.ctabMiddle.GetHeight():
            h = self.ctabMiddle.GetHeight()

        self.tabSize = (w,h)

        self.InitTab()

    def SetSelected(self, sel = True):
        self.selected = sel
        self.InitTab()
#        self._Render()

    def GetSelected(self):
        return self.selected

    def IsSelected(self):
        return self.selected

    def ShowCloseButtonHovering(self, hover = True):
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
        ebmp = wx.EmptyBitmap(1,1)
        mdc = wx.MemoryDC()
        mdc.SelectObject(ebmp)
        mdc.SetFont(self.font)
        textSizeX, textSizeY = mdc.GetTextExtent(self.text)
        totalSize = self.leftWidth + self.rightWidth + textSizeX + self.closeBtnWidth/2 + 16 + self.padding*2
        mdc.SelectObject(wx.NullBitmap)
        return (totalSize, self.tabHeight)

    def SetTabImage(self, img):
        self.tabImg = img

    def CopyRegion(self, region):
        rect = region.GetBox()

        newRegion = wx.Region(rect.X, rect.Y, rect.Width, rect.Height)
        newRegion.IntersectRegion(region)

        return newRegion

    def InitTab(self, skipLRzones = False):
        self.tabWidth, self.tabHeight = self.tabSize

        # content width is tabWidth - (left+right) zones

        self.contentWidth = self.tabWidth - self.leftWidth - self.rightWidth
        self.tabRegion = None
        self.closeBtnRegion = None

        self.InitColors()
        self.InitBitmaps()

        self.ComposeTabBack()
        self.InitTabRegions()
        self._Render()

    def InitBitmaps(self):

        if self.selected:
            tr,tg,tb = self.rightColor
        else:
            tr,tg,tb = self.leftColor

        ctabLeft = self.ctabLeft.Copy()
        ctabRight = self.ctabRight.Copy()
        ctabMiddle = self.ctabMiddle.Copy()

        ctabLeft.Replace(0,0,0,tr, tg, tb)
        ctabRight.Replace(0,0,0,tr, tg, tb)
        ctabMiddle.Replace(0,0,0,tr, tg, tb)

        self.ctabLeftBmp = wx.BitmapFromImage(ctabLeft)
        self.ctabRightBmp = wx.BitmapFromImage(ctabRight)
        self.ctabMiddleBmp = wx.BitmapFromImage(ctabMiddle)
        self.ctabCloseBmp = wx.BitmapFromImage(self.ctabClose)



    def ComposeTabBack(self):

        bkbmp = wx.EmptyBitmap(self.tabWidth, self.tabHeight)

        mdc = wx.MemoryDC()
        mdc.SelectObject(bkbmp)

        mdc.SetBackground( wx.Brush((0x12,0x23,0x32)))
        mdc.Clear()

        mdc.DrawBitmap(self.ctabLeftBmp, 0, 0)
        cm = self.ctabMiddleBmp.ConvertToImage()
        mimg = cm.Scale(self.contentWidth, self.ctabMiddle.GetHeight(), wx.IMAGE_QUALITY_NORMAL)
        mbmp = wx.BitmapFromImage(mimg)
        mdc.DrawBitmap(mbmp, self.leftWidth, 0 )
        mdc.DrawBitmap(self.ctabRightBmp, self.contentWidth + self.leftWidth, 0 )
        mdc.SelectObject(wx.NullBitmap)
        bkbmp.SetMaskColour( (0x12, 0x23, 0x32) )
        if self.tabBackBitmap:
            del self.tabBackBitmap

        self.tabBackBitmap = bkbmp

    def InitTabRegions(self):
        self.tabRegion = wx.RegionFromBitmap(self.tabBackBitmap)
        self.closeBtnRegion = wx.RegionFromBitmap(self.ctabCloseBmp)
        self.closeBtnRegion.Offset(self.contentWidth+self.leftWidth - self.ctabCloseBmp.GetWidth()/2, (self.tabHeight - self.ctabCloseBmp.GetHeight())/2)


    def InitColors(self):
        self.tabColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        self.leftColor = self.CalculateColor(self.tabColor, 0x60)
        self.rightColor = self.CalculateColor(self.tabColor, 0x30)

    def CalculateColor(self, color, delta):
        bkR ,bkG , bkB = color
        if bkR + bkG + bkB > 127*3:
            scale = - delta
        else:
            scale = delta

        r = bkR + scale
        g = bkG + scale
        b = bkB + scale

        r = min(max(r,0),255)
        b = min(max(b,0),255)
        g = min(max(g,0),255)

        return wx.Colour(r,g,b,255)


    def Render(self):
        return self.tabBitmap

    def _Render(self):
        if self.tabBitmap:
            del self.tabBitmap

        inc = 6
        height = self.tabHeight
        width = self.tabWidth
        contentWidth = self.contentWidth

        rect = wx.Rect(0,0,self.tabWidth, self.tabHeight)

        canvas = wx.EmptyBitmap(rect.width, rect.height)

        mdc = wx.MemoryDC()

        mdc.SelectObject(canvas)
        mdc.SetBackground(wx.Brush ((0x12,0x23,0x32)))
        mdc.Clear()


        r = copy.copy(rect)
        r.top = r.left = 0
        r.height = height
        mdc.DrawBitmap(self.tabBackBitmap, 0, 0, True)

        if self.tabImg:
            bmp = wx.BitmapFromImage(self.tabImg)
            if self.contentWidth > 16:
                mdc.DrawBitmap(bmp, self.leftWidth + self.padding  - bmp.GetWidth()/2, (height - bmp.GetHeight())/2)
            textStart = self.leftWidth + self.padding + bmp.GetWidth()/2
        else:
            textStart = self.leftWidth

        mdc.SetFont(self.font)
        text = self.text
        fnwidths = mdc.GetPartialTextExtents(text)
        count = 0
        maxsize = self.tabWidth - textStart - self.rightWidth - self.padding*2
        for i in fnwidths:
            if i <= maxsize:
                count +=1
            else:
                break
        if count > 0:
#            text = "%s%s" % (text[:count],".." if len(text)>count else "")
            text = "%s" % text[:count]

            tx,ty = mdc.GetTextExtent(text)
            if self.selected:
                mdc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
            else:
                color = self.CalculateColor(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT), 0x20)
                mdc.SetTextForeground(color)

            mdc.DrawText(text, textStart + self.padding , height / 2 - ty / 2)

#        mdc.DestroyClippingRegion()
        if self.closeButton:
            if self.closeBtnHovering:
                mdc.DrawBitmap(self.ctabCloseBmp,self.contentWidth+self.leftWidth - self.ctabCloseBmp.GetWidth()/2,(height - self.ctabCloseBmp.GetHeight())/2)
            else:
                cimg = self.ctabCloseBmp.ConvertToImage()
                cimg = cimg.AdjustChannels(0.7,0.7,0.7,0.3)
                cbmp = wx.BitmapFromImage(cimg)
                mdc.DrawBitmap(cbmp,self.contentWidth+self.leftWidth - self.ctabCloseBmp.GetWidth()/2,(height - self.ctabCloseBmp.GetHeight())/2)

        mdc.SelectObject(wx.NullBitmap)


        canvas.SetMaskColour((0x12,0x23,0x32))
        img = canvas.ConvertToImage()
        if not img.HasAlpha():
            img.InitAlpha()
        bmp = wx.BitmapFromImage(img)
        self.tabBitmap = bmp

class PFAddRenderer:
    def __init__(self, size = (24,12)):
        self.width, self.height = size
        self.addImg = bitmapLoader.getImage("ctabadd", "icons")
        self.width = self.addImg.GetWidth()
        self.height = self.addImg.GetHeight()
        self.spline = []
        self.inclination = 3
        self.region = None
        self.tbmp = wx.BitmapFromImage(self.addImg)
        self.addBitmap = None

        self.position = (0,0)
        self.highlighted = False

        self.InitRenderer()

    def GetPosition(self):
        return self.position

    def SetPosition(self,pos):
        self.position = pos

    def GetSize(self):
        return (self.width, self.height)

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

    def CopyRegion(self, region):
        rect = region.GetBox()

        newRegion = wx.Region(rect.X, rect.Y, rect.Width, rect.Height)
        newRegion.IntersectRegion(region)

        return newRegion

    def GetRegion(self):
        return self.CopyRegion(self.region)

    def CalculateColor(self, color, delta):
        bkR ,bkG , bkB = color
        if bkR + bkG + bkB > 127*3:
            scale = - delta
        else:
            scale = delta*2

        r = bkR + scale
        g = bkG + scale
        b = bkB + scale

        r = min(max(r,0),255)
        b = min(max(b,0),255)
        g = min(max(g,0),255)

        return wx.Colour(r,b,g)

    def Highlight(self, highlight = False):
        self.highlighted = highlight
        self._Render()

    def Render(self):
        return self.addBitmap

    def _Render(self):
        inc = self.inclination
        rect = wx.Rect(0 ,0 ,self.width, self.height)
        if self.addBitmap:
            del self.addBitmap

#        canvas = wx.EmptyBitmap(self.width, self.height)
#
#        mdc = wx.MemoryDC()
#        mdc.SelectObject(canvas)
#
#        mdc.SetBackground(wx.Brush ((0x12,0x23,0x32)))
#        mdc.Clear()
#        mdc.SelectObject(wx.NullBitmap)
#        canvas.SetMaskColour((255,255,255))

#        img = canvas.ConvertToImage()
#        if not img.HasAlpha():
#            img.InitAlpha()
        if self.highlighted:
            alpha = 1
        else:
            alpha = 0.3
        img = self.addImg.AdjustChannels(1, 1, 1, alpha)

        bbmp = wx.BitmapFromImage(img)
        self.addBitmap = bbmp
#        self.addBitmap.SetMaskColour((0x12,0x23,0x32))


class PFTabsContainer(wx.Panel):
    def __init__(self, parent, pos = (0,0), size = (100,22), id = wx.ID_ANY, canAdd = True):
        wx.Panel.__init__(self, parent, id , pos, size)
        self.tabs = []
        width, height = size
        self.width  = width
        self.height = height
        self.containerHeight = height
        self.startDrag = False
        self.dragging = False
        self.reserved = 48
        self.inclination = 6
        self.dragTrail = 3
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
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.tabShadow = PFTabRenderer((self.tabMinWidth, self.height + 1), inclination = self.inclination)

    def OnSize(self, event):
        self.UpdateSize()
        event.Skip()

    def UpdateSize(self):
        width, dummy = self.GetSize()
        if width != self.width:
            self.width = width
            self.tabContainerWidth = self.width - self.reserved
            self.AdjustTabsSize()

    def OnLeftDown(self, event):
        mposx,mposy = event.GetPosition()
        if not self.startDrag:
            tab = self.FindTabAtPos(mposx, mposy)
            if tab:
                self.CheckTabSelected(tab, mposx, mposy)
                if self.showAddButton:
                    self.startDrag = True
                    tx,ty = tab.GetPosition()
                    self.dragx = mposx - tx
                    self.dragy = self.containerHeight - self.height
                self.Refresh()

            self.draggedTab = tab

    def OnLeftUp(self, event):
        mposx,mposy = event.GetPosition()
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

        if self.CheckAddButton(mposx, mposy):
            return

        if self.GetTabsCount() == 0:
            return
        selTab = self.GetSelectedTab()

        if self.CheckTabClose(selTab, mposx, mposy):
            return

#        if self.CheckTabSelected(selTab, mposx, mposy):
#            return

        for tab in self.tabs:

            if self.CheckTabClose(tab, mposx, mposy):
                return

#            if self.CheckTabSelected(tab, mposx, mposy):
#                return

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

    def CheckTabSelected(self,tab, mposx, mposy):
        oldSelTab = self.GetSelectedTab()
        if oldSelTab == tab:
            return True

        if self.TabHitTest(tab, mposx, mposy):
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

    def CheckTabClose(self, tab, mposx, mposy):
        if not tab.closeButton:
            return False

        closeBtnReg = tab.GetCloseButtonRegion()
        tabPosX, tabPosY = tab.GetPosition()

        closeBtnReg.Offset(tabPosX,tabPosY)

        if closeBtnReg.Contains(mposx, mposy):
            index = self.tabs.index(tab)
            ev = PageClosing(index)
            wx.PostEvent(self.Parent, ev)
            if ev.isVetoed():
                return False

            index = self.GetTabIndex(tab)
            self.DeleteTab(index)
            wx.PostEvent(self.Parent, PageClosed(index=index))
            sel = self.GetSelected()
            if sel  is not None:
                wx.PostEvent(self.Parent, PageChanged(-1, sel))
            return True
        return False

    def CheckAddButton(self, mposx,mposy):
        if not self.showAddButton:
            return
        reg = self.addButton.GetRegion()
        ax,ay = self.addButton.GetPosition()
        reg.Offset(ax,ay)
        if reg.Contains(mposx, mposy):
            ev = PageAdding()
            wx.PostEvent(self.Parent, ev)
            if ev.isVetoed():
                return False

            self.Parent.AddPage()
            wx.PostEvent(self.Parent, PageAdded())
            return True

    def CheckCloseButtons(self, mposx, mposy):
        dirty = False

        for tab in self.tabs:
            closeBtnReg = tab.GetCloseButtonRegion()
            tabPos = tab.GetPosition()
            tabPosX, tabPosY = tabPos
            closeBtnReg.Offset(tabPosX,tabPosY)
            if closeBtnReg.Contains(mposx,mposy):
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

    def TabHitTest(self, tab, x, y):
        tabRegion = tab.GetTabRegion()
        tabPos = tab.GetPosition()
        tabPosX, tabPosY = tabPos
        tabRegion.Offset(tabPosX, tabPosY)
        if tabRegion.Contains(x, y):
            return True
        return False

    def GetTabAtLeft(self, tabIndex):
        if tabIndex>0:
            return self.tabs[tabIndex - 1]
        else:
            return None

    def GetTabAtRight(self, tabIndex):
        if tabIndex < self.GetTabsCount() - 1:
            return self.tabs[tabIndex + 1]
        else:
            return None

    def SwitchTabs(self, src, dest, draggedTab = None):
        self.tabs[src], self.tabs[dest] = self.tabs[dest], self.tabs[src]
        self.UpdateTabsPosition(draggedTab)

        self.Parent.SwitchPages(src,dest, True)

        self.Refresh()

    def GetTabIndex(self, tab):
        return self.tabs.index(tab)

    def OnMotion(self, event):
        mposx,mposy = event.GetPosition()
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
                w,h = self.draggedTab.GetSize()

                if dtx < 0:
                    dtx = 0
                if dtx + w > self.tabContainerWidth + self.inclination * 2:
                    dtx = self.tabContainerWidth - w + self.inclination * 2
                self.draggedTab.SetPosition( (dtx, self.dragy))

                index = self.GetTabIndex(self.draggedTab)

                leftTab = self.GetTabAtLeft(index)
                rightTab = self.GetTabAtRight(index)

                if leftTab:
                    lw,lh = leftTab.GetSize()
                    lx,ly = leftTab.GetPosition()

                    if lx + lw / 2 - self.inclination * 2 > dtx:
                        self.SwitchTabs(index - 1 , index, self.draggedTab)
                        return

                if rightTab:
                    rw,rh = rightTab.GetSize()
                    rx,ry = rightTab.GetPosition()

                    if rx + rw / 2 + self.inclination * 2 < dtx + w:
                        self.SwitchTabs(index + 1 , index, self.draggedTab)
                        return
                self.UpdateTabsPosition(self.draggedTab)
                self.Refresh()
                return
            return
        self.CheckCloseButtons(mposx, mposy)

        self.CheckAddHighlighted(mposx,mposy)
        self.CheckTabPreview(mposx, mposy)
        event.Skip()

    def CheckTabPreview(self, mposx, mposy):

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
                            self.previewTimer.Start(1500, True)
                            break
                    except:
                        pass


    def CheckAddHighlighted(self, mposx, mposy):
        if not self.showAddButton:
            return
        reg = self.addButton.GetRegion()
        ax,ay = self.addButton.GetPosition()
        reg.Offset(ax,ay)
        if reg.Contains(mposx, mposy):
            self.addButton.Highlight(True)
        else:
            self.addButton.Highlight(False)

        self.Refresh()

    def OnPaint(self, event):
        rect = self.GetRect()
        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)

        selected = 0
        # TODO
        # This is a hack because on mac os the system colour constants are somehow wrong,
        # additionally somehow the colors get changed when drawing (all RGB values are off by 4)
        # TODO
        if 'wxMac' in wx.PlatformInfo:
            color = wx.Colour(232, 232, 232)
        else:
            color = wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE)
        mdc.SetBackground (wx.Brush(color))

#        mdc.SetBackground (wx.Brush((66,113,202)))
        mdc.Clear()

        selected = None
        selpos = 0
        selWidth = selHeight = 0
        selColor = self.CalculateColor(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW), 0x66)
        startColor = self.leftColor = self.CalculateColor(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW), 0x50)
        tabsWidth = 0


        for tab in self.tabs:
            tabsWidth += tab.tabWidth - self.inclination*2

        pos = tabsWidth
        if self.showAddButton:
            ax,ay = self.addButton.GetPosition()
            mdc.DrawBitmap(self.addButton.Render(), ax, ay, True)

        for i in xrange(len(self.tabs) - 1, -1, -1):
            tab = self.tabs[i]
            width = tab.tabWidth - 6
            posx, posy  = tab.GetPosition()
            if not tab.IsSelected():
#                if not 'wxMac' in wx.PlatformInfo:
                mdc.DrawBitmap(self.efxBmp, posx, posy, True )
                img = tab.Render().ConvertToImage()
                img = img.AdjustChannels(1, 1, 1, 0.8)
                bmp = wx.BitmapFromImage(img)
                mdc.DrawBitmap(bmp, posx, posy, True)
            else:
                selected = tab
        if selected:
            posx, posy  = selected.GetPosition()
#            if not 'wxMac' in wx.PlatformInfo:
            mdc.DrawBitmap(self.efxBmp, posx, posy, True)
            bmp = selected.Render()
            if self.dragging:
                img = bmp.ConvertToImage()
                img = img.AdjustChannels(1.2, 1.2, 1.2, 0.7)
                bmp = wx.BitmapFromImage(img)

            mdc.DrawBitmap(bmp, posx, posy, True)
            selpos = posx
            selWidth,selHeight = selected.GetSize()

        if selWidth%2:
            offset = 1
        else:
            offset = 0
        r1 = wx.Rect(0,self.containerHeight -1,selpos,1)
        r2 = wx.Rect(0, self.containerHeight -1 , self.width,1)
#        mdc.GradientFillLinear(r1, startColor, selColor, wx.EAST)
#        mdc.GradientFillLinear(r2, selColor, startColor, wx.EAST)

    def OnErase(self, event):
        pass

    def UpdateTabFX(self):
        w,h = self.tabShadow.GetSize()
        if w != self.tabMinWidth:
            self.tabShadow.SetSize((self.tabMinWidth, self.height + 1))
            fxBmp = self.tabShadow.Render()

            simg = fxBmp.ConvertToImage()
            if not simg.HasAlpha():
                simg.InitAlpha()
#            if 'wxMac' not in wx.PlatformInfo:
            simg = simg.Blur(2)
            simg = simg.AdjustChannels(0.3,0.3,0.3,0.3)

            self.efxBmp = wx.BitmapFromImage(simg)

    def AddTab(self, title = wx.EmptyString, img = None, showClose = False):
        self.ClearTabsSelected()

        tabRenderer = PFTabRenderer( (120,self.height), title, img, self.inclination, closeButton = showClose)
        tabRenderer.SetSelected(True)

        self.tabs.append( tabRenderer )
        self.AdjustTabsSize()
        self.Refresh()

    def ClearTabsSelected(self):
        for tab in self.tabs:
            tab.SetSelected(False)

    def DeleteTab(self, tab, external = False):
        tabRenderer = self.tabs[tab]
        wasSelected = tabRenderer.GetSelected()
        self.tabs.remove(tabRenderer)

        if tabRenderer:
            del tabRenderer

        if wasSelected and self.GetTabsCount() > 0:
            if tab > self.GetTabsCount() -1:
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

        tabMinWidth = 9000000 # Really, it should be over 9000
        tabMaxWidth = 0
        for tab in self.tabs:
            mw,mh = tab.GetMinSize()
            if tabMinWidth > mw:
                tabMinWidth = mw
            if tabMaxWidth < mw:
                tabMaxWidth = mw
        if tabMaxWidth < 100:
            tabMaxWidth = 100
        if self.GetTabsCount() >0:
            if (self.GetTabsCount()) * (tabMaxWidth - self.inclination * 2) > self.tabContainerWidth:
                self.tabMinWidth = float(self.tabContainerWidth) / float(self.GetTabsCount()) + self.inclination * 2
            else:
                self.tabMinWidth = tabMaxWidth

        if self.tabMinWidth <1:
            self.tabMinWidth = 1
        for tab in self.tabs:
            w,h = tab.GetSize()
            tab.SetSize( (self.tabMinWidth, self.height) )

        if self.GetTabsCount() > 0:
            self.UpdateTabFX()

        self.UpdateTabsPosition()

    def UpdateTabsPosition(self, skipTab = None):
        tabsWidth = 0
        for tab in self.tabs:
            tabsWidth += tab.tabWidth - self.inclination*2

        pos = tabsWidth
        selected = None
        for i in xrange(len(self.tabs) - 1, -1, -1):
            tab = self.tabs[i]
            width = tab.tabWidth - self.inclination*2
            pos -= width
            if not tab.IsSelected():
                tab.SetPosition((pos, self.containerHeight - self.height))
            else:
                selected = tab
                selpos = pos
        if selected is not skipTab:
            selected.SetPosition((selpos, self.containerHeight - self.height))
        self.addButton.SetPosition((round(tabsWidth) + self.inclination*2, self.containerHeight - self.height/2 - self.addButton.GetHeight()/2))

    def CalculateColor(self, color, delta):
        bkR ,bkG , bkB = color
        if bkR + bkG + bkB > 127*3:
            scale = - delta
        else:
            scale = delta*2

        r = bkR + scale
        g = bkG + scale
        b = bkB + scale

        r = min(max(r,0),255)
        g = min(max(g,0),255)
        b = min(max(b,0),255)

        return wx.Colour(r,g,b)

    def OnLeaveWindow(self, event):
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
                    self.previewWnd = PFNotebookPagePreview(self,(mposx+3,mposy+3), page.Snapshot(), self.previewTab.text)
                    self.previewWnd.Show()

        event.Skip()

class PFNotebookPagePreview(wx.Frame):
    def __init__ (self,parent, pos, bitmap, title):
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = pos, size = wx.DefaultSize, style =
                                                               wx.NO_BORDER
                                                             | wx.FRAME_NO_TASKBAR
                                                             | wx.STAY_ON_TOP)
        img = bitmap.ConvertToImage()
        img = img.ConvertToGreyscale()
        bitmap = wx.BitmapFromImage(img)
        self.title = title
        self.bitmap = bitmap
        self.SetSize((bitmap.GetWidth(), bitmap.GetHeight()))
        self.Bind(wx.EVT_PAINT,self.OnWindowPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnWindowEraseBk)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        self.timer = wx.Timer(self,wx.ID_ANY)
        self.timerSleep = None
        self.timerSleepId = wx.NewId()
        self.direction = 1
        self.padding = 15
        self.transp = 0

        hfont = wx.FontFromPixelSize((0,14), wx.SWISS, wx.NORMAL,wx.NORMAL, False)
        self.SetFont(hfont)

        tx, ty = self.GetTextExtent(self.title)
        tx +=  self.padding * 2

        if bitmap.GetWidth() < tx:
            width = tx
        else:
            width = bitmap.GetWidth()

        self.SetSize((width, bitmap.GetHeight()+16))

        self.SetTransparent(0)
        self.Refresh()

    def OnTimer(self, event):
        self.transp += 20*self.direction

        if self.transp > 240:
            self.transp = 240
            self.timer.Stop()

        if self.transp < 0:
            self.transp = 0
            self.timer.Stop()
            wx.Frame.Show(self,False)
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

    def Show(self, showWnd = True):
        if showWnd:
            wx.Frame.Show(self, showWnd)
            self.RaiseParent()
            self.direction = 1
            self.timer.Start(10)
        else:
            self.direction = -1
            self.timer.Start(10)


    def OnWindowEraseBk(self,event):
        pass

    def OnWindowPaint(self,event):
        rect = self.GetRect()
        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)
        color = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        mdc.SetBackground(wx.Brush(color))
        mdc.Clear()

        font = wx.FontFromPixelSize((0,14), wx.SWISS, wx.NORMAL,wx.NORMAL, False)
        mdc.SetFont(font)

        x,y = mdc.GetTextExtent(self.title)

        mdc.SetBrush(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT)))
        mdc.DrawRectangle(0,0,rect.width,16)

        mdc.SetTextForeground(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))

        mdc.DrawText(self.title, (rect.width - x)/2, (16 -y)/2)

        mdc.DrawBitmap(self.bitmap, 0, 16)

        mdc.SetPen( wx.Pen("#000000", width = 1 ) )
        mdc.SetBrush( wx.TRANSPARENT_BRUSH )

        mdc.DrawRectangle( 0, 16, rect.width,rect.height - 16)
