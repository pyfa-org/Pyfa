#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.    If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import wx
import bitmapLoader
from wx.lib.intctrl import IntCtrl
###########################################################################
## Class DmgPatternEditorDlg
###########################################################################

class DmgPatternEditorDlg ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Damage Pattern Editor", pos = wx.DefaultPosition, size = wx.Size( 300,240 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        headerSizer = wx.BoxSizer( wx.HORIZONTAL )

        ccDmgPatternChoices = [ u"uniform", u"sansha", u"gurista", u"blood raiders", u"drones", u"angels", "cnc" ]
        self.ccDmgPattern = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ccDmgPatternChoices, 0 )
        self.ccDmgPattern.SetSelection( 0 )
        size = None
        headerSizer.Add( self.ccDmgPattern, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT|wx.LEFT, 3 )
        for name, art in (("new", wx.ART_NEW), ("rename", bitmapLoader.getBitmap("rename", "icons")), ("copy", wx.ART_COPY), ("delete", wx.ART_DELETE)):
                bitmap = wx.ArtProvider.GetBitmap(art, wx.ART_BUTTON) if name != "rename" else art
                btn = wx.BitmapButton(self, wx.ID_ANY, bitmap)
                if size is None:
                        size = btn.GetSize()

                btn.SetMinSize(size)
                btn.SetMaxSize(size)

                btn.Layout()
                setattr(self, name, btn)
                btn.Enable(True)
                btn.SetToolTipString("%s fit" % name.capitalize())
                headerSizer.Add(btn, 0, wx.ALIGN_CENTER_VERTICAL)


        mainSizer.Add( headerSizer, 0, wx.EXPAND | wx.ALL, 2 )

        self.sl = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        mainSizer.Add( self.sl, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )

        contentSizer = wx.BoxSizer( wx.VERTICAL )
        self.embitmap = bitmapLoader.getBitmap("em_big", "icons")
        self.thermbitmap = bitmapLoader.getBitmap("thermal_big", "icons")
        self.kinbitmap = bitmapLoader.getBitmap("kinetic_big", "icons")
        self.expbitmap = bitmapLoader.getBitmap("explosive_big", "icons")

        dmgeditSizer = wx.FlexGridSizer( 2, 4, 0, 2 )
        dmgeditSizer.AddGrowableCol( 1 )
        dmgeditSizer.AddGrowableCol( 2 )
        dmgeditSizer.SetFlexibleDirection( wx.BOTH )
        dmgeditSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        #width,height = self.GetTextExtent("9999999999")
        width = -1
        defSize = wx.Size(width,-1)


        self.editEM = IntCtrl( self, wx.ID_ANY, 0, wx.DefaultPosition, defSize, wx.TE_RIGHT )
        dmgeditSizer.Add( self.editEM, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

#        self.stEM = wx.StaticText( self, wx.ID_ANY, u"0%", wx.DefaultPosition, wx.DefaultSize, 0 )
#        self.stEM.Wrap( -1 )
#        dmgeditSizer.Add( self.stEM, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.bmpEM = wx.StaticBitmap( self, wx.ID_ANY, self.embitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        dmgeditSizer.Add( self.bmpEM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.bmpTHERM = wx.StaticBitmap( self, wx.ID_ANY, self.thermbitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        dmgeditSizer.Add( self.bmpTHERM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5 )

        self.editTHERM = IntCtrl( self, wx.ID_ANY, 0, wx.DefaultPosition, defSize, 0,  )
        dmgeditSizer.Add( self.editTHERM, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

#        self.stTHERM = wx.StaticText( self, wx.ID_ANY, u"0%", wx.DefaultPosition, wx.DefaultSize, 0 )
#        self.stTHERM.Wrap( -1 )
#        dmgeditSizer.Add( self.stTHERM, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        self.editKIN = IntCtrl( self, wx.ID_ANY, 0, wx.DefaultPosition, defSize, wx.TE_RIGHT )
        dmgeditSizer.Add( self.editKIN, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

#        self.stKIN = wx.StaticText( self, wx.ID_ANY, u"0%", wx.DefaultPosition, wx.DefaultSize, 0 )
#        self.stKIN.Wrap( -1 )
#        dmgeditSizer.Add( self.stKIN, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.bmpKIN = wx.StaticBitmap( self, wx.ID_ANY, self.kinbitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        dmgeditSizer.Add( self.bmpKIN, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.bmpEXP = wx.StaticBitmap( self, wx.ID_ANY, self.expbitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        dmgeditSizer.Add( self.bmpEXP, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5 )

        self.editEXP = IntCtrl( self, wx.ID_ANY, 0, wx.DefaultPosition, defSize, 0 )
        dmgeditSizer.Add( self.editEXP, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

#        self.stEXP = wx.StaticText( self, wx.ID_ANY, u"0%", wx.DefaultPosition, wx.DefaultSize, 0 )
#        self.stEXP.Wrap( -1 )
#        dmgeditSizer.Add( self.stEXP, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        contentSizer.Add( dmgeditSizer, 1, wx.EXPAND|wx.ALL, 5 )
        self.slfooter = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        contentSizer.Add( self.slfooter, 0, wx.EXPAND|wx.TOP, 5 )

        footerSizer = wx.BoxSizer( wx.HORIZONTAL )

        perSizer = wx.BoxSizer( wx.VERTICAL )

        self.stPercentages = wx.StaticText( self, wx.ID_ANY, u"EM: 0% THERM: 0% KIN: 0% EXP: 0%", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stPercentages.Wrap( -1 )
        perSizer.Add( self.stPercentages, 0, wx.BOTTOM|wx.LEFT, 5 )

        footerSizer.Add( perSizer, 0, 0, 5 )

        totSizer = wx.BoxSizer( wx.VERTICAL )

        self.stTotal = wx.StaticText( self, wx.ID_ANY, u"Total: 0 hp", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stTotal.Wrap( -1 )
        totSizer.Add( self.stTotal, 0, wx.ALIGN_RIGHT|wx.BOTTOM|wx.RIGHT, 5 )

        footerSizer.Add( totSizer, 1, 0, 5 )

        contentSizer.Add( footerSizer, 0, wx.EXPAND, 5 )

        mainSizer.Add( contentSizer, 1, wx.EXPAND, 0 )

        self.SetSizer( mainSizer )


        self.Layout()
        bsize = self.GetBestSize()
        self.SetSize((-1,bsize.height))
        self.Show()

        self.new.Bind(wx.EVT_BUTTON, self.newPattern)
        self.rename.Bind(wx.EVT_BUTTON, self.renamePattern)
        self.delete.Bind(wx.EVT_BUTTON, self.deletePattern)
        self.copy.Bind(wx.EVT_BUTTON, self.copyPattern)


    def newPattern(self,event):
        event.Skip()

    def renamePattern(self,event):
        event.Skip()

    def copyPattern(self,event):
        event.Skip()

    def deletePattern(self,event):
        event.Skip()


    def __del__( self ):
                pass
