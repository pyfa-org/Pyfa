from collections import OrderedDict
from itertools import chain

# noinspection PyPackageRequirements
import wx

from gui.utils.sorter import smartSort
from service.damagePattern import DamagePattern as DmgPatternSvc

_t = wx.GetTranslation


class DamagePatternMixin:

    def _getPatterns(self):
        sDP = DmgPatternSvc.getInstance()
        builtinPatterns = sDP.getBuiltinDamagePatternList()
        userPatterns = sorted(sDP.getUserDamagePatternList(), key=lambda p: smartSort(p.fullName))
        # Order here is important: patterns with duplicate names from the latter will overwrite
        # patterns from the former
        patterns = sorted(
                chain(builtinPatterns, userPatterns),
                key=lambda p: p.fullName not in ["Uniform", "Selected Ammo"])
        return patterns

    def _getItems(self, patterns):
        items = (OrderedDict(), OrderedDict())
        for pattern in patterns:
            container = items
            for categoryName in pattern.hierarchy:
                categoryName = _t(categoryName) if pattern.builtin else categoryName
                container = container[1].setdefault(categoryName, (OrderedDict(), OrderedDict()))
            shortName = _t(pattern.shortName) if pattern.builtin else pattern.shortName
            container[0][shortName] = pattern
        return items
