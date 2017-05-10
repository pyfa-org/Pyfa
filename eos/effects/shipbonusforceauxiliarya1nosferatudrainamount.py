# shipBonusForceAuxiliaryA1NosferatuDrainAmount
#
# Used by:
# Ship: Dagon
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                  "powerTransferAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryA1"), skill="Amarr Carrier")
