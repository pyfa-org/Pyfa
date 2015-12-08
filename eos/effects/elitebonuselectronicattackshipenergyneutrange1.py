# eliteBonusElectronicAttackShipEnergyNeutRange1
#
# Used by:
# Ship: Sentinel
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                  "energyDestabilizationRange", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip1"), skill="Electronic Attack Ships")
