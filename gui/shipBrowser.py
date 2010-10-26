import wx
import copy
from gui import bitmapLoader
import gui.mainFrame
import service

FitRenamed, EVT_FIT_RENAMED = wx.lib.newevent.NewEvent()
FitSelected, EVT_FIT_SELECTED = wx.lib.newevent.NewEvent()
FitRemoved, EVT_FIT_REMOVED = wx.lib.newevent.NewEvent()

Stage1Selected, EVT_SB_STAGE1_SEL = wx.lib.newevent.NewEvent()
Stage2Selected, EVT_SB_STAGE2_SEL = wx.lib.newevent.NewEvent()
Stage3Selected, EVT_SB_STAGE3_SEL = wx.lib.newevent.NewEvent()

class ShipBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ (self, parent)

        self._lastWidth = 0
        self._activeStage = 0

        self._stage1Data = -1
        self._stage2Data = -1
        self._stage3Data = -1
        self._stage3ShipName = ""

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.hpane = HeaderPane(self)
        mainSizer.Add(self.hpane, 0, wx.EXPAND)

        self.lpane = ListPane(self)
        mainSizer.Add(self.lpane, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        self.Layout()
        self.Show()

        self.Centre(wx.BOTH)
        self.Bind(wx.EVT_SIZE, self.SizeRefreshList)
        self.Bind(EVT_SB_STAGE2_SEL, self.stage2)
        self.Bind(EVT_SB_STAGE1_SEL, self.stage1)
        self.Bind(EVT_SB_STAGE3_SEL, self.stage3)

        self.stage1(None)

    def SizeRefreshList(self, event):
        ewidth, eheight = event.GetSize()
##            if ewidth != self._lastWidth:
##                self._lastWidth = ewidth
        self.Layout()
        self.lpane.Layout()
        self.lpane.RefreshList(True)
        event.Skip()

    def __del__(self):
        pass
    def GetActiveStage(self):
        return self._activeStage

    def GetStageData(self, stage):
        if stage == 1:
            return self._stage1Data
        if stage == 2:
            return self._stage2Data
        if stage == 3:
            return self._stage3Data
        return -1
    def GetStage3ShipName(self):
        return self._stage3ShipName

    def nameKey(self, info):
        return info[1]

    def stage1(self, event):
        self._activeStage = 1
        self.hpane.ToggleNewFitSB(False)
        sMarket = service.Market.getInstance()
        self.lpane.RemoveAllChildren()
        categoryList = sMarket.getShipRoot()
        categoryList.sort(key=self.nameKey)
        for ID, name in categoryList:
            self.lpane.AddWidget(CategoryItem(self.lpane, ID, (name, 0)))

        self.lpane.RefreshList()
        self.Show()

    RACE_ORDER = ["amarr", "caldari", "gallente", "minmatar", "ore", "serpentis", "angel", "blood", "sansha", "guristas", None]
    def raceNameKey(self, shipInfo):
        return self.RACE_ORDER.index(shipInfo[2]), shipInfo[1]


    def stage2(self, event):
        self._activeStage = 2
        categoryID = event.categoryID
        if self.GetStageData(self._activeStage) != categoryID:
            self._stage3Data = -1

        self._stage2Data = categoryID
        self.hpane.ToggleNewFitSB(False)
        sMarket = service.Market.getInstance()
        sFit = service.Fit.getInstance()
        self.lpane.RemoveAllChildren()
        shipList = sMarket.getShipList(categoryID)
        shipList.sort(key=self.raceNameKey)
        for ID, name, race in shipList:
            self.lpane.AddWidget(ShipItem(self.lpane, ID, (name, len(sFit.getFitsWithShip(ID))), race))

        self.lpane.RefreshList()
        self.Show()

    def stage3(self, event):
        self._activeStage = 3

        shipID = event.shipID
        self._stage3Data = shipID

        sFit = service.Fit.getInstance()
        sMarket = service.Market.getInstance()
        self.lpane.RemoveAllChildren()
        fitList = sFit.getFitsWithShip(shipID)

        if len(fitList) == 0:
            self._stage3Data = -1
            self.hpane.gotoStage(2)
            return
        self.hpane.ToggleNewFitSB(True)
        fitList.sort(key=self.nameKey)
        shipName = sMarket.getItem(shipID).name
        self._stage3ShipName = shipName
        for ID, name in fitList:
            self.lpane.AddWidget(FitItem(self.lpane, ID, (shipName, name),shipID))

        self.lpane.RefreshList()
        self.Show()

class HeaderPane (wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 32), style=wx.TAB_TRAVERSAL)

        self.rewBmp = bitmapLoader.getBitmap("frewind_small","icons")
        self.forwBmp = bitmapLoader.getBitmap("fforward_small","icons")
        self.searchBmp = bitmapLoader.getBitmap("fsearch_small","icons")
        self.newBmp = bitmapLoader.getBitmap("fit_add_small","icons")

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.sbRewind = wx.StaticBitmap( self, wx.ID_ANY, self.rewBmp, wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add(self.sbRewind, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL , 5)

        self.sbForward = wx.StaticBitmap( self, wx.ID_ANY, self.forwBmp, wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add(self.sbForward, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL , 5)

        self.sbSearch = wx.StaticBitmap( self, wx.ID_ANY, self.searchBmp, wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add(self.sbSearch, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL , 5)

        self.sbNewFit = wx.StaticBitmap( self, wx.ID_ANY, self.newBmp, wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add(self.sbNewFit, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL , 5)

        self.stStatus = wx.StaticText( self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stStatus.Wrap( -1 )
        mainSizer.Add(self.stStatus, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL , 5)

        self.SetSizer(mainSizer)

        self.sbForward.Bind(wx.EVT_LEFT_UP,self.OnForward)
        self.sbForward.Bind( wx.EVT_ENTER_WINDOW, self.OnEnterWForward )
        self.sbForward.Bind( wx.EVT_LEAVE_WINDOW, self.OnLeaveWForward )

        self.sbRewind.Bind(wx.EVT_LEFT_UP,self.OnBack)
        self.sbRewind.Bind( wx.EVT_ENTER_WINDOW, self.OnEnterWRewind )
        self.sbRewind.Bind( wx.EVT_LEAVE_WINDOW, self.OnLeaveWRewind )

        self.sbSearch.Bind(wx.EVT_LEFT_UP,self.OnSearch)
        self.sbSearch.Bind( wx.EVT_ENTER_WINDOW, self.OnEnterWSearch )
        self.sbSearch.Bind( wx.EVT_LEAVE_WINDOW, self.OnLeaveWSearch )

        self.sbNewFit.Bind(wx.EVT_LEFT_UP,self.OnNewFitting)
        self.sbNewFit.Bind( wx.EVT_ENTER_WINDOW, self.OnEnterWNewFit )
        self.sbNewFit.Bind( wx.EVT_LEAVE_WINDOW, self.OnLeaveWNewFit )

        self.Layout()

    def ToggleNewFitSB(self, toggle):
        self.sbNewFit.Show(toggle)
        self.Layout()

    def OnEnterWForward(self, event):
        self.stStatus.SetLabel("Forward")
        stage = self.Parent.GetActiveStage()

        if stage < 3:
            if self.Parent.GetStageData(stage+1) != -1:
                self.stStatus.Enable()
            else:
                self.stStatus.Disable()
        else:
            self.stStatus.Disable()

        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        event.Skip()

    def OnLeaveWForward(self, event):
        self.stStatus.Enable()
        self.stStatus.SetLabel("")
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        event.Skip()

    def OnEnterWRewind(self, event):
        self.stStatus.SetLabel("Back")

        stage = self.Parent.GetActiveStage()

        if stage > 1:
            self.stStatus.Enable()
        else:
            self.stStatus.Disable()


        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        event.Skip()

    def OnLeaveWRewind(self, event):
        self.stStatus.Enable()
        self.stStatus.SetLabel("")
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        event.Skip()

    def OnEnterWSearch(self, event):
        self.stStatus.SetLabel("Search fittings")
        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        event.Skip()

    def OnLeaveWSearch(self, event):
        self.stStatus.SetLabel("")
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        event.Skip()

    def OnEnterWNewFit(self, event):
        self.stStatus.SetLabel("New fitting")
        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        event.Skip()

    def OnLeaveWNewFit(self, event):
        self.stStatus.SetLabel("")
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        event.Skip()

    def OnSearch(self, event):
        event.Skip()

    def OnNewFitting(self, event):
        stage = self.Parent.GetActiveStage()
        if stage == 3:
            shipID = self.Parent.GetStageData(stage)
            shipName = self.Parent.GetStage3ShipName()
            sFit = service.Fit.getInstance()
            sFit.newFit(shipID, "%s fit" %shipName)
            wx.PostEvent(self.Parent,Stage3Selected(shipID=shipID))
        event.Skip()

    def OnForward(self,event):
        stage = self.Parent.GetActiveStage()
        stage +=1
        if stage >3:
            stage = 3
            return
        self.gotoStage(stage)

        self.stStatus.Enable()
        self.stStatus.SetLabel("")

        event.Skip()

    def OnBack(self,event):
        stage = self.Parent.GetActiveStage()
        stage -=1
        if stage <1:
            stage = 1
            return
        self.gotoStage(stage)

        self.stStatus.Enable()
        self.stStatus.SetLabel("")

        event.Skip()
    def gotoStage(self,stage):
        if stage == 1:
            wx.PostEvent(self.Parent,Stage1Selected())
        elif stage == 2:
            categoryID = self.Parent.GetStageData(stage)
            if categoryID != -1:
                wx.PostEvent(self.Parent,Stage2Selected(categoryID=categoryID))
        elif stage == 3:
            shipID = self.Parent.GetStageData(stage)
            if shipID != -1:
                wx.PostEvent(self.Parent,Stage3Selected(shipID=shipID))

class ListPane (wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(1, 1), style=wx.TAB_TRAVERSAL)
        self._wList = []
        self._wCount = 0
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))


        self.SetVirtualSize((1, 1))
        self.SetScrollRate(0, 1)
        self.Bind(wx.EVT_SCROLLWIN_LINEUP, self.MScrollUp)
        self.Bind(wx.EVT_SCROLLWIN_LINEDOWN, self.MScrollDown)

    def MScrollUp(self, event):

        posy = self.GetScrollPos(wx.VERTICAL)
        posy -= 8
        self.Scroll(0, posy)
#        self.RefreshList()
        event.Skip()

    def MScrollDown(self, event):

        posy = self.GetScrollPos(wx.VERTICAL)
        posy += 8
        self.Scroll(0, posy)
#        self.RefreshList()
        event.Skip()


    def AddWidget(self, widget):
        widget.Reparent(self)
        self._wList.append(widget)
        self._wCount += 1

    def RefreshList(self, doRefresh = False):
        ypos = 0
        maxy = 0
        for i in xrange( len(self._wList) ):
            iwidth, iheight = self._wList[i].GetSize()
            xa, ya = self.CalcScrolledPosition((0, maxy))
            self._wList[i].SetPosition((xa, ya))
            maxy += iheight
        self.SetVirtualSize((1, maxy))
        cwidth, cheight = self.GetVirtualSize()

        clientW,clientH = self.GetSize()
        for i in xrange( len(self._wList) ):
            iwidth, iheight = self._wList[i].GetSize()
            itemX,itemY = self._wList[i].GetPosition()
            self._wList[i].SetSize((cwidth, iheight))
            if doRefresh == True:
                if itemY >=-iheight and itemY< clientH:
                    self._wList[i].Refresh()

    def RemoveWidget(self, child):
        child.Destroy()
        self._wList.remove(child)


    def RemoveAllChildren(self):
        for widget in self._wList:
            widget.Destroy()

        self._wList = []

class CategoryItem(wx.Window):
    def __init__(self, parent, categoryID, shipFittingInfo,
                 id=wx.ID_ANY, range=100, pos=wx.DefaultPosition,
                 size=(0,16), style=0):
        wx.Window.__init__(self, parent, id, pos, size, style)

        if categoryID:
            self.shipBmp = bitmapLoader.getBitmap("ship_small","icons")
        else:
            self.shipBmp = wx.EmptyBitmap(16,16)

        self.categoryID = categoryID
        self.shipFittingInfo = shipFittingInfo
        self.shipName, dummy = shipFittingInfo
        self.width,self.height = size

        self.highlighted = 0
        self.editWasShown = 0

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_UP, self.checkPosition)
        self.Bind(wx.EVT_ENTER_WINDOW, self.enterW)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.leaveW)

        self.shipBrowser = self.Parent.Parent

    def checkPosition(self, event):

        pos = event.GetPosition()
        x,y = pos
        categoryID = self.categoryID
        wx.PostEvent(self.shipBrowser,Stage2Selected(categoryID=categoryID))

    def enterW(self,event):
        self.highlighted = 1
        self.Refresh()
        event.Skip()

    def leaveW(self,event):
        self.highlighted = 0
        self.Refresh()
        event.Skip()


    def OnEraseBackground(self, event):
        pass

    def OnPaint(self,event):
        rect = self.GetRect()

        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)
        r = copy.copy(rect)
        r.top = 0
        r.left = 0
        r.height = r.height / 2
        if self.highlighted:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)))
            mdc.Clear()
            mdc.SetTextForeground(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

            sr = 221
            sg = 221
            sb = 221

            startColor = (sr,sg,sb)

            mdc.GradientFillLinear(r,startColor,wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.SOUTH)
            r.top = r.height
            mdc.GradientFillLinear(r,startColor,wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.NORTH)
            mdc.SetTextForeground(wx.BLACK)

        else:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)))
            mdc.SetTextForeground(wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ))
            mdc.Clear()

        mdc.DrawBitmap(self.shipBmp,5+(rect.height-self.shipBmp.GetHeight())/2,(rect.height-self.shipBmp.GetWidth())/2,0)
        mdc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False))



        shipName, fittings = self.shipFittingInfo



        xpos = self.shipBmp.GetWidth() + 10

        xtext, ytext = mdc.GetTextExtent(shipName)
        ypos = (rect.height - ytext) / 2
        mdc.DrawText(shipName, xpos, ypos)
        xpos+=xtext+5

        mdc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False))

        if fittings <1:
            fformat = "No fits"
        else:
            if fittings == 1:
                fformat = "%d fit"
            else:
                fformat = "%d fits"

        if fittings>0:
            xtext, ytext = mdc.GetTextExtent(fformat % fittings)
            ypos = (rect.height - ytext)/2
        else:
            xtext, ytext = mdc.GetTextExtent(fformat)
            ypos = (rect.height - ytext)/2

        #seems that a scrolled window without scrollbars shown always HasScrollbar ><

        addX = 5

        fPosX = rect.width - addX - xtext
        fPosY = (rect.height -ytext)/2
        if fittings > 0:
            mdc.DrawText(fformat % fittings, fPosX, fPosY)
        else:
            mdc.DrawText(fformat, fPosX, fPosY)

        event.Skip()

