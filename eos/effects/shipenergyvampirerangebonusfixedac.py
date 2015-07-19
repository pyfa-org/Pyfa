# shipEnergyVampireRangeBonusFixedAC
#
# Used by:
# Ship: Vangel
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Vampire",
                                  "powerTransferRange", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
