# shipProjectileRofBonusMBC1
#
# Used by:
# Ship: Tornado
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusMBC1"), skill="Minmatar Battlecruiser")
