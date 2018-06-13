# noinspection PyPackageRequirements
import wx

from gui.bitmap_loader import BitmapLoader


class ItemDependents(wx.Panel):
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
        self.reqTree.SetItemData(self.root, None)

        self.imageList = wx.ImageList(16, 16)
        self.reqTree.SetImageList(self.imageList)
        skillBookId = self.imageList.Add(BitmapLoader.getBitmap("skill_small", "gui"))

        self.getFullSkillTree(item, self.root, skillBookId)

        self.Layout()

    def getFullSkillTree(self, parentSkill, parent, sbIconId):
        levelToItems = {}

        for item, level in parentSkill.requiredFor.items():
            if level not in levelToItems:
                levelToItems[level] = []
            levelToItems[level].append(item)

        for x in sorted(levelToItems.keys()):
            items = levelToItems[x]
            items.sort(key=lambda x: x.name)

            child = self.reqTree.AppendItem(parent, "Level {}".format(self.romanNb[int(x)]), sbIconId)
            for item in items:

                if item.iconID:
                    bitmap = BitmapLoader.getBitmap(item.iconID, "icons")
                    itemIcon = self.imageList.Add(bitmap) if bitmap else -1
                else:
                    itemIcon = -1

                self.reqTree.AppendItem(child, "{}".format(item.name), itemIcon)