class ShipItem(wx.Window):
    def __init__(self, parent, shipID=None, shipFittingInfo=("Test", 2), itemData=None,
                 id=wx.ID_ANY, range=100, pos=wx.DefaultPosition,
                 size=(0, 38), style=0):
        wx.Window.__init__(self, parent, id, pos, size, style)

        self._itemData = itemData

        self.shipRace = itemData

        self.shipID = shipID
        self.shipBmp = None
        if shipID:
            self.shipBmp = bitmapLoader.getBitmap(str(shipID),"ships")
        if not self.shipBmp:
            self.shipBmp = wx.EmptyBitmap(32, 32)
        self.shipFittingInfo = shipFittingInfo
        self.shipName, self.shipFits = shipFittingInfo

        self.newBmp = bitmapLoader.getBitmap("fit_add_small", "icons")
        self.acceptBmp = bitmapLoader.getBitmap("faccept_small", "icons")
        self.newToggleBmp = self.newBmp
        self.shipEffBk = bitmapLoader.getBitmap("fshipbk_big","icons")
        self.raceBmp = bitmapLoader.getBitmap("race_%s_small" % self.shipRace, "icons")

        self.shipBrowser = self.Parent.Parent

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.editPosX = 0
        self.editPosY = 0
        self.highlighted = 0
        self.editWasShown = 0

        self.tcFitName = wx.TextCtrl(self, wx.ID_ANY, "%s fit" % self.shipName, wx.DefaultPosition, (120,-1), wx.TE_PROCESS_ENTER)
        self.tcFitName.Show(False)

        self.btnsStatus = ""

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        self.Bind(wx.EVT_LEFT_UP, self.checkPosition)
        self.Bind(wx.EVT_MOTION, self.cursorCheck)

        self.Bind(wx.EVT_ENTER_WINDOW, self.enterW)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.leaveW)

        self.tcFitName.Bind(wx.EVT_TEXT_ENTER, self.createNewFit)
        self.tcFitName.Bind(wx.EVT_KILL_FOCUS, self.editLostFocus)
        self.tcFitName.Bind(wx.EVT_KEY_DOWN, self.editCheckEsc)

    def SetData(self, data):
        self._itemData = data

    def GetData(self):
        return self._itemData

    def editLostFocus(self, event):
        self.tcFitName.Show(False)
        if self.highlighted == 1:
            self.editWasShown = 1

    def editCheckEsc(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.tcFitName.Show(False)
            self.editWasShown = 0
        else:
            event.Skip()

    def cursorCheck(self, event):
        pos = event.GetPosition()
        if self.NHitTest((self.editPosX, self.editPosY), pos, (16, 16)):
            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            if self.btnsStatus != "New fit":
                self.btnsStatus = "New fit"
                self.Refresh()
        else:
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            if self.btnsStatus != "":
                self.btnsStatus = ""
                self.Refresh()

    def checkPosition(self, event):

        pos = event.GetPosition()
        x, y = pos
        if self.NHitTest((self.editPosX, self.editPosY), pos, (16, 16)):
            if self.editWasShown == 1:
                self.createNewFit()
                return
            else:
                fnEditSize = self.tcFitName.GetSize()
                wSize = self.GetSize()
                fnEditPosX = self.editPosX - fnEditSize.width - 5
                fnEditPosY = (wSize.height - fnEditSize.height) / 2
                self.tcFitName.SetPosition((fnEditPosX, fnEditPosY))
                self.tcFitName.Show(True)
                self.tcFitName.SetFocus()
                self.tcFitName.SelectAll()
                self.newToggleBmp = self.acceptBmp
                self.Refresh()
                return

        if (not self.NHitTest((self.editPosX, self.editPosY), pos, (16, 16))):
            if self.shipFits > 0:
                if self.editWasShown == 1:
                    self.editWasShown = 0
                else:
                    wx.PostEvent(self.shipBrowser,Stage3Selected(shipID=self.shipID))
            else:
                if self.editWasShown == 0:
                    fnEditSize = self.tcFitName.GetSize()
                    wSize = self.GetSize()
                    fnEditPosX = self.editPosX - fnEditSize.width - 5
                    fnEditPosY = (wSize.height - fnEditSize.height) / 2
                    self.tcFitName.SetPosition((fnEditPosX, fnEditPosY))
                    self.tcFitName.Show(True)
                    self.tcFitName.SetFocus()
                    self.tcFitName.SelectAll()
                    self.newToggleBmp = self.acceptBmp
                    self.Refresh()
                else:
                    self.editWasShown = 0
                    self.newToggleBmp = self.newBmp
                    self.Refresh()



        event.Skip()

    def createNewFit(self, event=None):
        sFit = service.Fit.getInstance()
        sFit.newFit(self.shipID, self.tcFitName.GetValue())
        self.tcFitName.Show(False)
        self.editWasShown = 0
        wx.PostEvent(self.shipBrowser,Stage3Selected(shipID=self.shipID))

    def NHitTest(self, target, position, area):
        x, y = target
        px, py = position
        aX, aY = area
        if (px > x and px < x + aX) and (py > y and py < y + aY):
            return True
        return False
    def enterW(self, event):
        self.highlighted = 1
        self.Refresh()
        event.Skip()

    def leaveW(self, event):
        self.highlighted = 0
        self.Refresh()
        event.Skip()

    def OnEraseBackground(self, event):
        pass

    def OnPaint(self, event):
        rect = self.GetRect()

        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)
        r = copy.copy(rect)
        r.top = 0
        r.left = 0
        r.height = r.height / 2
        if self.highlighted:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)))
            mdc.Clear()
            mdc.SetTextForeground(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

            sr = 221
            sg = 221
            sb = 221

            startColor = (sr,sg,sb)

            mdc.GradientFillLinear(r,startColor,wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.SOUTH)
            r.top = r.height
            mdc.GradientFillLinear(r,startColor,wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.NORTH)
            mdc.SetTextForeground(wx.BLACK)

        else:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)))
            mdc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
            mdc.Clear()

        mdc.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        mdc.DrawBitmap(self.shipEffBk, 5 + (rect.height - self.shipEffBk.GetWidth())/2, (rect.height - self.shipEffBk.GetHeight())/2, 0)
        mdc.DrawBitmap(self.shipBmp, 5 + (rect.height - 32) / 2, (rect.height - 32) / 2, 0)

