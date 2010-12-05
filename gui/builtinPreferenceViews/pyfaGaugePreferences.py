#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version May    4 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import copy

###########################################################################
## Class PFGaugePref
###########################################################################

class PFGaugePreview(wx.Window):
    def __init__ (self, parent, id = wx.ID_ANY, value = 0, pos = wx.DefaultPosition, size = wx.DefaultSize, style = 0):
        wx.Window.__init__(self, parent, id, pos = pos, size = size, style = style)

        self.value = float(value)
        self.oldValue = self.value

        self.percS = 0
        self.percE = 0

        self.animate = True
        self.animDir = 1
        self._fractionDigits = 2

        self.colorS = wx.Colour(0,0,0)
        self.colorE = wx.Colour(0,0,0)
        self.gradientStart = 0

        self.bkColor = wx.Colour(0,0,0)
        self.SetMinSize((100,-1))

        self.font = wx.FontFromPixelSize((0,13),wx.SWISS, wx.NORMAL, wx.NORMAL, False)

        self.timerID = wx.NewId()
        self.timer = wx.Timer(self, self.timerID)
        self.timerInterval = 20

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnWindowEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnWindowLeave)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBk)

    def OnEraseBk(self, event):
        pass

    def OnTimer(self, event):
        if event.GetId() == self.timerID:
            self.value += self.animDir
            if self.value > 100:
                self.value = 100
                self.animDir = -1
            if self.value <0:
                self.value = 0
                self.animDir = 1
            self.Refresh()

    def OnWindowEnter(self, event):
        if not self.animate:
            return
        self.oldValue = self.value
        if self.timer.IsRunning():
            self.timer.Stop()
        self.timer.Start(self.timerInterval)
        event.Skip()

    def OnWindowLeave(self, event):
        if not self.animate:
            return
        if self.timer.IsRunning():
            self.timer.Stop()
        self.value = self.oldValue
        self.Refresh()
        event.Skip()

    def CanAnimate(self, anim = True):
        self.animate = anim
        if self.timer.IsRunning():
            self.timer.Stop()
        self.value = self.oldValue
        self.Refresh()

    def SetGradientStart(self, value):
        self.gradientStart = value
        self.Refresh()

    def SetColour(self, colorS, colorE):
        self.colorS = colorS
        self.colorE = colorE

        self.Refresh()

    def SetValue(self, value):
        self.value = min(max(value,0),100)
        self.Refresh()

    def SetPercentages(self, start, end):
        self.percS = start
        self.percE = end
        self.Refresh()

    def CalculateGColor(self, color, delta):
        bkR ,bkG , bkB = color
        scale = delta

        r = bkR + scale
        g = bkG + scale
        b = bkB + scale

        r = min(max(r,0),255)
        b = min(max(b,0),255)
        g = min(max(g,0),255)

        return wx.Colour(r,g,b,255)

    def CalculateTransitionColor(self, startColor, endColor, delta):
        sR,sG,sB = startColor
        eR,eG,eB = endColor

        tR = sR + (eR - sR) *  delta
        tG = sG + (eG - sG) *  delta
        tB = sB + (eB - sB) *  delta

        return (tR, tG, tB)

    def OnPaint(self, event):
        rect = self.GetClientRect()
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.bkColor))
        dc.Clear()

        value = float(self.value)
        if self.percS >= 100:
            w = rect.width
        else:
            w = rect.width * (float(value) / 100)
        r = copy.copy(rect)
        r.width = w
        r.height = r.height/2+1

        color = self.CalculateTransitionColor(self.colorS, self.colorE, float(value)/100)
        gcolor = self.CalculateGColor(color, - self.gradientStart)
        dc.GradientFillLinear(r, gcolor, color, wx.SOUTH)
        r.top = r.height
        dc.GradientFillLinear(r, gcolor, color, wx.NORTH)

        dc.SetFont(self.font)

        r = copy.copy(rect)
        r.left +=1
        r.top +=1


        formatStr = "{0:." + str(self._fractionDigits) + "f}%"
        value = (self.percE - self.percS) * value / (self.percE - self.percS)
        value = self.percS + (self.percE - self.percS) * value / 100
        dc.SetTextForeground(wx.Colour(80,80,80))
        dc.DrawLabel(formatStr.format(value), r, wx.ALIGN_CENTER)

        dc.SetTextForeground(wx.Colour(255,255,255))
        dc.DrawLabel(formatStr.format(value), rect, wx.ALIGN_CENTER)


