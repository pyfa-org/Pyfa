import wx
import copy
import time

class PFTabRenderer:
    def __init__(self, size = (36,24), text = wx.EmptyString, img = None, inclination = 6 , closeButton = True, fontSize = 8):

        # tab left/right zones inclination
        self.inclination = inclination
        self.text = text
        self.img = img
        self.tabSize = size
        self.closeButton = closeButton
        self.fontSize = fontSize
        self.selected = False
        self.closeBtnHovering = False
        self.tabBitmap = None
        self.cbSize = 6
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
        self.tabSize = size
        w,h = self.tabSize
        if h != oth:
            self.InitTab(True)
        else:
            self.InitTab()

    def SetSelected(self, sel = True):
        self.selected = sel
        self.InitColors()
        self._Render()

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
        mdc = wx.MemoryDC()
        mdc.SetFont(self.font)
        textSizeX, textSizeY = mdc.GetTextExtent(self.text)
        totalSize = self.lrZoneWidth * 2 + textSizeX + self.cbSize*2 if self.closeButton else 0
        return (totalSize, self.tabHeight)


    def CopyRegion(self, region):
        rect = region.GetBox()

        newRegion = wx.Region(rect.X, rect.Y, rect.Width, rect.Height)
        newRegion.IntersectRegion(region)

        return newRegion
    def InitTab(self, skipLRzones = False):
        self.tabWidth, self.tabHeight = self.tabSize

        # content width is tabWidth - (left+right) zones

        self.contentWidth = self.tabWidth - self.inclination * 6 - self.cbSize if self.closeButton else 0

        self.leftZoneSpline = []
        self.rightZoneSpline = []

        self.lrZoneWidth = self.inclination * 3
        if not skipLRzones:
            self.CreateLRZoneSplines()

            self.leftRegion = self.CreateLeftRegion()
            self.rightRegion = self.CreateRightRegion()

        self.contentRegion = wx.Region(0, 0, self.contentWidth, self.tabHeight)
        self.tabRegion = None
        self.closeBtnRegion = None
        self.font = wx.Font(self.fontSize, wx.SWISS, wx.NORMAL, wx.NORMAL, False)

        self.InitTabRegions()
        self.InitColors()
        self._Render()

    def InitColors(self):
        self.tabColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        self.leftColor = self.CalculateColor(self.tabColor, 0x1F)
        self.rightColor = self.CalculateColor(self.tabColor, 0x24)
        self.gradientStartColor = self.CalculateColor(self.tabColor, 0x17 if self.selected else 0x27)

    def CalculateColor(self, color, delta):
        bkR ,bkG , bkB = color
        if bkR + bkG + bkB > 127*3:
            scale = - delta
        else:
            scale = delta*2

        r = bkR + scale
        g = bkG + scale
        b = bkB + scale

        if r > 255: r = 255
        if r < 0: r = 0
        if g > 255: g = 255
        if g < 0: g = 0
        if b > 255: b = 255
        if b < 0: b = 0

        return wx.Colour(r,b,g)

    def InitTabRegions(self):
        self.tabRegion = wx.Region(0, 0, self.tabWidth, self.tabHeight)
        self.tabRegion.IntersectRegion(self.leftRegion)

        self.contentRegion.Offset(self.lrZoneWidth, 0)
        self.tabRegion.UnionRegion(self.contentRegion)

        self.rightRegion.Offset(self.tabWidth - self.lrZoneWidth, 0)
        self.tabRegion.UnionRegion(self.rightRegion)
        self.closeBtnRegion = wx.Region(self.tabWidth - self.lrZoneWidth - self.cbSize -2 , (self.tabHeight - self.cbSize) / 2 - 2, self.cbSize + 4, self.cbSize + 4)
        cbtRegion = wx.Region(self.tabWidth - self.lrZoneWidth - self.cbSize ,0, self.cbSize, self.tabHeight)
        self.tabRegion.UnionRegion(cbtRegion)

    def CreateLRZoneSplines(self):
        height = self.tabHeight
        inc = self.inclination

        self.leftZoneSpline = [wx.Point(0, height), wx.Point(inc * 2/3, height - inc/2), wx.Point(inc+inc/2, 2),
                 wx.Point(inc * 3, 0)]
        self.rightZoneSpline = [wx.Point(0, 0), wx.Point(inc+inc/2,2),wx.Point(inc*2 +inc*2/3,height-inc/2), wx.Point(inc*3,height) ]

    def CreateLeftRegion(self):

        width = self.lrZoneWidth + 1
        height = self.tabHeight + 1
        inc = self.inclination

        mdc = wx.MemoryDC()

        mbmp = wx.EmptyBitmap(width,height)
        mdc.SelectObject(mbmp)

        mdc.SetBackground( wx.Brush((255,255,255)))
        mdc.Clear()

        mdc.SetPen( wx.Pen("#000000", width = 1 ) )
        mdc.DrawSpline(self.leftZoneSpline)

        mdc.SetBrush(wx.Brush((255,255,0)))
        mdc.FloodFill(inc*2,height-2, wx.Color(0,0,0), wx.FLOOD_BORDER)

        mdc.SelectObject(wx.NullBitmap)

        mbmp.SetMaskColour( (255, 255, 255) )

        region = wx.RegionFromBitmap(mbmp)
        region.Offset(-1,0)

        return region

    def CreateRightRegion(self):

        width = self.lrZoneWidth + 1
        height = self.tabHeight
        inc = self.inclination

        mdc = wx.MemoryDC()

        mbmp = wx.EmptyBitmap(width,height)
        mdc.SelectObject(mbmp)

        mdc.SetBackground( wx.Brush((255,255,255)))
        mdc.Clear()

        mdc.SetPen( wx.Pen("#000000", width = 1 ) )
        mdc.DrawSpline(self.rightZoneSpline)

        mdc.SetBrush(wx.Brush((255,255,0)))
        mdc.FloodFill(inc,height-inc, wx.Color(0,0,0), wx.FLOOD_BORDER)

        mdc.SelectObject(wx.NullBitmap)

        mbmp.SetMaskColour( (255, 255, 255) )

        region = wx.RegionFromBitmap(mbmp)

        return region

    def OffsetPointList(self, list , x, y):
        tlist = []
        for i in list:
            tlist.append(wx.Point(i.x + x, i.y + y))

        return tlist

    def Render(self):
        return self.tabBitmap

    def _Render(self):
        if self.tabBitmap:
            del self.tabBitmap

        inc = self.lrZoneWidth
        height = self.tabHeight
        width = self.tabWidth
        contentWidth = self.contentWidth + self.cbSize if self.closeButton else 0

        rect = wx.Rect(0,0,self.tabWidth, self.tabHeight)

        canvas = wx.EmptyBitmap(rect.width, rect.height)

        mdc = wx.MemoryDC()

        mdc.SelectObject(canvas)
        mdc.SetBackground(wx.Brush ((13,22,31)))
        mdc.Clear()
        mdc.DestroyClippingRegion()
        mdc.SetClippingRegionAsRegion(self.tabRegion)

        r = copy.copy(rect)
        r.top = r.left = 0
        r.height = height

        mdc.GradientFillLinear(r,self.gradientStartColor,self.tabColor,wx.SOUTH)
        mdc.SetPen( wx.Pen(self.leftColor, width = 1 ) )

        dpleft = self.OffsetPointList(self.leftZoneSpline, -1, 0)
        dpright = self.OffsetPointList(self.rightZoneSpline, inc + contentWidth, 0)

        mdc.DrawSpline(dpleft)
        mdc.SetPen( wx.Pen(self.rightColor, width = 1 ) )
        mdc.DrawSpline(dpright)

        lrect = wx.Rect()
        lrect.left=inc - 1
        lrect.top=0
        lrect.width = contentWidth+1
        lrect.height = 1
        mdc.GradientFillLinear(lrect,self.leftColor,self.rightColor, wx.EAST)
