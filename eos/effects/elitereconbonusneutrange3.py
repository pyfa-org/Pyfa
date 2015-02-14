# eliteReconBonusNeutRange3
#
# Used by:
# Ship: Pilgrim
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Recon Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Destabilizer",
                                  "energyDestabilizationRange", ship.getModifiedItemAttr("eliteBonusReconShip3") * level)
