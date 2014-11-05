# eliteBonusViolatorsLargeProjectileTurretTracking1
#
# Used by:
# Ships named like: Vargur (4 of 4)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Marauders").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("eliteBonusViolators1") * level)
