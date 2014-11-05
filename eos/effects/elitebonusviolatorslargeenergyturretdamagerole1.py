# eliteBonusViolatorsLargeEnergyTurretDamageRole1
#
# Used by:
# Ships named like: Paladin (4 of 4)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("eliteBonusViolatorsRole1"))