#        if not self.selected:
#            mdc.DrawLine(0,height - 1,width,height - 1)
        mdc.SetPen( wx.Pen(self.rightColor, width = 2 ) )
        if self.closeButton:
            cbsize = self.cbSize

            if self.closeBtnHovering:
                mdc.SetPen( wx.Pen( wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT), 2))

            cbx = width - self.lrZoneWidth-cbsize
            cby = (height - cbsize)/2
            mdc.DrawLine(cbx, cby, cbx + cbsize , cby + cbsize )
            mdc.DrawLine(cbx, cby + cbsize, cbx + cbsize , cby )

        mdc.SetClippingRegionAsRegion(self.contentRegion)
        mdc.SetFont(self.font)
        text = self.text
        fnwidths = mdc.GetPartialTextExtents(text)
        count = 0
        maxsize = self.contentWidth - self.cbSize if self.closeButton else 0
        for i in fnwidths:
            if i <= maxsize:
                count +=1
            else:
                break

#        text = "%s%s" % (text[:count],"." if len(text)>count else "")
        text = "%s" % text[:count]


        tx,ty = mdc.GetTextExtent(text)
        if self.selected:
            mdc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        else:
            color = self.CalculateColor(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT), 0x44)
            mdc.SetTextForeground(color)
        mdc.DrawText(text, inc, height / 2 - ty / 2)

        mdc.DestroyClippingRegion()

        mdc.SelectObject(wx.NullBitmap)
        canvas.SetMaskColour((13,22,31))

        self.tabBitmap = canvas

