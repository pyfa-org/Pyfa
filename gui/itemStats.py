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
import wx.gizmos
import gui.mainFrame
import bitmapLoader
import sys
import  wx.lib.mixins.listctrl  as  listmix
import wx.html
import service


from util import formatAmount

class ItemStatsDialog(wx.Dialog):
    counter = 0
    def __init__(self, victim, context = None):
        wx.Dialog.__init__(self,
                          gui.mainFrame.MainFrame.getInstance(),
                          wx.ID_ANY, title="Item stats",
                          #style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)
                          style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|
                           wx.MAXIMIZE_BOX|
                           wx.RESIZE_BORDER|
                           wx.SYSTEM_MENU )

        empty = getattr(victim, "isEmpty", False)

        if empty:
            self.Hide()
            self.Destroy()
            return

        item = getattr(victim, "item", None) if context != "ammo" else getattr(victim, "charge", None)
        if item is None:
            item = victim
            victim = None
        self.context = context
        if item.icon is not None:
            before,sep,after = item.icon.iconFile.rpartition("_")
            iconFile = "%s%s%s" % (before,sep,"0%s" % after if len(after) < 2 else after)

            self.SetIcon(wx.IconFromBitmap(bitmapLoader.getBitmap(iconFile, "pack")))
        self.SetTitle("%s: %s" % ("%s stats" % context.capitalize() if context is not None else "Stats", item.name))

        self.SetMinSize((300, 200))
        self.SetSize((500, 300))
        self.SetMaxSize((500, -1))
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.container = ItemStatsContainer(self, victim, item, context)
        self.mainSizer.Add(self.container, 1, wx.EXPAND)
        self.SetSizer(self.mainSizer)

        parent = gui.mainFrame.MainFrame.getInstance()

        dlgsize = self.GetSize()
        psize = parent.GetSize()
        ppos = parent.GetPosition()

        ItemStatsDialog.counter += 1
        self.dlgOrder = ItemStatsDialog.counter

        counter = ItemStatsDialog.counter
        dlgStep = 30
        if counter * dlgStep > ppos.x+psize.width-dlgsize.x or counter * dlgStep > ppos.y+psize.height-dlgsize.y:
            ItemStatsDialog.counter = 1

        dlgx = ppos.x + counter * dlgStep
        dlgy = ppos.y + counter * dlgStep
        self.SetPosition((dlgx,dlgy))

        self.Show()

        self.Bind(wx.EVT_CLOSE, self.closeEvent)

    def closeEvent(self, event):

        if self.dlgOrder==ItemStatsDialog.counter:
            ItemStatsDialog.counter -= 1
        self.Destroy()
        event.Skip()

###########################################################################
## Class ItemStatsContainer
###########################################################################

class ItemStatsContainer ( wx.Panel ):

    def __init__( self, parent, stuff, item, context = None):
        wx.Panel.__init__ ( self, parent )
        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.nbContainer = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.nbContainer, 1, wx.EXPAND |wx.ALL, 2 )

        self.desc = ItemDescription(self.nbContainer, stuff, item)
        self.nbContainer.AddPage(self.desc, "Description")

        self.params = ItemParams(self.nbContainer, stuff, item, context)
        self.nbContainer.AddPage(self.params, "Attributes")

        self.reqs = ItemRequirements(self.nbContainer, stuff, item)
        self.nbContainer.AddPage(self.reqs, "Requirements")

        self.effects = ItemEffects(self.nbContainer, stuff, item)
        self.nbContainer.AddPage(self.effects, "Effects")

        if stuff is not None:
            self.affectedby = ItemAffectedBy(self.nbContainer, stuff, item)
            self.nbContainer.AddPage(self.affectedby, "Affected by")

        self.SetSizer(mainSizer)
        self.Layout()

    def __del__( self ):
        pass

###########################################################################
## Class AutoListCtrl
###########################################################################

class AutoListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ListRowHighlighter):

    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ListRowHighlighter.__init__(self)

###########################################################################
## Class AutoListCtrl
###########################################################################

class AutoListCtrlNoHighlight(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ListRowHighlighter):

    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


###########################################################################
## Class ItemDescription
###########################################################################

class ItemDescription ( wx.Panel ):

    def __init__(self, parent, stuff, item):
        wx.Panel.__init__ (self, parent)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)


        self.description = wx.html.HtmlWindow(self)

        desc = item.description.replace("\r","<br>")

        self.description.SetPage(desc)

        mainSizer.Add(self.description, 1, wx.ALL|wx.EXPAND, 0)
        self.Layout()

###########################################################################
## Class ItemParams
###########################################################################

