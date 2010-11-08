import wx
import copy

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
        self.tabSize = size
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

    def GetTabRegion(self):
        nregion = self.CopyRegion(self.tabRegion)
        nregion.SubtractRegion(self.closeBtnRegion) if self.closeButton else self.tabRegion
        return nregion

    def GetCloseButtonRegion(self):
        return self.CopyRegion(self.closeBtnRegion)

    def GetMinSize(self):
        self.InitTab()
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
    def InitTab(self):
        self.tabWidth, self.tabHeight = self.tabSize

        # content width is tabWidth - (left+right) zones

        self.contentWidth = self.tabWidth - self.inclination * 6 - self.cbSize if self.closeButton else 0

        self.leftZoneSpline = []
        self.rightZoneSpline = []

        self.lrZoneWidth = self.inclination * 3

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
        self.rightColor = self.CalculateColor(self.tabColor, 0x20)
        self.gradientStartColor = self.CalculateColor(self.tabColor, 0x17 if self.selected else 0x27)

    def CalculateColor(self, color, delta):
        bkR ,bkG , bkB = color
        if bkR + bkG + bkB > 127*3:
            scale = - delta
        else:
            scale = delta*2
        return wx.Colour(bkR + scale, bkG + scale, bkR + scale)

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
        if not self.selected:
            mdc.DrawLine(0,height - 1,width,height - 1)
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
        mdc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        mdc.DrawText(text, inc, height / 2 - ty / 2)

        mdc.DestroyClippingRegion()

        mdc.SelectObject(wx.NullBitmap)
        canvas.SetMaskColour((13,22,31))

        self.tabBitmap = canvas

class PFTabsContainer(wx.Window):
    def __init__(self, parent, pos = (0,0), size = (100,24), id = wx.ID_ANY):
        wx.Window.__init__(self, parent, id , pos, size , style = 0)
        self.tabs = []
        width, height = size
        self.height = height
        self.reserved = 24
        self.tabContainerWidth = width - self.reserved
        self.tabMinWidth = 0
        self.tabShadow = None

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)

    def OnLeftUp(self, event):
        mposx,mposy = event.GetPosition()
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

    def OnMotion(self, event):
        mposx,mposy = event.GetPosition()
        for tab in self.tabs:
            closeBtnReg = tab.GetCloseButtonRegion()
            tabPos = tab.GetPosition()
            tabPosX, tabPosY = tabPos
            closeBtnReg.Offset(tabPosX,tabPosY)
            if closeBtnReg.Contains(mposx,mposy):
                tab.ShowCloseButtonHovering(True)
            else:
                tab.ShowCloseButtonHovering(False)

        self.Refresh()
        event.Skip()

    def OnPaint(self, event):
        rect = self.GetRect()
        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)

        selected = 0

        mdc.SetBackground (wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)))
        mdc.Clear()

        selected = None
        selpos = 0
        tabsWidth = 0

        for tab in self.tabs:
            tabsWidth += tab.tabWidth - tab.lrZoneWidth/2

        pos = tabsWidth

        for i in xrange(len(self.tabs) - 1, -1, -1):
            tab = self.tabs[i]
            width = tab.tabWidth - tab.lrZoneWidth/2
            pos -= width
            if not tab.IsSelected():
                mdc.DrawBitmap(self.efxBmp, pos, 0)
                mdc.DrawBitmap(tab.Render(), pos, 0, True)
                tab.SetPosition((pos, 0))
            else:
                selected = tab
                selpos = pos
        if selected:
            mdc.DrawBitmap(self.efxBmp, selpos, 0, True)
            mdc.DrawBitmap(selected.Render(), selpos, 0, True)
            selected.SetPosition((selpos, 0))

    def OnErase(self, event):
        pass

    def CreateShadow(self):
        self.tabShadow = PFTabRenderer( (self.tabMinWidth, self.height))

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
        self.AdjustTabsSize()
        self.Refresh()

    def GetTabsCount(self):
        return len(self.tabs)

    def AdjustTabsSize(self):
        tabMinWidth = 9000000 # Really, it should be over 9000
        for tab in self.tabs:
            tx,ty = tab.GetMinSize()
            if tabMinWidth > tx:
               tabMinWidth = tx
        if self.GetTabsCount() >0:
            if self.GetTabsCount() * tabMinWidth > self.tabContainerWidth:
                self.tabMinWidth = (self.tabContainerWidth - self.reserved) / self.GetTabsCount()
            else:
                self.tabMinWidth = tabMinWidth
        else:
            self.tabMinWidth = 1
        for tab in self.tabs:
            tab.SetSize( (self.tabMinWidth, self.height) )
        self.CreateShadow()

        shadowBmp = self.tabShadow.Render()

        simg = shadowBmp.ConvertToImage()
        simg.InitAlpha()
        simg = simg.Blur(2)
        simg = simg.AdjustChannels(0.8,0.8,0.8,0.3)

        self.efxBmp = wx.BitmapFromImage(simg)

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
