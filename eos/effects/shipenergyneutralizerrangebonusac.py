# shipEnergyNeutralizerRangeBonusAC
#
# Used by:
# Ship: Vangel
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                  "energyDestabilizationRange", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
