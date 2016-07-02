import wx
import gui.mainFrame

def formatTable(valueList, numColumns, panel):
    '''
    bSizer = wx.BoxSizer(wx.VERTICAL)

    for valueRow in valueList:
        gSizer = wx.GridSizer(0, numColumns, 0, 0)

        for valueColumn in valueRow:
            #panel.StaticText = wx.StaticText(panel, wx.ID_ANY, valueColumn, wx.DefaultPosition, wx.DefaultSize, 0)
            panel.StaticText = wx.StaticText(panel, wx.ID_ANY, valueColumn, wx.DefaultPosition, wx.DefaultSize, 0)
            panel.StaticText.Wrap(-1)
            gSizer.Add(panel.StaticText, 0, wx.ALIGN_LEFT, 0)

        bSizer.Add(gSizer, 1, wx.ALIGN_LEFT, 0)
    '''

    fgSizer = wx.FlexGridSizer(0, numColumns, 0, 0)
    fgSizer.SetFlexibleDirection(wx.BOTH)
    fgSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

    for valueRow in valueList:
        #gSizer = wx.GridSizer(0, numColumns, 0, 0)

        for valueColumn in valueRow:
            panel.StaticText = wx.StaticText(panel, wx.ID_ANY, valueColumn, wx.DefaultPosition, wx.DefaultSize, 50)
            panel.StaticText.Wrap(-1)
            fgSizer.Add(panel.StaticText, 0, wx.ALIGN_LEFT, 50)

        #bSizer.Add(gSizer, 1, wx.ALIGN_LEFT, 0)


    return fgSizer