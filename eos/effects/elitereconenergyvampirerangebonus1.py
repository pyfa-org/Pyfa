# eliteReconEnergyVampireRangeBonus1
#
# Used by:
# Ship: Curse
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Vampire",
                                  "powerTransferRange", ship.getModifiedItemAttr("eliteBonusReconShip1"), skill="Recon Ships")
