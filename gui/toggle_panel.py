# ===============================================================================
# TogglePanel is based on PyCollapsiblePane - includes a few improvements
# such as adding items to header, lack of button implementation ("GTK
# expander" style is implemented with plain text with unicode arrows rather
# than drawn geometry), etc.
#
# When adding TogglePanel to sizer, it is important to ensure the following:
#     sizer is vertical
#     set proportion = 0
#
# ToDo: Create animations for collapsing / expanding
#
# ===============================================================================

import wx


class TogglePanel(wx.Panel):
    def __init__(self, parent, force_layout=False, *args, **kargs):
        super().__init__(parent, *args, **kargs)

        self._toggled = True
        self.parent = parent
        self.force_layout = force_layout

        # Create the main sizer of this panel
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)

        # Create the header panel, set sizer, and add to main sizer
        self.header_panel = wx.Panel(self)
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.header_panel.SetSizer(header_sizer)

        self.main_sizer.Add(self.header_panel, 0, wx.EXPAND | wx.TOP |
                            wx.BOTTOM | wx.RIGHT, 1)

        # Add arrow
        self.header_arrow = wx.StaticText(self.header_panel, wx.ID_ANY,
                                          "\u25bc", size=wx.Size((10, -1)))
        header_sizer.Add(self.header_arrow, 0, wx.RIGHT, 5)

        # Add header text
        self.header_label = wx.StaticText(self.header_panel, wx.ID_ANY, "")
        font = parent.GetFont()
        font.SetWeight(wx.BOLD)
        self.header_label.SetFont(font)
        header_sizer.Add(self.header_label, 0, wx.RIGHT, 5)

        # Add a sizer for additional header items if we need it
        self.hcontent_sizer = wx.BoxSizer(wx.HORIZONTAL)
        header_sizer.Add(self.hcontent_sizer, 1, wx.RIGHT, 5)

        # Create the content panel, set sizer, and add to main sizer
        self.content_panel = wx.Panel(self)
        self.content_sizer = wx.BoxSizer(wx.VERTICAL)
        self.content_panel.SetSizer(self.content_sizer)

        self.main_sizer.Add(self.content_panel, 0, wx.EXPAND | wx.RIGHT |
                            wx.LEFT, 5)

        self.Layout()

        # Connect Events
        self.header_label.Bind(wx.EVT_LEFT_UP, self.ToggleContent)
        self.header_arrow.Bind(wx.EVT_LEFT_UP, self.ToggleContent)
        self.header_panel.Bind(wx.EVT_LEFT_UP, self.ToggleContent)

    def __del__(self):
        pass

    def AddToggleItem(self, item):
        item.Bind(wx.EVT_LEFT_UP, self.ToggleContent)

    def GetHeaderContentSizer(self):
        return self.hcontent_sizer

    def GetHeaderPanel(self):
        return self.header_panel

    def InsertItemInHeader(self, item):
        self.hcontent_sizer.Add(item, 0, 0, 0)
        self.AddToggleItem(item)
        self.Layout()

    def AddSizer(self, sizer):
        self.content_sizer.Add(sizer, 0, wx.EXPAND | wx.ALL, 0)
        self.Layout()

    def GetContentPanel(self):
        return self.content_panel

    def SetLabel(self, label):
        self.header_label.SetLabel(label)

    def IsCollapsed(self):
        return not self._toggled

    def IsExpanded(self):
        return self._toggled

    def OnStateChange(self, sz):
        self.SetSize(sz)

        self.parent.GetSizer().SetSizeHints(self.parent)

        if not self._toggled:
            if self.parent.GetSizer():
                # we have just set the size hints...
                sz = self.parent.GetSizer().CalcMin()

                # use SetClientSize() and not SetSize() otherwise the size for
                # e.g. a wxFrame with a menubar wouldn't be correctly set
                self.parent.SetClientSize(sz)
            else:
                self.parent.Layout()
        else:
            # force our parent to "fit", i.e. expand so that it can honor
            # our minimal size
            self.parent.Fit()

    def ToggleContent(self, event):
        # self.Freeze()

        if self._toggled:
            # If we are expanded, save previous size and collapse by setting
            # content height to 0
            self.content_min_size = self.content_panel.GetSize()
            self.content_panel.SetMinSize((self.content_min_size[0], 0))
            self.header_arrow.SetLabel("\u25b6")
        else:
            # If we are collapsed, set content size to previously saved value
            self.content_panel.SetMinSize(self.content_min_size)
            self.header_arrow.SetLabel("\u25bc")

        self._toggled = not self._toggled

        # self.Thaw()

        if self.force_layout:
            self.parent.Layout()
        else:
            self.OnStateChange(self.GetBestSize())
