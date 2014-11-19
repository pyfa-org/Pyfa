# eliteBonusViolatorsLargeEnergyTurretDamage1
#
# Used by:
# Ships named like: Paladin (4 of 4)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Marauders").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("eliteBonusViolators1") * level)
