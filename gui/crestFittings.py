import time
import webbrowser
import json
# noinspection PyPackageRequirements
import wx
import requests

from service.port import Port
from service.fit import Fit

from eos.saveddata.cargo import Cargo
from eos.db import getItem

from gui.display import Display
import gui.globalEvents as GE

from logbook import Logger
pyfalog = Logger(__name__)

if 'wxMac' not in wx.PlatformInfo or ('wxMac' in wx.PlatformInfo and wx.VERSION >= (3, 0)):
    from service.crest import Crest, CrestModes


class CrestFittings(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Browse EVE Fittings", pos=wx.DefaultPosition,
                          size=wx.Size(550, 450), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        self.mainFrame = parent
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sCrest = Crest.getInstance()

        characterSelectSizer = wx.BoxSizer(wx.HORIZONTAL)

        if sCrest.settings.get('mode') == CrestModes.IMPLICIT:
            self.stLogged = wx.StaticText(self, wx.ID_ANY, "Currently logged in as %s" % sCrest.implicitCharacter.name,
                                          wx.DefaultPosition, wx.DefaultSize)
            self.stLogged.Wrap(-1)

            characterSelectSizer.Add(self.stLogged, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        else:
            self.charChoice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [])
            characterSelectSizer.Add(self.charChoice, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.updateCharList()

        self.fetchBtn = wx.Button(self, wx.ID_ANY, u"Fetch Fits", wx.DefaultPosition, wx.DefaultSize, 5)
        characterSelectSizer.Add(self.fetchBtn, 0, wx.ALL, 5)
        mainSizer.Add(characterSelectSizer, 0, wx.EXPAND, 5)

        self.sl = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.sl, 0, wx.EXPAND | wx.ALL, 5)

        contentSizer = wx.BoxSizer(wx.HORIZONTAL)
        browserSizer = wx.BoxSizer(wx.VERTICAL)

        self.fitTree = FittingsTreeView(self)
        browserSizer.Add(self.fitTree, 1, wx.ALL | wx.EXPAND, 5)
        contentSizer.Add(browserSizer, 1, wx.EXPAND, 0)
        fitSizer = wx.BoxSizer(wx.VERTICAL)

        self.fitView = FitView(self)
        fitSizer.Add(self.fitView, 1, wx.ALL | wx.EXPAND, 5)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.importBtn = wx.Button(self, wx.ID_ANY, u"Import to pyfa", wx.DefaultPosition, wx.DefaultSize, 5)
        self.deleteBtn = wx.Button(self, wx.ID_ANY, u"Delete from EVE", wx.DefaultPosition, wx.DefaultSize, 5)
        btnSizer.Add(self.importBtn, 1, wx.ALL, 5)
        btnSizer.Add(self.deleteBtn, 1, wx.ALL, 5)
        fitSizer.Add(btnSizer, 0, wx.EXPAND)

        contentSizer.Add(fitSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(contentSizer, 1, wx.EXPAND, 5)

        self.fetchBtn.Bind(wx.EVT_BUTTON, self.fetchFittings)
        self.importBtn.Bind(wx.EVT_BUTTON, self.importFitting)
        self.deleteBtn.Bind(wx.EVT_BUTTON, self.deleteFitting)

        self.mainFrame.Bind(GE.EVT_SSO_LOGOUT, self.ssoLogout)
        self.mainFrame.Bind(GE.EVT_SSO_LOGIN, self.ssoLogin)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.statusbar = wx.StatusBar(self)
        self.statusbar.SetFieldsCount()
        self.SetStatusBar(self.statusbar)

        self.cacheTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updateCacheStatus, self.cacheTimer)

        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

    def ssoLogin(self, event):
        self.updateCharList()
        event.Skip()

    def updateCharList(self):
        sCrest = Crest.getInstance()
        chars = sCrest.getCrestCharacters()

        if len(chars) == 0:
            self.Close()

        self.charChoice.Clear()
        for char in chars:
            self.charChoice.Append(char.name, char.ID)

        self.charChoice.SetSelection(0)

    def updateCacheStatus(self, event):
        t = time.gmtime(self.cacheTime - time.time())
        if t < 0:
            self.cacheTimer.Stop()
        else:
            sTime = time.strftime("%H:%M:%S", t)
            self.statusbar.SetStatusText("Cached for %s" % sTime, 0)

    def ssoLogout(self, event):
        if event.type == CrestModes.IMPLICIT:
            self.Close()
        else:
            self.updateCharList()
        event.Skip()  # continue event

    def OnClose(self, event):
        self.mainFrame.Unbind(GE.EVT_SSO_LOGOUT, handler=self.ssoLogout)
        self.mainFrame.Unbind(GE.EVT_SSO_LOGIN, handler=self.ssoLogin)
        event.Skip()

    def getActiveCharacter(self):
        sCrest = Crest.getInstance()

        if sCrest.settings.get('mode') == CrestModes.IMPLICIT:
            return sCrest.implicitCharacter.ID

        selection = self.charChoice.GetCurrentSelection()
        return self.charChoice.GetClientData(selection) if selection is not None else None

    def fetchFittings(self, event):
        sCrest = Crest.getInstance()
        try:
            waitDialog = wx.BusyInfo("Fetching fits, please wait...", parent=self)
            fittings = sCrest.getFittings(self.getActiveCharacter())
            self.cacheTime = fittings.get('cached_until')
            self.updateCacheStatus(None)
            self.cacheTimer.Start(1000)
            self.fitTree.populateSkillTree(fittings)
            del waitDialog
        except requests.exceptions.ConnectionError:
            msg = "Connection error, please check your internet connection"
            pyfalog.error(msg)
            self.statusbar.SetStatusText(msg)

    def importFitting(self, event):
        selection = self.fitView.fitSelection
        if not selection:
            return
        data = self.fitTree.fittingsTreeCtrl.GetPyData(selection)
        sPort = Port.getInstance()
        fits = sPort.importFitFromBuffer(data)
        self.mainFrame._openAfterImport(fits)

    def deleteFitting(self, event):
        sCrest = Crest.getInstance()
        selection = self.fitView.fitSelection
        if not selection:
            return
        data = json.loads(self.fitTree.fittingsTreeCtrl.GetPyData(selection))

        dlg = wx.MessageDialog(self,
                               "Do you really want to delete %s (%s) from EVE?" % (data['name'], data['ship']['name']),
                               "Confirm Delete", wx.YES | wx.NO | wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
            try:
                sCrest.delFitting(self.getActiveCharacter(), data['fittingID'])
            except requests.exceptions.ConnectionError:
                msg = "Connection error, please check your internet connection"
                pyfalog.error(msg)
                self.statusbar.SetStatusText(msg)


class ExportToEve(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Export fit to EVE", pos=wx.DefaultPosition,
                          size=(wx.Size(350, 100)), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.mainFrame = parent
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        sCrest = Crest.getInstance()
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        if sCrest.settings.get('mode') == CrestModes.IMPLICIT:
            self.stLogged = wx.StaticText(self, wx.ID_ANY, "Currently logged in as %s" % sCrest.implicitCharacter.name,
                                          wx.DefaultPosition, wx.DefaultSize)
            self.stLogged.Wrap(-1)

            hSizer.Add(self.stLogged, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        else:
            self.charChoice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [])
            hSizer.Add(self.charChoice, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.updateCharList()
            self.charChoice.SetSelection(0)

        self.exportBtn = wx.Button(self, wx.ID_ANY, u"Export Fit", wx.DefaultPosition, wx.DefaultSize, 5)
        hSizer.Add(self.exportBtn, 0, wx.ALL, 5)

        mainSizer.Add(hSizer, 0, wx.EXPAND, 5)

        self.exportBtn.Bind(wx.EVT_BUTTON, self.exportFitting)

        self.statusbar = wx.StatusBar(self)
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([100, -1])

        self.mainFrame.Bind(GE.EVT_SSO_LOGOUT, self.ssoLogout)
        self.mainFrame.Bind(GE.EVT_SSO_LOGIN, self.ssoLogin)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.SetSizer(hSizer)
        self.SetStatusBar(self.statusbar)
        self.Layout()

        self.Centre(wx.BOTH)

    def updateCharList(self):
        sCrest = Crest.getInstance()
        chars = sCrest.getCrestCharacters()

        if len(chars) == 0:
            self.Close()

        self.charChoice.Clear()
        for char in chars:
            self.charChoice.Append(char.name, char.ID)

        self.charChoice.SetSelection(0)

    def ssoLogin(self, event):
        self.updateCharList()
        event.Skip()

    def ssoLogout(self, event):
        if event.type == CrestModes.IMPLICIT:
            self.Close()
        else:
            self.updateCharList()
        event.Skip()  # continue event

    def OnClose(self, event):
        self.mainFrame.Unbind(GE.EVT_SSO_LOGOUT, handler=self.ssoLogout)
        self.mainFrame.Unbind(GE.EVT_SSO_LOGIN, handler=self.ssoLogin)

        event.Skip()

    def getActiveCharacter(self):
        sCrest = Crest.getInstance()

        if sCrest.settings.get('mode') == CrestModes.IMPLICIT:
            return sCrest.implicitCharacter.ID

        selection = self.charChoice.GetCurrentSelection()
        return self.charChoice.GetClientData(selection) if selection is not None else None

    def exportFitting(self, event):
        sPort = Port.getInstance()
        fitID = self.mainFrame.getActiveFit()

        self.statusbar.SetStatusText("", 0)

        if fitID is None:
            self.statusbar.SetStatusText("Please select an active fitting in the main window", 1)
            return

        self.statusbar.SetStatusText("Sending request and awaiting response", 1)
        sCrest = Crest.getInstance()

        try:
            sFit = Fit.getInstance()
            data = sPort.exportCrest(sFit.getFit(fitID))
            res = sCrest.postFitting(self.getActiveCharacter(), data)

            self.statusbar.SetStatusText("%d: %s" % (res.status_code, res.reason), 0)
            try:
                text = json.loads(res.text)
                self.statusbar.SetStatusText(text['message'], 1)
            except ValueError:
                pyfalog.warning("Value error on loading JSON.")
                self.statusbar.SetStatusText("", 1)
        except requests.exceptions.ConnectionError:
            msg = "Connection error, please check your internet connection"
            pyfalog.error(msg)
            self.statusbar.SetStatusText(msg)


class CrestMgmt(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="CREST Character Management", pos=wx.DefaultPosition,
                           size=wx.Size(550, 250), style=wx.DEFAULT_DIALOG_STYLE)
        self.mainFrame = parent
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.lcCharacters = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)

        self.lcCharacters.InsertColumn(0, heading='Character')
        self.lcCharacters.InsertColumn(1, heading='Refresh Token')

        self.popCharList()

        mainSizer.Add(self.lcCharacters, 1, wx.ALL | wx.EXPAND, 5)

        btnSizer = wx.BoxSizer(wx.VERTICAL)

        self.addBtn = wx.Button(self, wx.ID_ANY, u"Add Character", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer.Add(self.addBtn, 0, wx.ALL | wx.EXPAND, 5)

        self.deleteBtn = wx.Button(self, wx.ID_ANY, u"Revoke Character", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer.Add(self.deleteBtn, 0, wx.ALL | wx.EXPAND, 5)

        mainSizer.Add(btnSizer, 0, wx.EXPAND, 5)

        self.addBtn.Bind(wx.EVT_BUTTON, self.addChar)
        self.deleteBtn.Bind(wx.EVT_BUTTON, self.delChar)

        self.mainFrame.Bind(GE.EVT_SSO_LOGIN, self.ssoLogin)

        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

    def ssoLogin(self, event):
        self.popCharList()
        event.Skip()

    def popCharList(self):
        sCrest = Crest.getInstance()
        chars = sCrest.getCrestCharacters()

        self.lcCharacters.DeleteAllItems()

        for index, char in enumerate(chars):
            self.lcCharacters.InsertStringItem(index, char.name)
            self.lcCharacters.SetStringItem(index, 1, char.refresh_token)
            self.lcCharacters.SetItemData(index, char.ID)

        self.lcCharacters.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.lcCharacters.SetColumnWidth(1, wx.LIST_AUTOSIZE)

    @staticmethod
    def addChar(event):
        sCrest = Crest.getInstance()
        uri = sCrest.startServer()
        webbrowser.open(uri)

    def delChar(self, event):
        item = self.lcCharacters.GetFirstSelected()
        if item > -1:
            charID = self.lcCharacters.GetItemData(item)
            sCrest = Crest.getInstance()
            sCrest.delCrestCharacter(charID)
            self.popCharList()


class FittingsTreeView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY)
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
                tree.SetPyData(fitId, json.dumps(fit))

        tree.SortChildren(root)

    def displayFit(self, event):
        selection = self.fittingsTreeCtrl.GetSelection()
        data = self.fittingsTreeCtrl.GetPyData(selection)

        if data is None:
            event.Skip()
            return

        fit = json.loads(data)
        list = []

        for item in fit['items']:
            try:
                cargo = Cargo(getItem(item['type']['id']))
                cargo.amount = item['quantity']
                list.append(cargo)
            except Exception as e:
                pyfalog.critical("Exception caught in displayFit")
                pyfalog.critical(e)

        self.parent.fitView.fitSelection = selection
        self.parent.fitView.update(list)


class FitView(Display):
    DEFAULT_COLS = ["Base Icon",
                    "Base Name"]

    def __init__(self, parent):
        Display.__init__(self, parent, style=wx.LC_SINGLE_SEL)
        self.fitSelection = None
