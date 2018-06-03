# ===============================================================================
#
# ToDo: Bug - when selecting close on a tab, sometimes the tab to the right is
#       selected, most likely due to determination of mouse position
# ToDo: Tab Selection seems overly complicated. OnLeftDown finds tab at
#       position, and then call's CheckTabSelected which calls TabHitTest (when
#       we are already aware it will return due to FindTabAtPos)
# ToDo: Perhaps a better way of finding tabs at position instead of looping
#       through them and getting their regions. Perhaps some smart trickery with
#       mouse pos x (all tabs have same width, so we divide x by width to find
#       tab index?). This will also help with finding close buttons.
# ToDo: Fix page preview code (PFNotebookPagePreview)
#
# ===============================================================================

import wx
import wx.lib.newevent

from gui.bitmap_loader import BitmapLoader
from gui.utils import draw
from gui.utils import color as color_utils
from service.fit import Fit

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
        _PageChanging.__init__(self)
        NotebookTabChangeEvent.__init__(self, old, new)
        VetoAble.__init__(self)


class PageChanged(_PageChanged, NotebookTabChangeEvent):
    def __init__(self, old, new):
        _PageChanged.__init__(self)
        NotebookTabChangeEvent.__init__(self, old, new)


class PageClosing(_PageClosing, VetoAble):
    def __init__(self, i):
        _PageClosing.__init__(self)
        self.__index = i
        VetoAble.__init__(self)
        self.Selection = property(self.GetSelection)

    def GetSelection(self):
        return self.__index


class PageAdding(_PageAdding, VetoAble):
    def __init__(self):
        _PageAdding.__init__(self)
        VetoAble.__init__(self)


class ChromeNotebook(wx.Panel):

    def __init__(self, parent, can_add=True):
        """
        Instance of Notebook. Initializes general layout, includes methods
        for setting current page, replacing pages, any public function for the
        notebook
        """
        super().__init__(parent, wx.ID_ANY, size=(-1, -1))

        self._pages = []
        self._active_page = None

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        tabs_sizer = wx.BoxSizer(wx.VERTICAL)
        self.tabs_container = _TabsContainer(self, can_add=can_add)
        tabs_sizer.Add(self.tabs_container, 0, wx.EXPAND)

        if 'wxMSW' in wx.PlatformInfo:
            style = wx.DOUBLE_BORDER
        else:
            style = wx.SIMPLE_BORDER

        back_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)

        content_sizer = wx.BoxSizer(wx.VERTICAL)
        self.page_container = wx.Panel(self, style=style)
        self.page_container.SetBackgroundColour(back_color)
        content_sizer.Add(self.page_container, 1, wx.EXPAND, 5)

        main_sizer.Add(tabs_sizer, 0, wx.EXPAND, 5)
        main_sizer.Add(content_sizer, 1, wx.EXPAND | wx.BOTTOM, 2)

        self.SetSizer(main_sizer)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Layout()

    def GetPage(self, i):
        return self._pages[i]

    def SetPage(self, i, page):
        if i >= len(self._pages) or i is None or page is None:
            return

        old_page = self._pages[i]
        self._pages[i] = page
        if old_page == self._active_page:
            old_page.Destroy()
            self._active_page = page
        else:
            old_page.Destroy()

        page.Reparent(self.page_container)

        if self._active_page == page:
            self.ShowActive()

    def GetBorders(self):
        """Gets border widths to better determine page size in ShowActive()"""

        bx = wx.SystemSettings.GetMetric(wx.SYS_BORDER_X)
        by = wx.SystemSettings.GetMetric(wx.SYS_BORDER_Y)

        if bx < 0:
            bx = 1
        if by < 0:
            by = 1

        return bx, by

    def ReplaceActivePage(self, page):
        self.SetPage(self.GetSelection(), page)

    def GetSelectedPage(self):
        return self._active_page

    def GetPageIndex(self, page):
        return self._pages.index(page) if page in self._pages else None

    def GetSelection(self):
        return self.GetPageIndex(self._active_page)

    def GetCurrentPage(self):
        return self._active_page

    def GetPageCount(self):
        return len(self._pages)

    def NextPage(self):
        """Used with keyboard shortcut for next page navigation"""
        current_page = self.GetSelection()

        if current_page is None:
            return

        if current_page < self.GetPageCount() - 1:
            self.SetSelection(current_page + 1)
            new_page = current_page + 1
        else:
            self.SetSelection(0)
            new_page = 0

        wx.PostEvent(self, PageChanged(current_page, new_page))

    def PrevPage(self):
        """Used with keyboard shortcut for previous page navigation"""
        current_page = self.GetSelection()

        if current_page is None:
            return

        if current_page > 0:
            self.SetSelection(current_page - 1)
            new_page = current_page - 1
        else:
            self.SetSelection(self.GetPageCount() - 1)
            new_page = self.GetPageCount() - 1

        wx.PostEvent(self, PageChanged(current_page, new_page))

    def AddPage(self, win=None, title="Empty Tab", image: wx.Image=None, closeable=True):
        if self._active_page:
            self._active_page.Hide()

        if not win:
            win = wx.Panel(self)

        win.Reparent(self.page_container)

        self.page_container.Layout()

        self._pages.append(win)
        self.tabs_container.AddTab(title, image, closeable)

        self._active_page = win
        self.ShowActive(True)

    def DisablePage(self, page, toggle):
        idx = self.GetPageIndex(page)

        if toggle and page == self._active_page:
            try:
                # Set page to the first non-disabled page
                self.SetSelection(next(i for i, _ in enumerate(self._pages) if not self.tabs_container.tabs[i].disabled))
            except StopIteration:
                self.SetSelection(0)

        self.tabs_container.DisableTab(idx, toggle)

    def SetSelection(self, page):
        old_selection = self.GetSelection()
        if old_selection != page:
            self._active_page.Hide()
            self._active_page = self._pages[page]
            self.tabs_container.SetSelected(page)
            self.ShowActive()

    def DeletePage(self, n):
        page = self._pages[n]
        self._pages.remove(page)
        page.Destroy()

        self.tabs_container.DeleteTab(n)

        selection = self.tabs_container.GetSelected()
        if selection is not None:
            self._active_page = self._pages[selection]
            self.ShowActive()
            wx.PostEvent(self, PageChanged(-1, selection))
        else:
            self._active_page = None

    def SwitchPages(self, src, dst):
        self._pages[src], self._pages[dst] = self._pages[dst], self._pages[src]

    def ShowActive(self, resize_only=False):
        """
        Sets the size of the page and shows. The sizing logic adjusts for some
        minor sizing errors (scrollbars going beyond bounds)

        resize_only
            if we are not interested in showing the page, only setting the size

        @todo: is resize_only still needed? Was introduced with 8b8b97 in mid
        2011 to fix a resizing bug with blank _pages, cannot reproduce
        13Sept2014
        """

        ww, wh = self.page_container.GetSize()
        bx, by = self.GetBorders()
        ww -= bx * 4
        wh -= by * 4
        self._active_page.SetSize((max(ww, -1), max(wh, -1)))
        self._active_page.SetPosition((0, 0))

        if not resize_only:
            self._active_page.Show()

        self.Layout()

    def IsActive(self, page):
        return self._active_page == page

    def SetPageTitle(self, i, text, refresh=True):
        tab = self.tabs_container.tabs[i]
        tab.text = text
        if refresh:
            self.tabs_container.AdjustTabsSize()
            self.Refresh()

    def SetPageIcon(self, i, icon, refresh=True):
        tab = self.tabs_container.tabs[i]
        tab.tab_img = icon
        if refresh:
            self.tabs_container.AdjustTabsSize()
            self.Refresh()

    def SetPageTextIcon(self, i, text=wx.EmptyString, icon=None):
        self.SetPageTitle(i, text, False)
        self.SetPageIcon(i, icon, False)
        self.tabs_container.AdjustTabsSize()
        self.Refresh()

    def Refresh(self):
        self.tabs_container.Refresh()

    def OnSize(self, event):
        w, h = self.GetSize()
        self.tabs_container.SetSize((w, -1))
        self.tabs_container.UpdateSize()
        self.tabs_container.Refresh()
        self.Layout()

        if self._active_page:
            self.ShowActive()
        event.Skip()


