# Not used by any item
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Gunnery"),
                                     "turretDamageScalingRadius", ship.getModifiedItemAttr("titanBonusScalingRadius"))
