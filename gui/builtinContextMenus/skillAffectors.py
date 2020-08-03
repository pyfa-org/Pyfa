# noinspection PyPackageRequirements

import wx

import gui.globalEvents as GE
import gui.mainFrame
from eos.saveddata.character import Skill
from gui.bitmap_loader import BitmapLoader
from gui.contextMenu import ContextMenuSingle
from service.character import Character
from service.fit import Fit

_t = wx.GetTranslation


class ChangeAffectingSkills(ContextMenuSingle):
    visibilitySetting = 'changeAffectingSkills'

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext not in (
                "fittingModule", "fittingCharge",
                "fittingShip", "droneItem",
                "fighterItem"
        ):
            return False

        fitID = self.mainFrame.getActiveFit()
        if fitID is None:
            return False

        if (mainItem is None or getattr(mainItem, "isEmpty", False)) and srcContext != "fittingShip":
            return False

        self.sChar = Character.getInstance()
        self.sFit = Fit.getInstance()
        fit = self.sFit.getFit(fitID)

        self.charID = fit.character.ID

        # if self.sChar.getCharName(self.charID) in ("All 0", "All 5"):
        #    return False

        if srcContext == "fittingShip":
            sFit = Fit.getInstance()
            self.stuff = sFit.getFit(fitID).ship
            cont = sFit.getFit(fitID).ship.itemModifiedAttributes
        elif srcContext == "fittingCharge":
            cont = mainItem.chargeModifiedAttributes
        else:
            cont = mainItem.itemModifiedAttributes

        skills = set()

        for attrName in cont.iterAfflictions():
            if cont[attrName] == 0:
                continue

            for fit, afflictors in cont.getAfflictions(attrName).items():
                for afflictor, operator, stackingGroup, preResAmount, postResAmount, used in afflictors:
                    # only add Skills
                    if not isinstance(afflictor, Skill):
                        continue

                    skills.add(afflictor)

        self.skills = sorted(skills, key=lambda x: x.item.name)
        return len(self.skills) > 0

    def getText(self, callingWindow, itmContext, mainItem):
        return _t("Change %s Skills") % itmContext

    def addSkill(self, rootMenu, skill, i):
        if i < 0:
            label = _t("Not Learned")
        else:
            label = _t("Level %s") % i

        id = ContextMenuSingle.nextID()
        self.skillIds[id] = (skill, i)
        menuItem = wx.MenuItem(rootMenu, id, label, kind=wx.ITEM_RADIO)
        rootMenu.Bind(wx.EVT_MENU, self.handleSkillChange, menuItem)
        return menuItem

    def getSubMenu(self, callingWindow, context, mainItem, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.skillIds = {}
        sub = wx.Menu()

        for skill in self.skills:
            skillItem = wx.MenuItem(sub, ContextMenuSingle.nextID(), skill.item.name)
            grandSub = wx.Menu()
            skillItem.SetSubMenu(grandSub)
            if skill.learned:
                bitmap = BitmapLoader.getBitmap("lvl%s" % skill.level, "gui")
                if bitmap is not None:
                    skillItem.SetBitmap(bitmap)

            for i in range(-1, 6):
                levelItem = self.addSkill(rootMenu if msw else grandSub, skill, i)
                grandSub.Append(levelItem)
                if (not skill.learned and i == -1) or (skill.learned and skill.level == i):
                    levelItem.Check(True)
            sub.Append(skillItem)

        return sub

    def handleSkillChange(self, event):
        skill, level = self.skillIds[event.Id]

        self.sChar.changeLevel(self.charID, skill.item.ID, level)
        fitID = self.mainFrame.getActiveFit()
        self.sFit.changeChar(fitID, self.charID)

        wx.PostEvent(self.mainFrame, GE.CharListUpdated())
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))


ChangeAffectingSkills.register()