class PFAddRenderer:
    def __init__(self, size = (24,12)):
        self.width, self.height = size
        self.addBitmap = None
        self.spline = []
        self.inclination = 3
        self.region = None
        self.InitRenderer()

    def GetSize(self):
        return (self.width, self.height)

    def InitRenderer(self):
        self.CreateSpline()
        self.region = self.CreateRegion()
        self._Render()

    def CreateSpline(self):
        width = self.width
        height = self.height - 1
        inc = self.inclination

        self.spline = [wx.Point(0, 0), wx.Point(inc*3/2, height),wx.Point(inc*2 + inc*2/3, height), wx.Point(width, height), wx.Point(width, height),
                       wx.Point(width - inc, inc), wx.Point(width - inc*2, 0), wx.Point(0, 0), wx.Point(0, 0)]
    def CreateRegion(self):
        width = self.width
        height = self.height
        inc = self.inclination

        mdc = wx.MemoryDC()

        mbmp = wx.EmptyBitmap(width,height)
        mdc.SelectObject(mbmp)

        mdc.SetBackground( wx.Brush((255,255,255)))
        mdc.Clear()

        mdc.SetPen( wx.Pen("#000000", width = 1 ) )
        mdc.DrawSpline(self.spline)

        mdc.SetBrush(wx.Brush((255,255,0)))
        mdc.FloodFill(width/2,height/2, wx.Color(0,0,0), wx.FLOOD_BORDER)

        mdc.SelectObject(wx.NullBitmap)

        mbmp.SetMaskColour( (255, 255, 255) )

        region = wx.RegionFromBitmap(mbmp)
#        region.Offset(-1,0)

        return region

    def CalculateColor(self, color, delta):
        bkR ,bkG , bkB = color
        if bkR + bkG + bkB > 127*3:
            scale = - delta
        else:
            scale = delta*2

        r = bkR + scale
        g = bkG + scale
        b = bkB + scale

        if r > 255: r = 255
        if r < 0: r = 0
        if g > 255: g = 255
        if g < 0: g = 0
        if b > 255: b = 255
        if b < 0: b = 0

        return wx.Colour(r,b,g)

    def Render(self):
        return self.addBitmap

    def _Render(self):
        inc = self.inclination
        rect = wx.Rect(0 ,0 ,self.width, self.height)
        if self.addBitmap:
            del self.addBitmap

        canvas = wx.EmptyBitmap(self.width, self.height)

        mdc = wx.MemoryDC()
        mdc.SelectObject(canvas)

        mdc.SetBackground(wx.Brush ((13,22,31)))
        mdc.Clear()

        mdc.DestroyClippingRegion()
        mdc.SetClippingRegionAsRegion(self.region)
