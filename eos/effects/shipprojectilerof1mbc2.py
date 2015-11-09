# shipProjectileRof1MBC2
#
# Used by:
# Ship: Hurricane
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusMBC2"), skill="Minmatar Battlecruiser")
