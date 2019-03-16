# shipBonusDreadnoughtG3RepairTime
#
# Used by:
# Ship: Moros
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"), "duration",
                                  src.getModifiedItemAttr("shipBonusDreadnoughtG3"), skill="Gallente Dreadnought")
