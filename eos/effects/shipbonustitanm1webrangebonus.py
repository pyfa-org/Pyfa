# shipBonusTitanM1WebRangeBonus
#
# Used by:
# Ship: Molok
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                  "maxRange", src.getModifiedItemAttr("shipBonusTitanM1"), skill="Minmatar Titan")
