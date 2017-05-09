# shipBonusForceAuxiliaryA1NosferatuRangeBonus
#
# Used by:
# Ship: Dagon
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                  "maxRange", src.getModifiedItemAttr("shipBonusForceAuxiliaryA1"), skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                  "falloffEffectiveness", src.getModifiedItemAttr("shipBonusForceAuxiliaryA1"), skill="Amarr Carrier")