#        mdc.GradientFillLinear(rect, (0x30,0x30,0x30), (0x6f,0x6f,0x6f), wx.SOUTH)
        mdc.FloodFill(self.width/2,self.height/2, wx.Color(13,22,31), wx.FLOOD_BORDER)
        mdc.DestroyClippingRegion()
        mdc.SetPen( wx.Pen( wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT), 1))
        mdc.DrawSpline(self.spline)
        mdc.SelectObject(wx.NullBitmap)

        canvas.SetMaskColour((13,22,31))

        img = canvas.ConvertToImage()
        img.InitAlpha()
        img = img.AdjustChannels(1, 1, 1, 0.6)
        img = img.Blur(1)
        bbmp = wx.BitmapFromImage(img)

        del mdc
        del canvas
        canvas = wx.EmptyBitmap(self.width, self.height)

        mdc = wx.MemoryDC()
        mdc.SelectObject(canvas)

        mdc.SetBackground(wx.Brush ((255,255,255 , 0)))
        mdc.Clear()

        mdc.DrawBitmap(bbmp,0,0,True)

        cx = self.width / 2 - 1
        cy = self.height / 2

        mdc.SetPen( wx.Pen( wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT), 1))
        mdc.DrawLine(cx - inc + 1, cy, cx + inc + 1, cy)
        mdc.DrawLine(cx - inc + 1, cy-1, cx + inc + 1, cy-1)
        mdc.DrawLine(cx, cy - inc, cx, cy + inc )
        mdc.DrawLine(cx+1, cy - inc, cx+1, cy + inc )

        self.wColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        color = self.CalculateColor(self.wColor, 0x99)
        mdc.SetPen( wx.Pen( color, 1))

        mdc.DrawSpline(self.spline)

        mdc.SelectObject(wx.NullBitmap)
        canvas.SetMaskColour((255,255,255))

        img = canvas.ConvertToImage()

        img.InitAlpha()
        img = img.AdjustChannels(1, 1, 1, 0.3)

        bbmp = wx.BitmapFromImage(img)
        self.addBitmap = bbmp


class PFTabsContainer(wx.Window):
    def __init__(self, parent, pos = (0,0), size = (100,24), id = wx.ID_ANY):
        wx.Window.__init__(self, parent, id , pos, size , style = 0)
        self.tabs = []
        width, height = size
        self.width  = width
        self.height = height
        self.startDrag = False
        self.dragging = False
        self.reserved = 48
        self.inclination = 6
        self.dragx = 0
        self.dragy = 0
        self.draggedTab = None
        self.dragTrigger = 5

        self.tabContainerWidth = width - self.reserved
        self.tabMinWidth = width
        self.tabShadow = None

        self.addButton = PFAddRenderer()
        self.addBitmap = self.addButton.Render()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)

        self.tabShadow = PFTabRenderer((self.tabMinWidth, self.height))

    def OnLeftDown(self, event):
        mposx,mposy = event.GetPosition()
        if not self.startDrag:
            tab = self.FindTabAtPos(mposx, mposy)
            if tab:
                for tabs in self.tabs:
                    tabs.SetSelected(False)
                tab.SetSelected(True)
                self.startDrag = True
                tx,ty = tab.GetPosition()
                self.dragx = mposx - tx
                self.dragy = 0
                self.Refresh()

            self.draggedTab = tab

    def OnLeftUp(self, event):
        mposx,mposy = event.GetPosition()
        if self.startDrag and self.dragging:
            self.dragging = False
            self.startDrag = False
            self.draggedTab = None
            self.dragTrigger = 5
            self.UpdateTabsPosition()
            self.Refresh()
            return

        if self.startDrag:
            self.startDrag = False
            self.dragTrigger = 5

        seltab = None
        oldSelTab = None
        for tab in self.tabs:
            if tab.GetSelected():
                oldSelTab = tab
                break
        count = 0
        for tab in self.tabs:
            tabRegion = tab.GetTabRegion()
            closeBtnReg = tab.GetCloseButtonRegion()
            tabPos = tab.GetPosition()
            tabPosX, tabPosY = tabPos
            tabRegion.Offset(tabPosX, tabPosY)
            closeBtnReg.Offset(tabPosX,tabPosY)

            if closeBtnReg.Contains(mposx, mposy):
                print "Close tab: %s" % tab.text
                self.DeleteTab(count)
                return

            if tabRegion.Contains(mposx, mposy):
                tab.SetSelected(True)
                if tab != oldSelTab:
                    oldSelTab.SetSelected(False)
                self.Refresh()
                print "Selected: %s" %tab.text
                break
            count += 1
        event.Skip()

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
        for tab in self.tabs:
            tabRegion = tab.GetTabRegion()
            tabPos = tab.GetPosition()
            tabPosX, tabPosY = tabPos
            tabRegion.Offset(tabPosX, tabPosY)
            if tabRegion.Contains(x, y):
                return tab
        return None

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
        self.Refresh()

    def OnMotion(self, event):
        mposx,mposy = event.GetPosition()
        if self.startDrag:
            if not self.dragging:
                if self.dragTrigger < 0:
                    self.dragging = True
                    self.dragTrigger = 5
                else:
                    self.dragTrigger -= 1
            if self.dragging:
                self.draggedTab.SetPosition( (mposx - self.dragx, self.dragy))
                w,h = self.draggedTab.GetSize()

                index = self.tabs.index(self.draggedTab)

                leftTab = self.GetTabAtLeft(index)
                rightTab = self.GetTabAtRight(index)

                dtx = mposx - self.dragx

                if leftTab:
                    lw,lh = leftTab.GetSize()
                    lx,ly = leftTab.GetPosition()

                    if lx + lw / 2 - 5> dtx:
                        self.SwitchTabs(index - 1 , index, self.draggedTab)
                        return

                if rightTab:
                    rw,rh = rightTab.GetSize()
                    rx,ry = rightTab.GetPosition()

                    if rx + rw / 2 + 5 < dtx + w:
                        self.SwitchTabs(index + 1 , index, self.draggedTab)
                        return
                self.UpdateTabsPosition(self.draggedTab)
                self.Refresh()
                return
            return
        self.CheckCloseButtons(mposx, mposy)

        event.Skip()

    def OnPaint(self, event):
        rect = self.GetRect()
        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)

        selected = 0

        mdc.SetBackground (wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)))
