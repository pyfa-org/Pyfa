# noinspection PyPackageRequirements
import wx
import gui.utils.drawUtils as drawUtils

SB_ITEM_NORMAL = 0
SB_ITEM_SELECTED = 1
SB_ITEM_HIGHLIGHTED = 2
SB_ITEM_DISABLED = 4

BTN_NORMAL = 1
BTN_PRESSED = 2
BTN_HOVER = 4
BTN_DISABLED = 8


class PFBaseButton(object):
    def __init__(self, normalBitmap=wx.NullBitmap, label="", callback=None, hoverBitmap=None, disabledBitmap=None,
                 show=True):

        self.normalBmp = normalBitmap
        self.dropShadowOpacity = 0.2
        self.dropShadowBmp = drawUtils.CreateDropShadowBitmap(self.normalBmp, self.dropShadowOpacity)
        self.hoverBmp = hoverBitmap
        self.disabledBmp = disabledBitmap
        self.label = label
        self.show = show

        self.callback = callback

        self.state = BTN_NORMAL
        # state : BTN_STUFF

    def Show(self, show):
        self.show = show

    def Hide(self):
        self.show = False

    def IsVisible(self):
        return self.show

    def SetCallback(self, callback):
        self.callback = callback

    def GetCallback(self):
        return self.callback

    def DoCallback(self):
        if self.callback:
            self.callback()

    def SetState(self, state=BTN_NORMAL):
        self.state = state

    def GetState(self):
        return self.state

    def GetSize(self):
        w = self.normalBmp.GetWidth()
        h = self.normalBmp.GetHeight()
        return w, h

    def GetBitmap(self):
        return self.normalBmp

    def SetBitmap(self, bitmap):
        self.normalBmp = bitmap
        self.dropShadowBmp = drawUtils.CreateDropShadowBitmap(self.normalBmp, self.dropShadowOpacity)

    def GetLabel(self):
        return self.label

    def GetHoverBitmap(self):
        if self.hoverBmp is None:
            return self.normalBmp
        return self.hoverBmp

    def GetDisabledBitmap(self):
        if self.disabledBmp is None:
            return self.normalBmp
        return self.disabledBmp

    def GetDropShadowBitmap(self):
        return self.dropShadowBmp


class PFToolbar(object):
    def __init__(self, parent):
        self.Parent = parent
        self.buttons = []
        self.toolbarX = 0
        self.toolbarY = 0
        self.padding = 2
        self.hoverLabel = ""

    def SetPosition(self, pos):
        self.toolbarX, self.toolbarY = pos

    def AddButton(self, btnBitmap, label="", clickCallback=None, hoverBitmap=None, disabledBitmap=None, show=True):
        btn = PFBaseButton(btnBitmap, label, clickCallback, hoverBitmap, disabledBitmap, show)
        self.buttons.append(btn)
        return btn

    def ClearState(self):
        for button in self.buttons:
            button.SetState()
        self.hoverLabel = ""

    def MouseMove(self, event):
        doRefresh = False
        changeCursor = False
        bx = self.toolbarX
        self.hoverLabel = ""

        for button in self.buttons:
            if not button.IsVisible():
                continue

            state = button.GetState()
            if self.HitTest((bx, self.toolbarY), event.GetPosition(), button.GetSize()):
                changeCursor = True
                if not state & BTN_HOVER:
                    button.SetState(state | BTN_HOVER)
                    self.hoverLabel = button.GetLabel()
                    self.Parent.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
                    doRefresh = True
            else:
                if state & BTN_HOVER:
                    button.SetState(state ^ BTN_HOVER)
                    doRefresh = True

            bwidth, bheight = button.GetSize()
            bx += bwidth + self.padding

        if not changeCursor:
            self.Parent.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        return doRefresh

    def MouseClick(self, event):
        bx = self.toolbarX
        for button in self.buttons:
            if not button.IsVisible():
                continue

            state = button.GetState()
            if state & BTN_PRESSED:
                button.SetState(state ^ BTN_PRESSED)
                if self.HitTest((bx, self.toolbarY), event.GetPosition(), button.GetSize()):
                    return button
                else:
                    return False
            bwidth, bheight = button.GetSize()
            bx += bwidth + self.padding

        bx = self.toolbarX
        for button in self.buttons:
            if not button.IsVisible():
                continue

            state = button.GetState()

            if self.HitTest((bx, self.toolbarY), event.GetPosition(), button.GetSize()):

                if event.LeftDown() or event.LeftDClick():
                    button.SetState(state | BTN_PRESSED)
                    return button

                elif event.LeftUp():
                    button.SetState(state | (not BTN_PRESSED))
                    return button

            bwidth, bheight = button.GetSize()
            bx += bwidth + self.padding

        return None

    def GetWidth(self):
        bx = 0
        for button in self.buttons:
            if not button.IsVisible():
                continue

            bwidth, bheight = button.GetSize()
            bx += bwidth + self.padding

        return bx

    def GetHeight(self):
        height = 0
        for button in self.buttons:
            if not button.IsVisible():
                continue

            bwidth, bheight = button.GetSize()
            height = max(height, bheight)

        return height

    @staticmethod
    def HitTest(target, position, area):
        x, y = target
        px, py = position
        aX, aY = area
        if (x < px < x + aX) and (y < py < y + aY):
            return True
        return False

    def Render(self, pdc):
        bx = self.toolbarX
        for button in self.buttons:
            if not button.IsVisible():
                continue

            by = self.toolbarY
            tbx = bx

            btnState = button.GetState()

            bmp = button.GetDisabledBitmap()
            dropShadowBmp = button.GetDropShadowBitmap()

            if btnState & BTN_NORMAL:
                bmp = button.GetBitmap()

            if btnState & BTN_HOVER:
                bmp = button.GetHoverBitmap()

            if btnState & BTN_PRESSED:
                bmp = button.GetBitmap()
                by += self.padding / 2
                tbx += self.padding / 2

            bmpWidth = bmp.GetWidth()

            pdc.DrawBitmap(dropShadowBmp, bx + self.padding / 2, self.toolbarY + self.padding / 2)
            pdc.DrawBitmap(bmp, tbx, by)

            bx += bmpWidth + self.padding


