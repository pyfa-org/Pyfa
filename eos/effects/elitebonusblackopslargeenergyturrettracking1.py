# eliteBonusBlackOpsLargeEnergyTurretTracking1
#
# Used by:
# Ship: Redeemer
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("eliteBonusBlackOps1"), skill="Black Ops")
