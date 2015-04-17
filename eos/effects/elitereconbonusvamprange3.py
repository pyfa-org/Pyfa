# eliteReconBonusVampRange3
#
# Used by:
# Ship: Pilgrim
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Recon Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Vampire",
                                  "powerTransferRange", ship.getModifiedItemAttr("eliteBonusReconShip3") * level)
