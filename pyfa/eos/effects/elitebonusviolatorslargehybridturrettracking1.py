# eliteBonusViolatorsLargeHybridTurretTracking1
#
# Used by:
# Ships named like: Kronos (4 of 4)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Marauders").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("eliteBonusViolators1") * level)
