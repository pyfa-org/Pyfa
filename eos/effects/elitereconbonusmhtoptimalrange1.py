# eliteReconBonusMHTOptimalRange1
#
# Used by:
# Ship: Lachesis
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Recon Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusReconShip1") * level)
