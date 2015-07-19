# -*- coding: utf-8 -*-
from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
import wx
from gui import bitmapLoader
from eos.types import Skill
import gui.globalEvents as GE

class ChangeAffectingSkills(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        if self.mainFrame.getActiveFit() is None or srcContext not in ("fittingModule", "fittingShip"):
            return False

        self.sChar = service.Character.getInstance()
        self.sFit = service.Fit.getInstance()
        fit = self.sFit.getFit(self.mainFrame.getActiveFit())

        self.charID = fit.character.ID

        if self.sChar.getCharName(self.charID) in ("All 0", "All 5"):
            return False

        if srcContext == "fittingShip":
            fitID = self.mainFrame.getActiveFit()
            sFit = service.Fit.getInstance()
            self.stuff = sFit.getFit(fitID).ship
        else:
            self.stuff = selection[0]

        cont = self.stuff.itemModifiedAttributes
        skills = set()

        for attrName in cont.iterAfflictions():
            if cont[attrName] == 0:
                continue

            for fit, afflictors in cont.getAfflictions(attrName).iteritems():
                for afflictor, modifier, amount, used in afflictors:
                    # only add Skills
                    if not isinstance(afflictor, Skill):
                        continue

                    skills.add(afflictor)

        self.skills = sorted(skills, key=lambda x: x.item.name)
        return len(self.skills) > 0

    def getText(self, itmContext, selection):
        return "Change %s Skills" % itmContext

    def addSkill(self, rootMenu, skill, i):
        if i < 0:
            label = "Not Learned"
        else:
            label = "Level %s" % i

        id = wx.NewId()
        self.skillIds[id] = (skill, i)
        menuItem = wx.MenuItem(rootMenu, id, label, kind=wx.ITEM_RADIO)
        rootMenu.Bind(wx.EVT_MENU, self.handleSkillChange, menuItem)
        return menuItem

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.skillIds = {}
        sub = wx.Menu()

        for skill in self.skills:
            skillItem = wx.MenuItem(sub, wx.NewId(), skill.item.name)
            grandSub = wx.Menu()
            skillItem.SetSubMenu(grandSub)
            if skill.learned:
                bitmap = bitmapLoader.getBitmap("lvl%s" % skill.level, "icons")
                if bitmap is not None:
                    skillItem.SetBitmap(bitmap)

            for i in xrange(-1, 6):
                levelItem = self.addSkill(rootMenu if msw else grandSub, skill, i)
                grandSub.AppendItem(levelItem)
                #@ todo: add check to current level. Need to fix #109 first
            sub.AppendItem(skillItem)

        return sub

    def handleSkillChange(self, event):
        skill, level = self.skillIds[event.Id]

        self.sChar.changeLevel(self.charID, skill.item.ID, level)
        fitID = self.mainFrame.getActiveFit()
        self.sFit.changeChar(fitID, self.charID)

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

ChangeAffectingSkills.register()
