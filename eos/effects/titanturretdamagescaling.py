# Used by:
# Ships from group: Titan (4 of 4)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Gunnery"),
                                     "turretDamageScalingRadius", ship.getModifiedItemAttr("titanBonusScalingRadius"))
