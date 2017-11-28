# coding: utf-8

import wx
from logbook import Logger

import gui.utils.anim_effects as animEffects
import gui.utils.color as colorUtils
import gui.utils.draw as drawUtils
from .events import Stage2Selected
from gui.bitmap_loader import BitmapLoader

pyfalog = Logger(__name__)


class RaceSelector(wx.Window):
    def __init__(self, parent, id=wx.ID_ANY, label="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 layout=wx.VERTICAL, animate=False):
        wx.Window.__init__(self, parent, id, pos=pos, size=size, style=style)

        self.animTimerID = wx.NewId()
        self.animTimer = wx.Timer(self, self.animTimerID)
        self.animPeriod = 25
        self.animDuration = 250
        self.animStep = 0
        self.maxWidth = 24
        self.minWidth = 5 if animate else self.maxWidth
        self.maxHeight = 24
        self.minHeight = 10 if animate else self.maxHeight

        self.direction = 0 if animate else 1
        self.layout = layout
        self.animate = animate

        if layout == wx.VERTICAL:
            self.SetSize(wx.Size(self.minWidth, -1))
            self.SetMinSize(wx.Size(self.minWidth, -1))
        else:
            self.SetSize(wx.Size(-1, self.minHeight))
            self.SetMinSize(wx.Size(-1, self.minHeight))

        self.checkTimerID = wx.NewId()
        self.checkTimer = wx.Timer(self, self.checkTimerID)
        self.checkPeriod = 250
        self.checkMaximize = True
        self.shipBrowser = self.Parent
        self.raceBmps = []
        self.raceNames = []
        self.hoveredItem = None

        if layout == wx.VERTICAL:
            self.buttonsBarPos = (4, 0)
        else:
            self.buttonsBarPos = (0, 4)

        self.buttonsPadding = 4

        if layout == wx.VERTICAL:
            self.bmpArrow = BitmapLoader.getBitmap("down-arrow2", "gui")
        else:
            self.bmpArrow = BitmapLoader.getBitmap("up-arrow2", "gui")

        # Make the bitmaps have the same color as window text

        sysTextColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)

        img = self.bmpArrow.ConvertToImage()
        if layout == wx.VERTICAL:
            img = img.Rotate90(False)
        img.Replace(0, 0, 0, sysTextColour[0], sysTextColour[1], sysTextColour[2])
        if layout == wx.VERTICAL:
            img = img.Scale(self.minWidth, 8, wx.IMAGE_QUALITY_HIGH)

        self.bmpArrow = wx.Bitmap(img)

        self.RebuildRaces(self.shipBrowser.RACE_ORDER)

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnWindowEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnWindowLeave)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnBackgroundErase)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_SIZE, self.OnSizeUpdate)

        self.Layout()

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

    def OnMouseMove(self, event):
        mx, my = event.GetPosition()

        location = self.HitTest(mx, my)
        if location != self.hoveredItem:
            self.hoveredItem = location
            self.Refresh()
            if location is not None:
                self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            else:
                self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

    def OnSizeUpdate(self, event):
        self.CalcButtonsBarPos()

        self.Refresh()

        event.Skip()

    def CalcButtonsBarPos(self):

        if self.layout == wx.HORIZONTAL:
            rect = self.GetRect()
            width = 0
            height = 0
            for bmp in self.raceBmps:
                width += bmp.GetWidth() + self.buttonsPadding
                height = max(bmp.GetHeight(), height)

            posx = (rect.width - width) / 2
            posy = (rect.height - height) / 2

            self.buttonsBarPos = (posx, posy)

    def OnLeftUp(self, event):

        mx, my = event.GetPosition()

        toggle = self.HitTest(mx, my)

        if toggle is not None:
            self.Refresh()

            self.shipBrowser.ToggleRacesFilter(self.raceNames[toggle])

            stage = self.shipBrowser.GetActiveStage()

            if stage == 2:
                categoryID = self.shipBrowser.GetStageData(stage)
                wx.PostEvent(self.shipBrowser, Stage2Selected(categoryID=categoryID, back=True))
        event.Skip()

    def HitTest(self, mx, my):
        x, y = self.buttonsBarPos
        padding = self.buttonsPadding

        for bmp in self.raceBmps:
            if (x < mx < x + bmp.GetWidth()) and (y < my < y + bmp.GetHeight()):
                return self.raceBmps.index(bmp)
            if self.layout == wx.VERTICAL:
                y += bmp.GetHeight() + padding
            else:
                x += bmp.GetWidth() + padding

        return None

    def RebuildRaces(self, races):
        self.raceBmps = []
        for race in races:
            if race:
                self.raceBmps.append(BitmapLoader.getBitmap("race_%s_small" % race, "gui"))
        self.raceNames = races
        self.CalcButtonsBarPos()
        self.Refresh()

    def OnBackgroundErase(self, event):
        pass

    def OnPaint(self, event):
        rect = self.GetRect()

        windowColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        # bkColor = colorUtils.GetSuitable(windowColor, 0.1)
        sepColor = colorUtils.GetSuitable(windowColor, 0.2)

        mdc = wx.AutoBufferedPaintDC(self)

        bkBitmap = drawUtils.RenderGradientBar(windowColor, rect.width, rect.height, 0.1, 0.1, 0.2, 2)
        mdc.DrawBitmap(bkBitmap, 0, 0, True)

        x, y = self.buttonsBarPos

        if self.direction == 1:
            for raceBmp in self.raceBmps:
                dropShadow = drawUtils.CreateDropShadowBitmap(raceBmp, 0.2)

                if self.shipBrowser.GetRaceFilterState(self.raceNames[self.raceBmps.index(raceBmp)]):
                    bmp = raceBmp
                else:
                    img = raceBmp.ConvertToImage()
                    if self.hoveredItem == self.raceBmps.index(raceBmp):
                        img = img.AdjustChannels(1, 1, 1, 0.7)
                    else:
                        img = img.AdjustChannels(1, 1, 1, 0.4)
                    bmp = wx.Bitmap(img)

                if self.layout == wx.VERTICAL:
                    mdc.DrawBitmap(dropShadow, rect.width - self.buttonsPadding - bmp.GetWidth() + 1, y + 1)
                    mdc.DrawBitmap(bmp, rect.width - self.buttonsPadding - bmp.GetWidth(), y)
                    y += raceBmp.GetHeight() + self.buttonsPadding
                    mdc.SetPen(wx.Pen(sepColor, 1))
                    mdc.DrawLine(rect.width - 1, 0, rect.width - 1, rect.height)
                else:
                    mdc.DrawBitmap(dropShadow, x + 1, self.buttonsPadding + 1)
                    mdc.DrawBitmap(bmp, x, self.buttonsPadding)
                    x += raceBmp.GetWidth() + self.buttonsPadding
                    mdc.SetPen(wx.Pen(sepColor, 1))
                    mdc.DrawLine(0, 0, rect.width, 0)

        if self.direction < 1:
            if self.layout == wx.VERTICAL:
                mdc.DrawBitmap(self.bmpArrow, -2, (rect.height - self.bmpArrow.GetHeight()) / 2)
            else:
                mdc.SetPen(wx.Pen(sepColor, 1))
                mdc.DrawLine(0, 0, rect.width, 0)
                mdc.DrawBitmap(self.bmpArrow, (rect.width - self.bmpArrow.GetWidth()) / 2, -2)

    def OnTimer(self, event):
        if event.GetId() == self.animTimerID:
            start = 0
            if self.layout == wx.VERTICAL:
                end = self.maxWidth - self.minWidth
            else:
                end = self.maxHeight - self.minHeight

            step = animEffects.OUT_CIRC(self.animStep, start, end, self.animDuration)
            self.animStep += self.animPeriod * self.direction

            self.AdjustSize((self.minWidth if self.layout == wx.VERTICAL else self.minHeight) + step)

            if self.animStep > self.animDuration or self.animStep < 0:
                self.animTimer.Stop()
                self.animStep = self.animDuration if self.direction == 1 else 0
                self.Parent.GetBrowserContainer().RefreshList(True)

        if event.GetId() == self.checkTimerID:
            if self.checkMaximize:
                self.direction = 1
            else:
                self.direction = -1

            if not self.animTimer.IsRunning():
                self.animTimer.Start(self.animPeriod)

    def AdjustSize(self, delta):
        self.SetMinSize(wx.Size(delta, -1) if self.layout == wx.VERTICAL else wx.Size(-1, delta))
        self.Parent.Layout()
        self.Refresh()

    def OnWindowEnter(self, event):
        if not self.animate:
            return

        if not self.checkTimer.IsRunning():
            self.checkTimer.Start(self.checkPeriod, wx.TIMER_ONE_SHOT)
        self.checkMaximize = True

        event.Skip()

    def OnWindowLeave(self, event):
        if self.hoveredItem is not None:
            self.hoveredItem = None
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
            self.Refresh()

        if not self.animate:
            return

        if not self.checkTimer.IsRunning():
            self.checkTimer.Start(self.checkPeriod, wx.TIMER_ONE_SHOT)
        self.checkMaximize = False

        event.Skip()