#        tempdc = wx.MemoryDCFromDC(mdc)
#        tempdc.DrawBitmap(self.raceBmp,0,0,0)
#        mdc.Blit(5 + (rect.height - self.raceBmp.GetWidth()) / 2, (rect.height - self.raceBmp.GetHeight()) / 2,
#                 self.raceBmp.GetWidth(),self.raceBmp.GetHeight(), tempdc, 0, 0, rop = wx.XOR, useMask = True)
#        img = self.raceBmp.ConvertToImage()
#        img.AdjustChannels(1, 1, 1,0)
#        self.raceBmp = wx.BitmapFromImage(img)
#        mdc.DrawBitmap(self.raceBmp, 5 + (rect.height - self.raceBmp.GetWidth()) , (rect.height - self.raceBmp.GetHeight()) , 0)
#        mdc.DrawBitmap(self.raceBmp, 5 + (rect.height - self.shipBmp.GetWidth()) / 2, (rect.height - self.shipBmp.GetHeight()) / 2, 0)
#        tempdc.SelectObject(wx.NullBitmap)


        shipName, fittings = self.shipFittingInfo


        ypos = (rect.height - 32) / 2
        textStart = 48
        xtext, ytext = mdc.GetTextExtent(shipName)
        mdc.DrawBitmap(self.raceBmp,textStart, ypos + self.raceBmp.GetHeight()/2)
        mdc.DrawText(shipName, textStart + self.raceBmp.GetWidth() + 4, ypos)
        textStart += self.raceBmp.GetWidth() + 4

        ypos += ytext

        mdc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False))

        if fittings <1:
            fformat = "No fits"
        else:
            if fittings == 1:
                fformat = "%d fit"
            else:
                fformat = "%d fits"

        if fittings>0:
            xtext, ytext = mdc.GetTextExtent(fformat % fittings)
        else:
            xtext, ytext = mdc.GetTextExtent(fformat)

        mdc.DrawText(fformat %fittings if fittings >0 else fformat, textStart, ypos)

