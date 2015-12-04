# eliteReconBonusEnergyNeutAmount2
#
# Used by:
# Ship: Curse
# Ship: Pilgrim
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                  "energyDestabilizationAmount", ship.getModifiedItemAttr("eliteBonusReconShip2"), skill="Recon Ships")
