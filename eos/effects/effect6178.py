# shipBonusProjectileTrackingMBC2
#
# Used by:
# Ship: Hurricane Fleet Issue
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusMBC2"),
                                  skill="Minmatar Battlecruiser")
