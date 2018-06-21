# noinspection PyPackageRequirements
import wx

from eos.saveddata.mode import Mode
from eos.saveddata.character import Skill
from eos.saveddata.implant import Implant
from eos.saveddata.booster import Booster
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.module import Module
from eos.saveddata.ship import Ship
from eos.saveddata.citadel import Citadel
from eos.saveddata.fit import Fit

import gui.mainFrame
from gui.contextMenu import ContextMenu
from gui.bitmap_loader import BitmapLoader


class ItemAffectedBy(wx.Panel):
    ORDER = [Fit, Ship, Citadel, Mode, Module, Drone, Fighter, Implant, Booster, Skill]

    def __init__(self, parent, stuff, item):
        wx.Panel.__init__(self, parent)
        self.stuff = stuff
        self.item = item

        self.activeFit = gui.mainFrame.MainFrame.getInstance().getActiveFit()

        self.showRealNames = False
        self.showAttrView = False
        self.expand = -1

        self.treeItems = []

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.affectedBy = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.NO_BORDER)
        mainSizer.Add(self.affectedBy, 1, wx.ALL | wx.EXPAND, 0)

        self.m_staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)

        mainSizer.Add(self.m_staticline, 0, wx.EXPAND)
        bSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.toggleExpandBtn = wx.ToggleButton(self, wx.ID_ANY, "Expand All", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.toggleExpandBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        self.toggleNameBtn = wx.ToggleButton(self, wx.ID_ANY, "Toggle Names", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.toggleNameBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        self.toggleViewBtn = wx.ToggleButton(self, wx.ID_ANY, "Toggle View", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.toggleViewBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        if stuff is not None:
            self.refreshBtn = wx.Button(self, wx.ID_ANY, "Refresh", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
            bSizer.Add(self.refreshBtn, 0, wx.ALIGN_CENTER_VERTICAL)
            self.refreshBtn.Bind(wx.EVT_BUTTON, self.RefreshTree)

        self.toggleNameBtn.Bind(wx.EVT_TOGGLEBUTTON, self.ToggleNameMode)
        self.toggleExpandBtn.Bind(wx.EVT_TOGGLEBUTTON, self.ToggleExpand)
        self.toggleViewBtn.Bind(wx.EVT_TOGGLEBUTTON, self.ToggleViewMode)

        mainSizer.Add(bSizer, 0, wx.ALIGN_RIGHT)
        self.SetSizer(mainSizer)
        self.PopulateTree()
        self.Layout()
        self.affectedBy.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.scheduleMenu)

    def scheduleMenu(self, event):
        event.Skip()
        wx.CallAfter(self.spawnMenu, event.Item)

    def spawnMenu(self, item):
        self.affectedBy.SelectItem(item)

        stuff = self.affectedBy.GetItemData(item)
        # String is set as data when we are dealing with attributes, not stuff containers
        if stuff is None or isinstance(stuff, str):
            return
        contexts = []

        # Skills are different in that they don't have itemModifiedAttributes,
        # which is needed if we send the container to itemStats dialog. So
        # instead, we send the item.
        type_ = stuff.__class__.__name__
        contexts.append(("itemStats", type_))
        menu = ContextMenu.getMenu(stuff if type_ != "Skill" else stuff.item, *contexts)
        self.PopupMenu(menu)

    def ExpandCollapseTree(self):

        self.Freeze()
        if self.expand == 1:
            self.affectedBy.ExpandAll()
        else:
            try:
                self.affectedBy.CollapseAll()
            except:
                pass

        self.Thaw()

    def ToggleExpand(self, event):
        self.expand *= -1
        self.ExpandCollapseTree()

    def ToggleViewTree(self):
        self.Freeze()

        for item in self.treeItems:
            change = self.affectedBy.GetItemData(item)
            display = self.affectedBy.GetItemText(item)
            self.affectedBy.SetItemText(item, change)
            self.affectedBy.SetItemData(item, display)

        self.Thaw()

    def UpdateTree(self):
        self.Freeze()
        self.affectedBy.DeleteAllItems()
        self.PopulateTree()
        self.Thaw()

    def RefreshTree(self, event):
        self.UpdateTree()
        event.Skip()

    def ToggleViewMode(self, event):
        self.showAttrView = not self.showAttrView
        self.affectedBy.DeleteAllItems()
        self.PopulateTree()
        event.Skip()

    def ToggleNameMode(self, event):
        self.showRealNames = not self.showRealNames
        self.ToggleViewTree()
        event.Skip()

    def PopulateTree(self):
        # sheri was here
        del self.treeItems[:]
        root = self.affectedBy.AddRoot("WINPWNZ0R")
        self.affectedBy.SetItemData(root, None)

        self.imageList = wx.ImageList(16, 16)
        self.affectedBy.SetImageList(self.imageList)

        if self.showAttrView:
            self.buildAttributeView(root)
        else:
            self.buildModuleView(root)

        self.ExpandCollapseTree()

    def sortAttrDisplayName(self, attr):
        info = self.stuff.item.attributes.get(attr)
        if info and info.displayName != "":
            return info.displayName

        return attr

    def buildAttributeView(self, root):
        """
        We first build a usable dictionary of items. The key is either a fit
        if the afflictions stem from a projected fit, or self.stuff if they
        are local afflictions (everything else, even gang boosts at this time)
        The value of this is yet another dictionary in the following format:

        "attribute name": {
              "Module Name": [
                   class of affliction,
                   affliction item (required due to GH issue #335)
                   modifier type
                   amount of modification
                   whether this affliction was projected
              ]
        }
        """

        attributes = self.stuff.itemModifiedAttributes if self.item == self.stuff.item else self.stuff.chargeModifiedAttributes
        container = {}
        for attrName in attributes.iterAfflictions():
            # if value is 0 or there has been no change from original to modified, return
            if attributes[attrName] == (attributes.getOriginal(attrName, 0)):
                continue

            for fit, afflictors in attributes.getAfflictions(attrName).items():
                for afflictor, modifier, amount, used in afflictors:

                    if not used or afflictor.item is None:
                        continue

                    if fit.ID != self.activeFit:
                        # affliction fit does not match our fit
                        if fit not in container:
                            container[fit] = {}
                        items = container[fit]
                    else:
                        # local afflictions
                        if self.stuff not in container:
                            container[self.stuff] = {}
                        items = container[self.stuff]

                    # items hold our module: info mappings
                    if attrName not in items:
                        items[attrName] = []

                    if afflictor == self.stuff and getattr(afflictor, 'charge', None):
                        # we are showing a charges modifications, see #335
                        item = afflictor.charge
                    else:
                        item = afflictor.item

                    items[attrName].append(
                            (type(afflictor), afflictor, item, modifier, amount, getattr(afflictor, "projected", False)))

        # Make sure projected fits are on top
        rootOrder = list(container.keys())
        rootOrder.sort(key=lambda x: self.ORDER.index(type(x)))

        # Now, we take our created dictionary and start adding stuff to our tree
        for thing in rootOrder:
            # This block simply directs which parent we are adding to (root or projected fit)
            if thing == self.stuff:
                parent = root
            else:  # projected fit
                icon = self.imageList.Add(BitmapLoader.getBitmap("ship_small", "gui"))
                child = self.affectedBy.AppendItem(root, "{} ({})".format(thing.name, thing.ship.item.name), icon)
                parent = child

            attributes = container[thing]
            attrOrder = sorted(list(attributes.keys()), key=self.sortAttrDisplayName)

            for attrName in attrOrder:
                attrInfo = self.stuff.item.attributes.get(attrName)
                displayName = attrInfo.displayName if attrInfo and attrInfo.displayName != "" else attrName

                if attrInfo:
                    if attrInfo.iconID is not None:
                        iconFile = attrInfo.iconID
                        icon = BitmapLoader.getBitmap(iconFile, "icons")
                        if icon is None:
                            icon = BitmapLoader.getBitmap("transparent16x16", "gui")
                        attrIcon = self.imageList.Add(icon)
                    else:
                        attrIcon = self.imageList.Add(BitmapLoader.getBitmap("0", "icons"))
                else:
                    attrIcon = self.imageList.Add(BitmapLoader.getBitmap("0", "icons"))

                if self.showRealNames:
                    display = attrName
                    saved = displayName
                else:
                    display = displayName
                    saved = attrName

                # this is the attribute node
                child = self.affectedBy.AppendItem(parent, display, attrIcon)
                self.affectedBy.SetItemData(child, saved)
                self.treeItems.append(child)

                items = attributes[attrName]
                items.sort(key=lambda x: self.ORDER.index(x[0]))
                for itemInfo in items:
                    afflictorType, afflictor, item, attrModifier, attrAmount, projected = itemInfo

                    if afflictorType == Ship:
                        itemIcon = self.imageList.Add(BitmapLoader.getBitmap("ship_small", "gui"))
                    elif item.iconID:
                        bitmap = BitmapLoader.getBitmap(item.iconID, "icons")
                        itemIcon = self.imageList.Add(bitmap) if bitmap else -1
                    else:
                        itemIcon = -1

                    displayStr = item.name

                    if projected:
                        displayStr += " (projected)"

                    penalized = ""
                    if '*' in attrModifier:
                        if 's' in attrModifier:
                            penalized += "(penalized)"
                        if 'r' in attrModifier:
                            penalized += "(resisted)"
                    attrModifier = "*"

                    # this is the Module node, the attribute will be attached to this
                    display = "%s %s %.2f %s" % (displayStr, attrModifier, attrAmount, penalized)
                    treeItem = self.affectedBy.AppendItem(child, display, itemIcon)
                    self.affectedBy.SetItemData(treeItem, afflictor)

    def buildModuleView(self, root):
        """
        We first build a usable dictionary of items. The key is either a fit
        if the afflictions stem from a projected fit, or self.stuff if they
        are local afflictions (everything else, even gang boosts at this time)
        The value of this is yet another dictionary in the following format:

        "Module Name": [
            class of affliction,
            set of afflictors (such as 2 of the same module),
            info on affliction (attribute name, modifier, and modification amount),
            item that will be used to determine icon (required due to GH issue #335)
            whether this affliction is actually used (unlearned skills are not used)
        ]
        """

        attributes = self.stuff.itemModifiedAttributes if self.item == self.stuff.item else self.stuff.chargeModifiedAttributes
        container = {}
        for attrName in attributes.iterAfflictions():
            # if value is 0 or there has been no change from original to modified, return
            if attributes[attrName] == (attributes.getOriginal(attrName, 0)):
                continue

            for fit, afflictors in attributes.getAfflictions(attrName).items():
                for afflictor, modifier, amount, used in afflictors:
                    if not used or getattr(afflictor, 'item', None) is None:
                        continue

                    if fit.ID != self.activeFit:
                        # affliction fit does not match our fit
                        if fit not in container:
                            container[fit] = {}
                        items = container[fit]
                    else:
                        # local afflictions
                        if self.stuff not in container:
                            container[self.stuff] = {}
                        items = container[self.stuff]

                    if afflictor == self.stuff and getattr(afflictor, 'charge', None):
                        # we are showing a charges modifications, see #335
                        item = afflictor.charge
                    else:
                        item = afflictor.item

                    # items hold our module: info mappings
                    if item.name not in items:
                        items[item.name] = [type(afflictor), set(), [], item, getattr(afflictor, "projected", False)]

                    info = items[item.name]
                    info[1].add(afflictor)
                    # If info[1] > 1, there are two separate modules working.
                    # Check to make sure we only include the modifier once
                    # See GH issue 154
                    if len(info[1]) > 1 and (attrName, modifier, amount) in info[2]:
                        continue
                    info[2].append((attrName, modifier, amount))

        # Make sure projected fits are on top
        rootOrder = list(container.keys())
        rootOrder.sort(key=lambda x: self.ORDER.index(type(x)))

        # Now, we take our created dictionary and start adding stuff to our tree
        for thing in rootOrder:
            # This block simply directs which parent we are adding to (root or projected fit)
            if thing == self.stuff:
                parent = root
            else:  # projected fit
                icon = self.imageList.Add(BitmapLoader.getBitmap("ship_small", "gui"))
                child = self.affectedBy.AppendItem(root, "{} ({})".format(thing.name, thing.ship.item.name), icon)
                parent = child

            items = container[thing]
            order = list(items.keys())
            order.sort(key=lambda x: (self.ORDER.index(items[x][0]), x))

            for itemName in order:
                info = items[itemName]
                afflictorType, afflictors, attrData, item, projected = info
                counter = len(afflictors)
                if afflictorType == Ship:
                    itemIcon = self.imageList.Add(BitmapLoader.getBitmap("ship_small", "gui"))
                elif item.iconID:
                    bitmap = BitmapLoader.getBitmap(item.iconID, "icons")
                    itemIcon = self.imageList.Add(bitmap) if bitmap else -1
                else:
                    itemIcon = -1

                displayStr = itemName

                if counter > 1:
                    displayStr += " x {}".format(counter)

                if projected:
                    displayStr += " (projected)"

                # this is the Module node, the attribute will be attached to this
                child = self.affectedBy.AppendItem(parent, displayStr, itemIcon)
                self.affectedBy.SetItemData(child, afflictors.pop())

                if counter > 0:
                    attributes = []
                    for attrName, attrModifier, attrAmount in attrData:
                        attrInfo = self.stuff.item.attributes.get(attrName)
                        displayName = attrInfo.displayName if attrInfo else ""

                        if attrInfo:
                            if attrInfo.iconID is not None:
                                iconFile = attrInfo.iconID
                                icon = BitmapLoader.getBitmap(iconFile, "icons")
                                if icon is None:
                                    icon = BitmapLoader.getBitmap("transparent16x16", "gui")

                                attrIcon = self.imageList.Add(icon)
                            else:
                                attrIcon = self.imageList.Add(BitmapLoader.getBitmap("0", "icons"))
                        else:
                            attrIcon = self.imageList.Add(BitmapLoader.getBitmap("0", "icons"))

                        penalized = ""
                        if '*' in attrModifier:
                            if 's' in attrModifier:
                                penalized += "(penalized)"
                            if 'r' in attrModifier:
                                penalized += "(resisted)"
                        attrModifier = "*"

                        attributes.append((attrName, (displayName if displayName != "" else attrName), attrModifier,
                                           attrAmount, penalized, attrIcon))

                    attrSorted = sorted(attributes, key=lambda attribName: attribName[0])
                    for attr in attrSorted:
                        attrName, displayName, attrModifier, attrAmount, penalized, attrIcon = attr

                        if self.showRealNames:
                            display = "%s %s %.2f %s" % (attrName, attrModifier, attrAmount, penalized)
                            saved = "%s %s %.2f %s" % (
                                displayName if displayName != "" else attrName,
                                attrModifier,
                                attrAmount,
                                penalized
                            )
                        else:
                            display = "%s %s %.2f %s" % (
                                displayName if displayName != "" else attrName,
                                attrModifier,
                                attrAmount,
                                penalized
                            )
                            saved = "%s %s %.2f %s" % (attrName, attrModifier, attrAmount, penalized)

                        treeitem = self.affectedBy.AppendItem(child, display, attrIcon)
                        self.affectedBy.SetItemData(treeitem, saved)
                        self.treeItems.append(treeitem)