class PFGaugePref ( wx.Dialog):

    def __init__( self ):
        wx.Dialog.__init__ ( self, None, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,261 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetTitle("Pyfa's Gauges colors editor")
        self.InitDefaultColours()

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        gSizer1 = wx.BoxSizer( wx.HORIZONTAL )

        self.st0100 = wx.StaticText( self, wx.ID_ANY, u"0 - 100", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.st0100.Wrap( -1 )
        gSizer1.Add( self.st0100, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.cp0100S = wx.ColourPickerCtrl( self, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
        gSizer1.Add( self.cp0100S, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.cp0100E = wx.ColourPickerCtrl( self, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
        gSizer1.Add( self.cp0100E, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.gauge0100S = PFGaugePreview( self, wx.ID_ANY, 33, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        gSizer1.Add( self.gauge0100S, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

        self.gauge0100M = PFGaugePreview( self, wx.ID_ANY, 66, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        gSizer1.Add( self.gauge0100M, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

        self.gauge0100E = PFGaugePreview( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        gSizer1.Add( self.gauge0100E, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )

        mainSizer.Add( gSizer1, 0, wx.EXPAND, 5 )

        gSizer2 = wx.BoxSizer( wx.HORIZONTAL )

        self.st100101 = wx.StaticText( self, wx.ID_ANY, u"100 - 101", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.st100101.Wrap( -1 )
        gSizer2.Add( self.st100101, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.cp100101S = wx.ColourPickerCtrl( self, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
        gSizer2.Add( self.cp100101S, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.cp100101E = wx.ColourPickerCtrl( self, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
        gSizer2.Add( self.cp100101E, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.gauge100101S = PFGaugePreview( self, wx.ID_ANY, 33, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        gSizer2.Add( self.gauge100101S, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

        self.gauge100101M = PFGaugePreview( self, wx.ID_ANY, 66, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        gSizer2.Add( self.gauge100101M, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

        self.gauge100101E = PFGaugePreview( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        gSizer2.Add( self.gauge100101E, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )

        mainSizer.Add( gSizer2, 0, wx.EXPAND, 5 )

        gSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        self.st101103 = wx.StaticText( self, wx.ID_ANY, u"101 - 103", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.st101103.Wrap( -1 )
        gSizer3.Add( self.st101103, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.cp101103S = wx.ColourPickerCtrl( self, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
        gSizer3.Add( self.cp101103S, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.cp101103E = wx.ColourPickerCtrl( self, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
        gSizer3.Add( self.cp101103E, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.gauge101103S = PFGaugePreview( self, wx.ID_ANY, 33, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        gSizer3.Add( self.gauge101103S, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

        self.gauge101103M = PFGaugePreview( self, wx.ID_ANY, 66, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        gSizer3.Add( self.gauge101103M, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

        self.gauge101103E = PFGaugePreview( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        gSizer3.Add( self.gauge101103E, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )

        mainSizer.Add( gSizer3, 0, wx.EXPAND, 5 )

        gSizer4 = wx.BoxSizer( wx.HORIZONTAL )

        self.st103105 = wx.StaticText( self, wx.ID_ANY, u"103 - 105", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.st103105.Wrap( -1 )
        gSizer4.Add( self.st103105, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.cp103105S = wx.ColourPickerCtrl( self, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
        gSizer4.Add( self.cp103105S, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.cp103105E = wx.ColourPickerCtrl( self, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
        gSizer4.Add( self.cp103105E, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.gauge103105S = PFGaugePreview( self, wx.ID_ANY, 33, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        gSizer4.Add( self.gauge103105S, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

        self.gauge103105M = PFGaugePreview( self, wx.ID_ANY, 66, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        gSizer4.Add( self.gauge103105M, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

        self.gauge103105E = PFGaugePreview( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        gSizer4.Add( self.gauge103105E, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )

        mainSizer.Add( gSizer4, 0, wx.EXPAND, 5 )

        footerSizer = wx.BoxSizer( wx.VERTICAL )

        self.sl1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        footerSizer.Add( self.sl1, 0, wx.EXPAND |wx.ALL, 5 )

        previewSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.wndPreview0100 = PFGaugePreview( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, 0)
        previewSizer.Add( self.wndPreview0100, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

        self.wndPreview100101 = PFGaugePreview( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, 0)
        previewSizer.Add( self.wndPreview100101, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

        self.wndPreview101103 = PFGaugePreview( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, 0)
        previewSizer.Add( self.wndPreview101103, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

        self.wndPreview103105 = PFGaugePreview( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, 0)
        previewSizer.Add( self.wndPreview103105, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

        footerSizer.Add( previewSizer, 1, wx.EXPAND | wx.ALL, 5 )

        buttonsSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.cbLink = wx.CheckBox( self, wx.ID_ANY, u"Link Colors", wx.DefaultPosition, wx.DefaultSize, 0 )
        buttonsSizer.Add( self.cbLink, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.LEFT, 5 )

        self.sliderGradientStart = wx.Slider( self, wx.ID_ANY, self.gradientStart, 0, 255, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_LABELS )
        buttonsSizer.Add( self.sliderGradientStart, 1, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )

        self.btnRestore = wx.Button( self, wx.ID_ANY, u"Restore Defaults", wx.DefaultPosition, wx.DefaultSize, 0 )
        buttonsSizer.Add( self.btnRestore, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )

        self.btnDump = wx.Button( self, wx.ID_ANY, u"Dump Colors", wx.DefaultPosition, wx.DefaultSize, 0 )
        buttonsSizer.Add( self.btnDump, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )

        self.btnOk = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        buttonsSizer.Add( self.btnOk, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )

        footerSizer.Add( buttonsSizer, 1, wx.ALIGN_RIGHT, 5 )
        mainSizer.Add( footerSizer, 0, wx.EXPAND, 5 )

        self.SetSizer( mainSizer )

        self.SetColours()

        self.Fit()
        self.Layout()

        self.sliderGradientStart.Bind(wx.EVT_SCROLL, self.OnGradientStartScroll)
        self.btnRestore.Bind(wx.EVT_BUTTON, self.RestoreDefaults)
        self.btnDump.Bind(wx.EVT_BUTTON, self.DumpColours)
        self.btnOk.Bind(wx.EVT_BUTTON, self.OnOk)

        self.cp0100S.Bind( wx.EVT_COLOURPICKER_CHANGED, self.OnColourChanged )
        self.cp0100E.Bind( wx.EVT_COLOURPICKER_CHANGED, self.OnColourChanged )

        self.cp100101S.Bind( wx.EVT_COLOURPICKER_CHANGED, self.OnColourChanged )
        self.cp100101E.Bind( wx.EVT_COLOURPICKER_CHANGED, self.OnColourChanged )

        self.cp101103S.Bind( wx.EVT_COLOURPICKER_CHANGED, self.OnColourChanged )
        self.cp101103E.Bind( wx.EVT_COLOURPICKER_CHANGED, self.OnColourChanged )

        self.cp103105S.Bind( wx.EVT_COLOURPICKER_CHANGED, self.OnColourChanged )
        self.cp103105E.Bind( wx.EVT_COLOURPICKER_CHANGED, self.OnColourChanged )


    def InitDefaultColours(self):
        self.c0100S = wx.Colour(153,153,153)
        self.c0100E = wx.Colour(153,185,56)

        self.c100101S = wx.Colour(153,185,56)
        self.c100101E = wx.Colour(163,206,53)

        self.c101103S = wx.Colour(163,206,53)
        self.c101103E = wx.Colour(223,146,53)

        self.c103105S = wx.Colour(223,146,53)
        self.c103105E = wx.Colour(243,86,53)
        self.gradientStart = 31

    def SetColours(self):
        self.cp0100S.SetColour(self.c0100S)
        self.cp0100E.SetColour(self.c0100E)
        self.gauge0100S.SetColour(self.c0100S, self.c0100E)
        self.gauge0100M.SetColour(self.c0100S, self.c0100E)
        self.gauge0100E.SetColour(self.c0100S, self.c0100E)

        self.gauge0100S.SetPercentages(0, 99.99)
        self.gauge0100M.SetPercentages(0, 99.99)
        self.gauge0100E.SetPercentages(0, 99.99)

        self.gauge0100S.SetGradientStart(self.sliderGradientStart.GetValue())
        self.gauge0100M.SetGradientStart(self.sliderGradientStart.GetValue())
        self.gauge0100E.SetGradientStart(self.sliderGradientStart.GetValue())


        self.cp100101S.SetColour(self.c100101S)
        self.cp100101E.SetColour(self.c100101E)
        self.gauge100101S.SetColour(self.c100101S, self.c100101E)
        self.gauge100101M.SetColour(self.c100101S, self.c100101E)
        self.gauge100101E.SetColour(self.c100101S, self.c100101E)

        self.gauge100101S.SetGradientStart(self.sliderGradientStart.GetValue())
        self.gauge100101M.SetGradientStart(self.sliderGradientStart.GetValue())
        self.gauge100101E.SetGradientStart(self.sliderGradientStart.GetValue())

        self.gauge100101S.SetPercentages(100, 100.99)
        self.gauge100101M.SetPercentages(100, 100.99)
        self.gauge100101E.SetPercentages(100, 100.99)

        self.gauge100101S.SetGradientStart(self.sliderGradientStart.GetValue())
        self.gauge100101M.SetGradientStart(self.sliderGradientStart.GetValue())
        self.gauge100101E.SetGradientStart(self.sliderGradientStart.GetValue())


        self.cp101103S.SetColour(self.c101103S)
        self.cp101103E.SetColour(self.c101103E)
        self.gauge101103S.SetColour(self.c101103S, self.c101103E)
        self.gauge101103M.SetColour(self.c101103S, self.c101103E)
        self.gauge101103E.SetColour(self.c101103S, self.c101103E)

        self.gauge101103S.SetPercentages(101, 102.99)
        self.gauge101103M.SetPercentages(101, 102.99)
        self.gauge101103E.SetPercentages(101, 102.99)

        self.gauge101103S.SetGradientStart(self.sliderGradientStart.GetValue())
        self.gauge101103M.SetGradientStart(self.sliderGradientStart.GetValue())
        self.gauge101103E.SetGradientStart(self.sliderGradientStart.GetValue())


        self.cp103105S.SetColour(self.c103105S)
        self.cp103105E.SetColour(self.c103105E)
        self.gauge103105S.SetColour(self.c103105S, self.c103105E)
        self.gauge103105M.SetColour(self.c103105S, self.c103105E)
        self.gauge103105E.SetColour(self.c103105S, self.c103105E)

        self.gauge103105S.SetPercentages(103, 104.99)
        self.gauge103105M.SetPercentages(103, 104.99)
        self.gauge103105E.SetPercentages(103, 104.99)

        self.gauge103105S.SetGradientStart(self.sliderGradientStart.GetValue())
        self.gauge103105M.SetGradientStart(self.sliderGradientStart.GetValue())
        self.gauge103105E.SetGradientStart(self.sliderGradientStart.GetValue())

        self.wndPreview0100.SetColour(self.c0100S, self.c0100E)
        self.wndPreview0100.SetPercentages(0, 99.99)
        self.wndPreview0100.SetGradientStart(self.sliderGradientStart.GetValue())

        self.wndPreview100101.SetColour(self.c100101S, self.c100101E)
        self.wndPreview100101.SetPercentages(100, 100.99)
        self.wndPreview100101.SetGradientStart(self.sliderGradientStart.GetValue())

        self.wndPreview101103.SetColour(self.c101103S, self.c101103E)
        self.wndPreview101103.SetPercentages(101, 102.99)
        self.wndPreview101103.SetGradientStart(self.sliderGradientStart.GetValue())

        self.wndPreview103105.SetColour(self.c103105S, self.c103105E)
        self.wndPreview103105.SetPercentages(103,104.99)
        self.wndPreview103105.SetGradientStart(self.sliderGradientStart.GetValue())

    def OnGradientStartScroll(self, event):
        self.gradientStart = self.sliderGradientStart.GetValue()
        self.SetColours()
        event.Skip()

    def OnOk(self, event):
        self.Close()
        event.Skip()

    def DumpColours(self, event):
        print "Gradient start: %d" % self.sliderGradientStart.GetValue()
        print "  0 <-> 100 Start: ", self.c0100S, " End: ", self.c0100E
        print "100 <-> 101 Start: ", self.c100101S, " End: ", self.c100101E
        print "101 <-> 103 Start: ", self.c101103S, " End: ", self.c101103E
        print "103 <-> 105 Start: ", self.c103105S, " End: ", self.c103105E

        event.Skip()

    def RestoreDefaults(self, event):
        self.InitDefaultColours()
        self.SetColours()

        event.Skip()

    def OnColourChanged(self, event):

        color = event.EventObject.GetColour()
        cpObj = event.EventObject

        if cpObj == self.cp0100S:
            self.c0100S = color

        if cpObj == self.cp0100E:
            self.c0100E = color
            if self.cbLink.IsChecked():
                self.c100101S = color

        if cpObj == self.cp100101S:
            self.c100101S = color
            if self.cbLink.IsChecked():
                self.c0100E = color

        if cpObj == self.cp100101E:
            self.c100101E = color
            if self.cbLink.IsChecked():
                self.c101103S = color

        if cpObj == self.cp101103S:
            self.c101103S = color
            if self.cbLink.IsChecked():
                self.c100101E = color

        if cpObj == self.cp101103E:
            self.c101103E = color
            if self.cbLink.IsChecked():
                self.c103105S = color

        if cpObj == self.cp103105S:
            self.c103105S = color
            if self.cbLink.IsChecked():
                self.c101103E = color

        if cpObj == self.cp103105E:
            self.c103105E = color

        self.SetColours()
        event.Skip()

    def __del__( self ):
        pass

if __name__ == '__main__':
    app = wx.PySimpleApp()
    dlg = PFGaugePref()
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()
