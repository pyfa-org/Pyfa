# eliteReconBonusMHTOptimalRange1
#
# Used by:
# Ship: Lachesis
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusReconShip1"), skill="Recon Ships")
