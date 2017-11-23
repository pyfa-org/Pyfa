# noinspection PyPackageRequirements
import wx

from gui.bitmapLoader import BitmapLoader


class ItemRequirements(wx.Panel):
    def __init__(self, parent, stuff, item):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)

        # itemId is set by the parent.
        self.romanNb = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
        self.skillIdHistory = []
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.reqTree = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.NO_BORDER)

        mainSizer.Add(self.reqTree, 1, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(mainSizer)
        self.root = self.reqTree.AddRoot("WINRARZOR")
        self.reqTree.SetPyData(self.root, None)

        self.imageList = wx.ImageList(16, 16)
        self.reqTree.SetImageList(self.imageList)
        skillBookId = self.imageList.Add(BitmapLoader.getBitmap("skill_small", "gui"))

        self.getFullSkillTree(item, self.root, skillBookId)

        self.reqTree.ExpandAll()

        self.Layout()

    def getFullSkillTree(self, parentSkill, parent, sbIconId):
        for skill, level in parentSkill.requiredSkills.iteritems():
            child = self.reqTree.AppendItem(parent, "%s  %s" % (skill.name, self.romanNb[int(level)]), sbIconId)
            if skill.ID not in self.skillIdHistory:
                self.getFullSkillTree(skill, child, sbIconId)
                self.skillIdHistory.append(skill.ID)
