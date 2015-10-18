import wx
import service
import gui.display as d
from eos.types import Cargo
from eos.db import getItem

class CrestFittings(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.Size( 550,450 ), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

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

    def populateSkillTree(self, json):
        if json is None:
            return
        root = self.root
        tree = self.fittingsTreeCtrl
        tree.DeleteChildren(root)

        dict = {}
        fits = json['items']
        for fit in fits:
            if fit['ship']['name'] not in dict:
                dict[fit['ship']['name']] = []
            dict[fit['ship']['name']].append(fit)

        for name, fits in dict.iteritems():
            shipID = tree.AppendItem(root, name)
            for fit in fits:
                fitId = tree.AppendItem(shipID, fit['name'])
                tree.SetPyData(fitId, fit['items'])

        tree.SortChildren(root)

    def displayFit(self, event):
        selection = self.fittingsTreeCtrl.GetSelection()
        items = self.fittingsTreeCtrl.GetPyData(selection)
        list = []

        for item in items:
            cargo = Cargo(getItem(item['type']['id']))
            cargo.amount = item['quantity']
            list.append(cargo)
        self.parent.fitView.populate(list)
        self.parent.fitView.refresh(list)

class FitView(d.Display):
    DEFAULT_COLS = ["Base Icon",
                    "Base Name"]

    def __init__(self, parent):
        d.Display.__init__(self, parent, style=wx.LC_SINGLE_SEL)

        #self.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)
        #self.Bind(wx.EVT_KEY_UP, self.kbEvent)
