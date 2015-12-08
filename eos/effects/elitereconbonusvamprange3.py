# eliteReconBonusVampRange3
#
# Used by:
# Ship: Pilgrim
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                  "powerTransferRange", ship.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")
