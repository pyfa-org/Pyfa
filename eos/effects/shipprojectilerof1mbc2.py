# shipProjectileRof1MBC2
#
# Used by:
# Ships named like: Hurricane (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusMBC2"), skill="Minmatar Battlecruiser")