#        mdc.SetBackground (wx.Brush((66,113,202)))
        mdc.Clear()

        selected = None
        selpos = 0
        selWidth = selHeight = 0
        selColor = self.CalculateColor(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW), 0x24)
        startColor = self.leftColor = self.CalculateColor(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW), 0x12)
        tabsWidth = 0


        for tab in self.tabs:
            tabsWidth += tab.tabWidth - tab.lrZoneWidth/2

        pos = tabsWidth

        mdc.DrawBitmap(self.addBitmap, round(tabsWidth) + 6, self.height/2 - self.addBitmap.GetHeight()/2, True)

        for i in xrange(len(self.tabs) - 1, -1, -1):
            tab = self.tabs[i]
            width = tab.tabWidth - tab.lrZoneWidth/2
            posx, posy  = tab.GetPosition()
            if not tab.IsSelected():
                mdc.DrawBitmap(self.efxBmp, posx, posy)
                mdc.DrawBitmap(tab.Render(), posx, posy, True)
            else:
                selected = tab
        if selected:
            posx, posy  = selected.GetPosition()
            mdc.DrawBitmap(self.efxBmp, posx, posy, True)
            mdc.DrawBitmap(selected.Render(), posx, posy, True)
            selpos = posx
            selWidth,selHeight = selected.GetSize()