class _TabRenderer:
    def __init__(self, size=(36, 24), text=wx.EmptyString, img: wx.Image=None,
                 closeable=True):

        # tab left/right zones inclination
        self.ctab_left = BitmapLoader.getImage("ctableft", "gui")
        self.ctab_middle = BitmapLoader.getImage("ctabmiddle", "gui")
        self.ctab_right = BitmapLoader.getImage("ctabright", "gui")
        self.ctab_close = BitmapLoader.getImage("ctabclose", "gui")

        self.left_width = self.ctab_left.GetWidth()
        self.right_width = self.ctab_right.GetWidth()
        self.middle_width = self.ctab_middle.GetWidth()
        self.close_btn_width = self.ctab_close.GetWidth()

        width, height = size

        self.min_width = self.left_width + self.right_width + self.middle_width
        self.min_height = self.ctab_middle.GetHeight()

        # set minimum width and height to what is allotted to images
        width = max(width, self.min_width)
        height = max(height, self.min_height)

        self.disabled = False
        self.text = text
        self.tab_size = (width, height)
        self.closeable = closeable
        self.selected = False
        self.close_btn_hovering = False
        self.tab_bitmap = None
        self.tab_back_bitmap = None
        self.padding = 4
        self.font = wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)

        self.tab_img = img
        self.position = (0, 0)  # Not used internally for rendering - helper for tab container
        self.InitTab()

    def SetPosition(self, position):
        self.position = position

    def GetPosition(self):
        return self.position

    def GetSize(self):
        return self.tab_size

    def SetSize(self, size):
        width, height = size

        width = max(width, self.min_width)
        height = max(height, self.min_height)

        self.tab_size = (width, height)
        self.InitTab()

    def SetSelected(self, sel=True):
        self.selected = sel
        self.InitTab()

    def GetSelected(self):
        return self.selected

    def IsSelected(self):
        return self.selected

    def ShowCloseButtonHovering(self, hover=True):
        if self.close_btn_hovering != hover:
            self.close_btn_hovering = hover
            self._Render()

    def GetCloseButtonHoverStatus(self):
        return self.close_btn_hovering

    def GetTabRegion(self):
        new_region = self.CopyRegion(self.tab_region)
        new_region.Subtract(self.close_region) if self.closeable else self.tab_region
        return new_region

    def GetCloseButtonRegion(self):
        return self.CopyRegion(self.close_region)

    def GetMinSize(self):
        ebmp = wx.Bitmap(1, 1)
        mdc = wx.MemoryDC()
        mdc.SelectObject(ebmp)
        mdc.SetFont(self.font)
        textSizeX, textSizeY = mdc.GetTextExtent(self.text)
        totalSize = self.left_width + self.right_width + textSizeX + self.close_btn_width / 2 + 16 + self.padding * 2
        mdc.SelectObject(wx.NullBitmap)
        return totalSize, self.tab_height

    def SetTabImage(self, img):
        self.tab_img = img

    def CopyRegion(self, region):
        rect = region.GetBox()

        newRegion = wx.Region(rect.X, rect.Y, rect.Width, rect.Height)
        newRegion.Intersect(region)

        return newRegion

    def InitTab(self):
        self.tab_width, self.tab_height = self.tab_size

        self.content_width = self.tab_width - self.left_width - self.right_width
        self.tab_region = None
        self.close_region = None

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
            tr, tg, tb, ta = self.selected_color
        else:
            tr, tg, tb, ta = self.inactive_color

        ctab_left = self.ctab_left.Copy()
        ctab_right = self.ctab_right.Copy()
        ctab_middle = self.ctab_middle.Copy()

        ctab_left.Replace(0, 0, 0, tr, tg, tb)
        ctab_right.Replace(0, 0, 0, tr, tg, tb)
        ctab_middle.Replace(0, 0, 0, tr, tg, tb)

        self.ctab_left_bmp = wx.Bitmap(ctab_left)
        self.ctab_right_bmp = wx.Bitmap(ctab_right)
        self.ctab_middle_bmp = wx.Bitmap(ctab_middle)
        self.ctab_close_bmp = wx.Bitmap(self.ctab_close)

    def ComposeTabBack(self):
        """
        Creates the tab background bitmap based upon calculated dimension values
        and modified bitmaps via InitBitmaps()
        """
        bk_bmp = wx.Bitmap(self.tab_width, self.tab_height)

        mdc = wx.MemoryDC()
        mdc.SelectObject(bk_bmp)
        mdc.Clear()

        # draw the left bitmap
        mdc.DrawBitmap(self.ctab_left_bmp, 0, 0)

        # convert middle bitmap and scale to tab width
        cm = self.ctab_middle_bmp.ConvertToImage()
        mimg = cm.Scale(self.content_width, self.ctab_middle.GetHeight(),
                        wx.IMAGE_QUALITY_NORMAL)
        mbmp = wx.Bitmap(mimg)

        # draw middle bitmap, offset by left
        mdc.DrawBitmap(mbmp, self.left_width, 0)

        # draw right bitmap offset by left + middle
        mdc.DrawBitmap(self.ctab_right_bmp,
                       self.content_width + self.left_width, 0)

        mdc.SelectObject(wx.NullBitmap)

        if self.tab_back_bitmap:
            del self.tab_back_bitmap

        self.tab_back_bitmap = bk_bmp

    def InitTabRegions(self):
        """
        Initializes regions for tab, which makes it easier to determine if
        given coordinates are included in a region
        """
        self.tab_region = wx.Region(self.tab_back_bitmap)
        self.close_region = wx.Region(self.ctab_close_bmp)

        x_offset = self.content_width \
            + self.left_width \
            - self.ctab_close_bmp.GetWidth() / 2
        y_offset = (self.tab_height - self.ctab_close_bmp.GetHeight()) / 2
        self.close_region.Offset(x_offset, y_offset)

    def InitColors(self):
        """Determines colors used for tab, based on system settings"""
        self.tab_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)
        self.inactive_color = color_utils.GetSuitable(self.tab_color, 0.25)
        self.selected_color = color_utils.GetSuitable(self.tab_color, 0.10)

    def Render(self):
        return self.tab_bitmap

    def _Render(self):
        """Renders the tab, complete with the icon, text, and close button"""
        if self.tab_bitmap:
            del self.tab_bitmap

        height = self.tab_height

        canvas = wx.Bitmap(self.tab_width, self.tab_height, 24)

        mdc = wx.MemoryDC()

        mdc.SelectObject(canvas)
        mdc.Clear()

        mdc.DrawBitmap(self.tab_back_bitmap, 0, 0, True)

        # draw the tab icon
        if self.tab_img:
            bmp = wx.Bitmap(self.tab_img.ConvertToGreyscale() if self.disabled else self.tab_img)
            # @todo: is this conditional relevant anymore?
            if self.content_width > 16:
                # Draw tab icon
                mdc.DrawBitmap(
                    bmp,
                    self.left_width + self.padding - bmp.GetWidth() / 2,
                    (height - bmp.GetHeight()) / 2)
            text_start = self.left_width + self.padding + bmp.GetWidth() / 2
        else:
            text_start = self.left_width

        mdc.SetFont(self.font)

        maxsize = self.tab_width \
            - text_start \
            - self.right_width \
            - self.padding * 4
        color = self.selected_color if self.selected else self.inactive_color

        mdc.SetTextForeground(color_utils.GetSuitable(color, 1))

        # draw text (with no ellipses)
        text = draw.GetPartialText(mdc, self.text, maxsize, "")
        tx, ty = mdc.GetTextExtent(text)
        mdc.DrawText(text, text_start + self.padding, height / 2 - ty / 2)

        # draw close button
        if self.closeable:
            if self.close_btn_hovering:
                cbmp = self.ctab_close_bmp
            else:
                cimg = self.ctab_close_bmp.ConvertToImage()
                cimg = cimg.AdjustChannels(0.7, 0.7, 0.7, 0.3)
                cbmp = wx.Bitmap(cimg)

            mdc.DrawBitmap(
                cbmp,
                self.content_width + self.left_width - cbmp.GetWidth() / 2,
                (height - cbmp.GetHeight()) / 2)

        mdc.SelectObject(wx.NullBitmap)

        canvas.SetMaskColour((0x12, 0x23, 0x32))
        img = canvas.ConvertToImage()

        if not img.HasAlpha():
            img.InitAlpha()

        bmp = wx.Bitmap(img)
        self.tab_bitmap = bmp

    def __repr__(self):
        return "_TabRenderer(text={}, disabled={}) at {}".format(
            self.text, self.disabled, hex(id(self))
        )


