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
from service.esi import Esi
from service.esiAccess import APIException
from service.port import ESIExportException

pyfalog = Logger(__name__)


class EveFittings(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Browse EVE Fittings", pos=wx.DefaultPosition,
                          size=wx.Size(550, 450), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        self.mainFrame = parent
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        characterSelectSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.charChoice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [])
        characterSelectSizer.Add(self.charChoice, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.updateCharList()

        self.fetchBtn = wx.Button(self, wx.ID_ANY, "Fetch Fits", wx.DefaultPosition, wx.DefaultSize, 5)
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
        self.importBtn = wx.Button(self, wx.ID_ANY, "Import to pyfa", wx.DefaultPosition, wx.DefaultSize, 5)
        self.deleteBtn = wx.Button(self, wx.ID_ANY, "Delete from EVE", wx.DefaultPosition, wx.DefaultSize, 5)
        btnSizer.Add(self.importBtn, 1, wx.ALL, 5)
        btnSizer.Add(self.deleteBtn, 1, wx.ALL, 5)
        fitSizer.Add(btnSizer, 0, wx.EXPAND)

        contentSizer.Add(fitSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(contentSizer, 1, wx.EXPAND, 5)

        self.fetchBtn.Bind(wx.EVT_BUTTON, self.fetchFittings)
        self.importBtn.Bind(wx.EVT_BUTTON, self.importFitting)
        self.deleteBtn.Bind(wx.EVT_BUTTON, self.deleteFitting)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.statusbar = wx.StatusBar(self)
        self.statusbar.SetFieldsCount()
        self.SetStatusBar(self.statusbar)

        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

    def updateCharList(self):
        sEsi = Esi.getInstance()
        chars = sEsi.getSsoCharacters()

        if len(chars) == 0:
            self.Close()

        self.charChoice.Clear()
        for char in chars:
            self.charChoice.Append(char.characterName, char.ID)

        self.charChoice.SetSelection(0)

    def OnClose(self, event):
        self.mainFrame.Unbind(GE.EVT_SSO_LOGOUT)
        self.mainFrame.Unbind(GE.EVT_SSO_LOGIN)
        # self.cacheTimer.Stop()  # must be manually stopped, otherwise crash. See https://github.com/wxWidgets/Phoenix/issues/632
        event.Skip()

    def getActiveCharacter(self):
        selection = self.charChoice.GetCurrentSelection()
        return self.charChoice.GetClientData(selection) if selection is not None else None

    def fetchFittings(self, event):
        sEsi = Esi.getInstance()
        waitDialog = wx.BusyInfo("Fetching fits, please wait...", parent=self)

        try:
            self.fittings = sEsi.getFittings(self.getActiveCharacter())
            # self.cacheTime = fittings.get('cached_until')
            # self.updateCacheStatus(None)
            # self.cacheTimer.Start(1000)
            self.fitTree.populateSkillTree(self.fittings)
            del waitDialog
        except requests.exceptions.ConnectionError:
            msg = "Connection error, please check your internet connection"
            pyfalog.error(msg)
            self.statusbar.SetStatusText(msg)
        except APIException as ex:
            #  Can't do this in a finally because then it obscures the message dialog
            del waitDialog  # noqa: F821
            ESIExceptionHandler(self, ex)
        except Exception as ex:
            del waitDialog  # noqa: F821
            raise ex

    def importFitting(self, event):
        selection = self.fitView.fitSelection
        if not selection:
            return
        data = self.fitTree.fittingsTreeCtrl.GetItemData(selection)
        sPort = Port.getInstance()
        fits = sPort.importFitFromBuffer(data)
        self.mainFrame._openAfterImport(fits)

    def deleteFitting(self, event):
        sEsi = Esi.getInstance()
        selection = self.fitView.fitSelection
        if not selection:
            return
        data = json.loads(self.fitTree.fittingsTreeCtrl.GetItemData(selection))

        dlg = wx.MessageDialog(self,
                               "Do you really want to delete %s (%s) from EVE?" % (data['name'], getItem(data['ship_type_id']).name),
                               "Confirm Delete", wx.YES | wx.NO | wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
            try:
                sEsi.delFitting(self.getActiveCharacter(), data['fitting_id'])
                # repopulate the fitting list
                self.fitTree.populateSkillTree(self.fittings)
                self.fitView.update([])
            except requests.exceptions.ConnectionError:
                msg = "Connection error, please check your internet connection"
                pyfalog.error(msg)
                self.statusbar.SetStatusText(msg)


class ESIExceptionHandler(object):
    # todo: make this a generate excetpion handler for all calls
    def __init__(self, parentWindow, ex):
        if ex.response['error'].startswith('Token is not valid') or ex.response['error'] == 'invalid_token':  # todo: this seems messy, figure out a better response
            dlg = wx.MessageDialog(parentWindow,
                                   "There was an error validating characters' SSO token. Please try "
                                   "logging into the character again to reset the token.", "Invalid Token",
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            pyfalog.error(ex)
        else:
            # We don't know how to handle the error, raise it for the global error handler to pick it up
            raise ex


class ExportToEve(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Export fit to EVE", pos=wx.DefaultPosition,
                          size=(wx.Size(350, 100)), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.mainFrame = parent
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.charChoice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [])
        hSizer.Add(self.charChoice, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.updateCharList()
        self.charChoice.SetSelection(0)

        self.exportBtn = wx.Button(self, wx.ID_ANY, "Export Fit", wx.DefaultPosition, wx.DefaultSize, 5)
        hSizer.Add(self.exportBtn, 0, wx.ALL, 5)

        mainSizer.Add(hSizer, 0, wx.EXPAND, 5)

        self.exportBtn.Bind(wx.EVT_BUTTON, self.exportFitting)

        self.statusbar = wx.StatusBar(self)
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([100, -1])

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.SetSizer(mainSizer)
        self.SetStatusBar(self.statusbar)
        self.Layout()

        self.Centre(wx.BOTH)

    def updateCharList(self):
        sEsi = Esi.getInstance()
        chars = sEsi.getSsoCharacters()

        if len(chars) == 0:
            self.Close()

        self.charChoice.Clear()
        for char in chars:
            self.charChoice.Append(char.characterName, char.ID)

        self.charChoice.SetSelection(0)

    def OnClose(self, event):
        self.mainFrame.Unbind(GE.EVT_SSO_LOGOUT)
        self.mainFrame.Unbind(GE.EVT_SSO_LOGIN)

        event.Skip()

    def getActiveCharacter(self):
        selection = self.charChoice.GetCurrentSelection()
        return self.charChoice.GetClientData(selection) if selection is not None else None

    def exportFitting(self, event):
        fitID = self.mainFrame.getActiveFit()

        self.statusbar.SetStatusText("", 0)

        if fitID is None:
            self.statusbar.SetStatusText("Please select an active fitting in the main window", 1)
            return

        self.statusbar.SetStatusText("Sending request and awaiting response", 1)

        try:

            self.statusbar.SetStatusText("", 0)
            self.statusbar.SetStatusText("", 1)
            # try:
            #     text = json.loads(res.text)
            #     self.statusbar.SetStatusText(text['message'], 1)
            # except ValueError:
            #     pyfalog.warning("Value error on loading JSON.")
            #     self.statusbar.SetStatusText("", 1)
        except requests.exceptions.ConnectionError:
            msg = "Connection error, please check your internet connection"
            pyfalog.error(msg)
            self.statusbar.SetStatusText(msg)
        except ESIExportException as ex:
            pyfalog.error(ex)
            self.statusbar.SetStatusText("ERROR", 0)
            self.statusbar.SetStatusText(ex.args[0], 1)
        except APIException as ex:
            ESIExceptionHandler(self, ex)


class SsoCharacterMgmt(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="SSO Character Management", pos=wx.DefaultPosition,
                           size=wx.Size(550, 250), style=wx.DEFAULT_DIALOG_STYLE)
        self.mainFrame = parent
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.lcCharacters = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)

        self.lcCharacters.InsertColumn(0, heading='Character')
        self.lcCharacters.InsertColumn(1, heading='Character ID')

        self.popCharList()

        mainSizer.Add(self.lcCharacters, 1, wx.ALL | wx.EXPAND, 5)

        btnSizer = wx.BoxSizer(wx.VERTICAL)

        self.addBtn = wx.Button(self, wx.ID_ANY, "Add Character", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer.Add(self.addBtn, 0, wx.ALL | wx.EXPAND, 5)

        self.deleteBtn = wx.Button(self, wx.ID_ANY, "Revoke Character", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer.Add(self.deleteBtn, 0, wx.ALL | wx.EXPAND, 5)

        mainSizer.Add(btnSizer, 0, wx.EXPAND, 5)

        self.addBtn.Bind(wx.EVT_BUTTON, self.addChar)
        self.deleteBtn.Bind(wx.EVT_BUTTON, self.delChar)

        self.mainFrame.Bind(GE.EVT_SSO_LOGIN, self.ssoLogin)

        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

    def ssoLogin(self, event):
        if (self):
            # todo: these events don't unbind properly when window is closed (?), hence the `if`. Figure out better way of doing this.
            self.popCharList()
            event.Skip()

    def popCharList(self):
        sEsi = Esi.getInstance()
        chars = sEsi.getSsoCharacters()

        self.lcCharacters.DeleteAllItems()

        for index, char in enumerate(chars):
            self.lcCharacters.InsertItem(index, char.characterName)
            self.lcCharacters.SetItem(index, 1, str(char.characterID))
            self.lcCharacters.SetItemData(index, char.ID)

        self.lcCharacters.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.lcCharacters.SetColumnWidth(1, wx.LIST_AUTOSIZE)

    @staticmethod
    def addChar(event):
        sEsi = Esi.getInstance()
        sEsi.login()

    def delChar(self, event):
        item = self.lcCharacters.GetFirstSelected()
        if item > -1:
            charID = self.lcCharacters.GetItemData(item)
            sEsi = Esi.getInstance()
            sEsi.delSsoCharacter(charID)
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

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.displayFit)

        self.SetSizer(pmainSizer)

        self.Layout()

    def populateSkillTree(self, data):
        if data is None:
            return
        root = self.root
        tree = self.fittingsTreeCtrl
        tree.DeleteChildren(root)

        sEsi = Esi.getInstance()

        dict = {}
        fits = data
        for fit in fits:
            if (fit['fitting_id'] in sEsi.fittings_deleted):
                continue
            ship = getItem(fit['ship_type_id'])
            if ship is None:
                pyfalog.debug('Cannot find ship type id: {}'.format(fit['ship_type_id']))
                continue
            if ship.name not in dict:
                dict[ship.name] = []
            dict[ship.name].append(fit)

        for name, fits in dict.items():
            shipID = tree.AppendItem(root, name)
            for fit in fits:
                fitId = tree.AppendItem(shipID, fit['name'])
                tree.SetItemData(fitId, json.dumps(fit))

        tree.SortChildren(root)

    def displayFit(self, event):
        selection = self.fittingsTreeCtrl.GetSelection()
        data = self.fittingsTreeCtrl.GetItemData(selection)

        if data is None:
            event.Skip()
            return

        fit = json.loads(data)
        list = []

        for item in fit['items']:
            try:
                cargo = Cargo(getItem(item['type_id']))
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