#        mdc.SetPen( wx.Pen( selColor, 1))
#        mdc.DrawLine(0,self.height-1,selpos,self.height-1)
#        mdc.DrawLine(selpos + selWidth,self.height-1,self.width,self.height-1)
        r1 = wx.Rect(0,self.height-1,selpos,1)
        r2 = wx.Rect(selpos + selWidth,self.height -1, self.width - selpos - selWidth,1)
        mdc.GradientFillLinear(r1, startColor, selColor, wx.EAST)
        mdc.GradientFillLinear(r2, selColor, startColor, wx.EAST)

    def OnErase(self, event):
        pass

    def UpdateTabFX(self):
        w,h = self.tabShadow.GetSize()
        if w != self.tabMinWidth:
            self.tabShadow.SetSize((self.tabMinWidth, self.height))
            fxBmp = self.tabShadow.Render()

            simg = fxBmp.ConvertToImage()
            simg.InitAlpha()
            simg = simg.Blur(2)
            simg = simg.AdjustChannels(1,1,1,0.3)

            self.efxBmp = wx.BitmapFromImage(simg)

    def AddTab(self, title = wx.EmptyString, img = None):
        self.ClearTabsSelected()

        tabRenderer = PFTabRenderer( (120,self.height), title, img)
        tabRenderer.SetSelected(True)

        self.tabs.append( tabRenderer )
        self.AdjustTabsSize()
        self.Refresh()

    def ClearTabsSelected(self):
        for tab in self.tabs:
            tab.SetSelected(False)

    def DeleteTab(self, tab):
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
        self.AdjustTabsSize()
        self.Refresh()

    def GetTabsCount(self):
        return len(self.tabs)

    def AdjustTabsSize(self):

        tabMinWidth = 9000000 # Really, it should be over 9000

        for tab in self.tabs:
            mw,mh = tab.GetMinSize()
            if tabMinWidth > mw:
               tabMinWidth = mw

        if self.GetTabsCount() >0:
            if (self.GetTabsCount()) * (tabMinWidth - 9) > self.tabContainerWidth - self.reserved:
                self.tabMinWidth = float(self.tabContainerWidth - self.reserved) / float(self.GetTabsCount()) + 9
            else:
                self.tabMinWidth = tabMinWidth

        for tab in self.tabs:
            w,h = tab.GetSize()
            if w != self.tabMinWidth:
                tab.SetSize( (self.tabMinWidth, self.height) )

        if self.GetTabsCount() > 0:
            self.UpdateTabFX()

        self.UpdateTabsPosition()

    def UpdateTabsPosition(self, skipTab = None):
        tabsWidth = 0
        for tab in self.tabs:
            tabsWidth += tab.tabWidth - tab.lrZoneWidth/2

        pos = tabsWidth

        for i in xrange(len(self.tabs) - 1, -1, -1):
            tab = self.tabs[i]
            width = tab.tabWidth - tab.lrZoneWidth/2
            pos -= width
            if not tab.IsSelected():
                tab.SetPosition((pos, 0))
            else:
                selected = tab
                selpos = pos
        if selected is not skipTab:
            selected.SetPosition((selpos, 0))


    def CalculateColor(self, color, delta):
        bkR ,bkG , bkB = color
        if bkR + bkG + bkB > 127*3:
            scale = - delta
        else:
            scale = delta*2

        r = bkR + scale
        g = bkG + scale
        b = bkB + scale

        if r > 255: r = 255
        if r < 0: r = 0
        if g > 255: g = 255
        if g < 0: g = 0
        if b > 255: b = 255
        if b < 0: b = 0

        return wx.Colour(r,b,g)

class MiniFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'MEGA Frame',
                size=(1000, 100), style = wx.FRAME_SHAPED)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
#        self.Bind(wx.EVT_PAINT, self.OnPaint)
#        self.Bind(wx.EVT_ERASE_BACKGROUND,self.OnErase)
#        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
#        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
#        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.SetBackgroundColour( (0xff,0xff,0xff))

        self.drag = False
        self.font8px = wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False)
        self.tabContainer = PFTabsContainer(self, (0,5), (1000,24))
        self.tabContainer.Show()
        for i in xrange(10):
            self.tabContainer.AddTab("Pyfa TAB #%d Aw" % i)

        self.Refresh()

    def OnLeftDown(self, event):
        event.Skip()

    def OnErase(self, event):
        pass
    def OnCloseWindow(self, event):
        self.Destroy()


#    def OnPaint(self, event):
#        rect = self.GetRect()
#        canvas = wx.EmptyBitmap(rect.width, rect.height)
#        mdc = wx.BufferedPaintDC(self)
#        mdc.SelectObject(canvas)
#
#        mdc.SetBackground (wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)))
#        mdc.Clear()
#
#        selected = None
#        selpos = 0
#        tabsWidth = 0
#        offset = 10
#
#        for tab in self.tabs:
#            tabsWidth += tab.tabWidth - tab.lrZoneWidth/2
#
#        pos = tabsWidth
#
#        for i in xrange(len(self.tabs) - 1, -1, -1):
#            tab = self.tabs[i]
#            width = tab.tabWidth - tab.lrZoneWidth/2
#            pos -= width
#            if not tab.IsSelected():
#                mdc.DrawBitmap(tab.Render(),pos+offset,10, True)
#                tab.SetPosition((pos + offset, 10))
#            else:
#                selected = tab
#                selpos = pos + offset
#        if selected:
#            mdc.DrawBitmap(selected.Render(), selpos,10,True)
#            selected.SetPosition((selpos, 10))
#
#        mdc.SetPen( wx.Pen("#D0D0D0", width = 1 ) )
#        mdc.DrawLine(10,34,10,100)
#        mdc.DrawLine(10,100,tabsWidth + 18,100)
#        mdc.DrawLine(tabsWidth+18,100,tabsWidth+18,33)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    MiniFrame().Show()
    app.MainLoop()