class _AddRenderer:
    def __init__(self):
        """Renders the add tab button"""
        self.add_img = BitmapLoader.getImage("ctabadd", "gui")
        self.width = self.add_img.GetWidth()
        self.height = self.add_img.GetHeight()

        self.region = None
        self.tbmp = wx.Bitmap(self.add_img)
        self.add_bitmap = None

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
        region = wx.Region(self.tbmp)
        return region

    def CopyRegion(self, region):
        rect = region.GetBox()

        new_region = wx.Region(rect.X, rect.Y, rect.Width, rect.Height)
        new_region.Intersect(region)

        return new_region

    def GetRegion(self):
        return self.CopyRegion(self.region)

    def Highlight(self, highlight=False):
        self.highlighted = highlight
        self._Render()

    def IsHighlighted(self):
        return self.highlighted

    def Render(self):
        return self.add_bitmap

    def _Render(self):
        if self.add_bitmap:
            del self.add_bitmap

        alpha = 1 if self.highlighted else 0.3

        img = self.add_img.AdjustChannels(1, 1, 1, alpha)
        bmp = wx.Bitmap(img)
        self.add_bitmap = bmp


class _TabsContainer(wx.Panel):
    def __init__(self, parent, pos=(50, 0), size=(100, 22), id=wx.ID_ANY,
                 can_add=True):
        """
        Defines the tab container. Handles functions such as tab selection and
        dragging, and defines minimum width of tabs (all tabs are of equal
        width, which is determined via widest tab). Also handles the tab
        preview, if any.
        """

        super().__init__(parent, id, pos, size)

        self.tabs = []
        self.width, self.height = size
        self.container_height = self.height
        self.start_drag = False
        self.dragging = False

        # amount of overlap of tabs?
        self.inclination = 7

        if can_add:
            self.reserved = 48
        else:
            self.reserved = self.inclination * 4

        # pixel distance to drag before we actually start dragging
        self.drag_trail = 5

        self.dragx = 0
        self.dragy = 0
        self.dragged_tab = None
        self.drag_trigger = self.drag_trail

        self.show_add_button = can_add

        self.tab_container_width = self.width - self.reserved
        self.tab_min_width = self.width
        self.tab_shadow = _TabRenderer((self.tab_min_width, self.height + 1))

        self.add_button = _AddRenderer()
        self.add_bitmap = self.add_button.Render()

        self.preview_timer = None
        self.preview_timer_id = wx.ID_ANY
        self.preview_wnd = None
        self.preview_bmp = None
        self.preview_pos = None
        self.preview_tab = None

        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SYS_COLOUR_CHANGED, self.OnSysColourChanged)

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

    def OnSysColourChanged(self, event):
        for tab in self.tabs:
            tab.InitTab()
        self.Refresh()

    def OnSize(self, event):
        self.UpdateSize()
        event.Skip()

    def UpdateSize(self):
        """Update tab sizes based on new tab container size"""
        width, _ = self.GetSize()
        if width != self.width:
            self.width = width
            self.tab_container_width = self.width - self.reserved
            self.AdjustTabsSize()

    def OnLeftDown(self, event):
        """ Select tab on mouse down and start dragging logic """
        mposx, mposy = event.GetPosition()
        if not self.start_drag:
            tab = self.FindTabAtPos(mposx, mposy)
            if tab:
                self.CheckTabSelected(tab, mposx, mposy)
                if self.show_add_button:
                    # If we can add tabs, we can drag them. Set flag
                    self.start_drag = True
                    tx, ty = tab.GetPosition()
                    self.dragx = mposx - tx
                    self.dragy = self.container_height - self.height
                self.Refresh()

            self.dragged_tab = tab

    def OnMotion(self, event):
        """
        Determines what happens when the mouse moves. This handles primarily
        dragging (region tab can be dragged) as well as checking if we are over
        an actionable button.
        """
        mposx, mposy = event.GetPosition()

        if self.start_drag:
            if not self.dragging:
                if self.drag_trigger < 0:
                    self.dragging = True
                    self.drag_trigger = self.drag_trail
                    self.CaptureMouse()
                else:
                    self.drag_trigger -= 1
            if self.dragging:
                # we wish to keep tab within tab container boundaries. To do
                # this, we must detect when mouse moves outside of boundaries.
                # Set hard limits to 0 and the size of tab container.
                dtx = mposx - self.dragx
                w, h = self.dragged_tab.GetSize()

                dtx = max(dtx, 0)

                if dtx + w > self.tab_container_width + self.inclination * 2:
                    dtx = self.tab_container_width - w + self.inclination * 2

                self.dragged_tab.SetPosition((dtx, self.dragy))

                # we must modify the surrounding tabs
                index = self.GetTabIndex(self.dragged_tab)

                left_tab = self.GetTabAtLeft(index)
                right_tab = self.GetTabAtRight(index)

                if left_tab:
                    lw, lh = left_tab.GetSize()
                    lx, ly = left_tab.GetPosition()

                    if lx + lw / 2 - self.inclination * 2 > dtx:
                        self.SwitchTabs(index - 1, index, self.dragged_tab)

                if right_tab:
                    rw, rh = right_tab.GetSize()
                    rx, ry = right_tab.GetPosition()

                    if rx + rw / 2 + self.inclination * 2 < dtx + w:
                        self.SwitchTabs(index + 1, index, self.dragged_tab)

                self.UpdateTabsPosition(self.dragged_tab)
                self.Refresh()
            return

        # If we aren't dragging, check for actionable buttons under mouse
        self.CheckCloseHighlighted(mposx, mposy)
        self.CheckAddHighlighted(mposx, mposy)
        self.CheckTabPreview(mposx, mposy)

        event.Skip()

    def OnLeftUp(self, event):
        """Determines what happens when user left clicks (up)"""
        mposx, mposy = event.GetPosition()
        if self.start_drag and self.dragging:
            self.dragging = False
            self.start_drag = False
            self.dragged_tab = None
            self.drag_trigger = self.drag_trail
            self.UpdateTabsPosition()
            self.Refresh()

            if self.HasCapture():
                self.ReleaseMouse()

            return

        if self.start_drag:
            self.start_drag = False
            self.drag_trigger = self.drag_trail

        # Checks if we selected the add button and, if True, returns
        if self.CheckAddButton(mposx, mposy):
            return

        # If there are no tabs, don't waste time
        if self.GetTabsCount() == 0:
            return

        # Gets selected tab (was set when user down clicked)
        sel_tab = self.GetSelectedTab()

        # Check if we selected close button for selected tab
        if self.CheckTabClose(sel_tab, mposx, mposy):
            return

        # Check if we selected close button for all others
        for tab in self.tabs:
            if self.CheckTabClose(tab, mposx, mposy):
                return

    def DisableTab(self, tab, disabled=True):
        tb_renderer = self.tabs[tab]
        tb_renderer.disabled = disabled

        self.AdjustTabsSize()
        self.Refresh()

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
        """Set tab as selected given its index"""
        old_sel_tab = self.GetSelectedTab()
        old_sel_tab.SetSelected(False)
        self.tabs[tabIndex].SetSelected(True)
        self.Refresh()

    def CheckTabSelected(self, tab, x, y):
        """
        Selects the tab at x, y. If the tab at x, y is already selected, simply
        return true. Otherwise, perform TabHitTest and set tab at position to
        selected
        """
        old_sel_tab = self.GetSelectedTab()
        if old_sel_tab == tab:
            return True

        if self.TabHitTest(tab, x, y):
            if tab.disabled:
                return
            tab.SetSelected(True)
            old_sel_tab.SetSelected(False)

            ev = PageChanging(self.tabs.index(old_sel_tab), self.tabs.index(tab))
            wx.PostEvent(self.Parent, ev)

            if ev.isVetoed():
                return False

            self.Refresh()
            sel_tab = self.tabs.index(tab)
            self.Parent.SetSelection(sel_tab)

            wx.PostEvent(self.Parent, PageChanged(self.tabs.index(old_sel_tab),
                                                  self.tabs.index(tab)))

            return True

        return False

    def CheckTabClose(self, tab, x, y):
        """
        Determines if close button was selected for the given tab by comparing
        x and y position with known close button region
        """
        if not tab.closeable:  # if not able to close, return False
            return False

        region = tab.GetCloseButtonRegion()
        posx, posy = tab.GetPosition()
        region.Offset(posx, posy)

        if region.Contains(x, y):
            index = self.tabs.index(tab)
            ev = PageClosing(index)
            wx.PostEvent(self.Parent, ev)

            if ev.isVetoed():
                return False

            index = self.GetTabIndex(tab)
            self.Parent.DeletePage(index)
            wx.PostEvent(self.Parent, PageClosed(index=index))

            sel = self.GetSelected()
            if sel is not None:
                wx.PostEvent(self.Parent, PageChanged(-1, sel))

            return True
        return False

    def CheckAddButton(self, x, y):
        """
        Determines if add button was selected by comparing x and y position with
        add button region
        """
        if not self.show_add_button:  # if not able to add, return False
            return

        region = self.add_button.GetRegion()
        ax, ay = self.add_button.GetPosition()
        region.Offset(ax, ay)

        if region.Contains(x, y):
            ev = PageAdding()
            wx.PostEvent(self.Parent, ev)
            if ev.isVetoed():
                return False

            self.Parent.AddPage()
            wx.PostEvent(self.Parent, PageAdded())
            return True

    def CheckCloseHighlighted(self, x, y):
        """
        Checks if mouse pos at x, y is over a close button. If so, set the
        close hovering flag for that tab
        """
        dirty = False

        for tab in self.tabs:
            region = tab.GetCloseButtonRegion()
            posx, posy = tab.GetPosition()
            region.Offset(posx, posy)

            if region.Contains(x, y):
                if not tab.GetCloseButtonHoverStatus():
                    tab.ShowCloseButtonHovering(True)
                    dirty = True
            else:
                if tab.GetCloseButtonHoverStatus():
                    tab.ShowCloseButtonHovering(False)
                    dirty = True
            if dirty:
                self.Refresh()
                break

    def FindTabAtPos(self, x, y):
        if self.GetTabsCount() == 0:
            return None

        # test current tab first
        sel_tab = self.GetSelectedTab()
        if self.TabHitTest(sel_tab, x, y):
            return sel_tab

        # test all other tabs next
        for tab in self.tabs:
            if self.TabHitTest(tab, x, y):
                return tab

        return None

    def TabHitTest(self, tab, x, y):
        """ Test if x and y are contained within a tabs region """
        tabRegion = tab.GetTabRegion()
        tabPos = tab.GetPosition()
        tabPosX, tabPosY = tabPos
        tabRegion.Offset(tabPosX, tabPosY)

        if tabRegion.Contains(x, y):
            return True

        return False

    def GetTabAtLeft(self, tab_index):
        return self.tabs[tab_index - 1] if tab_index > 0 else None

    def GetTabAtRight(self, tab_index):
        if tab_index < self.GetTabsCount() - 1:
            return self.tabs[tab_index + 1]
        else:
            return None

    def SwitchTabs(self, src, dst, dragged_tab=None):
        self.tabs[src], self.tabs[dst] = self.tabs[dst], self.tabs[src]
        self.UpdateTabsPosition(dragged_tab)
        self.Parent.SwitchPages(src, dst)
        self.Refresh()

    def GetTabIndex(self, tab):
        return self.tabs.index(tab)

    def CheckTabPreview(self, mposx, mposy):
        """
        Checks to see if we have a tab preview and sets up the timer for it
        to display
        """
        sFit = Fit.getInstance()
        if not sFit.serviceFittingOptions["showTooltip"] or False:
            return

        if self.preview_timer:
            if self.preview_timer.IsRunning():
                if self.preview_wnd:
                    self.preview_timer.Stop()
                return

        if self.preview_wnd:
            self.preview_wnd.Show(False)
            del self.preview_wnd
            self.preview_wnd = None

        for tab in self.tabs:
            if not tab.GetSelected():
                if self.TabHitTest(tab, mposx, mposy):
                    try:
                        page = self.Parent.GetPage(self.GetTabIndex(tab))
                        if hasattr(page, "Snapshot"):
                            if not self.preview_timer:
                                self.preview_timer = wx.Timer(
                                    self, self.preview_timer_id)

                            self.preview_tab = tab
                            self.preview_timer.Start(500, True)
                            break
                    except:
                        pass

    def CheckAddHighlighted(self, x, y):
        """
        Checks to see if x, y are in add button region, and sets the highlight
        flag
        """
        if not self.show_add_button:
            return

        region = self.add_button.GetRegion()
        ax, ay = self.add_button.GetPosition()
        region.Offset(ax, ay)

        if region.Contains(x, y):
            if not self.add_button.IsHighlighted():
                self.add_button.Highlight(True)
                self.Refresh()
        else:
            if self.add_button.IsHighlighted():
                self.add_button.Highlight(False)
                self.Refresh()

    def OnPaint(self, event):
        mdc = wx.AutoBufferedPaintDC(self)

        # if 'wxMac' in wx.PlatformInfo:
        #     color = wx.Colour(0, 0, 0)
        #     brush = wx.Brush(color)
        #     # @todo: what needs to be changed with wxPheonix?
        #     from Carbon.Appearance import kThemeBrushDialogBackgroundActive
        #     brush.MacSetTheme(kThemeBrushDialogBackgroundActive)
        # else:
        color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)
        brush = wx.Brush(color)

        if "wxGTK" not in wx.PlatformInfo:
            mdc.SetBackground(brush)
            mdc.Clear()

        selected = None

        if self.show_add_button:
            ax, ay = self.add_button.GetPosition()
            mdc.DrawBitmap(self.add_button.Render(), ax, ay, True)

        for i in range(len(self.tabs) - 1, -1, -1):
            tab = self.tabs[i]
            posx, posy = tab.GetPosition()

            if not tab.IsSelected():
                # drop shadow first
                mdc.DrawBitmap(self.fx_bmp, posx, posy, True)
                bmp = tab.Render()
                img = bmp.ConvertToImage()
                img = img.AdjustChannels(1, 1, 1, 0.85)
                bmp = wx.Bitmap(img)
                mdc.DrawBitmap(bmp, posx, posy, True)
            else:
                selected = tab

        # we draw selected tab separately (instead of in else) so as to not hide
        # the front bit behind the preceding tab
        if selected:
            posx, posy = selected.GetPosition()
            # drop shadow first
            mdc.DrawBitmap(self.fx_bmp, posx, posy, True)

            bmp = selected.Render()

            if self.dragging:
                img = bmp.ConvertToImage()
                img = img.AdjustChannels(1.2, 1.2, 1.2, 0.7)
                bmp = wx.Bitmap(img)

            mdc.DrawBitmap(bmp, posx, posy, True)

    def OnErase(self, event):
        pass

    def UpdateTabFX(self):
        """ Updates tab drop shadow bitmap """
        self.tab_shadow.SetSize((self.tab_min_width, self.height + 1))
        fx_bmp = self.tab_shadow.Render()

        img = fx_bmp.ConvertToImage()
        if not img.HasAlpha():
            img.InitAlpha()
        img = img.Blur(2)
        img = img.AdjustChannels(0.3, 0.3, 0.3, 0.35)

        self.fx_bmp = wx.Bitmap(img)

    def AddTab(self, title=wx.EmptyString, img=None, closeable=False):
        self.ClearTabsSelected()

        tab_renderer = _TabRenderer((200, self.height), title, img, closeable)
        tab_renderer.SetSelected(True)

        self.tabs.append(tab_renderer)
        self.AdjustTabsSize()
        self.Refresh()

    def ClearTabsSelected(self):
        for tab in self.tabs:
            tab.SetSelected(False)

    def DeleteTab(self, tab):
        tab_renderer = self.tabs[tab]
        was_selected = tab_renderer.GetSelected()
        self.tabs.remove(tab_renderer)

        if tab_renderer:
            del tab_renderer

        # determine our new selection
        if was_selected and self.GetTabsCount() > 0:
            if tab > self.GetTabsCount() - 1:
                self.tabs[self.GetTabsCount() - 1].SetSelected(True)
            else:
                self.tabs[tab].SetSelected(True)

        self.AdjustTabsSize()
        self.Refresh()

    def GetTabsCount(self):
        return len(self.tabs)

    def AdjustTabsSize(self):
        """
        Adjust tab sizes to ensure that they are all consistent and can fit into
        the tab container.
        """

        # first we loop through our tabs and calculate the the largest tab. This
        # is the size that we will base our calculations off

        max_width = 100  # Tab should be at least 100
        for tab in self.tabs:
            mw, _ = tab.GetMinSize()  # Tab min size includes tab contents
            max_width = max(mw, max_width)

        # Divide tab container by number of tabs and add inclination. This will
        # return the ideal max size for the containers size
        if self.GetTabsCount() > 0:
            dx = self.tab_container_width / self.GetTabsCount() + self.inclination * 2
            self.tab_min_width = min(dx, max_width)

        # Apply new size to all tabs
        for tab in self.tabs:
            tab.SetSize((self.tab_min_width, self.height))

        if self.GetTabsCount() > 0:
            # update drop shadow based on new sizes
            self.UpdateTabFX()

        self.UpdateTabsPosition()

    def UpdateTabsPosition(self, skip_tab=None):
        tabsWidth = 0
        for tab in self.tabs:
            tabsWidth += tab.tab_width - self.inclination * 2

        pos = tabsWidth
        selected = None
        for i in range(len(self.tabs) - 1, -1, -1):
            tab = self.tabs[i]
            width = tab.tab_width - self.inclination * 2
            pos -= width
            if not tab.IsSelected():
                tab.SetPosition((pos, self.container_height - self.height))
            else:
                selected = tab
                selpos = pos

        if selected is not skip_tab:
            selected.SetPosition((selpos, self.container_height - self.height))

        self.add_button.SetPosition((round(tabsWidth) + self.inclination * 2,
                                     self.container_height - self.height / 2 - self.add_button.GetHeight() / 3))

    def OnLeaveWindow(self, event):
        if self.start_drag and not self.dragging:
            self.dragging = False
            self.start_drag = False
            self.dragged_tab = None
            self.drag_trigger = self.drag_trail
            if self.HasCapture():
                self.ReleaseMouse()

        if self.preview_wnd:
            self.preview_wnd.Show(False)
            del self.preview_wnd
            self.preview_wnd = None
        event.Skip()

    def OnTimer(self, event):
        mposx, mposy = wx.GetMousePosition()
        cposx, cposy = self.ScreenToClient((mposx, mposy))

        if self.FindTabAtPos(cposx, cposy) == self.preview_tab:
            if not self.preview_tab.GetSelected():
                page = self.Parent.GetPage(self.GetTabIndex(self.preview_tab))
                if page.Snapshot():

                    self.preview_wnd = PFNotebookPagePreview(
                                                        self,
                                                        (mposx + 3, mposy + 3),
                                                        page.Snapshot(),
                                                        self.preview_tab.text)
                    self.preview_wnd.Show()

        event.Skip()


