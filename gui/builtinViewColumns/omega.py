# noinspection PyPackageRequirements
import wx

import eos.db
from eos.saveddata.module import Module, Rack
from eos.saveddata.drone import Drone
from gui.viewColumn import ViewColumn


_alpha_skill_caps = None


def _get_alpha_skill_caps():
    global _alpha_skill_caps
    if _alpha_skill_caps is None:
        _alpha_skill_caps = {}
        alpha_clone = eos.db.getAlphaClone(1)
        if alpha_clone is not None:
            for skill_entry in alpha_clone.skills:
                _alpha_skill_caps[skill_entry.typeID] = skill_entry.level
    return _alpha_skill_caps


class Omega(ViewColumn):
    name = "Omega"

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.size = 20
        self.mask = wx.LIST_MASK_IMAGE
        self.columnText = "\u03A9"

    def getImageId(self, stuff):
        if isinstance(stuff, (Module, Drone)):
            if stuff.isEmpty:
                return -1
            item = stuff.item
        else:
            item = getattr(stuff, "item", stuff)
        if item is None:
            return -1
        if item.getAttribute("cloneGradeRestriction", 0) > 0:
            return self.fittingView.imageList.GetImageIndex(25874, "icons")
        caps = _get_alpha_skill_caps()
        if caps:
            for skill_item, required_level in item.requiredSkills.items():
                max_alpha_level = caps.get(skill_item.ID)
                if max_alpha_level is None or required_level > max_alpha_level:
                    return self.fittingView.imageList.GetImageIndex(25874, "icons")
        return -1


Omega.register()
