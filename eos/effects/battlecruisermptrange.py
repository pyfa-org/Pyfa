# battlecruiserMPTRange
#
# Used by:
# Ships named like: Hurricane (2 of 2)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "maxRange", ship.getModifiedItemAttr("roleBonusCBC"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "falloff", ship.getModifiedItemAttr("roleBonusCBC"))