class SFBrowserItem(wx.Window):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=(0, 16), style=0):
        wx.Window.__init__(self, parent, id, pos, size, style)

        self.highlighted = False
        self.selected = False
        self.bkBitmap = None

        self.canBeDragged = False

        self.toolbar = PFToolbar(self)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

        if "wxMSW" in wx.PlatformInfo:
            self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDown)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

    def OnFocus(self, evt):
        self.SetHighlighted(True)
        self.Refresh()
        evt.Skip()

    def OnKillFocus(self, evt):
        self.SetHighlighted(False)
        self.Refresh()
        evt.Skip()

    def Refresh(self):
        self.RenderBackground()
        wx.Window.Refresh(self)

    def OnPaint(self, event):
        mdc = wx.BufferedPaintDC(self)

        self.RenderBackground()

        mdc.DrawBitmap(self.bkBitmap, 0, 0)

        self.DrawItem(mdc)
        self.toolbar.Render(mdc)

    def DrawItem(self, mdc):
        pass

    def OnEraseBackground(self, event):
        pass

    def OnKeyUp(self, event):
        pass

    def MouseLeftUp(self, event):
        pass

    def MouseLeftDown(self, event):
        pass

    def MouseMove(self, event):
        pass

    def SetDraggable(self, mode=True):
        self.canBeDragged = mode

    def OnLeftUp(self, event):

        if self.HasCapture():
            self.ReleaseMouse()
        if not self.canBeDragged:
            mposx, mposy = wx.GetMousePosition()
            rect = self.GetRect()
            rect.top = rect.left = 0
            cx, cy = self.ScreenToClient((mposx, mposy))
            if not rect.Contains((cx, cy)):
                self.SetHighlighted(False)
                self.toolbar.ClearState()
                self.Refresh()
                return

        btn = self.toolbar.MouseClick(event)

        if btn is not None:
            if btn is not False:
                if btn.GetState() & BTN_NORMAL:
                    btn.DoCallback()
                    self.Refresh()
            else:
                self.Refresh()
            return

        self.MouseLeftUp(event)

    def OnLeftDown(self, event):
        if not self.HasCapture():
            self.CaptureMouse()

        btn = self.toolbar.MouseClick(event)

        if btn is not None:
            if btn.GetState() & BTN_PRESSED:
                self.Refresh()
            return

        self.MouseLeftDown(event)

    def OnEnterWindow(self, event):
        self.SetHighlighted(True)
        self.toolbar.ClearState()
        self.Refresh()
        event.Skip()

    def OnLeaveWindow(self, event):
        self.SetHighlighted(False)
        self.toolbar.ClearState()
        self.Refresh()
        event.Skip()

    def OnMotion(self, event):
        if self.toolbar.MouseMove(event):
            self.Refresh()

        self.MouseMove(event)

        event.Skip()

    @staticmethod
    def GetType():
        return -1

    def SetSelected(self, select=True):
        self.selected = select

    def SetHighlighted(self, highlight=True):
        self.highlighted = highlight

    def GetState(self):

        if self.highlighted and not self.selected:
            state = SB_ITEM_HIGHLIGHTED

        elif self.selected:
            if self.highlighted:
                state = SB_ITEM_SELECTED | SB_ITEM_HIGHLIGHTED
            else:
                state = SB_ITEM_SELECTED
        else:
            state = SB_ITEM_NORMAL

        return state

    def RenderBackground(self):
        rect = self.GetRect()

        windowColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)

        state = self.GetState()

        sFactor = 0.2
        mFactor = None
        eFactor = 0

        if state == SB_ITEM_HIGHLIGHTED:
            mFactor = 0.45
            eFactor = 0.30

        elif state == SB_ITEM_SELECTED | SB_ITEM_HIGHLIGHTED:
            eFactor = 0.3
        elif state == SB_ITEM_SELECTED:
            eFactor = 0.15
        else:
            sFactor = 0.0

        if self.bkBitmap:
            if self.bkBitmap.eFactor == eFactor and self.bkBitmap.sFactor == sFactor and self.bkBitmap.mFactor == mFactor \
                    and rect.width == self.bkBitmap.GetWidth() and rect.height == self.bkBitmap.GetHeight():
                return
            else:
                del self.bkBitmap

        self.bkBitmap = drawUtils.RenderGradientBar(windowColor, rect.width, rect.height, sFactor, eFactor, mFactor)
        self.bkBitmap.state = state
        self.bkBitmap.sFactor = sFactor
        self.bkBitmap.eFactor = eFactor
        self.bkBitmap.mFactor = mFactor
