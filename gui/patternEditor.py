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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import wx

###########################################################################
## Class DmgPatternEditorDlg
###########################################################################

class DmgPatternEditorDlg ( wx.Dialog ):

  def __init__( self, parent ):
    wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Damage profile editor", pos = wx.DefaultPosition, size = wx.Size( 339,191 ), style = wx.DEFAULT_DIALOG_STYLE )

    self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

    mainSizer = wx.BoxSizer( wx.VERTICAL )

    headerSizer = wx.BoxSizer( wx.HORIZONTAL )

    ccDmgPatternChoices = [ u"uniform", u"sansha", u"gurista", u"blood raiders", u"drones", u"angels" ]
    self.ccDmgPattern = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ccDmgPatternChoices, 0 )
    self.ccDmgPattern.SetSelection( 0 )
    headerSizer.Add( self.ccDmgPattern, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

    self.btnNew = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
    headerSizer.Add( self.btnNew, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

    self.btnCopy = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
    headerSizer.Add( self.btnCopy, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

    self.btnRename = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
    headerSizer.Add( self.btnRename, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

    self.btnDelete = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
    headerSizer.Add( self.btnDelete, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

    mainSizer.Add( headerSizer, 0, wx.EXPAND, 5 )

    contentSizer = wx.BoxSizer( wx.VERTICAL )

    dmgeditSizer = wx.FlexGridSizer( 4, 3, 0, 2 )
    dmgeditSizer.AddGrowableCol( 2 )
    dmgeditSizer.SetFlexibleDirection( wx.BOTH )
    dmgeditSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

    self.bmpEM = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
    dmgeditSizer.Add( self.bmpEM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

    self.editEM = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
    dmgeditSizer.Add( self.editEM, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

    self.stEM = wx.StaticText( self, wx.ID_ANY, u"0%", wx.DefaultPosition, wx.DefaultSize, 0 )
    self.stEM.Wrap( -1 )
    dmgeditSizer.Add( self.stEM, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

    self.bmpTERM = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
    dmgeditSizer.Add( self.bmpTERM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

    self.editTERM = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
    dmgeditSizer.Add( self.editTERM, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

    self.stTERM = wx.StaticText( self, wx.ID_ANY, u"0%", wx.DefaultPosition, wx.DefaultSize, 0 )
    self.stTERM.Wrap( -1 )
    dmgeditSizer.Add( self.stTERM, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

    self.bmpKIN = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
    dmgeditSizer.Add( self.bmpKIN, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

    self.editKIN = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
    dmgeditSizer.Add( self.editKIN, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

    self.stKIN = wx.StaticText( self, wx.ID_ANY, u"0%", wx.DefaultPosition, wx.DefaultSize, 0 )
    self.stKIN.Wrap( -1 )
    dmgeditSizer.Add( self.stKIN, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

    self.bmpEXP = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
    dmgeditSizer.Add( self.bmpEXP, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

    self.editEXP = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
    dmgeditSizer.Add( self.editEXP, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

    self.stEXP = wx.StaticText( self, wx.ID_ANY, u"0%", wx.DefaultPosition, wx.DefaultSize, 0 )
    self.stEXP.Wrap( -1 )
    dmgeditSizer.Add( self.stEXP, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

    contentSizer.Add( dmgeditSizer, 1, wx.EXPAND, 0 )

    mainSizer.Add( contentSizer, 1, wx.EXPAND, 0 )

    self.SetSizer( mainSizer )
    self.Layout()

    self.Centre( wx.BOTH )

  def __del__( self ):
    pass


