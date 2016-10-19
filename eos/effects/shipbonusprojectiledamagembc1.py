# shipBonusProjectileDamageMBC1
#
# Used by:
# Ships named like: Hurricane (2 of 2)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusMBC1"),
                                  skill="Minmatar Battlecruiser")
