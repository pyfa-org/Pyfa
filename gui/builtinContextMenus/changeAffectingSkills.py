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
        self.sChar = service.Character.getInstance()

        self.sFit = service.Fit.getInstance()
        fit = self.sFit.getFit(self.mainFrame.getActiveFit())

        self.charID = fit.character.ID

    def display(self, srcContext, selection):
        if self.mainFrame.getActiveFit() is None or srcContext not in ("fittingModule", "fittingShip"):
            return False

        if self.sChar.getCharName(self.charID) in ("All 0", "All 5"):
            return False

        if srcContext == "fittingShip":
            fitID = self.mainFrame.getActiveFit()
            sFit = service.Fit.getInstance()
            self.stuff = sFit.getFit(fitID).ship
        else:
            self.stuff = selection[0]

        cont = self.stuff.itemModifiedAttributes
        self.skills = []

        for attrName in cont.iterAfflictions():
            if cont[attrName] == 0:
                continue

            for fit, afflictors in cont.getAfflictions(attrName).iteritems():
                for afflictor, modifier, amount, used in afflictors:
                    # only add Skills
                    if not isinstance(afflictor, Skill):
                        continue

                    self.skills.append(afflictor)
        self.skills.sort(key=lambda x: x.item.name)

        return len(self.skills) > 0

    def getText(self, itmContext, selection):
        return "Change Affecting Skills"

    def activate(self, fullContext, selection, i):
        pass

    def addSkill(self, rootMenu, skill, i):
        if i < 0:
            label = "Not Learned"
        else:
            label = "Level %s" % i

        id = wx.NewId()
        self.skillIds[id] = (skill, i)
        menuItem = wx.MenuItem(rootMenu, id, label)
        rootMenu.Bind(wx.EVT_MENU, self.handleSkillChange, menuItem)
        return menuItem

    def getSubMenu(self, context, selection, menu, i):
        self.context = context
        self.skillIds = {}

        m = wx.Menu()

        for skill in self.skills:
            skillItem = wx.MenuItem(m, wx.NewId(), skill.item.name)
            sub = wx.Menu()
            skillItem.SetSubMenu(sub)
            if skill.learned:
                bitmap = bitmapLoader.getBitmap("lvl%s" % skill.level, "icons")
                if bitmap is not None:
                    skillItem.SetBitmap(bitmap)

            for i in xrange(-1, 6):
                levelItem = self.addSkill(menu, skill, i)
                sub.AppendItem(levelItem)
            m.AppendItem(skillItem)

        return m

    def handleSkillChange(self, event):
        skill, level = self.skillIds[event.Id]

        self.sChar.changeLevel(self.charID, skill.item.ID, level)
        fitID = self.mainFrame.getActiveFit()
        self.sFit.changeChar(fitID, self.charID)

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

ChangeAffectingSkills.register()