#        mdc.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL, False))

        self.editPosX = rect.width - 20
        self.editPosY = (rect.height - 16) / 2

        mdc.DrawBitmap(self.newToggleBmp, self.editPosX, self.editPosY, 0)
        if self.btnsStatus != "":
            status = "%s" % self.btnsStatus
            xtext, ytext = mdc.GetTextExtent(status)
            ytext = (rect.height - ytext)/2
            mdc.DrawText(status, self.editPosX - xtext -5,ytext)
        event.Skip()

class FitItem(wx.Window):
    def __init__(self, parent, fitID=None, shipFittingInfo=("Test", "cnc's avatar"), shipID = None, itemData=None,
                 id=wx.ID_ANY, range=100, pos=wx.DefaultPosition,
                 size=(0, 36), style=0):
        wx.Window.__init__(self, parent, id, pos, size, style)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self._itemData = itemData
        self.fitID = fitID
        self.shipID = shipID
        self.shipBrowser = self.Parent.Parent
        self.shipBmp = None
        if shipID:
            self.shipBmp = bitmapLoader.getBitmap(str(shipID),"ships")
        if not self.shipBmp:
            self.shipBmp = wx.EmptyBitmap(32, 32)

        self.shipFittingInfo = shipFittingInfo
        self.shipName, self.fitName= shipFittingInfo
        self.copyBmp = bitmapLoader.getBitmap("fit_add_small", "icons")
        self.renameBmp = bitmapLoader.getBitmap("fit_rename_small", "icons")
        self.deleteBmp = bitmapLoader.getBitmap("fit_delete_small","icons")
        self.shipEffBk = bitmapLoader.getBitmap("fshipbk_big","icons")

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.renamePosX = 0
        self.renamePosY = 0

        self.deletePosX = 0
        self.deletePosY = 0

        self.copyPosX = 0
        self.copyPosY = 0

        self.highlighted = 0
        self.editWasShown = 0

        self.btnsStatus = ""

        self.tcFitName = wx.TextCtrl(self, wx.ID_ANY, "%s" % self.fitName, wx.DefaultPosition, (150,-1), wx.TE_PROCESS_ENTER)
        self.tcFitName.Show(False)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        self.Bind(wx.EVT_LEFT_UP, self.checkPosition)
        self.Bind(wx.EVT_MOTION, self.cursorCheck)

        self.Bind(wx.EVT_ENTER_WINDOW, self.enterW)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.leaveW)

        self.tcFitName.Bind(wx.EVT_TEXT_ENTER, self.renameFit)
        self.tcFitName.Bind(wx.EVT_KILL_FOCUS, self.editLostFocus)
        self.tcFitName.Bind(wx.EVT_KEY_DOWN, self.editCheckEsc)

    def SetData(self, data):
        self._itemData = data

    def GetData(self):
        return self._itemData

    def editLostFocus(self, event):
        self.tcFitName.Show(False)
        if self.highlighted == 1:
            self.editWasShown = 1

    def editCheckEsc(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.tcFitName.Show(False)
            self.editWasShown = 0
        else:
            event.Skip()

    def cursorCheck(self, event):
        pos = event.GetPosition()
        if self.NHitTest((self.renamePosX, self.renamePosY), pos, (16, 16)):
            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            if self.btnsStatus != "Rename":
                self.btnsStatus = "Rename"
                self.Refresh()
        elif self.NHitTest((self.deletePosX, self.deletePosY), pos, (16, 16)):
            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            if self.btnsStatus != "Delete":
                self.btnsStatus = "Delete"
                self.Refresh()
        elif self.NHitTest((self.copyPosX, self.copyPosY), pos, (16, 16)):
            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            if self.btnsStatus != "Copy":
                self.btnsStatus = "Copy"
                self.Refresh()
        else:
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            if self.btnsStatus != "":
                self.btnsStatus = ""
                self.Refresh()
    def checkPosition(self, event):

        pos = event.GetPosition()
        x, y = pos
        if self.NHitTest((self.renamePosX, self.renamePosY), pos, (16, 16)):
            if self.editWasShown == 1:
                self.renameFit()
                return
            else:
                self.Refresh()
                fnEditSize = self.tcFitName.GetSize()
                wSize = self.GetSize()
                fnrenamePosX = self.renamePosX - fnEditSize.width - 5
                fnrenamePosY = (wSize.height - fnEditSize.height) / 2
                self.tcFitName.SetPosition((fnrenamePosX, fnrenamePosY))
                self.tcFitName.Show(True)
                self.tcFitName.SetFocus()
                self.tcFitName.SelectAll()
                return
        if self.NHitTest((self.deletePosX,self.deletePosY), pos, (16,16)):
            if self.editWasShown != 1:
                self.deleteFit()
                return

        if self.NHitTest((self.copyPosX,self.copyPosY), pos, (16,16)):
            if self.editWasShown != 1:
                self.copyFit()
                return

        if self.editWasShown != 1:
            activeFitID = self.mainFrame.getActiveFit()
            if activeFitID != self.fitID:
                self.selectFit()
        else:
            self.editWasShown = 0
            self.Refresh()

        event.Skip()

    def renameFit(self, event=None):
        sFit = service.Fit.getInstance()
        self.tcFitName.Show(False)
        self.editWasShown = 0
        self.fitName = self.tcFitName.GetValue()
        sFit.renameFit(self.fitID, self.fitName)
        wx.PostEvent(self.mainFrame, FitRenamed(fitID=self.fitID))
        self.Refresh()

    def copyFit(self, event=None):
        sFit = service.Fit.getInstance()
        sFit.copyFit(self.fitID)
        wx.PostEvent(self.shipBrowser,Stage3Selected(shipID=self.shipID))

    def deleteFit(self, event=None):
        sFit = service.Fit.getInstance()
        sFit.deleteFit(self.fitID)
        wx.PostEvent(self.shipBrowser,Stage3Selected(shipID=self.shipID))
        wx.PostEvent(self.mainFrame, FitRemoved(fitID=self.fitID))

    def selectFit(self, event=None):
        wx.PostEvent(self.mainFrame, FitSelected(fitID=self.fitID))

    def NHitTest(self, target, position, area):
        x, y = target
        px, py = position
        aX, aY = area
        if (px > x and px < x + aX) and (py > y and py < y + aY):
            return True
        return False
    def enterW(self, event):
        self.highlighted = 1
        self.Refresh()
        event.Skip()

    def leaveW(self, event):
        self.highlighted = 0
        self.Refresh()
        event.Skip()

    def OnEraseBackground(self, event):
        pass

    def OnPaint(self, event):
        rect = self.GetRect()

        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)
        r = copy.copy(rect)
        r.top = 0
        r.left = 0
        r.height = r.height / 2
        if self.highlighted:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)))
            mdc.Clear()
            mdc.SetTextForeground(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

            sr = 221
            sg = 221
            sb = 221

            startColor = (sr,sg,sb)

            mdc.GradientFillLinear(r,startColor,wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.SOUTH)
            r.top = r.height
            mdc.GradientFillLinear(r,startColor,wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.NORTH)
            mdc.SetTextForeground(wx.BLACK)

        else:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)))
            mdc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
            mdc.Clear()
        mdc.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False))
