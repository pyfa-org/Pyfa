import json
import thread

import wx
from wx.lib.pubsub import pub

import service
import gui.display as d
from eos.types import Cargo
from eos.db import getItem
from service.server import *
import config
import time

class CrestFittings(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.Size( 550,450 ), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        self.mainFrame = parent
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sCrest = service.Crest.getInstance()

        self.charChoice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [])
        chars = sCrest.getCrestCharacters()
        for char in chars:
            self.charChoice.Append(char.name, char.ID)

        characterSelectSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.charChoice.SetSelection(0)


        characterSelectSizer.Add( self.charChoice, 1, wx.ALL, 5 )
        self.fetchBtn = wx.Button( self, wx.ID_ANY, u"Fetch Fits", wx.DefaultPosition, wx.DefaultSize, 5 )
        characterSelectSizer.Add( self.fetchBtn, 0, wx.ALL, 5 )
        mainSizer.Add( characterSelectSizer, 0, wx.EXPAND, 5 )

        self.sl = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        mainSizer.Add( self.sl, 0, wx.EXPAND |wx.ALL, 5 )

        contentSizer = wx.BoxSizer( wx.HORIZONTAL )
        browserSizer = wx.BoxSizer( wx.VERTICAL )

        self.fitTree = FittingsTreeView(self)
        browserSizer.Add( self.fitTree, 1, wx.ALL|wx.EXPAND, 5 )
        contentSizer.Add( browserSizer, 1, wx.EXPAND, 0 )
        fitSizer = wx.BoxSizer( wx.VERTICAL )

        self.fitView = FitView(self)
        self.importBtn = wx.Button( self, wx.ID_ANY, u"Import", wx.DefaultPosition, wx.DefaultSize, 5 )
        fitSizer.Add( self.fitView, 1, wx.ALL|wx.EXPAND, 5 )
        fitSizer.Add( self.importBtn, 0, wx.ALL|wx.EXPAND, 5 )

        contentSizer.Add(fitSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(contentSizer, 1, wx.EXPAND, 5)

        self.fetchBtn.Bind(wx.EVT_BUTTON, self.fetchFittings)
        self.importBtn.Bind(wx.EVT_BUTTON, self.importFitting)

        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

    def getActiveCharacter(self):
        selection = self.charChoice.GetCurrentSelection()
        return self.charChoice.GetClientData(selection) if selection is not None else None

    def fetchFittings(self, event):
        sCrest = service.Crest.getInstance()
        fittings = sCrest.getFittings(self.getActiveCharacter())
        self.fitTree.populateSkillTree(fittings)

    def importFitting(self, event):
        selection = self.fitView.fitSelection
        data = self.fitTree.fittingsTreeCtrl.GetPyData(selection)
        sFit = service.Fit.getInstance()
        fits = sFit.importFitFromBuffer(data)
        self.mainFrame._openAfterImport(fits)


class ExportToEve(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=(wx.Size(500,100)), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.mainFrame = parent
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        sCrest = service.Crest.getInstance()

        self.charChoice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [])
        chars = sCrest.getCrestCharacters()
        for char in chars:
            self.charChoice.Append(char.name, char.ID)

        mainSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.charChoice.SetSelection(0)

        mainSizer.Add( self.charChoice, 1, wx.ALL, 5 )
        self.exportBtn = wx.Button( self, wx.ID_ANY, u"Export Fit", wx.DefaultPosition, wx.DefaultSize, 5 )
        mainSizer.Add( self.exportBtn, 0, wx.ALL, 5 )

        self.exportBtn.Bind(wx.EVT_BUTTON, self.exportFitting)

        self.statusbar = wx.StatusBar(self)
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([100, -1])


        self.SetSizer(mainSizer)
        self.SetStatusBar(self.statusbar)
        self.Layout()

        self.Centre(wx.BOTH)

    def getActiveCharacter(self):
        selection = self.charChoice.GetCurrentSelection()
        return self.charChoice.GetClientData(selection) if selection is not None else None

    def exportFitting(self, event):
        self.statusbar.SetStatusText("", 0)
        self.statusbar.SetStatusText("Sending request and awaiting response", 1)
        sCrest = service.Crest.getInstance()

        sFit = service.Fit.getInstance()
        data = sFit.exportCrest(self.mainFrame.getActiveFit())
        res = sCrest.postFitting(self.getActiveCharacter(), data)

        self.statusbar.SetStatusText("%d: %s"%(res.status_code, res.reason), 0)
        try:
            text = json.loads(res.text)
            self.statusbar.SetStatusText(text['message'], 1)
        except ValueError:
            self.statusbar.SetStatusText("", 1)

class CrestCharacterInfo(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Character Info", pos=wx.DefaultPosition, size = wx.Size( 200,240 ))
        self.mainFrame = parent
        sCrest = service.Crest.getInstance()
        self.char = sCrest.implicitCharacter
        self.bitmapSet = False

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.headingText = wx.StaticText(self, wx.ID_ANY, "Currently logged in", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
        self.headingText.Wrap( -1 )
        self.headingText.SetFont( wx.Font( 12, 74, 90, 92, False) )
        mainSizer.Add( self.headingText, 0, wx.EXPAND|wx.ALL, 5 )

        self.pic = wx.StaticBitmap(self, -1, wx.EmptyBitmap(128, 128))
        mainSizer.Add(self.pic, 0, wx.EXPAND, 5 )

        self.characterText = wx.StaticText(self, wx.ID_ANY, self.char.name, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
        self.characterText.Wrap( -1 )
        self.characterText.SetFont( wx.Font( 11, 74, 90, 92, False) )
        mainSizer.Add( self.characterText, 0, wx.EXPAND|wx.ALL, 5 )

        self.coutdownText = wx.StaticText( self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE)
        self.coutdownText.Wrap( -1 )
        mainSizer.Add( self.coutdownText, 0, wx.EXPAND, 5 )

        self.SetSizer( mainSizer )
        self.Centre( wx.BOTH )

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(1)

    def update(self, event):
        t = time.gmtime(self.char.eve.expires-time.time())
        if not self.bitmapSet and hasattr(self.char, 'img'):
            self.pic.SetBitmap(wx.ImageFromStream(self.char.img).ConvertToBitmap())
            self.Layout()
            self.bitmapSet = True
        self.coutdownText.SetLabel(time.strftime("%H:%M:%S", t))


class FittingsTreeView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)
        self.parent = parent
        pmainSizer = wx.BoxSizer(wx.VERTICAL)

        tree = self.fittingsTreeCtrl = wx.TreeCtrl(self, wx.ID_ANY, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        pmainSizer.Add(tree, 1, wx.EXPAND | wx.ALL, 0)

        self.root = tree.AddRoot("Fits")
        self.populateSkillTree(None)

        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.displayFit)

        self.SetSizer(pmainSizer)

        self.Layout()

    def populateSkillTree(self, data):
        if data is None:
            return
        root = self.root
        tree = self.fittingsTreeCtrl
        tree.DeleteChildren(root)

        dict = {}
        fits = data['items']
        for fit in fits:
            if fit['ship']['name'] not in dict:
                dict[fit['ship']['name']] = []
            dict[fit['ship']['name']].append(fit)

        for name, fits in dict.iteritems():
            shipID = tree.AppendItem(root, name)
            for fit in fits:
                fitId = tree.AppendItem(shipID, fit['name'])
                print type(fit)
                tree.SetPyData(fitId, json.dumps(fit))

        tree.SortChildren(root)

    def displayFit(self, event):
        selection = self.fittingsTreeCtrl.GetSelection()
        fit = json.loads(self.fittingsTreeCtrl.GetPyData(selection))
        list = []

        for item in fit['items']:
            try:
                cargo = Cargo(getItem(item['type']['id']))
                cargo.amount = item['quantity']
                list.append(cargo)
            except:
                pass
        self.parent.fitView.fitSelection = selection
        self.parent.fitView.update(list)

class FitView(d.Display):
    DEFAULT_COLS = ["Base Icon",
                    "Base Name"]

    def __init__(self, parent):
        d.Display.__init__(self, parent, style=wx.LC_SINGLE_SEL)
        self.fitSelection = None
        #self.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)
        #self.Bind(wx.EVT_KEY_UP, self.kbEvent)