class PFNotebookPagePreview(wx.Frame):
    def __init__(self, parent, pos, bitmap, title):
        super().__init__(parent, id=wx.ID_ANY, title=wx.EmptyString, pos=pos,
                         size=wx.DefaultSize, style=wx.NO_BORDER |
                                                    wx.FRAME_NO_TASKBAR |
                                                    wx.STAY_ON_TOP)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
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

        hfont = wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
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
        canvas = wx.Bitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)
        color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        mdc.SetBackground(wx.Brush(color))
        mdc.Clear()

        font = wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        mdc.SetFont(font)

        x, y = mdc.GetTextExtent(self.title)

        mdc.SetBrush(wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)))
        mdc.DrawRectangle(0, 0, rect.width, 16)

        mdc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        mdc.DrawBitmap(self.bitmap, 0, 16)

        mdc.SetPen(wx.Pen("#000000", width=1))
        mdc.SetBrush(wx.TRANSPARENT_BRUSH)

        mdc.DrawRectangle(0, 16, rect.width, rect.height - 16)


if __name__ == "__main__":

    # need to set up some paths, since bitmap loader requires config to have things
    # Should probably change that so that it's not dependant on config
    import os
    os.chdir('..')
    import config
    config.defPaths(None)

    class Frame(wx.Frame):
        def __init__(self, title):
            super().__init__(None, title=title, size=(1000, 500))

            if 'wxMSW' in wx.PlatformInfo:
                color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
                self.SetBackgroundColour(color)

            main_sizer = wx.BoxSizer(wx.HORIZONTAL)
            splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
            main_sizer.Add(splitter, 1, wx.EXPAND | wx.ALL, 2)

            # Main test notebook
            self.notebook = ChromeNotebook(splitter)

            # Tests can_add, has dummy tabs
            notebook2 = ChromeNotebook(splitter, can_add=False)

            self.statusbar = self.CreateStatusBar()

            panel = wx.Panel(self)
            box = wx.BoxSizer(wx.VERTICAL)

            head = wx.StaticText(panel, -1, "Chome Tabs Test")
            head.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
            box.Add(head, 0, wx.ALL, 10)

            self.tctrl = wx.TextCtrl(panel, wx.ID_ANY, "Tab Name")

            self.close_check = wx.CheckBox(panel, label="Closable?")
            self.close_check.SetValue(True)

            self.icon_check = wx.CheckBox(panel, label="Icon?")
            self.icon_check.SetValue(True)

            button = wx.Button(panel, wx.ID_ANY, "Create")
            button.Bind(wx.EVT_BUTTON, self.OnCreate)

            box.Add(self.tctrl, 0, wx.ALL, 5)
            box.Add(self.close_check, 0, wx.ALL, 5)
            box.Add(self.icon_check, 0, wx.ALL, 5)
            box.Add(button, 0, wx.ALL, 10)

            self.notebook.AddPage(panel, "Tab1", closeable=False)

            # Add dummy pages
            notebook2.AddPage()
            notebook2.AddPage()

            splitter.SplitVertically(self.notebook, notebook2)

            panel.SetSizer(box)
            panel.Layout()
            self.SetSizer(main_sizer)

        def OnCreate(self, event):
            tab_name = self.tctrl.GetValue()
            tab_icon = BitmapLoader.getImage("ship_small", "gui")
            self.notebook.AddPage(
                title=tab_name,
                image=tab_icon if self.icon_check.GetValue() else None,
                closeable=self.close_check.GetValue())

    app = wx.App(redirect=False)   # Error messages go to popup window
    top = Frame("Test Chrome Tabs")
    top.Show()
    app.MainLoop()
