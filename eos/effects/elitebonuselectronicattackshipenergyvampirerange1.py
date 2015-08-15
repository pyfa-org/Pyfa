# eliteBonusElectronicAttackShipEnergyVampireRange1
#
# Used by:
# Ship: Sentinel
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Vampire",
                                  "powerTransferRange", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip1"), skill="Electronic Attack Ships")
