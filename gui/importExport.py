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
import service
import config
import gui.mainFrame
import os

class ImportDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__ (self, parent, id=wx.ID_ANY, title=u"Import fitting from ...", pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.DEFAULT_DIALOG_STYLE)
        self._toggleEdit = -1
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetMinSize((500,300))

        self._fitsFromFile = None
        self._fitsFromEdit = None

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        headerSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.cFilePicker = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a fit file", u"*.*", style=wx.FLP_DEFAULT_STYLE | wx.FLP_FILE_MUST_EXIST | wx.FLP_CHANGE_DIR)
        headerSizer.Add(self.cFilePicker, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.tbtnEdit = wx.ToggleButton( self, wx.ID_ANY, u"Text Edit", wx.DefaultPosition, wx.DefaultSize, 0 )
        headerSizer.Add( self.tbtnEdit, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5 )


        mainSizer.Add(headerSizer, 0, wx.EXPAND, 5)
        self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        self.m_staticline2.SetMinSize( wx.Size( 480,1 ) )
        mainSizer.Add( self.m_staticline2, 0, wx.EXPAND, 5 )
        contentSizer = wx.BoxSizer(wx.VERTICAL)

        self.tcEdit = wx.TextCtrl(self, wx.ID_ANY, u"", style=wx.TE_MULTILINE)
        self.tcEdit.SetMinSize( wx.Size( -1,250 ) )
        contentSizer.Add(self.tcEdit, 1, wx.EXPAND, 5)

        mainSizer.Add(contentSizer, 1, wx.EXPAND, 5)

        footerSizer = wx.BoxSizer(wx.HORIZONTAL)


        self.stStatus = wx.StaticText( self, wx.ID_ANY, u"Status: File mode.", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stStatus.Wrap( -1 )
        footerSizer.Add( self.stStatus, 1, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

        self.btnImport = wx.Button( self, wx.ID_ANY, u"Import", wx.DefaultPosition, wx.DefaultSize, 0 )
        footerSizer.Add( self.btnImport, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )

        self.btnOK = wx.Button(self, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        footerSizer.Add(self.btnOK, 0, wx.TOP|wx.BOTTOM|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)

        mainSizer.Add(footerSizer, 0, wx.EXPAND, 5)

        self.SetSizer(mainSizer)

        self.tbtnEdit.SetValue( True )
        self.tcEdit.Show(False)

        self.Layout()
        self.Fit()

        self.Bind( wx.EVT_CLOSE, self.CloseDlg )
        self.btnOK.Bind( wx.EVT_BUTTON, self.CloseDlg )
        self.cFilePicker.Bind( wx.EVT_FILEPICKER_CHANGED, self.prepareFileFits )
        self.tbtnEdit.Bind( wx.EVT_TOGGLEBUTTON, self.SwitchEditCtrl )
        self.btnImport.Bind( wx.EVT_BUTTON, self.ImportFittings )
        self.Centre(wx.BOTH)


    def ImportFittings( self, event ):
        sFit = service.Fit.getInstance()
        if self._toggleEdit == -1:
            if self._fitsFromFile:
                try:
                    sFit.saveImportedFits(self._fitsFromFile)
                    self.stStatus.SetLabel("Status: %d fit(s) imported" % len(self._fitsFromFile))
                except:
                    self.stStatus.SetLabel("Status: Error importing from file!")
                self._fitsFromFile = None
            else:
                self.stStatus.SetLabel("Status: No fits were specified. Use Browse button.")
        else:
            buffer = self.tcEdit.GetValue()
            if len(buffer) != 0:
                try:
                    self._fitsFromEdit = sFit.importFitFromBuffer(buffer)
                    sFit.saveImportedFits(self._fitsFromEdit)
                    self.stStatus.SetLabel("Status: %d fit(s) imported" % len(self._fitsFromEdit))
                except:
                    self.stStatus.SetLabel("Status: Error importing from text editor!")
            else:
                self.stStatus.SetLabel("Status: Nothing specified.")
        event.Skip()


    def prepareFileFits(self, event):
        sFit = service.Fit.getInstance()
        try:
            self._fitsFromFile = sFit.importFit(event.Path)
            self.stStatus.SetLabel("Status: Found %d fit(s)." % len(self._fitsFromFile))
        except:
            self.stStatus.SetLabel("Status: Invalid fitting file!")

    def ImportFromFile( self, event ):
        print event.Path
        event.Skip()

    def CloseDlg( self, event ):
        event.Skip()

    def SwitchEditCtrl( self, event ):
        self._toggleEdit *= -1
        if self._toggleEdit == -1:
            self.tcEdit.Show(False)
            self.cFilePicker.Enable( True )
            self.stStatus.SetLabel("Status: File mode.")
        else:
            self.tcEdit.Show(True)
            self.cFilePicker.Enable( False )
            self.stStatus.SetLabel("Status: Text edit mode.")
        self.Layout()
        self.Fit()
        event.Skip()

class ExportDialog ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Export fit as ...", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.srvFit = service.fit.Fit.getInstance()

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        fileSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.cFileSavePicker = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_CHANGE_DIR|wx.FLP_OVERWRITE_PROMPT|wx.FLP_SAVE|wx.FLP_USE_TEXTCTRL )
        fileSizer.Add( self.cFileSavePicker, 1, wx.ALL, 5 )

        mainSizer.Add( fileSizer, 0, wx.EXPAND, 5 )

        self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        self.m_staticline2.SetMinSize( wx.Size( 400,-1 ) )

        mainSizer.Add( self.m_staticline2, 0, wx.EXPAND, 5 )

        choiceSizer = wx.BoxSizer( wx.VERTICAL )

        chCtrlChoices = [ u"EFT file", u"XML file", u"EFT && XML file" ]
        self.chCtrl = wx.RadioBox( self, wx.ID_ANY, u"Export type", wx.DefaultPosition, wx.DefaultSize, chCtrlChoices, 3, wx.RA_SPECIFY_COLS )
        self.chCtrl.SetSelection( 0 )
        choiceSizer.Add( self.chCtrl, 0, wx.EXPAND|wx.ALL, 5 )

        mainSizer.Add( choiceSizer, 1, wx.EXPAND, 5 )

        footerSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.stStatus = wx.StaticText( self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stStatus.Wrap( -1 )
        footerSizer.Add( self.stStatus, 1, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

        self.bntExport = wx.Button( self, wx.ID_ANY, u"Export", wx.DefaultPosition, wx.DefaultSize, 0 )
        footerSizer.Add( self.bntExport, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM, 5 )

        self.btnOK = wx.Button( self, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        footerSizer.Add( self.btnOK, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5 )

        mainSizer.Add( footerSizer, 0, wx.EXPAND, 5 )

        self.SetSizer( mainSizer )
        self.Layout()

        fitID = self.mainFrame.getActiveFit()
        self.fit = self.srvFit.getFit(fitID)
        if self.fit is None:
            self.stStatus.SetLabel("Error: please select a fit before trying to export!")
            self.cFileSavePicker.Enable( False )
            self.chCtrl.Enable( False )
            self.bntExport.Enable( False )
        else:
            self.stStatus.SetLabel("Selected fit: %s" % self.fit.name)
            self.filePath = os.path.join(config.staticPath,self.fit.name)
            self.cFileSavePicker.SetPath(self.filePath)
        mainSizer.Fit( self )

        self.Centre( wx.BOTH )

        # Connect Events
        self.cFileSavePicker.Bind( wx.EVT_FILEPICKER_CHANGED, self.OnFileChoose )
        self.btnOK.Bind( wx.EVT_BUTTON, self.Close )


    # Virtual event handlers, overide them in your derived class
    def OnFileChoose( self, event ):
        self.filePath = event.Path
        event.Skip()

    def Close( self, event ):
        extensions = ["xml", "txt"]
        selection  = self.chCtrl.GetSelection()
        if selection <2:
            filename = "%s%s" %(self.filePath,extensions[selection])
        event.Skip()


