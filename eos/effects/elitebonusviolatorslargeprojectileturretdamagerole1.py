# eliteBonusViolatorsLargeProjectileTurretDamageRole1
#
# Used by:
# Ships named like: Vargur (4 of 4)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("eliteBonusViolatorsRole1"))
