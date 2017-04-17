# shipBonusTitanM1WebStrengthBonus
#
# Used by:
# Ship: Vanquisher
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web", "speedFactor",
                                  src.getModifiedItemAttr("shipBonusTitanM1"), skill="Minmatar Titan")
