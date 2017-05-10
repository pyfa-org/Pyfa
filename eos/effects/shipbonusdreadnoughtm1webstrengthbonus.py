# shipBonusDreadnoughtM1WebStrengthBonus
#
# Used by:
# Ship: Vehement
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web", "speedFactor",
                                  src.getModifiedItemAttr("shipBonusDreadnoughtM1"), skill="Minmatar Dreadnought")