#        mdc.DrawBitmap(self.effBmp,5+(rect.height-40)/2,(rect.height-40)/2,0)
        mdc.DrawBitmap(self.shipEffBk,5+(rect.height - self.shipEffBk.GetWidth())/2,(rect.height - self.shipEffBk.GetHeight())/2,0)
        mdc.DrawBitmap(self.shipBmp, 5 + (rect.height - 32) / 2, (rect.height - 32) / 2, 0)




        shipName = self.shipName
        fitName = self.fitName


        ypos = (rect.height - 32) / 2
        textStart = 48
        xtext, ytext = mdc.GetTextExtent(shipName)
        mdc.DrawText(fitName, textStart, ypos)
        ypos += ytext

        mdc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False))


        mdc.DrawText("%s" % shipName, textStart, ypos)
        mdc.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL, False))

        self.deletePosX = rect.width - self.deleteBmp.GetWidth() - 5
        self.renamePosX = self.deletePosX - self.renameBmp.GetWidth() - 5
        self.copyPosX = self.renamePosX - self.copyBmp.GetWidth() -5
        self.renamePosY = self.deletePosY = self.copyPosY = (rect.height - 16) / 2

        if self.btnsStatus != "":
            status = "%s" % self.btnsStatus
            xtext, ytext = mdc.GetTextExtent(status)
            ytext = (rect.height - ytext)/2
            mdc.DrawText(status, self.copyPosX - xtext -5,ytext)

        mdc.DrawBitmap(self.copyBmp, self.copyPosX, self.copyPosY, 0)
        mdc.DrawBitmap(self.renameBmp, self.renamePosX, self.renamePosY, 0)
        mdc.DrawBitmap(self.deleteBmp, self.deletePosX, self.deletePosY, 0)
        event.Skip()