class ItemParams (wx.Panel):
    def __init__(self, parent, stuff, item, context = None):
        wx.Panel.__init__ (self, parent)
        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.paramList = AutoListCtrl(self, wx.ID_ANY,
                                     style = #wx.LC_HRULES |
                                      #wx.LC_NO_HEADER |
                                      wx.LC_REPORT |wx.LC_SINGLE_SEL |wx.LC_VRULES |wx.NO_BORDER)
        mainSizer.Add( self.paramList, 1, wx.ALL|wx.EXPAND, 0 )
        self.SetSizer( mainSizer )

        self.toggleView = 1
        self.stuff = stuff
        self.item = item

        self.m_staticline = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        mainSizer.Add( self.m_staticline, 0, wx.EXPAND)
        bSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.totalAttrsLabel = wx.StaticText( self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer.Add( self.totalAttrsLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT)

        self.toggleViewBtn = wx.ToggleButton( self, wx.ID_ANY, u"Toggle view mode", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer.Add( self.toggleViewBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        if stuff is not None:
            self.refreshBtn = wx.Button( self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0 )
            bSizer.Add( self.refreshBtn, 0, wx.ALIGN_CENTER_VERTICAL)
            self.refreshBtn.Bind( wx.EVT_BUTTON, self.RefreshValues )

        mainSizer.Add( bSizer, 0, wx.ALIGN_RIGHT)

        self.PopulateList()

        self.toggleViewBtn.Bind(wx.EVT_TOGGLEBUTTON,self.ToggleViewMode)

    def UpdateList(self):
        self.Freeze()
        self.paramList.ClearAll()
        self.PopulateList()
        self.Thaw()
        self.paramList.resizeLastColumn(100)

    def RefreshValues(self, event):
        self.UpdateList()
        event.Skip()

    def ToggleViewMode(self, event):
        self.toggleView *=-1
        self.UpdateList()
        event.Skip()

    def PopulateList(self):
        self.paramList.InsertColumn(0,"Attribute")
        self.paramList.InsertColumn(1,"Value")
        self.paramList.SetColumnWidth(1,100)
        self.paramList.setResizeColumn(1)
        if self.stuff is None or self.stuff.item == self.item:
            attrs = self.stuff.itemModifiedAttributes if self.stuff is not None else self.item.attributes
            attrsInfo = self.item.attributes if self.stuff is None else self.stuff.item.attributes
        else:
            attrs = self.stuff.chargeModifiedAttributes if self.stuff is not None else self.item.attributes
            attrsInfo = self.item.attributes if self.stuff is None else self.stuff.charge.attributes

        names = list(attrs.iterkeys())
        names.sort()

        idNameMap = {}
        idCount = 0
        for name in names:
            info = attrsInfo.get(name)

            value = attrs[name] if self.stuff is not None else attrs[name].value

            if self.toggleView != 1:
                attrName = name
            else:
                attrName = info.displayName if info else name

            index = self.paramList.InsertStringItem(sys.maxint, attrName)
            idNameMap[idCount] = attrName
            self.paramList.SetItemData(index, idCount)
            idCount += 1

            if self.toggleView != 1:
                valueUnit = str(value)
            elif info and info.unit:
                valueUnit = self.TranslateValueUnit(value, info.unit.displayName, info.unit.name)
            else:
                valueUnit = formatAmount(value, 3, 0, 0)

            self.paramList.SetStringItem(index, 1, valueUnit)



        self.paramList.SortItems(lambda id1, id2: cmp(idNameMap[id1], idNameMap[id2]))
        self.paramList.RefreshRows()
        self.totalAttrsLabel.SetLabel("%d attributes. " %idCount)
        self.Layout()

    def TranslateValueUnit(self, value, unitName, unitDisplayName):
        trans = {"Inverse Absolute Percent": (lambda: (1-value)*100, unitName),
                 "Milliseconds": (lambda: value / 1000.0, unitName),
                 "Volume": (lambda: value, u"m\u00B3"),
                 "Sizeclass": (lambda: value, ""),
                 "typeID": (lambda: value, "")}

        override = trans.get(unitDisplayName)
        if override is not None:
            return "%s %s" % (formatAmount(override[0](), 3, 0, 0), override[1])
        else:
            return "%s %s" % (formatAmount(value, 3, 0),unitName)

###########################################################################
## Class ItemRequirements
###########################################################################

class ItemRequirements ( wx.Panel ):

    def __init__(self, parent, stuff, item):
        wx.Panel.__init__ (self, parent, style = wx.TAB_TRAVERSAL)

        #itemId is set by the parent.
        self.romanNb = ["0","I","II","III","IV","V","VI","VII","VIII","IX","X"]
        self.skillIdHistory=[]
        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.reqTree = wx.TreeCtrl(self, style = wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.NO_BORDER)

        mainSizer.Add(self.reqTree, 1, wx.ALL|wx.EXPAND, 0)

        self.SetSizer(mainSizer)
        self.root = self.reqTree.AddRoot("WINRARZOR")
        self.reqTree.SetPyData(self.root, None)

        self.imageList = wx.ImageList(16, 16)
        self.reqTree.SetImageList(self.imageList)
        skillBookId = self.imageList.Add(bitmapLoader.getBitmap("skill_small", "icons"))

        self.getFullSkillTree(item,self.root,skillBookId)

        self.reqTree.ExpandAll()

        self.Layout()

    def getFullSkillTree(self,parentSkill,parent,sbIconId):
        for skill, level in parentSkill.requiredSkills.iteritems():
            child = self.reqTree.AppendItem(parent,"%s  %s" %(skill.name,self.romanNb[int(level)]), sbIconId)
            if skill.ID not in self.skillIdHistory:
                self.getFullSkillTree(skill,child,sbIconId)
                self.skillIdHistory.append(skill.ID)


###########################################################################
## Class ItemEffects
###########################################################################

class ItemEffects (wx.Panel):
    def __init__(self, parent, stuff, item):
        wx.Panel.__init__ (self, parent)
        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.effectList = AutoListCtrl(self, wx.ID_ANY,
                                     style =
                                      #wx.LC_HRULES |
                                      #wx.LC_NO_HEADER |
                                      wx.LC_REPORT |wx.LC_SINGLE_SEL |wx.LC_VRULES |wx.NO_BORDER)
        mainSizer.Add( self.effectList, 1, wx.ALL|wx.EXPAND, 0 )
        self.SetSizer( mainSizer )

        self.effectList.InsertColumn(0,"Name")
        self.effectList.InsertColumn(1,"Implemented")

        self.effectList.SetColumnWidth(0,385)

        self.effectList.setResizeColumn(0)

        self.effectList.SetColumnWidth(1,80)

        effects = item.effects
        names = list(effects.iterkeys())
        names.sort()

        for name in names:
            index = self.effectList.InsertStringItem(sys.maxint, name)

            if effects[name].isImplemented:
                implemented = "Yes"
            else:
                implemented = "No"

            self.effectList.SetStringItem(index, 1, implemented)

        self.effectList.RefreshRows()
        self.Layout()


###########################################################################
## Class ItemAffectedBy
###########################################################################


class ItemAffectedBy (wx.Panel):
    def __init__(self, parent, stuff, item):
        wx.Panel.__init__ (self, parent)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.affectedBy = wx.TreeCtrl(self, style = wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.NO_BORDER)
        mainSizer.Add(self.affectedBy, 1, wx.ALL|wx.EXPAND, 0)

        root = self.affectedBy.AddRoot("WINPWNZ0R")
        self.affectedBy.SetPyData(root, None)

        self.imageList = wx.ImageList(16, 16)
        self.affectedBy.SetImageList(self.imageList)


        cont = stuff.itemModifiedAttributes if item == stuff.item else stuff.chargeModifiedAttributes
        things = {}
        for attrName in cont.iterAfflictions():
            for fit, afflictors in cont.getAfflictions(attrName).iteritems():
                for afflictor in afflictors:
                    if afflictor.item.name not in things:
                        things[afflictor.item.name] = [set(), set()]

                    info = things[afflictor.item.name]
                    info[0].add(afflictor)
                    info[1].add(attrName)

        for itemName, info in things.iteritems():
#            if wx.Platform in ['__WXGTK__', '__WXMSW__']:
#                color = wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DLIGHT)
#            else:
#                color = wx.Colour(237, 243, 254)

            afflictors, attrNames = info
            counter = len(afflictors)

            baseAfflictor = afflictors.pop()
            print baseAfflictor
            if baseAfflictor.item.icon:
                itemIcon = self.imageList.Add(bitmapLoader.getBitmap(baseAfflictor.item.icon.iconFile, "pack"))
            else:
                itemIcon = -1

            child = self.affectedBy.AppendItem(root, "%s" % itemName if counter == 1 else "%s x %d" % (itemName,counter), itemIcon)
#            self.effectList.SetItemBackgroundColour(index, color)
            if counter > 0:
                for attrName in attrNames:
                    attrInfo = stuff.item.attributes.get(attrName)
                    displayName = attrInfo.displayName if attrInfo else ""

                    self.affectedBy.AppendItem(child, "%s" % (displayName if displayName != "" else attrName), -1)

        self.m_staticline = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )

        mainSizer.Add( self.m_staticline, 0, wx.EXPAND)
        bSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.totalAttrsLabel = wx.StaticText( self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer.Add( self.totalAttrsLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT)

        self.toggleViewBtn = wx.ToggleButton( self, wx.ID_ANY, u"Toggle view mode", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer.Add( self.toggleViewBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        if stuff is not None:
            self.refreshBtn = wx.Button( self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0 )
            bSizer.Add( self.refreshBtn, 0, wx.ALIGN_CENTER_VERTICAL)
#            self.refreshBtn.Bind( wx.EVT_BUTTON, self.RefreshValues )

        mainSizer.Add( bSizer, 0, wx.ALIGN_RIGHT)
        self.SetSizer(mainSizer)
        self.Layout()
